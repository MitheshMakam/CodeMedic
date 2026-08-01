import re
from app.schemas.review import Finding, FindingSeverity

RULES = [
    (r"(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'$\"]{8,}", "Possible hard-coded secret", FindingSeverity.high, "Move the value to a secret manager or environment variable."),
    (r"\beval\s*\(", "Unsafe eval usage", FindingSeverity.high, "Replace eval with explicit parsing or a safe allow-listed evaluator."),
    (r"SELECT .*(?:\+|f['\"]|format\()", "Possible SQL injection", FindingSeverity.high, "Use parameterized queries and never concatenate user input into SQL."),
    (r"console\.log\(|print\(", "Debug output", FindingSeverity.low, "Use structured logging or remove debug output before release."),
    (r"TODO|FIXME", "Unresolved maintenance marker", FindingSeverity.info, "Resolve or track this work in the issue tracker."),
]

def scan(source: dict[str, str], security_only: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    for path, content in source.items():
        for expression, title, severity, recommendation in RULES:
            if security_only and severity not in {FindingSeverity.high, FindingSeverity.critical}:
                continue
            match = re.search(expression, content, re.IGNORECASE | re.MULTILINE)
            if match:
                findings.append(Finding(title=title, severity=severity, path=path, line=content[:match.start()].count("\n") + 1, description=f"{title} detected by repository preflight scan.", recommendation=recommendation))
    return findings

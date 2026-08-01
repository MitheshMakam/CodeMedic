import axios from 'axios'

// Vite proxies these routes to FastAPI in development. Production builds can
// still set VITE_API_URL for a separately hosted API.
const API = import.meta.env.VITE_API_URL || ''
const client = axios.create({ baseURL: API, timeout: 120000 })
const offlineMessage = 'The review service is unavailable. Start the backend on port 8000, then try again.'

async function withRetry(operation) {
  let lastError
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try { return await operation() } catch (error) {
      lastError = error
      if (error.response || attempt === 2) break
      await new Promise(resolve => setTimeout(resolve, 400 * (attempt + 1)))
    }
  }
  if (!lastError.response) throw new Error(offlineMessage)
  throw lastError
}

export async function review(endpoint, repository_url) {
  return (await withRetry(() => client.post(endpoint, { repository_url }))).data
}

export async function streamImprove(repositoryUrl, onEvent) {
  const response = await withRetry(() => fetch(`${API}/improve`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ repository_url: repositoryUrl }) }))
  if (!response.ok || !response.body) throw new Error((await response.json().catch(() => ({}))).detail || 'Unable to start review')
  const reader = response.body.getReader(), decoder = new TextDecoder(), buffer = { text: '' }
  while (true) { const { value, done } = await reader.read(); if (done) break; buffer.text += decoder.decode(value, { stream: true }); const parts = buffer.text.split('\n\n'); buffer.text = parts.pop(); parts.forEach(part => { if (part.startsWith('data: ')) onEvent(JSON.parse(part.slice(6))) }) }
}

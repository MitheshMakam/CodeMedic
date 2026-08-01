import { useState } from 'react'
import { review, streamImprove } from '../services/api'
export function useReview() {
  const [reports, setReports] = useState([]), [progress, setProgress] = useState([]), [loading, setLoading] = useState(false), [error, setError] = useState('')
  const run = async (endpoint, url) => { setLoading(true); setError(''); try { const data = await review(endpoint, url); setReports(items => [data, ...items.filter(item => item.title !== data.title)]); return data } catch (e) { setError(e.response?.data?.detail || e.message) } finally { setLoading(false) } }
  const improve = async url => { setLoading(true); setError(''); setProgress([]); setReports([]); try { await streamImprove(url, event => { setProgress(items => [...items.filter(item => item.step !== event.step), event]); if (event.status === 'error') setError(event.message); if (event.data) setReports(items => [...items, event.data]) }) } catch(e) { setError(e.message) } finally { setLoading(false) } }
  return { reports, progress, loading, error, run, improve }
}

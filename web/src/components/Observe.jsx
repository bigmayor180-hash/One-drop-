import { useState } from 'react'

export default function Observe() {
  const [source, setSource] = useState('web')
  const [payload, setPayload] = useState('{}')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handle_observe = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      let parsed = {}
      try {
        parsed = JSON.parse(payload)
      } catch {
        alert('Invalid JSON in payload')
        setLoading(false)
        return
      }
      const res = await fetch('/observe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, payload: parsed }),
      })
      const data = await res.json()
      setResult(data)
    } catch (err) {
      alert('Error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Observe</h2>
      <form onSubmit={handle_observe}>
        <input
          type="text"
          placeholder="source"
          value={source}
          onChange={(e) => setSource(e.target.value)}
        />
        <textarea
          placeholder='payload (JSON, e.g. {"msg":"hello"})'
          value={payload}
          onChange={(e) => setPayload(e.target.value)}
          rows="4"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  )
}

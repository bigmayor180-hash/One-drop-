import { useState, useEffect } from 'react'

export default function Status() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetch_status = async () => {
    setLoading(true)
    try {
      const res = await fetch('/status')
      const data = await res.json()
      setStatus(data)
    } catch (err) {
      alert('Error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetch_status()
  }, [])

  return (
    <div className="card">
      <h2>Status</h2>
      <button onClick={fetch_status} disabled={loading}>
        {loading ? 'Loading...' : 'Refresh'}
      </button>
      {status && (
        <pre>{JSON.stringify(status, null, 2)}</pre>
      )}
    </div>
  )
}

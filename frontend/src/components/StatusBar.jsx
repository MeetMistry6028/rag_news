import { useState, useEffect } from 'react'
import { healthCheck } from '../api'

export default function StatusBar() {
  const [health, setHealth] = useState(null)

  useEffect(() => {
    healthCheck()
      .then(setHealth)
      .catch(() => setHealth(null))
  }, [])

  if (!health) return null

  return (
    <div className="flex items-center gap-3 text-xs text-gray-400">
      <span className="flex items-center gap-1">
        <span className="w-1.5 h-1.5 rounded-full bg-green-400 inline-block"></span>
        {health.vector_count?.toLocaleString()} articles
      </span>
      <span>{health.embedding_model}</span>
      <span>{health.llm_model}</span>
    </div>
  )
}
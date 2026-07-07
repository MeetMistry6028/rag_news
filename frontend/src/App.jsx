import { useState } from 'react'
import SearchBar from './components/SearchBar'
import SearchResult from './components/SearchResult'
import AnswerCard from './components/AnswerCard'
import StatusBar from './components/StatusBar'
import { searchArticles, askQuestion } from './api'

export default function App() {
  const [query, setQuery] = useState('')
  const [mode, setMode] = useState('search')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searchResults, setSearchResults] = useState(null)
  const [askResult, setAskResult] = useState(null)

  async function handleSubmit() {
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    setSearchResults(null)
    setAskResult(null)

    try {
      if (mode === 'search') {
        const data = await searchArticles(query)
        setSearchResults(data)
      } else {
        const data = await askQuestion(query)
        setAskResult(data)
      }
    } catch (err) {
      setError('Something went wrong. Make sure the API is running.')
    } finally {
      setLoading(false)
    }
  }

  function handleModeChange(newMode) {
    setMode(newMode)
    setSearchResults(null)
    setAskResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-12">

        <div className="mb-10 text-center">
          <h1 className="text-2xl font-medium text-gray-900 mb-1">rag_news</h1>
          <p className="text-sm text-gray-400">Search and ask questions over 100k+ news articles</p>
          <div className="flex justify-center mt-3">
            <StatusBar />
          </div>
        </div>

        <div className="mb-8">
          <SearchBar
            value={query}
            onChange={setQuery}
            onSubmit={handleSubmit}
            mode={mode}
            onModeChange={handleModeChange}
            loading={loading}
          />
        </div>

        {loading && (
          <div className="text-center py-12">
            <p className="text-sm text-gray-400">
              {mode === 'ask' ? 'Generating answer...' : 'Searching...'}
            </p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-100 rounded-xl p-4 text-sm text-red-600 text-center">
            {error}
          </div>
        )}

        {searchResults && !loading && (
          <div>
            <p className="text-xs text-gray-400 mb-4">
              {searchResults.total} results for "{searchResults.query}"
            </p>
            <div className="flex flex-col gap-3">
              {searchResults.results.map((result, i) => (
                <SearchResult key={i} result={result} index={i} />
              ))}
            </div>
          </div>
        )}

        {askResult && !loading && (
          <AnswerCard result={askResult} />
        )}

      </div>
    </div>
  )
}
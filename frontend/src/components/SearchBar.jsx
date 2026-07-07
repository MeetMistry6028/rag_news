export default function SearchBar({ value, onChange, onSubmit, mode, onModeChange, loading }) {
  function handleKeyDown(e) {
    if (e.key === 'Enter' && !loading) onSubmit()
  }

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="flex gap-2 mb-3">
        <button
          onClick={() => onModeChange('search')}
          className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
            mode === 'search'
              ? 'bg-gray-900 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Search
        </button>
        <button
          onClick={() => onModeChange('ask')}
          className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
            mode === 'ask'
              ? 'bg-gray-900 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Ask
        </button>
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={value}
          onChange={e => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={mode === 'search' ? 'Search articles...' : 'Ask a question...'}
          className="flex-1 px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-gray-400 bg-white"
        />
        <button
          onClick={onSubmit}
          disabled={loading || !value.trim()}
          className="px-5 py-3 bg-gray-900 text-white rounded-xl text-sm font-medium hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? '...' : mode === 'search' ? 'Search' : 'Ask'}
        </button>
      </div>
    </div>
  )
}
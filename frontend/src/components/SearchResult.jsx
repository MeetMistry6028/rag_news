export default function SearchResult({ result, index }) {
  return (
    <div className="bg-white border border-gray-100 rounded-xl p-4 hover:border-gray-300 transition-colors">
      <div className="flex items-start justify-between gap-3 mb-2">
        <span className="text-xs font-medium text-gray-400">#{index + 1}</span>
        <div className="flex items-center gap-2">
          <span className="text-xs px-2 py-0.5 bg-gray-100 text-gray-500 rounded-full">
            {result.retrieval_method}
          </span>
          <span className="text-xs font-medium text-gray-900">
            {(result.score * 100).toFixed(0)}% match
          </span>
        </div>
      </div>

      <p className="text-sm text-gray-700 leading-relaxed mb-3">
        {result.text}
      </p>

      {result.highlights && (
        <div className="border-t border-gray-50 pt-3">
          <p className="text-xs text-gray-400 font-medium mb-1">Summary</p>
          <p className="text-xs text-gray-500 leading-relaxed">{result.highlights}</p>
        </div>
      )}

      <p className="text-xs text-gray-300 mt-2 font-mono truncate">
        {result.article_id}
      </p>
    </div>
  )
}
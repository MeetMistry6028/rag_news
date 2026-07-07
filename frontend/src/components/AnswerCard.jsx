export default function AnswerCard({ result }) {
  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="bg-white border border-gray-100 rounded-xl p-6 mb-4">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-xs font-medium text-gray-400 uppercase tracking-wide">Answer</span>
          {result.fallback && (
            <span className="text-xs px-2 py-0.5 bg-yellow-50 text-yellow-600 rounded-full">
              No relevant articles found
            </span>
          )}
        </div>

        <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
          {result.answer}
        </p>

        <div className="flex items-center gap-3 mt-4 pt-4 border-t border-gray-50">
          <span className="text-xs text-gray-400">
            {result.chunks_used} chunks retrieved
          </span>
          <span className="text-xs text-gray-400">
            {result.citations.length} citations
          </span>
        </div>
      </div>

      {result.citations.length > 0 && (
        <div>
          <p className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-3">
            Sources
          </p>
          <div className="flex flex-col gap-2">
            {result.citations.map((c) => (
              <div
                key={c.citation_num}
                className="bg-white border border-gray-100 rounded-xl p-4"
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-medium px-2 py-0.5 bg-gray-900 text-white rounded-full">
                    Article {c.citation_num}
                  </span>
                  <span className="text-xs text-gray-300 font-mono truncate">
                    {c.article_id}
                  </span>
                </div>
                <p className="text-xs text-gray-600 leading-relaxed">
                  {c.text_preview}...
                </p>
                {c.highlights && (
                  <p className="text-xs text-gray-400 mt-2 italic">
                    {c.highlights}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
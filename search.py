from config.logger import setup_logging
from retrieval.retriever import Retriever, RetrievalMode

setup_logging()

retriever = Retriever(mode=RetrievalMode.VECTOR)

queries = [
    "climate change and global warming",
    "football world cup results",
    "US presidential election",
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)
    results = retriever.search(query, top_k=3)
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] Score: {r['score']} | Article: {r['article_id']}")
        print(f"    {r['text'][:200]}...")
import argparse
from config.logger import setup_logging
from rag.chain import RAGChain

setup_logging()

parser = argparse.ArgumentParser(description="Ask a question to rag_news")
parser.add_argument("question", type=str, help="Your question")
parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to retrieve")
args = parser.parse_args()

chain = RAGChain()
result = chain.ask(args.question, top_k=args.top_k)

print("\n" + "="*60)
print("ANSWER")
print("="*60)
print(result["answer"])

if result["citations"]:
    print("\n" + "="*60)
    print("SOURCES")
    print("="*60)
    for c in result["citations"]:
        print(f"\n[Article {c['citation_num']}] ID: {c['article_id']}")
        print(f"  {c['text_preview']}...")

print(f"\nChunks used: {result['chunks_used']} | Fallback: {result['fallback']}")
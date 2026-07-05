import argparse
from config.logger import setup_logging
from ingestion.pipeline import run_pipeline

setup_logging()

parser = argparse.ArgumentParser(description="Ingest articles into rag_news vector store")
parser.add_argument("--csv", default="data/train.csv", help="Path to CSV file")
parser.add_argument("--limit", type=int, default=100, help="Number of rows to ingest")
args = parser.parse_args()

run_pipeline(csv_path=args.csv, limit=args.limit)
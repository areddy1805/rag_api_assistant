import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from backend.evaluation.evaluate_retrieval import evaluate as evaluate_retrieval
from backend.evaluation.evaluate_generation import evaluate as evaluate_generation
from backend.evaluation.report import build_report


retrieval_results = evaluate_retrieval() or []
generation_results = evaluate_generation() or []

build_report(retrieval_results, generation_results)
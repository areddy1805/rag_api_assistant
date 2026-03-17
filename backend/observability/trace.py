import time
from backend.observability.logger import logger


class RAGTrace:

    current = None

    def __init__(self, query):

        self.query = query
        self.start = time.time()

        self.service = None
        self.entities = None

        self.retrieved = []
        self.reranked = []

        self.prompt_tokens = 0
        self.completion_tokens = 0

        self.timers = {}

        RAGTrace.current = self

        logger.info(f"[QUERY] {query}")

    # ------------------------
    # Stage Timing
    # ------------------------

    def start_stage(self, name):

        self.timers[name] = time.time()

    def end_stage(self, name):

        if name in self.timers:

            duration = time.time() - self.timers[name]

            logger.info(f"[TIMING] {name}={duration:.3f}s")

    # ------------------------
    # Retrieval Logs
    # ------------------------

    def log_retrieval(self, candidates):

        ids = [c["chunk_id"] for c in candidates]

        self.retrieved = ids

        logger.info(f"[RETRIEVED] {ids}")

    def log_rerank(self, ranked):

        rows = []

        for r in ranked[:10]:

            cid = r["chunk_id"]
            score = r.get("score", 0)

            rows.append(f"{cid}:{score:.3f}")

        self.reranked = rows

        logger.info(f"[RERANKED] {rows}")

    # ------------------------
    # Token Aggregation
    # ------------------------

    def add_tokens(self, prompt_tokens, completion_tokens):

        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens

    # ------------------------
    # Finish Trace
    # ------------------------

    def finish(self):

        latency = time.time() - self.start

        total = self.prompt_tokens + self.completion_tokens

        logger.info(
            f"[TOKEN_SUMMARY] prompt={self.prompt_tokens} "
            f"completion={self.completion_tokens} "
            f"total={total}"
        )

        logger.info(f"[LATENCY] {latency:.3f}s")
        logger.info("---------------------------------------------------")

        RAGTrace.current = None
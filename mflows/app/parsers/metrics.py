class ParserMetrics:
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.regex_hits = 0
        self.llm_hits = 0
        self.failures = 0

    def to_dicts(self):
        return {
            "total_requests": self.total_requests,
            "cache_hits": self.cache_hits,
            "regex_hits": self.regex_hits,
            "llm_hits": self.llm_hits,
            "failures": self.failures,
        }

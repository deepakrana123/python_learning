class ParserMetrics:
    def __init__(self):
        self.total_requests = 0
        self.cache_hits = 0
        self.regex_hits = 0
        self.llm_hits = 0
        self.failures = 0
        self.fallback_user = 0
        self.total_cost = 0
        self.ollama_hits = 0
        self.gemini_hits = 0

    def to_dicts(self):
        return {
            "total_requests": self.total_requests,
            "cache_hits": self.cache_hits,
            "regex_hits": self.regex_hits,
            "llm_hits": self.llm_hits,
            "failures": self.failures,
            "total_cost": self.total_cost,
            "ollama_hits": self.ollama_hits,
            "gemini_hits": self.gemini_hits,
            "fallback_user": self.fallback_user,
        }


metrics = ParserMetrics()

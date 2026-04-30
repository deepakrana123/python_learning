class ExecutionMetrics:
 
    def __init__(self):
        self.total_events = 0
        self.events_completed = 0
        self.events_failed = 0
        self.events_duplicate_skipped = 0
        self.events_lost_race = 0
        self.total_workflows_matched = 0
        self.total_actions_executed = 0
        self.action_successes = 0
        self.action_failures = 0
        self.retries_scheduled = 0
        self.dlq_pushes = 0

    def reset(self):
        self.__init__()

    def to_dict(self):
        return {
            "total_events": self.total_events,
            "events_completed": self.events_completed,
            "events_failed": self.events_failed,
            "events_duplicate_skipped": self.events_duplicate_skipped,
            "events_lost_race": self.events_lost_race,
            "total_workflows_matched": self.total_workflows_matched,
            "total_actions_executed": self.total_actions_executed,
            "action_successes": self.action_successes,
            "action_failures": self.action_failures,
            "retries_scheduled": self.retries_scheduled,
            "dlq_pushes": self.dlq_pushes,
        }


execution_metrics = ExecutionMetrics()

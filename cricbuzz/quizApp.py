class QuizSession:
    def __init__(self, session_id: str, host_id: str, questions: list):
        self.session_id = session_id
        self.host_id = host_id
        self.questions = questions
        self.started_at = None
        self.status = "waiting"


class Question:
    def __init__(
        self,
        question_id: str,
        text: str,
        options: list,
        correct_option: int,
        time_limit_sec: int,
    ):
        pass


class UserAnswer:
    def __init__(
        self, user_id: str, question_id: str, selected_option: int, answered_at: str
    ):
        pass


class ScoreBoard:
    def __init__(self):
        self.user_scores = {}


class IQuizStateStore:
    def save_questions(self, session_id: str):
        pass

    def get_questions(self, session_id: str) -> QuizSession:
        pass

    def update_questions(self, session_id: str, user_id: str, delta: int):
        pass

    def get_scores(self, sesssion_id: str):
        pass


class IClientNotifier:
    def send_questions(self, session_id: str, question: Question):
        pass

    def notify_score_update(self, session_id: str, user_id: str, new_score: int):
        pass

    def notify_end_of_quiz(self, session_id: str):
        pass


class ITimerService:
    def schedule_questions_end(
        self, session_id: str, question_id: str, delay_seconds: int
    ):
        pass


class QuizOrchestrator:
    def __init__(self, store: IQuizStateStore, notifier: IClientNotifier, timer: str):
        self.store = store
        self.notifier = notifier
        self.timer = timer

    def start_session(self, session_id: str):
        session = self.store.get_session(session_id)
        session.status = "in_progress"
        self.send_next_questions(session)

    def send_next_questions(self, session):
        next_Q = session.questions.pop(0)
        self.notifier.send_questions(session.session_id, next_Q)
        self.timer.schedule_question_end(
            session.session_id, next_Q.question_id, next_Q.time_limit_sec
        )


class AnswerService:
    def __init__(self, store: IQuizStateStore, notifier: IClientNotifier):
        self.store = store
        self.notifier = notifier

    def submit_answer(self, session_id: str, user_id: str, answer: UserAnswer):
        pass

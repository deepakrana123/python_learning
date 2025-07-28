import uuid


class Movie:
    def __init__(self, title, genre, language, duration):
        self.movie_id = str(uuid.uuid4())
        self.title = title
        self.genre = genre
        self.language = language
        self.duration = duration

    def getMovieName(self):
        return self.title

class Movie:
    def __init__(self, title: str, year: int, director: str):
        self.title = title
        self.year = year
        self.director = director

    def __repr__(self):
        return f"Movie(title='{self.title}', year={self.year}, director='{self.director}')"
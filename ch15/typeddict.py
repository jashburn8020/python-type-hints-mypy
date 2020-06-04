"""`TypedDict`"""

from typing import TypedDict

Movie = TypedDict("Movie", {"name": str, "year": int})
movie: Movie = {"name": "Blade Runner", "year": 1982}

movie_bad: Movie = {"name": "Blade Runner", "year": 1982, "director": "Scott"}
director = movie_bad["director"]

toy_story = Movie(name="Toy Story", year=1995)

toy_story_2: Movie = {"name": "Toy Story 2"}

GuiOptions = TypedDict("GuiOptions", {"language": str, "color": str}, total=False)
options: GuiOptions = {}
options["language"] = "en"

print(options["color"])  # KeyError
print(options.get("color"))  # None

reveal_type(options)


class MovieClassBased(TypedDict):
    name: str
    year: int


class BookBasedMovie(MovieClassBased):
    based_on: str


book_based_movie = BookBasedMovie(
    name="The Social Network", year=2010, based_on="The Accidental Billionaires"
)
print(book_based_movie["name"])
print(book_based_movie.based_on)  # Error

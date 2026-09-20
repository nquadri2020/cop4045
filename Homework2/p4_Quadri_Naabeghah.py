import csv

def load_top_rated(filename: str) -> dict[tuple[str, str], int]:
    """Load top-rated movies into a dictionary.
    Args:
        filename: Name of the top-rated CSV file.
    Returns:
        Dictionary mapping (title, year) to rank.
    """
    movies = {}
    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            title = row["Title"]
            year = row["Year"]
            rank = int(row["Rank"])

            movies[(title, year)] = rank

    return movies

def load_top_grossing(filename: str) -> dict[tuple[str, str], float]:
    """Load top-grossing movies into a dictionary.
    Args:
        filename: Name of the top-grossing CSV file.
    Returns:
        Dictionary mapping (title, year) to box office amount.
    """
    movies = {}
    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            title = row["Title"]
            year = row["Year"]
            box_office = row["USA Box Office"]
            box_office = box_office.replace("$", "")
            box_office = box_office.replace(",", "")
            movies[(title, year)] = float(box_office)

    return movies

def load_casts(filename: str) -> dict[tuple[str, str], tuple[str, list[str]]]:
    """Load director and actors for each movie.
    Args:
        filename: Name of the cast CSV file.
    Returns:
        Dictionary mapping (title, year) to director and actors.
    """
    movies = {}
    with open(
            filename,
            "r",
            encoding="utf-8") as csv_file:

        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) >= 3:
                title = row[0]
                year = row[1]
                director = row[2]
                actors = row[3:]
                movies[(title, year)] = (director, actors)

    return movies

def display_top_collaborations(
        rated_filename: str,
        casts_filename: str,
        limit: int = 10) -> None:
    """Display director-actor collaborations from top-rated movies.
    Args:
        rated_filename: Top-rated movie CSV file.
        casts_filename: Movie cast CSV file.
        limit: Maximum number of collaborations to display.
    """
    top_rated = load_top_rated(rated_filename)
    casts = load_casts(casts_filename)

    collaborations = {}
    for movie in top_rated:
        if movie in casts:
            director, actors = casts[movie]
            for actor in actors:
                pair = (director, actor)
                if pair not in collaborations:
                    collaborations[pair] = 0
                collaborations[pair] += 1

    ranking = sorted(
        collaborations.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("Top director-actor collaborations:")
    for (director, actor), count in ranking[:limit]:
        print(
            "({}, {}, {})".format(
                director,
                actor,
                count
            )
        )

def display_top_actors(
        grossing_filename: str,
        casts_filename: str,
        limit: int = 10) -> None:
    """Display actors ranked by total box office.
    Args:
        grossing_filename: Top-grossing movie CSV file.
        casts_filename: Movie cast CSV file.
        limit: Maximum number of actors to display.
    """
    top_grossing = load_top_grossing(grossing_filename)
    casts = load_casts(casts_filename)

    actor_totals = {}
    for movie, box_office in top_grossing.items():
        if movie in casts:
            director, actors = casts[movie]
            for actor in actors:
                if actor not in actor_totals:
                    actor_totals[actor] = 0.0
                actor_totals[actor] += box_office

    ranking = sorted(
        actor_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("Top actors by total box office:")
    for actor, total in ranking[:limit]:
        print(
            "{}: ${:,.0f}".format(
                actor,
                total
            )
        )

def main() -> None:
    """Test the movie ranking functions."""
    rated_filename = "imdb-top-rated.csv"
    grossing_filename = "imdb-top-grossing.csv"
    casts_filename = "imdb-top-casts.csv"

    display_top_collaborations(
        rated_filename,
        casts_filename,
        10
    )

    print()

    display_top_actors(
        grossing_filename,
        casts_filename,
        10
    )

if __name__ == "__main__":
    main()
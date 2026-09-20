import csv

def add_user(
        sn: dict[str, tuple[str, list[str]]],
        username: str,
        fullname: str) -> bool:
    """Add a new user to the social network.
    Args:
        sn: Social network dictionary.
        username: Username of the new user.
        fullname: Full name of the new user.
    Returns:
        True if the user was added, False if the username already exists.
    """
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])

        return True
    except Exception as error:
        print("Error adding user: {}".format(error))
        raise

def add_friend(
        sn: dict[str, tuple[str, list[str]]],
        user1: str,
        user2: str) -> bool:
    """Add a mutual friendship between two users.
    Args:
        sn: Social network dictionary.
        user1: First username.
        user2: Second username.
    Returns:
        True if the friendship was added, otherwise False.
    """
    try:
        if user1 not in sn or user2 not in sn:
            return False
        if user1 == user2:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)

        return True
    except Exception as error:
        print("Error adding friendship: {}".format(error))
        raise

def get_friends(
        sn: dict[str, tuple[str, list[str]]],
        user1: str,
        distance: int) -> list[str]:
    """Return friends within a specified link distance.
    Args:
        sn: Social network dictionary.
        user1: Starting username.
        distance: Maximum friendship-link distance.
    Returns:
        A list of users reachable within the requested distance.
    """
    try:
        if user1 not in sn or distance <= 0:
            return []

        visited = {user1}
        current_level = [user1]
        friends = []
        for _ in range(distance):
            next_level = []
            for user in current_level:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.add(friend)
                        next_level.append(friend)
                        friends.append(friend)
            current_level = next_level
            if not current_level:
                break

        return friends
    except Exception as error:
        print("Error finding friends: {}".format(error))
        raise

def save_network(
        filename: str,
        sn: dict[str, tuple[str, list[str]]]) -> None:
    """Save a social network dictionary to a CSV file.
    Args:
        filename: Name of the CSV file.
        sn: Social network dictionary.
    Raises:
        OSError: If the file cannot be written.
    """
    try:
        with open(
                filename,
                "w",
                newline="",
                encoding="utf-8") as csv_file:

            writer = csv.writer(csv_file)
            for username in sn:
                fullname, friends = sn[username]
                writer.writerow(
                    [username, fullname] + friends
                )

    except OSError as error:
        print("Error saving network: {}".format(error))
        raise

def load_network(
        filename: str) -> dict[str, tuple[str, list[str]]]:
    """Load a social network from a CSV file.
    Args:
        filename: Name of the CSV file.
    Returns:
        The social network represented by the CSV file.
    Raises:
        OSError: If the file cannot be read.
    """
    try:
        sn = {}
        with open(
                filename,
                "r",
                newline="",
                encoding="utf-8") as csv_file:

            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) >= 2:
                    username = row[0]
                    fullname = row[1]
                    friends = row[2:]
                    sn[username] = (fullname, friends)

        return sn
    except OSError as error:
        print("Error loading network: {}".format(error))
        raise

def main() -> None:
    """Test all social network functions."""
    sn = {
        "alice": ("Alice Smith", ["maria"]),
        "maria": ("Maria Cortez", ["alice", "joe", "david"]),
        "joe": ("Joseph Adams", ["maria", "eve"]),
        "eve": ("Evelyn Cooper", ["joe"]),
        "david": ("David Benson", ["maria"]),
    }

    print("Original network:")
    print(sn)

    print("\nAdding user:")
    print(add_user(sn, "john", "John Smith"))
    print(sn)

    print("\nAdding duplicate user:")
    print(add_user(sn, "john", "John Smith"))

    print("\nAdding friendship:")
    print(add_friend(sn, "john", "alice"))
    print(sn)

    print("\nAdding invalid friendship:")
    print(add_friend(sn, "john", "unknown"))

    print("\nFriends of alice at distance 1:")
    print(get_friends(sn, "alice", 1))

    print("\nFriends of alice at distance 2:")
    print(get_friends(sn, "alice", 2))

    print("\nFriends of alice at distance 3:")
    print(get_friends(sn, "alice", 3))

    print("\nInvalid user:")
    print(get_friends(sn, "unknown", 2))

    filename = "social_network.csv"
    save_network(filename, sn)
    loaded_network = load_network(filename)
    print("\nLoaded network:")
    print(loaded_network)

if __name__ == "__main__":
    main()
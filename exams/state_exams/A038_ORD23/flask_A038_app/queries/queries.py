import os


class QueryLoader:
    def __init__(self):
        self.queries = {}
        self._load_queries()

    def _load_queries(self):
        """Load SQL queries from queries.sql in the same directory"""
        file_path = os.path.join(os.path.dirname(__file__), "queries.sql")
        with open(file_path, "r") as f:
            current_query = []
            current_name = None

            for line in f:
                if line.strip().startswith("--"):
                    # Save previous query if exists
                    if current_name and current_query:
                        self.queries[current_name] = "\n".join(current_query).strip()
                    # Start new query
                    current_name = line.strip("- \n").strip()
                    current_query = []
                else:
                    if current_name and line.strip():
                        current_query.append(line.strip())

            # Save the last query
            if current_name and current_query:
                self.queries[current_name] = "\n".join(current_query).strip()

    def get(self, name):
        """Get a query by name"""
        return self.queries.get(name)


# Initialize queries
QUERIES = QueryLoader()

# Export common queries
GET_ALL_GAMES = QUERIES.get("Get all games")
GET_GAME_DETAILS = QUERIES.get("Get game details")
GET_GAME_LEADERBOARD = QUERIES.get("Get game leaderboard")

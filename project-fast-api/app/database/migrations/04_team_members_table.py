def migrate():
    return """
        CREATE TABLE IF NOT EXISTS team_members (
            id SERIAL PRIMARY KEY,
            team_id INT NOT NULL REFERENCES teams(id),
            user_id INT NOT NULL REFERENCES users(id)
        )
    """
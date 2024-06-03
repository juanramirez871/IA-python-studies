def migrate():
    return """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            team_id INT NOT NULL REFERENCES teams(id)
        )
    """
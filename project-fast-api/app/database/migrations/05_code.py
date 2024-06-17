def migrate():
    return """
        CREATE TABLE IF NOT EXISTS code (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id),
            code INT NOT NULL
        )
    """
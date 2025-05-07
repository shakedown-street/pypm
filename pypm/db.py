import sqlite3

DB_NAME = "pypm.db"


def get_connection():
    """
    Get a connection to the SQLite database.
    """
    return sqlite3.connect(DB_NAME)


def create_projects_table(cursor):
    """
    Create the projects table in the SQLite database.
    """

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL CHECK(status IN ('active', 'archived', 'completed'))
        )
        """
    )


def create_tasks_table(cursor):
    """
    Create the tasks table in the SQLite database.
    """

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT,
            status TEXT NOT NULL CHECK(status IN ('todo', 'in_progress', 'done', 'blocked')),
            priority TEXT NOT NULL CHECK(priority IN ('low', 'medium', 'high')),
            due_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES Project(id) ON DELETE CASCADE
        )
        """
    )


def init_db():
    """
    Initialize the SQLite database and create tables.
    """
    connection = get_connection()
    cursor = connection.cursor()

    create_projects_table(cursor)
    create_tasks_table(cursor)

    connection.commit()
    connection.close()

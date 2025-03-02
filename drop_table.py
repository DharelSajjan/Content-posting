import sqlite3
from logger_config import get_logger

logger = get_logger(__name__)

def drop_table():
    # Connect to the database
    conn = sqlite3.connect('content.db')
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS posts")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    drop_table()
    logger.info("Table 'posts' has been dropped.")
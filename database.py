import sqlite3
import logging


class TriangleDatabase:
    """Класс работы с базой данных (SQLite)."""

    def __init__(self, db_name=":memory:"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side_a TEXT,
                side_b TEXT,
                side_c TEXT,
                triangle_type TEXT,
                coordinates TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        """)
        self.connection.commit()

    def add_record(self, side_a, side_b, side_c, triangle_type,
                   coordinates, error_message=""):
        logging.info(f"Добавление записи в БД: {side_a}, {side_b}, {side_c}")
        self.cursor.execute("""
            INSERT OR REPLACE INTO triangles
            (side_a, side_b, side_c, triangle_type, coordinates, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(side_a), str(side_b), str(side_c),
              triangle_type, str(coordinates), error_message))
        self.connection.commit()

    def get_record(self, side_a, side_b, side_c):
        logging.info(f"Поиск записи в БД: {side_a}, {side_b}, {side_c}")
        self.cursor.execute("""
            SELECT triangle_type, coordinates, error_message
            FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        """, (str(side_a), str(side_b), str(side_c)))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return {
            "triangle_type": row[0],
            "coordinates": row[1],
            "error_message": row[2]
        }

    def delete_record(self, side_a, side_b, side_c):
        logging.info(f"Удаление записи из БД: {side_a}, {side_b}, {side_c}")
        self.cursor.execute("""
            DELETE FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        """, (str(side_a), str(side_b), str(side_c)))
        self.connection.commit()

    def close(self):
        self.connection.close()
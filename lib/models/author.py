from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"Author(id={self.id}, name='{self.name}')"

    def save(self):
        if self.id is None:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self.id = cursor.lastrowid
        else:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE authors SET name = ? WHERE id = ?",
                    (self.name, self.id)
                )

    @classmethod
    def create(cls, name):
        author = cls(name)
        author.save()
        return author

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return cls(row['name'], row['id'])
            return None

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return cls(row['name'], row['id'])
            return None

    def articles(self):
        from lib.models.article import Article
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
            return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                    for row in cursor.fetchall()]

    def magazines(self):
        from lib.models.magazine import Magazine
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return [Magazine(row['name'], row['category'], row['id']) 
                    for row in cursor.fetchall()]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article.create(title, self.id, magazine.id)

    def topic_areas(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return [row['category'] for row in cursor.fetchall()]
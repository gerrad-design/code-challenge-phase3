from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.name = name
        self.category = category
        self.id = id

    def __repr__(self):
        return f"Magazine(id={self.id}, name='{self.name}', category='{self.category}')"

    def save(self):
        if self.id is None:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
        else:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return cls(row['name'], row['category'], row['id'])
            return None

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return cls(row['name'], row['category'], row['id'])
            return None

    def articles(self):
        from lib.models.article import Article
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
            return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                    for row in cursor.fetchall()]

    def contributors(self):
        from lib.models.author import Author
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT a.* FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            return [Author(row['name'], row['id']) for row in cursor.fetchall()]

    def article_titles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title FROM articles
                WHERE magazine_id = ?
            """, (self.id,))
            return [row['title'] for row in cursor.fetchall()]

    def contributing_authors(self):
        from lib.models.author import Author
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, COUNT(ar.id) as article_count
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
                GROUP BY a.id
                HAVING article_count > 2
            """, (self.id,))
            return [Author(row['name'], row['id']) for row in cursor.fetchall()]

    @classmethod
    def top_publisher(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.*, COUNT(a.id) as article_count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return cls(row['name'], row['category'], row['id'])
            return None
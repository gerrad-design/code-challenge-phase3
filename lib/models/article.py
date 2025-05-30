from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    def __repr__(self):
        return f"Article(id={self.id}, title='{self.title}', author_id={self.author_id}, magazine_id={self.magazine_id})"

    def save(self):
        if self.id is None:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
        else:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author_id, self.magazine_id, self.id)
                )

    @classmethod
    def create(cls, title, author_id, magazine_id):
        article = cls(title, author_id, magazine_id)
        article.save()
        return article

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return cls(row['title'], row['author_id'], row['magazine_id'], row['id'])
            return None

    @classmethod
    def find_by_title(cls, title):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
            row = cursor.fetchone()
            if row:
                return cls(row['title'], row['author_id'], row['magazine_id'], row['id'])
            return None

    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    @classmethod
    def all(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles")
            return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                    for row in cursor.fetchall()]
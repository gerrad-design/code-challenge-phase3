from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    # Create authors
    author1 = Author.create("John Doe")
    author2 = Author.create("Jane Smith")
    author3 = Author.create("Bob Johnson")

    # Create magazines
    magazine1 = Magazine.create("Tech Today", "Technology")
    magazine2 = Magazine.create("Science Weekly", "Science")
    magazine3 = Magazine.create("Business Insights", "Business")

    # Create articles
    Article.create("Python Programming", author1.id, magazine1.id)
    Article.create("Machine Learning", author1.id, magazine1.id)
    Article.create("Quantum Physics", author2.id, magazine2.id)
    Article.create("Neuroscience", author2.id, magazine2.id)
    Article.create("Stock Market", author3.id, magazine3.id)
    Article.create("Startup Funding", author3.id, magazine3.id)
    Article.create("AI Ethics", author1.id, magazine2.id)
    Article.create("Data Science", author2.id, magazine1.id)
    Article.create("Blockchain", author3.id, magazine1.id)

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")
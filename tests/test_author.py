import pytest
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.seed import seed_database

@pytest.fixture(autouse=True)
def setup_database():
    seed_database()
    yield

def test_author_creation():
    author = Author.find_by_name("John Doe")
    assert author is not None
    assert author.name == "John Doe"

def test_author_articles():
    author = Author.find_by_name("John Doe")
    articles = author.articles()
    assert len(articles) == 3
    assert all(isinstance(article, Article) for article in articles)

def test_author_magazines():
    author = Author.find_by_name("John Doe")
    magazines = author.magazines()
    assert len(magazines) == 2
    assert all(isinstance(magazine, Magazine) for magazine in magazines)

def test_author_topic_areas():
    author = Author.find_by_name("John Doe")
    topics = author.topic_areas()
    assert len(topics) == 2
    assert "Technology" in topics
    assert "Science" in topics
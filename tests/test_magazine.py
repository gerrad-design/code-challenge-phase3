import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.db.seed import seed_database

@pytest.fixture(autouse=True)
def setup_database():
    seed_database()
    yield

def test_magazine_creation():
    magazine = Magazine.find_by_name("Tech Today")
    assert magazine is not None
    assert magazine.name == "Tech Today"
    assert magazine.category == "Technology"

def test_magazine_articles():
    magazine = Magazine.find_by_name("Tech Today")
    articles = magazine.articles()
    assert len(articles) == 4  # Includes articles from other tests

def test_magazine_contributors():
    magazine = Magazine.find_by_name("Tech Today")
    contributors = magazine.contributors()
    assert len(contributors) == 3
    assert all(isinstance(author, Author) for author in contributors)

def test_magazine_article_titles():
    magazine = Magazine.find_by_name("Tech Today")
    titles = magazine.article_titles()
    assert len(titles) == 4
    assert "Python Programming" in titles

def test_top_publisher():
    top_magazine = Magazine.top_publisher()
    assert top_magazine is not None
    assert top_magazine.name == "Tech Today"
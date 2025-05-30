import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.seed import seed_database

@pytest.fixture(autouse=True)
def setup_database():
    seed_database()
    yield

def test_article_creation():
    article = Article.find_by_title("Python Programming")
    assert article is not None
    assert article.title == "Python Programming"

def test_article_author():
    article = Article.find_by_title("Python Programming")
    author = article.author()
    assert author is not None
    assert author.name == "John Doe"

def test_article_magazine():
    article = Article.find_by_title("Python Programming")
    magazine = article.magazine()
    assert magazine is not None
    assert magazine.name == "Tech Today"

def test_all_articles():
    articles = Article.all()
    assert len(articles) >= 6  # At least the seeded articles
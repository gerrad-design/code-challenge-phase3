from lib.db.seed import seed_database
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def debug():
    # Setup database and seed data
    seed_database()

    # Example queries
    print("\nAll Authors:")
    authors = [Author.find_by_id(i) for i in range(1, 4)]
    for author in authors:
        print(author)

    print("\nAll Magazines:")
    magazines = [Magazine.find_by_id(i) for i in range(1, 4)]
    for magazine in magazines:
        print(magazine)

    print("\nAll Articles:")
    articles = Article.all()
    for article in articles:
        print(article)

    # Example relationship queries
    print("\nArticles by John Doe:")
    john = Author.find_by_name("John Doe")
    for article in john.articles():
        print(article)

    print("\nMagazines John Doe has written for:")
    for magazine in john.magazines():
        print(magazine)

    print("\nContributors to Tech Today:")
    tech_today = Magazine.find_by_name("Tech Today")
    for author in tech_today.contributors():
        print(author)

    print("\nTop Publisher:")
    print(Magazine.top_publisher())

if __name__ == '__main__':
    debug()
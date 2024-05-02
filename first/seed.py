import json

from mongoengine import NotUniqueError

from models import Author, Quote

if __name__ == '__main__':
    with open("authors.json", "r") as file:
        authors = json.load(file)
        try:
            for el in authors:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
        except NotUniqueError:
            print(f"Already exists {el.get('fullname')}")

    with open("quotes.json", "r") as file:
        quotes = json.load(file)

        for el in quotes:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(tags=el.get('tags'), quote=el.get('quote'), author=author)

            quote.save()

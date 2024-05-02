import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags__iregex=tag)
    result = [quote.quote for quote in quotes]

    return result


@cache
def find_by_tags(tags: str) -> list[str | None]:
    tags = tags.split(",")
    quotes = Quote.objects(tags__in=tags)
    result = [quote.quote for quote in quotes]

    return result


@cache
def find_by_author(author: str) -> dict:
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]

    return result


def main():
    while True:
        command = input('Enter command name: ')
        if command == 'exit':
            break
        else:
            command_splited = command.split(':')
            search_type = command_splited[0]
            search_value = command_splited[1]

            if search_type == 'tag':
                print(find_by_tag(search_value))
            elif search_type == 'tags':
                print(find_by_tags(search_value))
            elif search_type == 'author':
                print(find_by_author(search_value))


if __name__ == '__main__':
    main()

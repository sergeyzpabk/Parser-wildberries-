import asyncio

from card import main
from get_cookie import startProxy

if __name__ == "__main__":
    startProxy()
    query = "пальто из натуральной шерсти"
    queue = asyncio.Queue()
    asyncio.run(main(queue=queue, query=query))

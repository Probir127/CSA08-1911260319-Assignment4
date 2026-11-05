def save_returns(books):
    log = open("returns.log", "w")
    for b in books:
        log.write(b)
    log.close()
def process(day_file):
    try:
        books = open(day_file).read().split("\n")
        save_returns(books)
    except FileNotFoundError:
        print("missing")

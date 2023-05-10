BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end = start + size - 1
    sym = ['.', ',', ':', ';', '!', '?']
    page = text[start:]

    if size > len(page):
        return (page, len(page))

    while True:
        if text[end- 1] in sym and text[end] in sym:
            end -= 2
            res = text[start: end+1]
        elif text[end] not in sym:
            end -= 1
            res = text[start: end+1]
        else:
            res = text[start: end+1]
            break

    return (res, len(res))


def prepare_book(path: str) -> None:
    with open(path, 'r') as file:
        f = file.read()
        pages = (len(f) // PAGE_SIZE) + 1
        start = 0
        for p in range(1, pages + 1):
            book[p] = _get_part_text(f, start, PAGE_SIZE)[0].lstrip(' \n.')
            start += _get_part_text(f, start, PAGE_SIZE)[1]




prepare_book(BOOK_PATH)

QUOTES = "\"'"


class ParseError(Exception):
    pass


def split_line(line: str) -> list[str]:
    args = []
    word = ""
    quote = None
    has_word = False
    for char in line:
        if quote:
            if char == quote:
                quote = None
            else:
                word += char
        elif char in QUOTES:
            quote = char
            has_word = True
        elif char.isspace():
            if has_word:
                args.append(word)
            word = ""
            has_word = False
        else:
            word += char
            has_word = True
    if quote:
        raise ParseError(f"unclosed quote {quote}")
    if has_word:
        args.append(word)
    return args


def strip_comment(line: str) -> str:
    quote = None
    for index, char in enumerate(line):
        if quote:
            if char == quote:
                quote = None
        elif char in QUOTES:
            quote = char
        elif char == "#":
            return line[:index]
    return line

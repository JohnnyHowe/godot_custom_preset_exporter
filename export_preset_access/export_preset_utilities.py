import re


INDEX_FROM_HEADER_PATTERN = re.compile(r"^\[preset\.(\d+)(?:\.options)?\]$")


def get_index_from_header(header: str) -> int:
    match = INDEX_FROM_HEADER_PATTERN.match(header)
    return int(match.group(1))


def set_header_index(header: str, index: int) -> str:
    return _replace(header, INDEX_FROM_HEADER_PATTERN, str(index), 1)


def _replace(text: str, pattern: re.Pattern, new_value: str, group_index: int) -> str:
    match = pattern.search(text)
    if not match:
        return text

    start, end = match.span(group_index)
    return text[:start] + new_value + text[end:]

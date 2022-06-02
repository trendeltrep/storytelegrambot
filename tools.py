def more_replacer(string: str, olds: list, new: str) -> str:
    for old in olds:
        string = string.replace(old, new)
    return string


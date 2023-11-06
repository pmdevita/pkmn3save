import string

AMERICAN = string.ascii_uppercase + string.ascii_lowercase


def to_ascii(pkmn_string: bytes) -> str:
    final = ""
    for b in pkmn_string:
        if b == 0xff:
            break
        try:
            final += AMERICAN[b - 0xBB]
        except IndexError:
            final += "_"
    return final

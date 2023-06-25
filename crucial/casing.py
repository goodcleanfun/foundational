import re

camel_to_snake_re_all_caps = re.compile("([A-Z\\d]+)([A-Z][a-z])")
camel_to_snake_re_before_word = re.compile("([a-z])([A-Z])")


def camel_to_snake_case(name):
    name = camel_to_snake_re_all_caps.sub("\\1_\\2", name)
    name = camel_to_snake_re_before_word.sub("\\1_\\2", name)
    name = name.replace("-", "_")
    return name.lower()


def to_camel_case(name):
    return name.title().replace(" ", "").replace("_", "")


def to_title_case(name):
    """Convert all upper or all lower case names to title case, otherwise preserve casing."""
    if name.islower() or name.isupper():
        return name.title()
    else:
        return name

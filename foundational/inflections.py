import inflect

inflections = inflect.engine()


def pluralize(word):
    return inflections.plural(word)

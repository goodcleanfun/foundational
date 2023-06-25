def safe_decode(
    value, encoding="utf-8", errors="strict", text_types=str, binary_types=bytes
):
    if isinstance(value, text_types):
        return value

    if isinstance(value, binary_types):
        return value.decode(encoding, errors)
    else:
        return str(value)


def safe_encode(
    value,
    encoding="utf-8",
    from_encoding=None,
    errors="strict",
    text_types=str,
    binary_types=bytes,
):
    if isinstance(value, text_types):
        return value.encode(encoding, errors=errors)
    elif isinstance(value, binary_types):
        if hasattr(from_encoding, "lower"):
            from_encoding = from_encoding.lower()
        if hasattr(encoding, "lower"):
            encoding = encoding.lower()

        if value and from_encoding and encoding and encoding != from_encoding:
            value = safe_decode(value, encoding=from_encoding, errors=errors)
            return value.encode(encoding, errors)
        return value
    else:
        return bytes(repr(value), encoding=encoding)

import secrets


def generate_token():
    """
    Generates a 16 hex symbols long string
    :return: String with 16 hex symbols
    """
    return secrets.token_hex(8)

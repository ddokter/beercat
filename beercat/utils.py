def get_model_name(obj):

    return obj.__class__.__name__.lower()


def normalize_name(name):

    """ Normalize names that use the <part, part> notation """

    parts = name.split(",")
    parts.reverse()

    return " ".join(parts).strip()

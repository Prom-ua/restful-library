from uuid import UUID


def str_to_uuid(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return None
    return val

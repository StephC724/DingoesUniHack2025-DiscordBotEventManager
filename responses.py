from random import choice, randint


def get_response(user_input: str) -> str:
    # Can return any response... AI?
    lowered: str = user_input.lower()

    if lowered == '':
        return "hello...?"

    elif 'hello' in lowered:
        return 'Hello there!'

    elif 'create_event' in lowered:
        return 'Attempting to create event, check event list...'




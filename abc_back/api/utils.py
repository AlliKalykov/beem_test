from rest_framework.request import Request


def get_session_key(request: Request) -> str:
    """Универсальный метод для получения user_id и session_key."""
    session_key = request.session.session_key
    if session_key:
        return session_key
    request.session.flush()
    request.session.create()
    request.session.save()
    return request.session.session_key

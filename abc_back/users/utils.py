from requests import Request


def get_client_ip(request: Request) -> str:
    """Получение IP."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip: str = x_forwarded_for.split(",")[-1].strip()
        return ip
    ip: str = request.META.get("REMOTE_ADDR")
    return ip

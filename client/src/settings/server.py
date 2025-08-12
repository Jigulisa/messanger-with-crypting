from settings.storage import Storage


class ServerMixin:
    @staticmethod
    def get_server_host() -> str:
        return Storage[str].get_value("server_host", "127.0.0.1")

    @staticmethod
    def server_secure() -> bool:
        return Storage[bool].get_value("server_secure", default=False)

    @staticmethod
    def get_server_http_protocol() -> str:
        if ServerMixin.server_secure():
            return "https"
        return "http"

    @staticmethod
    def get_server_ws_protocol() -> str:
        if ServerMixin.server_secure():
            return "wss"
        return "ws"

    @staticmethod
    def get_server_url(postfix: str = "") -> str:
        return f"{ServerMixin.get_server_http_protocol()}://{ServerMixin.get_server_host()}/{postfix}"

    @staticmethod
    def get_server_storage_url(postfix: str = "") -> str:
        return ServerMixin.get_server_url(f"storage/{postfix}")

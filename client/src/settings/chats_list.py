from settings.file import FileMixin
class ChatsMixin:
    @staticmethod
    def add_chat(new_chat: str) -> str:
        chats = FileMixin.get_value("chats", default=set())
        if not isinstance(chats, set):
            chats = set(chats)
   
        chats.add(new_chat)
        FileMixin.set_value("chats", chats)
        return new_chat
            
    @staticmethod
    def delete_chat(chat: str) -> str:
        chats = FileMixin.get_value("chats", default=set())
        chats.remove(chat)
        FileMixin.set_value("chats", chats)
        return chat
    
    @staticmethod
    def get_chats() -> set[str]:
        chats = FileMixin.get_value("chats", default=set())
        return chats
    
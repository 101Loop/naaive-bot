class ErrorMessages:
    """Error messages from Telegram API"""

    CHAT_ADMIN_REQUIRED: str = "CHAT_ADMIN_REQUIRED"
    CAN_NOT_REMOVE_CHAT_OWNER: str = "can't remove chat owner"
    USER_IS_AN_ADMIN: str = "user is an administrator of the chat"
    BOT_USED_IN_PRIVATE_CHAT: str = "can't ban members in private chats"
    NOT_ENOUGH_RIGHTS: str = "not enough rights to restrict/unrestrict chat member"


class BotPermissions:
    """Bot permission names from Telegram API"""

    CREATOR: str = "creator"
    ADMINISTRATOR: str = "administrator"

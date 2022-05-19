import qqbot

from load_config import t_token
from my_handlers import _direct_message_handler, _message_handler


if __name__ == "__main__":
    message_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
    direct_message_handler = qqbot.Handler(qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler)
    
    qqbot.async_listen_events(t_token, False, message_handler, direct_message_handler)

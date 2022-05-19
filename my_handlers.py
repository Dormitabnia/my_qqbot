import qqbot
from qqbot.model.ws_context import WsContext

from bot_core import bot_bot
from load_config import t_token


async def _message_handler(context: WsContext, message: qqbot.Message):
    """
    处理群中@
    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event_type %s" % context.event_type + ",receive message %s" % message.content)
    # 机器人做出回应
    bot_reply = bot_bot.handle_message(message)
    # 构造消息并发送
    send = qqbot.MessageSendRequest("<@{}>{}".format(message.author.id, bot_reply), message.id)
    await msg_api.post_message(message.channel_id, send)
    # for i in range(5):
    #     await asyncio.sleep(5)
    #     # 构造消息发送请求数据对象
    #     send = qqbot.MessageSendRequest("<@%s>谢谢你，加油 " % message.author.id, message.id)
    #     # 通过api发送回复消息
    #     await msg_api.post_message(message.channel_id, send)


async def _direct_message_handler(context: WsContext, message: qqbot.Message):
    """
    处理私信
    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncDmsAPI(t_token, False)

    # 打印返回信息
    qqbot.logger.info("event_type %s" % context.event_type + ",receive message %s" % message.content)
    # qqbot.logger.info("user_info: {}".format(message.author.__dict__))

    # 机器人做出回应
    bot_reply = bot_bot.handle_message(message)

    # 构造消息并发送
    send = qqbot.MessageSendRequest(bot_reply, message.id)
    # send = qqbot.MessageSendRequest("收到你的私信消息了：%s" % message.content, message.id)
    await msg_api.post_direct_message(message.guild_id, send)

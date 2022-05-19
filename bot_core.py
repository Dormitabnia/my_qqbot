import re

import qqbot
from qqbot import Message, logger

from games import GameBase, game_map


class UserServer:
    def __init__(self, user: qqbot.model.member.User):
        self.user = user

        self.status = UserStatus.NORMAL
        self.game_loading: GameBase = None


class UserStatus:
    NORMAL = 0  # 通常
    GAMING = 1  # 游戏中


class Bot:
    def __init__(self):
        self.users = dict()  # {(id: UserServer}
    
    def handle_message(self, message: Message) -> str:
        """
        对外接口，处理Message对象
        """
        msg_user = message.author
        if msg_user.id not in self.users:
            self.users[msg_user.id] = UserServer(msg_user)
        
        raw_message = message.content
        msg = re.sub('<@.*>', '', raw_message).strip()
        reply_str = self._handle_text(msg, self.users[msg_user.id])
        return reply_str

    def _handle_text(self, input_str: str, user_server: UserServer) -> str:
        """
        处理传入的消息内容
        """
        if '/游戏列表' in input_str:
            return self._list_games()
        
        if '/结束游戏' in input_str:
            if user_server.status != UserStatus.GAMING:
                return '当前未在游戏中'
            return self._end_game(user_server)
        
        if user_server.status == UserStatus.GAMING:
            assert user_server.game_loading is not None
            return user_server.game_loading.reply(input_str) 
        
        if '/猜数字' in input_str or input_str == '1':
            return self._start_game('猜数字', user_server)
        if '/成语接龙' in input_str or input_str == '2':
            return self._start_game('成语接龙', user_server)
        
        return self._normal_reply()
    
    def _normal_reply(self):
        return '有什么事情吗？'
    
    def _list_games(self) -> str:
        reply_str = '当前支持的游戏有：'
        list_str = '\n'.join(['{}. {}'.format(index + 1, name) for index, name in enumerate(game_map.keys())])

        return '{}\n{}'.format(reply_str, list_str)
    
    def _start_game(self, game_name: str, user_server: UserServer):
        """
        开始游戏
        """
        logger.info('{} start game {}'.format(user_server.user.username, game_name))

        game_cls = game_map[game_name]
        user_server.game_loading = game_cls()
        user_server.status = UserStatus.GAMING

        return user_server.game_loading.first_reply()
    
    def _end_game(self, user_server: UserServer):
        """
        结束游戏
        """
        logger.info('{}\'s game end'.format(user_server.user.username))

        end_reply = user_server.game_loading.end_reply()
        user_server.game_loading = None
        user_server.status = UserStatus.NORMAL

        return end_reply


bot_bot = Bot()

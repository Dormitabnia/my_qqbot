import abc
import random

from qqbot import logger
from .idioms.idioms_buffer import all_idioms, first_char_map


class GameBase:
    def __init__(self) -> None:
        self.name = None

    @abc.abstractmethod
    def first_reply(self) -> str:
        """
        返回游戏开始时的语句
        """
    
    def end_reply(self) -> str:
        """
        返回游戏结束时的语句
        """
        return '【{}】游戏已结束！感谢您的参与！'.format(self.name)

    @abc.abstractmethod
    def reply(self, user_input: str) -> str:
        """
        在这里对用户输入做出反应
        """
    
    def exception_reply(self) -> str:
        """
        出现错误时的回复语句
        """
        return '搞不懂你说了什么捏\n\n正在【{}】游戏中，如果要退出游戏请使用\'/结束游戏\'指令'.format(self.name)


class GuessNumberGame(GameBase):
    def __init__(self):
        self.name = '猜数字'
    
    def reset_game(self):
        self.target = random.randint(1, 100)
        self.steps_used = 0
    
    def first_reply(self) -> str:
        self.reset_game()
        return '【开始猜数字游戏！】\n我已经准备好了一个1-100之间的整数，来猜一下这个数是多少吧！'
    
    def reply(self, user_input: str) -> str:
        self.steps_used += 1
        guess_number = None
        try:
            guess_number = int(user_input)
        except:
            logger.info('user_input: "{}" 出错'.format(user_input))
            return super().exception_reply()
        
        if guess_number == self.target:
            step_used = self.steps_used
            self.reset_game()
            return 'Bingo！你一共猜了{}次！\n\n我又准备好了一个数，再来猜一下吧！'.format(step_used)
        
        elif guess_number < self.target:
            return '你猜的数字比我准备的数字要小'
        
        elif guess_number > self.target:
            return '你猜的数字比我准备的数字要大'


class SolitaireGame(GameBase):
    def __init__(self):
        self.name = '成语接龙'
    
    def reset_game(self):
        self.idioms_used = set()
        self.n_follow = 0
    
    def first_reply(self) -> str:
        self.reset_game()

        first_idioms = random.sample(all_idioms, 1)[0]
        self.idioms_used.add(first_idioms)
        return '【开始成语接龙游戏！】\n我先来！\n{}'.format(first_idioms)
    
    def reply(self, user_input: str) -> str:
        input_words = user_input.strip()
        if input_words not in all_idioms:
            return '这个是成语吗？\n\n正在【{}】游戏中，如果要退出游戏请使用\'/结束游戏\'指令'.format(self.name)
        
        if input_words in self.idioms_used:
            return '这个词已经用过啦！'
        
        self.n_follow += 1
        
        input_last_char = input_words[-1]
        candidates = first_char_map.get(input_last_char, set())
        candidates = candidates - self.idioms_used
        
        if len(candidates) == 0:
            return '哇，我想不到了，你赢了！\n本次【成语接龙】中，您一共接上了{}次！\n\n我们重新开始游戏吧！\n{}'.format(
                self.n_follow, self.first_reply()
            )
        
        choice = random.sample(candidates, 1)[0]
        return '我接\n{}'.format(choice)

    def end_reply(self) -> str:
        common_reply = super().end_reply()
        result_reply = '本次【成语接龙】中，您一共接上了{}次！'.format(self.n_follow)
        return '{}\n\n{}'.format(common_reply, result_reply)

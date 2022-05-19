import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil

bot_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))

t_token = qqbot.Token(bot_config["token"]["appid"], bot_config["token"]["token"])

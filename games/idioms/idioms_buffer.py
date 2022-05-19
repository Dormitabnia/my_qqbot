import os.path
from qqbot import logger


all_idioms: set = set()
first_char_map: dict = dict()
with open(os.path.join(os.path.dirname(__file__), "idiom.txt"), 'r', encoding='gbk') as f:
    for line in f.readlines():
        all_idioms.add(line.strip())
        first_char = line[0]
        if first_char not in first_char_map:
            first_char_map[first_char] = set()
        first_char_map[first_char].add(line.strip())

n_all_idioms = len(all_idioms)
logger.info('{} idioms loaded.'.format(n_all_idioms))

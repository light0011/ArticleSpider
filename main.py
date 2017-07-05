#即可使用 PyCharm 进行调试
import sys, os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy', 'crawl', 'zhihu'])




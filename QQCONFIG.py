from socket import *
import re
ADDR = ('202.114.196.97',21558)

s = socket(AF_INET, SOCK_DGRAM)

register_re = re.compile(r"[\w]{6,}")

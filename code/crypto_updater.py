import hashlib
import struct
from Crypto.Cipher import AES
import sys
import zlib
import os

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

# {
# "hash": "9ee81d31778f44b17d6d3872778a634a0e80d7b468c0b655bdd4e8401699cce2",
# "encrypted_length": 144,
# "length": 126,
# "key": "5301204a25c17c834a1cf7b4650b5f207610302907a771cf6b6852a00bc2a636",
# "path": "PwnAdventure3/Content/Server/server.ini",
# "encrypted_hash": "45ac77e287db66a1b1a33b522abae366adc0cad65e8f6ee37f8ddf67b8fd6ff0"
# }

buf = open("45ac77e287db66a1b1a33b522abae366adc0cad65e8f6ee37f8ddf67b8fd6ff0", "rb").read()
m = hashlib.sha256()
m.update(buf)
print m.digest().encode('hex')

print "[+] len(buf) = %d" % len(buf)

iv = buf[0:16]
buf = buf[16:]

obj = AES.new("5301204a25c17c834a1cf7b4650b5f207610302907a771cf6b6852a00bc2a636".decode('hex'), AES.MODE_CBC, iv)
buf_d = obj.decrypt(buf)
print hexdump(buf_d)
buf_d = buf_d[:-2]
m = hashlib.sha256()
m.update(buf_d)
print m.digest().encode('hex')

import hashlib
import sys

HASH = '98842E0C0A6C6C1CAE04E5FE74A60278C5BE5473'
NEW_HASH = '3E6539AC0C9833BC0FD59F49BF69C4A739D0E0A1'

buf = open("Assembly-CSharp.dll.original", "rb").read()
pos = buf.find('\x00'.join(HASH))
if pos == -1:
    print "[-] can't find hash"
    sys.exit(1)
buf = buf[:pos] + '\x00'.join(NEW_HASH) + "\x00" + buf[pos + (len(NEW_HASH) * 2):]
print "[+] now saving patched file"

import socket, ssl
import struct

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)

class Buffer:
    def __init__(self, buf):
        self.buf = buf
        self.length = len(self.buf)
        self.pos = 0

    def GetByte(self):
        byte = struct.unpack("<B", self.buf[self.pos: self.pos + 1])[0]
        self.pos += 1
        return byte

    def GetWord(self, endian = "<"):
        word = struct.unpack(endian + "H", self.buf[self.pos: self.pos + 2])[0]
        self.pos += 2
        return word

    def GetDword(self, endian = "<"):
        dword = struct.unpack(endian + "I", self.buf[self.pos: self.pos + 4])[0]
        self.pos += 4
        return dword

    def GetString(self):
        len_string = self.GetWord()
        buf = self.buf[self.pos:self.pos + len_string]
        self.pos += len_string
        return buf

    def GetVector(self, endian = "<"):
        unk_00 = self.GetDword()
        unk_01 = self.GetDword()
        unk_02 = self.GetDword()
        return unk_00, unk_01, unk_02

    def GetRotation(self, endian = "<"):
        unk_00 = self.GetWord()
        unk_01 = self.GetWord()
        unk_02 = self.GetWord()
        return unk_00, unk_01, unk_02


def MakePWNString(buf):
    return struct.pack("<H", len(buf)) + buf

def SendMOTD(sock):
    buf = "PWN3"                        # Signature
    buf += struct.pack("<H", 0x05)      # Master Server version
    buf += MakePWNString("Ghost in the Shellcode")
    buf += MakePWNString("Welcome to Pwn Adventure 3")
    sock.write(buf)

def HandleLogin(sock, buf):
    print "[+] HandleLogin"
    login = buf.GetString()
    passwd = buf.GetString()
    print "[+] login : %s" % login
    print "[+] passwd: %s" % passwd
    buf = "\x01"        # return value
    buf += struct.pack("<I", 0x13337)
    buf += MakePWNString("1b3f03c9dfd2562934352179be88e721")
    buf += MakePWNString("sucemwa")
    buf += "\x01"
    sock.write(buf)

def HandleGetCharacterList(sock, buf):
    print "[+] HandleGetCharacterList"
    buf = struct.pack("<H", 0x1)        # NB_CHARACTER
    buf += struct.pack("<I", 0x13337)   # CHARACTER_ID
    buf += MakePWNString("NICKNAME")
    buf += MakePWNString("Town")        # LOCATION
    buf += "\x02"                       # CHARACTER_AVATAR
    buf += struct.pack("<I", 0x00471E19)
    buf += struct.pack("<I", 0x00B061A3)
    buf += struct.pack("<I", 0x00D0D0D0)
    buf += struct.pack("<I", 0x00000000)
    buf += struct.pack("<I", 0x00000000)
    buf += "\x01"                       # CHARACTER_IS_ADMIN
    sock.write(buf)

def HandleGetPlayerCounts(sock, buf):
    print "[+] HandleGetPlayerCounts"
    buf = struct.pack("<I", 0x00000001)
    buf += struct.pack("<I", 0x00000000)
    sock.write(buf)

def HandleJoinGameServer(sock, buf):
    print "[+] HandleJoinGameServer"
    player_id = buf.GetDword()
    print "[+] player_id: %08X" % player_id
    buf = "\x01"    # return_value_00
    buf += "\x01"    # return_value_01
    buf += MakePWNString("127.0.0.1")      # SERVER IP ADDR
    buf += struct.pack("<H", 4242)
    buf += MakePWNString("1b3f03c9dfd2562934352179be88e122")    # token ?
    buf += MakePWNString("NICKNAME")
    buf += MakePWNString("sucemwa")
    buf += "\x01"                       # IS_ADMIN
    buf += struct.pack("<H", 0x1)       # NB_QUEST
    buf += MakePWNString("Bears")       # QUEST_NAME
    buf += MakePWNString("Initial")     # STATE_NAME
    buf += struct.pack("<I", 0x0)       # UNK ??? STATE ??

    buf += MakePWNString("Bears")       # ACTIVE_QUEST

    buf += struct.pack("<H", 0x2)       # NB_ITEM

    buf += MakePWNString("GreatBallsOfFire")       # ITEM_NAME
    buf += struct.pack("<I", 0x1)                  # NB
    buf += struct.pack("<H", 0x0)                  # NB

    buf += MakePWNString("ShotgunAmmo")            # ITEM_NAME
    buf += struct.pack("<I", 0x8)                  # NB
    buf += struct.pack("<H", 0x10)                 # NB

    # SLOT BAR ?
    buf += MakePWNString("GreatBallsOfFire")       # ACTIVE?
    for i in xrange(0, 0xA - 1):
        buf += MakePWNString("")

    buf += struct.pack("<B", 0x0)       # ACTIVE_SLOT ?

    buf += struct.pack("<H", 0x01)      # NB_ACHIEVEMENT

    buf += MakePWNString("Achievement_GreatBallsOfFire")

    sock.write(buf)

def HandleNotifyDisconnect(sock, buf):
    print "[+] HandleNotifyDisconnect"

def HandleTick(sock, buf):
    print "[+] HandleTick"

def HandleClient(sock):
    SendMOTD(sock)
    while True:
        buf = sock.recv(1000)
        if len(buf) == 0:
            continue
        buf = Buffer(buf)
        print hexdump(buf.buf)
        opcode = buf.GetByte()
        print "[+] Opcode: %02X" % opcode
        if opcode == 0x00:
            HandleLogin(sock, buf)
        elif opcode == 0x0A:
            HandleGetCharacterList(sock, buf)
        elif opcode == 0x02:
            HandleGetPlayerCounts(sock, buf)
        elif opcode == 0x0D:
            HandleJoinGameServer(sock, buf)
        elif opcode == 0x80:
            HandleTick(sock, buf)
        elif opcode == 0x81:
            HandleNotifyDisconnect(sock, buf)
        else:
            print "[-] unhandled opcode!"

bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bindsocket.bind(('', 3333))
bindsocket.listen(5)
newsocket, fromaddr = bindsocket.accept()
print newsocket, fromaddr
c = ssl.wrap_socket(newsocket, server_side=True, certfile="root-ca.crt", keyfile="root-ca.key", ssl_version=ssl.PROTOCOL_TLSv1)
HandleClient(c)
bindsocket.close()

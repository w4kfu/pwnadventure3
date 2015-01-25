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

def ReadPWNString(sock):
    length = struct.unpack("<H", sock.recv(2))[0]
    return sock.recv(length)

def HandleJump(sock):
    # Opcode: 0x706A
    print "[+] HandleOnPositionEvent"
    bool_j = struct.unpack("<B", sock.recv(1))[0]
    print "[+] bool_j : 0x%02X" % bool_j

def HandleOnPositionEvent(sock):
    # Opcode: 0x766D
    print "[+] HandleOnPositionEvent"
    #player_id = struct.unpack("<I", sock.recv(4))[0]
    coord_00 = struct.unpack("<f", sock.recv(4))[0]
    coord_01 = struct.unpack("<f", sock.recv(4))[0]
    coord_02 = struct.unpack("<f", sock.recv(4))[0]
    rota_00 = struct.unpack("<H", sock.recv(2))[0]  # PITCH
    rota_01 = struct.unpack("<H", sock.recv(2))[0]  # YAW
    rota_02 = struct.unpack("<H", sock.recv(2))[0]  # ROLL
    unk = struct.unpack("<H", sock.recv(2))[0]  # UNK
    print "[+] coord_00    : %f" % coord_00
    print "[+] coord_01    : %f" % coord_01
    print "[+] coord_02    : %f" % coord_02
    print "[+] rota_00     : 0x%04X" % rota_00
    print "[+] rota_01     : 0x%04X" % rota_01
    print "[+] rota_02     : 0x%04X" % rota_02
    print "[+] unk         : 0x%04X" % unk

    buf = struct.pack("<H", 0x766D)
    buf += struct.pack("<I", 0x13337)
    buf += struct.pack("<f", coord_00)
    buf += struct.pack("<f", coord_01)
    buf += struct.pack("<f", coord_02)
    buf += struct.pack("<H", 0x00)
    buf += struct.pack("<H", 0x00)
    buf += struct.pack("<H", 0x00)
    buf += struct.pack("<H", 0x00)
    sock.send(buf)

def HandleSendCurrentSlotEvent(sock):
    # opcode : 0x3D73
    print "[+] HandleSendCurrentSlotEvent"
    slot_n = struct.unpack("<B", sock.recv(1))[0]
    print "[+] slot_n : 0x%02X" % slot_n
    if slot_n < 0x0A:
        sock.send(struct.pack("<H", 0x3D73) + struct.pack("<B", slot_n))

def HandleSprint(sock):
    # opcode : 0x6E72
    print "[+] HandleSprint"
    unk_b = struct.unpack("<B", sock.recv(1))[0]
    print "[+] unk_b : 0x%02X" % unk_b

def HandleActivate(sock):
    # opcode : 0x692A
    print "[+] HandleActivate"
    unk_word_00 = struct.unpack("<H", sock.recv(2))[0]      # READ STRING
    name = sock.recv(unk_word_00)
    unk_dword_00 = struct.unpack("<f", sock.recv(4))[0]
    unk_dword_01 = struct.unpack("<f", sock.recv(4))[0]
    unk_dword_02 = struct.unpack("<f", sock.recv(4))[0]
    print "[+] unk_word_00      : 0x%04X" % unk_word_00
    print "[+] name             : %s" % name
    print "[+] unk_dword_00     : %f" % unk_dword_00
    print "[+] unk_dword_01     : %f" % unk_dword_01
    print "[+] unk_dword_02     : %f" % unk_dword_02

def HandleSetPvPDesired(sock):
    # opcode : 0x7670
    print "[+] HandleSetPvPDesired"
    unk_b = struct.unpack("<B", sock.recv(1))[0]
    print "[+] unk_b : 0x%02X" % unk_b

def HandleSetCircuitInputs(sock):
    # opcode : 0x3130
    print "[+] HandleSetCircuitInputs"
    name = ReadPWNString(sock)
    unk_dword_00 = struct.unpack("<I", sock.recv(4))[0]
    print "[+] name             : %s" % name
    print "[+] unk_dword_00     : 0x%08X" % unk_dword_00

def HandleChat(sock):
    # opcode : 0x2A23
    print "[+] HandleChat"
    msg = ReadPWNString(sock)
    if len(msg) == 0:
        return
    print "msg: %s" % msg
    buf = struct.pack("<H", 0x2A23)
    buf += struct.pack("<I", 0x13337) # PLAYER_ID
    buf += MakePWNString(msg)
    sock.send(buf)

def HandleClient(sock):
    print "[+] HandleClient"
    buf = Buffer(sock.recv(1000))
    print hexdump(buf.buf)
    buf = struct.pack("<I", 0x13337)
    buf += struct.pack("<I", 0xC71C6A27)
    buf += struct.pack("<I", 0xC696A4E9)
    buf += struct.pack("<I", 0x45189497)
    buf += struct.pack("<H", 0x00)
    buf += struct.pack("<H", 0x00)
    buf += struct.pack("<H", 0x00)
    sock.send(buf)
    while True:
        buf = sock.recv(2)
        if len(buf) == 0:
            continue
        buf = Buffer(buf)
        opcode = buf.GetWord()
        print "[+] Opcode: %02X" % opcode
        if opcode == 0x766D:
            HandleOnPositionEvent(sock)
        elif opcode == 0x706A:
            HandleJump(sock)
        elif opcode == 0x3D73:
            HandleSendCurrentSlotEvent(sock)
        elif opcode == 0x692A:
            HandleActivate(sock)
        elif opcode == 0x6E72:
            HandleSprint(sock)
        elif opcode == 0x7670:
            HandleSetPvPDesired(sock)
        elif opcode == 0x2A23:
            HandleChat(sock)
        elif opcode == 0x3130:
            HandleSetCircuitInputs(sock)
        else:
            print "[-] unhandled opcode!"
            sys.exit()


bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bindsocket.bind(('', 4242))
bindsocket.listen(5)
newsocket, fromaddr = bindsocket.accept()
print newsocket, fromaddr
HandleClient(newsocket)
bindsocket.close()

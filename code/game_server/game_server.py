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
    #player_id = struct.unpack("<I", sock.recv(4))[0]
    coord_00 = struct.unpack("<f", sock.recv(4))[0]
    coord_01 = struct.unpack("<f", sock.recv(4))[0]
    coord_02 = struct.unpack("<f", sock.recv(4))[0]
    rota_00 = struct.unpack("<H", sock.recv(2))[0]  # PITCH
    rota_01 = struct.unpack("<H", sock.recv(2))[0]  # YAW
    rota_02 = struct.unpack("<H", sock.recv(2))[0]  # ROLL
    unk = struct.unpack("<H", sock.recv(2))[0]  # UNK
    if False:
        print "[+] HandleOnPositionEvent"
        print "[+] coord_00    : %f (0x%08X)" % (coord_00, coord_00)
        print "[+] coord_01    : %f (0x%08X)" % (coord_01, coord_01)
        print "[+] coord_02    : %f (0x%08X)" % (coord_02, coord_02)
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
    name = ReadPWNString(sock)
    unk_dword_00 = struct.unpack("<f", sock.recv(4))[0]
    unk_dword_01 = struct.unpack("<f", sock.recv(4))[0]
    unk_dword_02 = struct.unpack("<f", sock.recv(4))[0]
    print "[+] name             : %s" % name
    print "[+] unk_dword_00     : %f (0x%08X)" % (unk_dword_00, unk_dword_00)
    print "[+] unk_dword_01     : %f (0x%08X)" % (unk_dword_01, unk_dword_01)
    print "[+] unk_dword_02     : %f (0x%08X)" % (unk_dword_02, unk_dword_02)

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

def ActorSpawnEvent(sock):
    buf = struct.pack("<H", 0x6B6D)
    buf += struct.pack("<I", 0x01)      # UNK_
    buf += struct.pack("<I", 0x00)      # UNK_
    buf += struct.pack("<B", 0x00)      # UNK_
    buf += MakePWNString("GreatBallsOfFire")
    buf += struct.pack("<I", 0xC71C6A27 + 100)
    buf += struct.pack("<I", 0xC696A4E9 + 100)
    buf += struct.pack("<I", 0x00000988)
    buf += struct.pack("<H", 0x00)
    buf += struct.pack("<H", 0x80)
    buf += struct.pack("<H", 0x00)
    buf += struct.pack("<I", 0x00)
    #sock.send(buf)
    buf = '6d6b0700000000000000000c0047756e53686f704f776e6572005712c700048dc6000017450000ff7f000064000000'.decode('hex')
    sock.send(buf)

def HandleUse(sock):
    # opcode: 0x6565
    print "[+] HandleUse"
    unk_dword_00 = struct.unpack("<I", sock.recv(4))[0]
    print "[+] unk_dword_00 : 0x%08X" % unk_dword_00
    buf = struct.pack("<H", 0x7323)
    buf += struct.pack("<I", unk_dword_00)
    buf += MakePWNString("Initial")
    sock.send(buf)

def HandleTransitionToNPCState(sock):
    # opcode: 0x3E23
    print "[+] HandleTransitionToNPCState"
    name = ReadPWNString(sock)
    print "[+] name: %s" % name
    buf = struct.pack("<H", 0x7323)
    buf += struct.pack("<I", 0x08)
    buf += MakePWNString(name)
    sock.send(buf)

def HandleOnSetCurrentQuestEvent(sock):
    # opcode: 0x3D71
    print "[+] HandleOnSetCurrentQuestEvent"
    name = ReadPWNString(sock)
    print "[+] name: %s" % name

def SendManaUpdate(sock):
    buf = struct.pack("<H", 0x616D)
    buf += struct.pack("<I", 0x42)  # MANA VALUE
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
    ActorSpawnEvent(sock)
    b = '6d6b0100000000000000001000477265617442616c6c734f664669726500872ac7000c5ac70000a143000000800000640000006d6b0200000000000000000c004c6f73744361766542757368002351c700d62cc70000b343000000000000640000006d6b030000000000000000090042656172436865737400b0f6c500e27b470070264523fde67f8100640000006d6b0400000000000000000800436f77436865737400fe764800a16fc80040924422fe088fc5fd640000006d6b05000000000000000009004c617661436865737400bc464700d8a3c50060be440000e3380000640000006d6b0600000000000000000b00426c6f636b79436865737400f03ec500bab34600300e45000000c00000640000006d6b0700000000000000000c0047756e53686f704f776e6572005712c700048dc6000017450000ff7f0000640000006d6b0800000000000000000f004a757374696e546f6c657261626c65007c20c700007ec600e00d450000aa6a0000640000006d6b09000000000000000006004661726d65720062a84600102147005005450000e3380000640000006d6b0a00000000000000000d004d69636861656c416e67656c6fc0277e48c0ba72c800e0b0440000c7510000640000006d6b0b00000000000000000a00476f6c64656e4567673100aac3c6004a8d4600008243000000000000640000006d6b0c00000000000000000a00476f6c64656e45676732007249c7001f6fc700e09c45000000000000640000006d6b0d00000000000000000a00476f6c64656e456767330080bf460019884700302645000000000000640000006d6b0e00000000000000000a00476f6c64656e4567673400256c47000288c600b03745000000000000640000006d6b0f00000000000000000a00476f6c64656e456767350040be4400d869460070db45000000000000640000006d6b1000000000000000000a00476f6c64656e4567673600503546002c4dc60080cd43000000000000640000006d6b1100000000000000000a00476f6c64656e4567673780ed8dc7003f51c700a0cd44000000000000640000006d6b1200000000000000000a00476f6c64656e4567673800143d4700aadb4600003044000000000000640000006d6b1300000000000000000a00476f6c64656e4567673900c97e470060b3c500009a45000000000000640000006d6b1400000000000000000e0042616c6c6d65725065616b45676700a02dc5006c2cc600202446000000000000640000006d6b150000000000000000110042616c6c6d65725065616b506f7374657200a8bec500302bc600302646000000000000640000000000'
    sock.send(b.decode('hex'))
    #sock.send("\x00" * 4)
    while True:
        buf = sock.recv(2)
        if len(buf) == 0:
            continue
        buf = Buffer(buf)
        opcode = buf.GetWord()
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
        elif opcode == 0x6565:
            HandleUse(sock)
        elif opcode == 0x3E23:
            HandleTransitionToNPCState(sock)
        elif opcode == 0x3D71:
            HandleOnSetCurrentQuestEvent(sock)
        else:
            print "[-] unhandled opcode! 0x%02X" % opcode
            sys.exit()


bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bindsocket.bind(('', 4242))
bindsocket.listen(5)
newsocket, fromaddr = bindsocket.accept()
print newsocket, fromaddr
HandleClient(newsocket)
bindsocket.close()

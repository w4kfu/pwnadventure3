# Master Server

Server.ini can be found in "PwnAdventure3_Data\PwnAdventure3\PwnAdventure3\Content\Server"

    [MasterServer]
    Hostname=192.168.30.131
    Port=443

## GameLogic.dll

    MD5  : 386CAC989E58396CD7A9505657D0BDE5
    SHA-1: 45B6BACA117092BAF6AA3045AEF3190EBACE4219

## Network

All data are stored in little-endian

## Struct

All string inside packet use the following representation, PWN_STRING:

    + 0x00:         LENGTH_BUF [WORD]
    + 0x02:         BUF        [BYTE] * LENGTH_BUF

## Function

### Login

* VA: 0x1003E800
* Opcode: 0x00

#### Packet (Client -> Server)

    + 0x00:         CMD         [BYTE] // 0x00
    + 0x01:         USERNAME    [PWN_STRING]
    + 0x..:         PASSWORD    [PWN_STRING]

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE    [BYTE]
    + 0x01:         PLAYER_ID       [DWORD]
    + 0x05:         TEAM_HASH       [PWN_STRING]
    + 0x..:         TEAM_NAME       [PWN_STRING]
    + 0x..:         IS_ADMIN        [BYTE]

### Register

* VA: 0x1003F260
* Opcode: 0x01

#### Packet (Client -> Server)

    + 0x00:         CMD         [BYTE] // 0x01
    + 0x01:         USERNAME    [PWN_STRING]
    + 0x..:         TEAM_NAME   [PWN_STRING]
    + 0x..:         PASSWORD    [PWN_STRING]

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE    [BYTE]
    + 0x01:         PLAYER_ID       [DWORD]
    + 0x05:         TEAM_HASH       [PWN_STRING]
    + 0x..:         TEAM_NAME       [PWN_STRING]
    + 0x..:         IS_ADMIN        [BYTE]

### GetPlayerCounts

* VA: 0x1003FC10
* Opcode: 0x02

#### Packet (Client -> Server)

    + 0x00:         CMD         [BYTE] // 0x02

#### Packet (Server -> Client)

    + 0x00:         DWORD_00    [DWORD]
    + 0x01:         DWORD_01    [DWORD]

### GetTeammates

* VA: 0x10040000
* Opcode: 0x03

#### Packet (Client -> Server)

    + 0x00:         CMD         [BYTE] // 0x03

#### Packet (Server -> Client)

    + 0x00:         NB_TEAMMATES [WORD]
        for (i = 0; i < NB_TEAMMATES; i++) {
            + 0x..:     NICKNAME        [PWN_STRING]
            + 0x..:     LOCATION        [PWN_STRING]
        }

### GetCharacterList

* VA: 0x10040740
* Opcode: 0x0A

#### Packet (Client -> Server)

    + 0x00:         CMD         [BYTE] // 0x0A

#### Packet (Server -> Client)

    + 0x00:         NB_CHARACTER [WORD]
        for (i = 0; i < NB_CHARACTER; i++) {
            + 0x..:     CHARACTER_ID        [WORD]
            + 0x..:     CHARACTER_NAME      [PWN_STRING]
            + 0x..:     CHARACTER_LOCATION  [PWN_STRING]
            + 0x..:     CHARACTER_AVATAR    [BYTE]
            + 0x..:     CHARACTER_COLOR_0   [DWORD]
            + 0x..:     CHARACTER_COLOR_1   [DWORD]
            + 0x..:     CHARACTER_COLOR_2   [DWORD]
            + 0x..:     CHARACTER_COLOR_3   [DWORD]
            + 0x..:     CHARACTER_FLAGS     [DWORD]
            + 0x..:     CHARACTER_IS_ADMIN  [BYTE]
        }

### CreateCharacter

* VA: 0x10041060
* Opcode: 0x0B

#### Packet (Client -> Server)

    + 0x00:         CMD         [BYTE] // 0x0B
    + TODO TODO TODO

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE    [BYTE]
    + 0x01:         CHARACTER_ID    [DWORD]


[+] Function DeleteCharacter (0x10041750), opcode = 0x0C
[+] Function JoinGameServer (0x10041AC0), opcode = 0x0D
[+] Function GetFlag (0x10042F60), opcode = 0x28
[+] Function SubmitAnswer (0x10043440), opcode = 0x2A
[+] Function StartQuest (0x10044710), opcode = 0x1E
[+] Function UpdateQuest (0x10044A30), opcode = 0x1F
[+] Function CompleteQuest (0x10044CA0), opcode = 0x20
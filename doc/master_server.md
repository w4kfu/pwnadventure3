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

    + 0x00:         OPCODE      [BYTE] // 0x00
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

    + 0x00:         OPCODE      [BYTE] // 0x01
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

    + 0x00:         OPCODE          [BYTE] // 0x02

#### Packet (Server -> Client)

    + 0x00:         NB_TEAMMATES_CONNECTED    [DWORD]
    + 0x01:         NB_PLAYER_CONNECTED    [DWORD]

### GetTeammates

* VA: 0x10040000
* Opcode: 0x03

#### Packet (Client -> Server)

    + 0x00:         OPCODE         [BYTE] // 0x03

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

    + 0x00:         OPCODE         [BYTE] // 0x0A

#### Packet (Server -> Client)

    + 0x00:         NB_CHARACTER [WORD]
        for (i = 0; i < NB_CHARACTER; i++) {
            + 0x..:     CHARACTER_ID        [DWORD]
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

    + 0x00:         OPCODE          [BYTE] // 0x0B
    + TODO TODO TODO

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE    [BYTE]
    + 0x01:         CHARACTER_ID    [DWORD]

### DeleteCharacter

* VA: 0x10041750
* Opcode: 0x0C

#### Packet (Client -> Server)

    + 0x00:         OPCODE        [BYTE] // 0x0C
    + 0x01:         CHARACTER_ID  [DWORD]

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE    [BYTE]

### JoinGameServer

* VA: 0x10041AC0
* Opcode: 0x0D

#### Packet (Client -> Server)

    + 0x00:         OPCODE        [BYTE] // 0x0D
    + 0x01:         CHARACTER_ID  [DWORD]

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE_00    [BYTE]
    + 0x01:         RETURN_VALUE_01    [BYTE]
    + 0x..:         SERVER_ADDR        [PWN_STRING]
    + 0x..:         SERVER_PORT        [WORD]
    + 0x..:         TOKEN              [PWN_STRING]
    + 0x..:         CHARACTER_NAME     [PWN_STRING]
    + 0x..:         TEAM_NAME          [PWN_STRING]
    + 0x..:         IS_ADMIN           [BYTE]
    + 0x..:         NB_SOMETHING       [WORD]
        for (i = 0; i < NB_SOMETHING; i++) {
            + 0x0..:    LOCATION            [PWN_STRING]
            + 0x0..:    QUEST_NAME          [PWN_STRING]
            + 0x0..:    UNK_DWORD_00        [DWORD]
    + 0x..:         ????               [PWN_STRING]
        TODO TODO TODO TODO

### GetFlag

* VA: 0x10042F60
* Opcode: 0x28

#### Packet (Client -> Server)

    + 0x00:         OPCODE        [BYTE]        // 0x28
    + 0x01:         FLAG_NAME     [PWN_STRING]

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE_00    [BYTE]
    + 0x01:         RESULT_STRING      [PWN_STRING]
    TODO ?

### SubmitAnswer

* VA: 0x10043440
* Opcode: 0x2A

#### Packet (Client -> Server)

    + 0x00:         OPCODE        [BYTE]        // 0x2A
    + 0x01:         QUESTION      [PWN_STRING]
    + 0x..:         ANSWER        [PWN_STRING]

#### Packet (Server -> Client)

    + 0x00:         RETURN_VALUE_00    [BYTE]
    + 0x01:         RESULT_STRING      [PWN_STRING]

[+] Function StartQuest (0x10044710), opcode = 0x1E
[+] Function UpdateQuest (0x10044A30), opcode = 0x1F
[+] Function CompleteQuest (0x10044CA0), opcode = 0x20
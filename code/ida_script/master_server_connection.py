from idaapi import *
from idc import *
from idautils import *

text_seg = idaapi.get_segm_by_name('.text')
print text_seg
print text_seg.startEA
print text_seg.endEA

def get_jmp_operator(funcea):
    f = idaapi.FlowChart(idaapi.get_func(funcea))
    for block in f:
        print hex(block.startEA)

def search_opcode(funcea):
    #print "[+] search_opcode: ", hex(funcea)
    rfuncea = 0
    for x in FuncItems(funcea):
        if GetMnem(x) == "jmp":
            rfuncea = list(XrefsFrom(x, idaapi.XREF_FAR))[0].to
            break
    if rfuncea == 0:
        print "[-] WTF?"
        sys.exit()
    for x in [x for x in FuncItems(rfuncea) if idaapi.is_call_insn(x)]:
        for xref in XrefsFrom(x, idaapi.XREF_FAR):
            if not xref.iscode:
                continue
            t = GetFunctionName(xref.to)
            #print t
            if "??$_Insert@PBE@?$" in t:
                #print "x:", hex(x)
                prev_ea = PrevHead(x)
                while GetMnem(prev_ea) != "mov":
                    prev_ea = PrevHead(prev_ea)
                #print "[+] Opcode: ", hex(GetOperandValue(prev_ea, 1))
                return rfuncea, GetOperandValue(prev_ea, 1)
    sys.exit()
    return None

def detect_lambda(funcea):
    #print hex(funcea)
    for x in FuncItems(funcea):
        if GetMnem(x) == "mov" and GetOpType(x, 0) == o_phrase and GetOpType(x, 1) == o_imm and GetOperandValue(x, 0) == 6:
            #print "x:", hex(x)
            imm = GetOperandValue(x, 1)
            do_call = Dword(imm + 4 * 2)
            return do_call
    return 0

def get_xref_by_name(funcea, name):
    for x in [x for x in FuncItems(funcea) if idaapi.is_call_insn(x)]:
        for xref in XrefsFrom(x, idaapi.XREF_FAR):
            if not xref.iscode:
                continue
            if name in GetFunctionName(xref.to):
                return xref
    return None

for funcea in Functions(text_seg.startEA, text_seg.endEA):
        if "MasterServerConnection" in GetFunctionName(funcea) and "?Connect@MasterServerConnection" not in GetFunctionName(funcea):
        #    print "Function %s at 0x%x" % (GetFunctionName(funcea), funcea)
        #if funcea == 0x10040630:
            for x in [x for x in FuncItems(funcea) if idaapi.is_call_insn(x)]:
                for xref in XrefsFrom(x, idaapi.XREF_FAR):
                    if not xref.iscode:
                        continue
                    t = GetFunctionName(xref.to)
                    if "ServerEnqueue" in t:
                        #print "[+] Function %s at 0x%x" % (GetFunctionName(funcea), funcea)
                        prev_ea = xref.frm
                        prev_ea = PrevHead(prev_ea)
                        #print hex(xref.frm)
                        #sys.exit()
                        while GetMnem(prev_ea) != "call":
                            prev_ea = PrevHead(prev_ea)
                        prev_p_ea = PrevHead(prev_ea)
                        #print hex(prev_p_ea)
                        if GetMnem(prev_p_ea) != "mov" or GetOpType(prev_p_ea, 0) != o_phrase or GetOpType(prev_p_ea, 1) != o_imm:
                            prev_p_ea = PrevHead(prev_p_ea)
                            if GetMnem(prev_p_ea) != "mov" or GetOpType(prev_p_ea, 0) != o_phrase or GetOpType(prev_p_ea, 1) != o_imm:
                                do_call = detect_lambda(list(XrefsFrom(prev_ea, idaapi.XREF_FAR))[0].to)
                                #print "[+] addr do call: %08X" % do_call
                                rfuncea, opcode = search_opcode(do_call)
                                print "[+] Function %s (0x%08X), opcode = 0x%02X" % (GetFunctionName(funcea).split('@')[0].replace("?", ""), rfuncea, opcode)
                                #exit()
                                continue
                                #print "[-] Fu :("
                                #sys.exit()
                            #print "[-] Fu :("
                            #sys.exit()
                        #prev_p_ea = PrevHead(prev_ea)
                        #print "Jump table?"
                        imm = GetOperandValue(prev_p_ea, 1)
                        #print hex(imm)
                        do_call = Dword(imm + 4 * 2)
                        #print "[+] addr do call: %08X" % do_call
                        rfuncea, opcode = search_opcode(do_call)
                        print "[+] Function %s (0x%08X), opcode = 0x%02X" % (GetFunctionName(funcea).split('@')[0].replace("?", ""), rfuncea, opcode)
                        #sys.exit()

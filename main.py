# SYMULATOR PROCESORA 8086

# dzialania matematyczne na rejestrach dodawanie, odejmowanie, mnozenie, dzielenie

# rejestry w arch x86
R8 = ['AL', 'CL', 'DL', 'BL', 'AH', 'CH', 'DH', 'BH']
R16 = ['AX', 'CX', 'DX', 'BX', 'SP', 'BP', 'SI', 'DI']
R32 = ['EAX', 'ECX', 'EDX', 'EBX', 'ESP', 'EBP', 'ESI', 'EDI']

MOD = ['11', '00']
LABELS = []
COUNTER = [0]
MACHINCODES = []

OPCODES = {
    "ADD": ['0x00', '0x01', '0x02', '0x03'],
    "SUB": ['0x28', '0x29', '0x2A', '0x2B'],
    "AND": ["0x20", "0x21", "0x22", "0x23"],
    "OR": ['0x08', '0x09', '0x0A', '0X0B']
}

BYTE = 8
WORD = 16
DWORD = 32
WIADOMOSC_BLEDU = 'Coś poszło niezgodnie z planem'


def check_registers(register):
    """Sprawdza typ rejestru i zwraca jego rozmiar i numer"""
    if register in R8:
        return [BYTE, R8.index(register)]
    elif register in R16:
        return [WORD, R16.index(register)]
    elif register in R32:
        return [DWORD, R32.index(register)]
    else:  # Jesli n jest rejesrem
        return [1, 'Nieprawidłowy rejestr']


def decimal_to_bin(number):
    """konwersja dziesietna na 3-bitowa binarna"""
    value = bin(number).replace('0b', '')
    if len(value) == 2:
        values = "0" + value
    elif len(value) == 1:
        value = '00' + value
    return value


def block_function(opcodes, reg1, reg2):
    """sprawdza, czy drugi argument nie jest pamiecia"""
    is_memory = reg2[0] != '['
    return_reg1 = check_registers(reg1.upper())
    return_reg2 = check_registers((reg2 if is_memory else reg2[1:-1]).upper())

    if return_reg1[0] == 1 or return_reg2[0] == 1:
        return WIADOMOSC_BLEDU  # jesli jeden z argumentpw nie jest
    if return_reg1[0] != return_reg2[0]:
        return 'Argumenty musza byc tego samego typu'

    binary_value = MOD[0 if is_memory else 1] + decimal_to_bin(return_reg2[1]) + decimal_to_bin(return_reg1[1])
    dec_value = int(binary_value, 2)

    if return_reg1[0] == BYTE:
        return [opcodes[0 if is_memory else 2], hex(dec_value)]
    elif return_reg1[0] == WORD:
        return ['0x66', opcodes[1 if is_memory else 3], hex(dec_value)]
    elif return_reg1[0] == DWORD:  # rejestry sa typu dword
        return [opcodes[1 if is_memory else 3], hex(dec_value)]
    else:
        return WIADOMOSC_BLEDU


def assembler(instructions, counter):
    operation = instructions[0].upper()
    if operation in OPCODES:
        retToken = block_function(OPCODES[operation], instructions[1], instructions[2])
        machine_code(retToken, counter)
    elif operation == "JMP":
        label = instructions[1]
        LABELS.append([label, counter])
        retToken = ['0xEB', label]
        machine_code(retToken, counter)
    elif operation[-1] == ":":
        label_address = operation[:-1]
        retToken = [label_address]
        machine_code(retToken, counter)
    else:
        print(WIADOMOSC_BLEDU)


def machine_code(token, counter):
    if len(token) == 1:
        newCounter = COUNTER[counter] + 0  # zliczanie pamieci dla skoków
        COUNTER.append(newCounter)
        for label in LABELS:
            if label[0] == token[0]:
                jmpAmount = hex(COUNTER[counter] - COUNTER[label[1]] - 2)  # liczenie ilosci skoków
                for mCode in MACHINCODES:
                    if mCode[2] == token[0]:
                        mCode[2] = jmpAmount
                        break
                break

    else:
        newCounter = COUNTER[counter] + len(token)
        COUNTER.append(newCounter)
        mem = hex(COUNTER[counter]) + '\t'
        newList = []
        newList.append(mem)
        for item in token:
            newList.append(item)

        MACHINCODES.append(newList)


def entry():
    print("Wprowadz dane: ")
    line = input().lower()
    instructions = []
    while line != 'end':
        instructions.append(line.split(" "))
        line = input()
    counter = 0
    for instruction in instructions:
        assembler(instruction, counter)
        counter = counter + 1

    # WYSWIETL WYNIKI

    print("\n Rezultat:")

    for code in MACHINCODES:
        print(*code)


entry()

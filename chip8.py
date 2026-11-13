import random

GEHEUGEN_GROOTTE = 4096
START_ADRES = 512
STACK_GROOTTE = 16

registers = [0] * 16
I = 0
geheugen = [0] * GEHEUGEN_GROOTTE
stack = []

toetsen = [0] * 16
nieuwe_toets = [0] * 16

delay_timer = 0
sound_timer = 0

fx0a_wacht = False

def haal_instructie_op(adres):
    byte1 = geheugen[adres]
    byte2 = geheugen[adres + 1]
    instructie = (byte1 << 8) | byte2

    return instructie

def voer_instructie_uit(instructie, pc, teken_sprite, wis_scherm):

    global delay_timer, sound_timer, fx0a_wacht, I
 
    type_instructie = instructie >> 12
    register_x = (instructie >> 8) & 0xF
    register_y = (instructie >> 4) & 0xF
    waarde = instructie & 0xFF

    if type_instructie == 1:
        adres = instructie & 0x0FFF
        print("Sprong naar adres:", hex(adres))
        return adres

    elif type_instructie == 0x2:
        if len(stack) >= STACK_GROOTTE:
            raise ValueError("Stack overflow: maximale stackgrootte bereikt")
        
        adres = instructie & 0x0FFF
        stack.append(pc + 2)
        pc = adres
        return pc

    elif type_instructie == 3:
        if registers[register_x] == waarde:
            return pc + 4

    elif type_instructie == 4:
        if registers[register_x] != waarde:
            return pc + 4

    elif type_instructie == 5:
        laatste_cijfer = instructie & 0xF
        if laatste_cijfer == 0:
            if registers[register_x] == registers[register_y]:
                return pc + 4
        else:
            raise ValueError(f"Ongeldige instructie: {hex(instructie)}")

    elif type_instructie == 6:
        registers[register_x] = waarde

    elif type_instructie == 7:
        registers[register_x] = (registers[register_x] + waarde) & 0xFF

    elif type_instructie == 8:
        laatste_cijfer = instructie & 0xF

        if laatste_cijfer == 4:
            som = registers[register_x] + registers[register_y]
            if som > 255:
                registers[0xF] = 1
            else: 
                registers[0xF] = 0
            registers[register_x] = som & 0xFF

        elif laatste_cijfer == 0:
            registers[register_x] = registers[register_y]

        elif laatste_cijfer == 1:
            registers[register_x] = registers[register_x] | registers[register_y]

        elif laatste_cijfer == 2:
            registers[register_x] = registers[register_x] & registers[register_y]

        elif laatste_cijfer == 3:
            registers[register_x] = registers[register_x] ^ registers[register_y]

        elif laatste_cijfer == 5:
            if registers[register_x] >= registers[register_y]:
                registers[0xF] = 1
            else:
                registers[0xF] = 0
            registers[register_x] = (registers[register_x] - registers[register_y]) & 0xFF

        elif laatste_cijfer == 6:
            registers[0xF] = registers[register_x] & 0x1
            registers[register_x] = registers[register_x] >> 1

        elif laatste_cijfer == 7:
            if registers[register_y] >= registers[register_x]:
                registers[15] = 1
            else:
                registers[15] = 0
            registers[register_x] = (registers[register_y] - registers[register_x]) & 0xFF

        elif laatste_cijfer == 14:
            registers[0xF] = (registers[register_x] >> 7) & 0x1
            registers[register_x] = (registers[register_x] << 1) & 0xFF
            
        else:
            raise ValueError(f"Ongeldige instructie: {hex(instructie)}")

    elif type_instructie == 9:
        laatste_cijfer = instructie & 0xF
        if laatste_cijfer == 0:
            if registers[register_x] != registers[register_y]:
                return pc + 4
        else:
            raise ValueError(f"Ongeldige instructie: {hex(instructie)}")

    elif type_instructie == 10:
        adres = instructie & 0x0FFF
        I = adres

    elif type_instructie == 0xB:
        adres = (instructie & 0x0FFF) + registers[0]
        return adres

    elif type_instructie == 0xC:
        getal = random.randint(0, 255)
        waarde = getal & waarde
        registers[register_x] = waarde

    elif type_instructie == 0xD:
        N = instructie & 0xF
        teken_sprite(registers[register_x], registers[register_y], N)

    elif type_instructie == 0:
        waarde = instructie & 0xFF
        if waarde == 0xE0:
            wis_scherm()
        elif waarde == 0xEE:
            if stack == []:
                raise ValueError("Stack underflow: RETURN zonder CALL")
            else:
                adres = stack.pop()
                pc = adres
                return pc
        else:
            return pc + 2

    elif type_instructie == 0xE:
        waarde = instructie & 0xFF
        
        if waarde == 0x9E:
            if toetsen[registers[register_x]] == 1:
                return pc + 4
            else: 
                return pc + 2

        elif waarde == 0xA1:
            if toetsen[registers[register_x]] == 0:
                return pc + 4
            else: 
                return pc + 2

        else: raise ValueError("Onbekende instructie")

    elif type_instructie == 0xF:
        waarde = instructie & 0xFF

        if waarde == 0x0A:
            if not fx0a_wacht:
                nieuwe_toets[:] = [0] * 16
                fx0a_wacht = True

            toets = zoek_ingedrukte_toets()
            if toets is not None:
                fx0a_wacht = False
                registers[register_x] = toets
                return pc + 2
            else:
                return pc 

        elif waarde == 0x55:
            for i in range(register_x +1):
                geheugen[I + i] = registers[i]

        elif waarde == 0x65:
            for i in range(register_x +1):
                registers[i] = geheugen[I + i]

        elif waarde == 0x07:
            registers[register_x] = delay_timer

        elif waarde == 0x15:
            delay_timer = registers[register_x]

        elif waarde == 0x18:
            sound_timer = registers[register_x]

        elif waarde == 0x1E:
            I = I + registers[register_x]

        elif waarde == 0x29:
            I = registers[register_x] * 5

        elif waarde == 0x33:
            getal = registers[register_x]
            geheugen[I] = getal // 100
            geheugen[I + 1] = getal // 10 % 10
            geheugen[I + 2] = getal % 10

        else: raise ValueError("Onbekende instructie")

    else:
        raise ValueError(f"Onbekende instructie: {hex(instructie)}")

    return pc + 2


def update_timers(verstreken_tijd):
    global delay_timer, sound_timer

    intervallen = 0

    while verstreken_tijd >= 1000 / 60:
        if delay_timer > 0:
            delay_timer -= 1

        if sound_timer > 0:
            sound_timer -= 1

        verstreken_tijd -= 1000 / 60
        intervallen += 1
    return intervallen

def toets_ingedrukt(toets):
    return toetsen[toets]

def zoek_ingedrukte_toets():
    for index, waarde in enumerate(nieuwe_toets):
        if waarde == 1:
            nieuwe_toets[index] = 0
            return index
    return None
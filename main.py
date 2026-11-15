import pygame
import tests
import chip8

pygame.init()

# Scherminstellingen
SCHAAL = 10
SCHERM_BREEDTE = 64
SCHERM_HOOGTE = 32

pygame_scherm = pygame.display.set_mode((
    SCHERM_BREEDTE * SCHAAL,
    SCHERM_HOOGTE * SCHAAL
))

# CHIP-8 Toetsenbord
toets_koppeling = {
    pygame.K_1: 0x01,
    pygame.K_2: 0x02,
    pygame.K_3: 0x03,
    pygame.K_4: 0x0C,
    pygame.K_q: 0x04,
    pygame.K_w: 0x05,
    pygame.K_e: 0x06,
    pygame.K_r: 0x0D,
    pygame.K_a: 0x07,
    pygame.K_s: 0x08,
    pygame.K_d: 0x09,
    pygame.K_f: 0x0E,
    pygame.K_z: 0x0A,
    pygame.K_x: 0x00,
    pygame.K_c: 0x0B,
    pygame.K_v: 0x0F
}

# ==========================================
# Configuratie
# ==========================================
# Scherm initialiseren
scherm = [[0 for x in range(SCHERM_BREEDTE)] for y in range(SCHERM_HOOGTE)]

# ==========================================
# Hulpfuncties
# ==========================================
def toon_status():
    print("V0:", chip8.registers[0])
    print("V1:", chip8.registers[1])
    print("V2:", chip8.registers[2])
    print("VF:", chip8.registers[15])
    print("I:", chip8.I)

    #toon_geheugen(START_ADRES, len(programma))

def toon_geheugen(adres, aantal):
    for i in range(adres, adres + aantal):
        print(chip8.geheugen[i])

def teken_rechthoek(start_x, start_y, breedte, hoogte):
    for y in range(start_y, start_y + hoogte):
        for x in range(start_x, start_x + breedte):
            scherm[y][x] = 1

def toon_scherm():
    for rij in scherm:
        for pixel in rij:
            if pixel == 1:
                teken = "#"
            else:
                teken = " "

            print(teken, end="")

        print()

def wis_scherm():
    for y in range(SCHERM_HOOGTE):
        for x in range(SCHERM_BREEDTE):
            scherm[y][x] = 0

def teken_sprite(start_x, start_y, N):
    chip8.registers[15] = 0

    for y in range(N):
        sprite_byte = chip8.geheugen[chip8.I + y]

        for x in range(8):
            bit = (sprite_byte >> (7 - x)) & 1

            scherm_y = (start_y + y) % SCHERM_HOOGTE
            scherm_x = (start_x + x) % SCHERM_BREEDTE

            if scherm[scherm_y][scherm_x] == 1 and bit == 1:
                chip8.registers[15] = 1

            scherm[scherm_y][scherm_x] ^= bit

def druk_toets_in(toets):
    chip8.toetsen[toets] = 1
    print("CHIP-8 toets ingedrukt:", toets)

def laat_toets_los(toets):
    chip8.toetsen[toets] = 0
    print("CHIP-8 toets losgelaten:", toets)

# ==========================================
# Geheugen en programma laden
# ==========================================

gelukt, rom_lengte = chip8.laad_rom("C:/Development/Python/Chip8-emulator/roms/Soccer.ch8")
if gelukt:
    print("ROM succesvol geladen!")
else:
    print("ROM kan niet worden geladen.")

programma = [

]

rom_einde = chip8.START_ADRES + rom_lengte
TEST_EINDE = chip8.START_ADRES + len(programma)

for i, byte in enumerate(programma):
    chip8.geheugen[chip8.START_ADRES + i] = byte

pc = chip8.START_ADRES

# ==========================================
# Geen idee???
# ==========================================
chip8.I = 300

# ==========================================
# Programma uitvoeren
# ==========================================
emulator_actief = True
pygame_actief = True
aantal_instructies = 0
max_instructies = 20
wit = (255,255,255)

klok = pygame.time.Clock()
laatste_timer_update = pygame.time.get_ticks()

while pygame_actief:
    for gebeurtenis in pygame.event.get():
        if gebeurtenis.type == pygame.QUIT:
            pygame_actief = False
            break
        elif gebeurtenis.type == pygame.KEYDOWN:
            if gebeurtenis.key in toets_koppeling:
                chip8_toets = toets_koppeling[gebeurtenis.key]
                if chip8.toetsen[chip8_toets] == 0:
                    druk_toets_in(chip8_toets)
                    chip8.nieuwe_toets[chip8_toets] = 1

        elif gebeurtenis.type == pygame.KEYUP:
            if gebeurtenis.key in toets_koppeling:
                chip8_toets = toets_koppeling[gebeurtenis.key]
                laat_toets_los(chip8_toets)

    if emulator_actief:
        try:
            for _ in range(8):
                instructie = chip8.haal_instructie_op(pc)

                #print("PC: ", pc, "| Instructie: ", hex(instructie))

                pc = chip8.voer_instructie_uit(instructie, pc, teken_sprite, wis_scherm)
                # print(hex(pc), hex(instructie))
                if chip8.delay_timer > 0:
                    print("Delay timer:", chip8.delay_timer)

        except ValueError as fout:
            print(f"Emulator gestopt: {fout}")
            emulator_actief = False

    pygame_scherm.fill((0, 0, 0))
    for y in range(SCHERM_HOOGTE):
        for x in range(SCHERM_BREEDTE):
            if scherm[y][x] == 1:
                pygame.draw.rect(pygame_scherm, wit, (x * SCHAAL, y * SCHAAL, SCHAAL, SCHAAL))

    pygame.display.flip()
    klok.tick(60)

    huidige_tijd = pygame.time.get_ticks()
    verstreken_tijd = huidige_tijd - laatste_timer_update

    intervallen = chip8.update_timers(verstreken_tijd)

    laatste_timer_update += intervallen * (1000 / 60)

pygame.quit()

##########################################




# 1NNN — springen naar een adres
# 3XNN — sla volgende instructie over als VX gelijk is aan NN
# 6XNN — een waarde in een register zetten
# 7XNN — een waarde bij een register optellen
# 8XY0 — een register kopiëren
# 8XY4 — twee registers optellen
# 8XY5 — registers aftrekken, inclusief VF.
# 8XY6 — bits naar rechts verschuiven.
# 8XYE — bits naar links verschuiven.
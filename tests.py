import chip8


def test_8xy4_scenario(begin_v1, begin_v2, eind_v1, verwacht_vf):
    chip8.registers = [0] * 16
    chip8.registers[1] = begin_v1
    chip8.registers[2] = begin_v2

    pc = chip8.START_ADRES

    assert chip8.registers[0xF] == 0

    pc = chip8.voer_instructie_uit(0x8124, pc, teken_sprite=None, wis_scherm=None)

    assert chip8.registers[1] == eind_v1, "V1 bevat niet de verwachte waarde"
    assert chip8.registers[2] == begin_v2, "V2 bevat niet de verwachte waarde"
    assert chip8.registers[0xF] == verwacht_vf, "VF bevat niet de verwachte waarde"
    assert pc == 514

def test_8xy5_scenario(begin_v1, begin_v2, eind_v1, verwacht_vf):
    chip8.registers = [0] * 16
    chip8.registers[1] = begin_v1
    chip8.registers[2] = begin_v2

    pc = chip8.START_ADRES

    assert chip8.registers[0xF] == 0

    pc = chip8.voer_instructie_uit(0x8125, pc, teken_sprite=None, wis_scherm=None)

    assert chip8.registers[1] == eind_v1, "V1 bevat niet de verwachte waarde"
    assert chip8.registers[2] == begin_v2, "V2 bevat niet de verwachte waarde"
    assert chip8.registers[0xF] == verwacht_vf, "VF bevat niet de verwachte waarde"
    assert pc == 514

def test_8xy7_scenario(begin_v1, begin_v2, eind_v1, verwacht_vf):
    chip8.registers = [0] * 16
    chip8.registers[1] = begin_v1
    chip8.registers[2] = begin_v2

    pc = chip8.START_ADRES

    assert chip8.registers[0xF] == 0

    pc = chip8.voer_instructie_uit(0x8127, pc, teken_sprite=None, wis_scherm=None)

    assert chip8.registers[1] == eind_v1, "V1 bevat niet de verwachte waarde"
    assert chip8.registers[2] == begin_v2, "V2 bevat niet de verwachte waarde"
    assert chip8.registers[0xF] == verwacht_vf, "VF bevat niet de verwachte waarde"
    assert pc == 514

def test_8xy7():
    scenario_s = [
    (8, 20, 12, 1),
    (20, 8, 244, 0),
    (20, 20, 0, 1)
    ]
    for begin_v1, begin_v2, eind_v1, verwacht_vf in scenario_s:
        test_8xy7_scenario(begin_v1, begin_v2, eind_v1, verwacht_vf)

def run_tests():
    test_geslaagd = 0
    test_mislukt = 0

    tests = [
        test_8xy7
    ]

    for test in tests:
        try:
            test()
            test_geslaagd += 1
            print(test.__name__, "gelukt!")
        except AssertionError as fout:
            test_mislukt += 1
            print(test.__name__, "mislukt!", fout)

    tests_uitgevoerd = test_geslaagd + test_mislukt
    print("Tests uitgevoerd: ", tests_uitgevoerd)
    print("Tests geslaagd: ", test_geslaagd)
    print("Tests mislukt: ", test_mislukt)


if __name__ == "__main__":
    run_tests()
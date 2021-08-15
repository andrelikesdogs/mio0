from mio0.endians import Endianness

ROM_START_ADDR = 0x000D0000

def find_mio0_indices(rom: bytes):

    mio0_indices = []
    
    for rom_index in range(ROM_START_ADDR, len(rom), 16):
        if rom[rom_index:rom_index+4].decode('ascii', errors='ignore') == 'MIO0':
            mio0_indices.append(rom_index)

    return mio0_indices
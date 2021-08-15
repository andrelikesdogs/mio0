from mio0.endians import Endianness

HEADER_SIZE = 0x10


def read_layout_bit(data, bit_idx):
    byte_index = (bit_idx // 8)
    bit_mod_offset = bit_idx % 8
    return data[HEADER_SIZE + byte_index] & (1 << (7 - bit_mod_offset))

def decompress_mio0(data: bytes, endianness: Endianness):
    header = str(data[0x0:0x4], 'ascii')
    
    if header != 'MIO0':
        raise ValueError('Invalid header, not starting with "MIO0"')

    # length of decompressed contents
    dl = int.from_bytes(data[4:8], endianness.value)

    # offset of compressed data
    co = int.from_bytes(data[8:12], endianness.value)

    # offset of uncompressed data
    uo = int.from_bytes(data[12:16], endianness.value)

    output_byte_array = bytearray()
    output_index = 0
    layout_bit_index = 0

    ci = 0
    ui = 0

    while output_index < dl:
        layout_bit = read_layout_bit(data, layout_bit_index)

        is_uncompressed = layout_bit > 0
        layout_bit_index += 1

        if output_index >= dl:
            break
        
        if is_uncompressed:
            output_byte_array.append(data[uo + ui])
            ui += 1
            output_index += 1
        else:

            # bytes formated for length and index of where to read from uncompressed
            # 1 0 1 0 0 0 0 1   0 0 0 0 0 0 0 0
            # [     ] [                       ]
            #    \ Length   \_ Lookback Index
            len_idx_bytes = data[co + ci:co + ci + 2]
            ci += 2

            length = ((len_idx_bytes[0] & 0xF0) >> 4) + 3
            index = ((len_idx_bytes[0] & 0xF) << 8) + (len_idx_bytes[1] + 1)

            if length < 3 or length > 18:
                raise Exception(f"unplausible length value: {length}")

            if index < 1 or index > 4096:
                raise Exception(f"unplausible index value: {index}")
            
            for i in range(length):
                output_byte_array.append(output_byte_array[output_index - index])
                output_index += 1
    
    end = uo + ui

    return bytes(output_byte_array), end
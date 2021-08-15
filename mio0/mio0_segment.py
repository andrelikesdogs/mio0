from mio0.endians import Endianness

HEADER_SIZE = 0x10

def as_hex_str(byteslike: bytearray):
    output_str = ""
    for m in byteslike:
        output_str += f"{hex(m)} "
        
    return output_str

class MIO0_Segment:
    input_data: bytes
    output_data: bytes
    start_in_rom: int
    end_in_rom: int
    decompressed_length: int
    compressed_offset: int
    uncompressed_offset: int

    @staticmethod
    def from_mio0_start(data: bytes, mio0_index: int, endianess: Endianness):

        
        #print(mio0_index, dl, co, uo)
        #return
        return MIO0_Segment(data, mio0_index, None, endianess)

    def read_layout_bit(self, bit_idx):
        byte_index = (bit_idx // 8)
        bit_mod_offset = bit_idx % 8
        #print(byte_index, bin(1 << (7 - bit_mod_offset)))
        return self.input_data[HEADER_SIZE + byte_index] & (1 << (7 - bit_mod_offset))

    def decompress(self):
        output_index = 0

        # uncompressed and compressed index
        ui = 0
        ci = 0

        bit_index = 0

        output_byte_array = bytearray()
        while output_index < self.decompressed_length:
            layout_bit = self.read_layout_bit(bit_index)
            
            is_uncompressed = layout_bit > 0
            bit_index += 1
            
            if output_index >= self.decompressed_length:
                break

            if is_uncompressed:
                output_byte_array.append(self.uncompressed_data[ui])
                ui += 1

                output_index += 1
            else:
                #print("compressed", ci)
                comp_b = self.compressed_data[ci:ci+2]
                ci += 2

                length = ((comp_b[0] & 0xF0) >> 4) + 3
                index = ((comp_b[0] & 0xF) << 8) + comp_b[1] + 1

                if length < 3 or length > 18:
                    raise Exception("unplausible value, length var mismatch")

                if index < 1 or index > 4096:
                    raise Exception("unplausible value, idx var mismatch")
                
                for i in range(length):
                    output_byte_array.append(output_byte_array[output_index - index])
                    output_index += 1

                '''
                print(
                    "ERROR: " if compare_bytes[output_index-1] != output_byte_array[output_index-1] else "",
                    compare_bytes[output_index-1], 
                    output_byte_array[output_index-1], 
                    "uncompressed" if is_uncompressed else "compressed"
                )
                assert compare_bytes[output_index-1] == output_byte_array[output_index-1]
                '''
        self.output_data = bytes(output_byte_array)
        self.end_in_rom = HEADER_SIZE + ui + ci
        return self.output_data

    def read_header(self):
        header = str(self.input_data[0x0:0x4], 'ascii')

        if header != 'MIO0':
            raise ValueError('Invalid Header found, not a MIO0 segment')

        dl = int.from_bytes(self.input_data[4:8], self.endianness.value)
        co = int.from_bytes(self.input_data[8:12], self.endianness.value)
        uo = int.from_bytes(self.input_data[12:16], self.endianness.value)

        self.decompressed_length = dl
        self.compressed_offset = co
        self.uncompressed_offset = uo
        self.compressed_length = uo - co + HEADER_SIZE
        self.uncompressed_length = (dl + HEADER_SIZE) - uo

    def __init__(self, input_data: bytes, start_in_rom: int, end_in_rom: int, endianness: Endianness):
        # , dl: int, co: int, uo: int
        self.input_data = input_data
        self.endianness = endianness

        self.start_in_rom = start_in_rom
        self.end_in_rom = end_in_rom
        
        self.read_header()

        if self.end_in_rom is not None and self.start_in_rom is not None:
            self.length_on_rom = self.end_in_rom - self.start_in_rom

        # at this point we 100% have the end pos, so lets truncate the input data
        self.input_data = self.input_data[0:self.length_on_rom]

        self.output_data = None
        self.compressed_data = self.input_data[self.compressed_offset:]
        self.uncompressed_data = self.input_data[self.uncompressed_offset:]


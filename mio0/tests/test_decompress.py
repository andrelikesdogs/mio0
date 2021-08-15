from mio0 import find_mio0_indices, decompress_mio0, Endianness

from pathlib import Path

def test_decompress():
    with open("SM64_US.z64", "rb") as rom:
        rom_data = rom.read()

        segment_indices = find_mio0_indices(rom_data)

        assert len(segment_indices) == 79 # test rom has exactly 79 mio0 segments

        for segment_start in segment_indices:
            compare_file_name = f"mio0_output_{segment_start}.dat"
            compare_file_path = Path(f"./decompressed_mio0/{compare_file_name}")

            assert compare_file_path.exists(), "Must have matching comparison file (possibly detected mio0 segment at wrong position)"

            output, _ = decompress_mio0(rom_data[segment_start:], Endianness.BIG)
            
            #print(segment_length)
            
            with open(compare_file_path, 'rb') as compare_source:
                compare_bytes = compare_source.read()
                assert output == compare_bytes, "Must match comparison file"
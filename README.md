# MIO0 Python Implementation

Python implementation of the N64 compression algorithm "MIO0". Technical documentation of this was taken from [hack64](https://hack64.net/wiki/doku.php?id=super_mario_64:mio0) with a lot of help by looking at [https://github.com/queueRAM/sm64tools](queueRAM/sm64tools)

# Installation
```bash
pip install mio0
```

# Quick start

```py
from mio0 import find_mio0_indices, Endianness, decompress_mio0

# obtain rom as bytes
rom = open("SM64_US.z64", "rb").read() # "rb" => read binary results in bytes return value

# lists all mio0 segments found in rom
indices = find_mio0_indices(rom)

for segment_index in indices:
    # endianness will depend on rom used
    # - z64 = big
    # - n64 = little
    # - v64 = mixed (convert before)
    output, segment_length = decompress_mio0(rom[segment_index:], Endianness.BIG)
```
from nbt import nbt
from frozendict import frozendict
from pyblock.editor import Editor
from pyblock.block import Block
import os
import shutil
import logging
import math
from pathlib import Path
from typing import Tuple

# Define Region size and chunk size
REGION_SIZE = 512
CHUNK_SIZE = 16
CHUNKS_REGION = 32

def block_to_id_index(x: int, y: int, z: int) -> Tuple:
    """Returns the ID of the section and the index of the block location for the section.

    Args:
        x, y, z: Absolute block coordinates
    """
    def block_to_region(x:int, z:int) -> list:
        return (x // REGION_SIZE, z // REGION_SIZE)
    def block_to_chunk(xr: int, zr: int) -> list:
        return (xr // CHUNK_SIZE, zr // CHUNK_SIZE)
    def block_to_ylevel(y: int) -> int:
        return y // CHUNK_SIZE
    def block_index(xs:int, ys:int, zs:int) -> int:
        return ys * 320 + zs * 16 + xs

    region = block_to_region(x, z)
    chunk = block_to_chunk(x % REGION_SIZE, z % REGION_SIZE)
    ylevel = block_to_ylevel(y)
    index = block_index(x % CHUNK_SIZE, y % CHUNK_SIZE, z % CHUNK_SIZE)
    return region, chunk, ylevel, index

# Load the source world and destination world
source_world_path = r'C:\\Users\\zombi\\Documents\\Capstone Project\\minecraft_worlds_tests\\Tutorial\\'
destination_world_path = r'C:\\Users\\zombi\\Documents\\Capstone Project\\minecraft_worlds_tests\\TU recreation\\'

try:
    source_editor = Editor(source_world_path)
    print("Source world loaded successfully.")
    destination_editor = Editor(destination_world_path)
    print("Destination world loaded successfully.")
except Exception as e:
    print(f"Error loading world: {e}")

# Defines the starting chunk coordinates in the source world which will be copied
source_start_coords = (1 * CHUNK_SIZE, 0, 0 * CHUNK_SIZE)  
# Sets the size of one chunk
chunk_size = [CHUNK_SIZE, 320, CHUNK_SIZE]  

# Defines the starting chunk coordinates in the destination world
destination_start_coords = (5 * CHUNK_SIZE, 0, 0 * CHUNK_SIZE)  

# Define the range of chunks to be copied based on the x and z chunks 
# (Note: y chunks do not exist if you were thinking about asking that)
chunks_x = 10  
chunks_z = 10  

# Copy the chunks from the source world to the destination world
for dx in range(chunks_x):
    for dz in range(chunks_z):
        source_coords = (source_start_coords[0] + dx * CHUNK_SIZE, source_start_coords[1], source_start_coords[2] + dz * CHUNK_SIZE)
        destination_coords = (destination_start_coords[0] + dx * CHUNK_SIZE, destination_start_coords[1], destination_start_coords[2] + dz * CHUNK_SIZE)
        destination_editor.copy_blocks(source_coords, destination_coords, chunk_size, world_source=source_world_path)

# Save the destination world
try:
    print("Saving the destination world")
    destination_editor.done()
    print("Destination world saved successfully.")
except Exception as e:
    print(f"Error saving destination world: {e}")
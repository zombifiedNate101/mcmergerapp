from nbt import nbt
from frozendict import frozendict
import pymcworld.world as pmw
from pymcworld.block import Block
from pymcworld.chunk import Chunk
import os
import shutil

# Define the GoldBlock class
class GoldBlock(Block):
    def __init__(self):
        super().__init__("minecraft:gold_block", {})

# Load the Minecraft world from its path
world = pmw.World()
world.load(r'C:\\Users\\zombi\\Documents\\Capstone Project\\minecraft_worlds_tests\\Pack.PNG (1.16)\\')

# Define the chunk coordinates
chunk_x, chunk_z = 0, 0

# Define the block type and coordinates where it should start and end
# Create an instance of GoldBlock
gold_block = GoldBlock()
start_coords = (10, 64, 10)
end_coords = (20, 70, 20)

# Helper function to retrieve or create a chunk
def get_or_create_chunk(world, chunk_x, chunk_z):
    region_x = chunk_x >> 5
    region_z = chunk_z >> 5

    region = world.region_exists(region_x, region_z)
    if not region:
        region = pmw.Region(region_x, region_z)
        world.regions.append(region)

    chunk = region.get_chunk(chunk_x % 32, chunk_z % 32)
    if not chunk:
        chunk = Chunk(chunk_x, chunk_z)
        region.add_chunk(chunk)

    return chunk

# Retrieve or create the chunk
chunk = get_or_create_chunk(world, chunk_x, chunk_z)

# Fill the blocks within the specified range
for x in range(start_coords[0], end_coords[0] + 1):
    for y in range(start_coords[1], end_coords[1] + 1):
        for z in range(start_coords[2], end_coords[2] + 1):
            print(f"Setting block at ({x}, {y}, {z}) to {gold_block}")
            chunk.set_block(x % 16, y, z % 16, gold_block)

# Save the world
# Define the folder path
folder_path = r'C:\\Users\\zombi\\Documents\\minecraft_worlds_tests\\Pack.PNG (1.16)'

# Delete the existing folder if it exists
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)

# Save the world
print("Saving the world")
world.save(folder_path)
print("World saved")

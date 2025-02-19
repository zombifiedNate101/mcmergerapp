from nbt import nbt
from frozendict import frozendict
import pymcworld.world as pmw
from pymcworld.block import Block
import os
import shutil

# Define the GoldBlock class
class GoldBlock(Block):
    def __init__(self):
        super().__init__("minecraft:gold_block", {})

# Load the Minecraft world from its path
world = pmw.World()
world.load(r'C:\\Users\\zombi\\Documents\\Capstone Project\\minecraft_worlds_tests\\Pack.PNG (1.16)\\')

# Define the block type and coordinates where it should start and end
# Create an instance of GoldBlock
gold_block = GoldBlock()
start_coords = (10, 64, 10)
end_coords = (20, 70, 20)

# Fill the blocks
for x in range(start_coords[0], end_coords[0] + 1):
    for y in range(start_coords[1], end_coords[1] + 1):
        for z in range(start_coords[2], end_coords[2] + 1):
            print(f"Setting block at ({x}, {y}, {z}) to {gold_block}")
            world.set_block(x, y, z, gold_block)

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

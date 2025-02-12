from nbt import nbt
from frozendict import frozendict

import mcworldlib as mwl
import pyblock.block as pb_block 

# Load the Minecraft world
world = mwl.World('C:\\Users\\zombi\\AppData\\Roaming\\.minecraft\\saves\\Pack.PNG (1.16)')

# Define the block type and coordinates
block_type = pb_block('minecraft:gold_block')
start_coords = (10, 64, 10)
end_coords = (20, 70, 20)

# Fill the blocks
for x in range(start_coords[0], end_coords[0] + 1):
    for y in range(start_coords[1], end_coords[1] + 1):
        for z in range(start_coords[2], end_coords[2] + 1):
            world.set_block((x, y, z), block_type)

# Save the world
world.save()




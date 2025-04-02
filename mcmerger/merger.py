from pyblock.editor import Editor

def merge_worlds(source_world_path, destination_world_path, chunk_size, chunks_x, chunks_z):
    try:
        source_editor = Editor(source_world_path)
        destination_editor = Editor(destination_world_path)

        source_start_coords = (1 * chunk_size[0], 0, 0 * chunk_size[2])
        destination_start_coords = (5 * chunk_size[0], 0, 0 * chunk_size[2])

        for dx in range(chunks_x):
            for dz in range(chunks_z):
                source_coords = (source_start_coords[0] + dx * chunk_size[0],
                                 source_start_coords[1],
                                 source_start_coords[2] + dz * chunk_size[2])
                destination_coords = (destination_start_coords[0] + dx * chunk_size[0],
                                      destination_start_coords[1],
                                      destination_start_coords[2] + dz * chunk_size[2])
                destination_editor.copy_blocks(source_coords, destination_coords, chunk_size, world_source=source_world_path)

        destination_editor.done()
        return "Merge completed successfully!"
    except Exception as e:
        return f"Error: {e}"

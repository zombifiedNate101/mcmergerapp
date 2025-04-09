from pyblock.editor import Editor

def merge_worlds(source_world_path, destination_world_path, chunk_size, start_chunk_coords, end_chunk_coords):
    try:
        source_editor = Editor(source_world_path)
        destination_editor = Editor(destination_world_path)

        # Extract chunk ranges
        start_x, start_z = start_chunk_coords
        end_x, end_z = end_chunk_coords

        for chunk_x in range(start_x, end_x + 1):
            for chunk_z in range(start_z, end_z + 1):
                # Calculate source and destination coordinates for each chunk
                source_coords = (chunk_x * chunk_size[0], 0, chunk_z * chunk_size[2])
                destination_coords = (chunk_x * chunk_size[0], 0, chunk_z * chunk_size[2])

                # Copy chunk data
                destination_editor.copy_blocks(source_coords, destination_coords, chunk_size, world_source=source_world_path)

        # Save changes to the destination world
        destination_editor.done()
        return "Merge completed successfully!"
    except Exception as e:
        return f"Error: {e}"


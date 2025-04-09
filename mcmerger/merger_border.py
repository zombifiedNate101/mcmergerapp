
from pyblock.editor import Editor


def merge_worlds(source_world_path, destination_world_path, chunk_size, 
                 source_start_chunk_coords, source_end_chunk_coords,
                 destination_start_chunk_coords, destination_end_chunk_coords):
    try:
        source_editor = Editor(source_world_path)
        destination_editor = Editor(destination_world_path)

        # Extract source and destination chunk ranges
        source_start_x, source_start_z = source_start_chunk_coords
        source_end_x, source_end_z = source_end_chunk_coords
        dest_start_x, dest_start_z = destination_start_chunk_coords
        dest_end_x, dest_end_z = destination_end_chunk_coords

        # Map chunks from source to destination
        for source_chunk_x, dest_chunk_x in zip(range(source_start_x, source_end_x + 1),
                                                range(dest_start_x, dest_end_x + 1)):
            for source_chunk_z, dest_chunk_z in zip(range(source_start_z, source_end_z + 1),
                                                    range(dest_start_z, dest_end_z + 1)):
                # Calculate coordinates for each chunk
                source_coords = (source_chunk_x * chunk_size[0], 0, source_chunk_z * chunk_size[2])
                destination_coords = (dest_chunk_x * chunk_size[0], 0, dest_chunk_z * chunk_size[2])

                # Smooth terrain borders
                destination_editor.smooth_chunk_borders(source_editor, source_coords, destination_coords, chunk_size)

                # Merge and copy blocks as usual
                destination_editor.copy_blocks(source_coords, destination_coords, chunk_size, world_source=source_world_path)

        # Save changes to the destination world
        destination_editor.done()
        return "Merge completed successfully!"
    except Exception as e:
        return f"Error: {e}"

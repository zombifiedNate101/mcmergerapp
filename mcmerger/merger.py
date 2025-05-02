from pyblock.editor import Editor

def merge_worlds(source_world_path, destination_world_path, chunk_size, source_start_chunk_coords, source_end_chunk_coords, destination_start_chunk_coords):
    try:
        source_editor = Editor(source_world_path)
        destination_editor = Editor(destination_world_path)

        # Extract source and destination chunk ranges
        source_start_x, source_start_z = source_start_chunk_coords
        source_end_x, source_end_z = source_end_chunk_coords
        destination_start_x, destination_start_z = destination_start_chunk_coords

        for chunk_x in range(source_start_x, source_end_x + 1):
            for chunk_z in range(source_start_z, source_end_z + 1):
                # Calculate source coordinates
                source_coords = (chunk_x * chunk_size[0], 0, chunk_z * chunk_size[2])

                # Calculate destination coordinates with offset
                destination_coords = (
                    (chunk_x - source_start_x) * chunk_size[0] + destination_start_x * chunk_size[0],
                    0,
                    (chunk_z - source_start_z) * chunk_size[2] + destination_start_z * chunk_size[2]
                )

                # Debugging output
                print(f"Copying from Source: {source_coords} to Destination: {destination_coords}")

                # Copy chunk data
                try:
                    destination_editor.copy_blocks(source_coords, destination_coords, chunk_size, world_source=source_world_path)
                except Exception as e:
                    print(f"Error copying blocks from {source_coords} to {destination_coords}: {e}")

        # Save changes to the destination world
        destination_editor.done()
        return "Merge completed successfully!"
    except Exception as e:
        return f"Error: {e}"


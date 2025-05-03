from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner

import os
from pathlib import Path
    
from mcmerger.merger import merge_worlds  # Import the merger module
from pyblock.editor import Editor
from pyblock.block import Block
from pyblock import tools, chunk  # Import tools and chunk from pyblock
import pyblock  # Import the pyblock module to use its namespace
from pyblock.region import Region  # Import the Region class
from pyblock.constants import MIN_SECTION, MAX_SECTION  # Import constants for section limits

Window.size = (1280, 720)

# Define the base directory where all Minecraft worlds are stored
worlds_directory = os.path.normpath("C:/Users/zombi/Documents/Capstone Project/minecraft_worlds_tests")

# Define the get_region_folder function
def get_region_folder(worlds_directory, world_name):
    """
    Constructs the path to the region folder for a given world and validates its existence.

    Args:
        worlds_directory (str): The base directory where all Minecraft worlds are stored.
        world_name (str): The name of the world.

    Returns:
        str: The path to the region folder if it exists.

    Raises:
        FileNotFoundError: If the region folder does not exist.
    """
    world_path = os.path.join(worlds_directory, world_name)
    region_folder = os.path.join(world_path, "region")

    if not os.path.exists(region_folder):
        raise FileNotFoundError(f"Region folder not found at {region_folder}")

    return region_folder


class ChunkMapViewer(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.4)  # Viewer size hint
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark gray background
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)  # Placeholder rectangle

        # Bind the position and size of the rectangle to the widget
        self.bind(pos=self._update_rectangle, size=self._update_rectangle)

    def _update_rectangle(self, instance, value):
        """
        Updates the background rectangle's position and size to match the widget.
        """
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def draw_chunks(self, chunk_data, color=(0, 0, 1, 0.5), scale=10):
        self.canvas.clear()
        with self.canvas:
            Color(*color)
            for chunk_x, chunk_z in chunk_data:
                rect_x = self.pos[0] + chunk_x * scale
                rect_z = self.pos[1] + chunk_z * scale
                Rectangle(pos=(rect_x, rect_z), size=(scale, scale))

    def draw_surface_blocks(self, editor, world_name, chunk_coords, scale=10):
        """
        Draws the surface blocks for the given chunk coordinates.
        """
        print(f"Drawing surface blocks for world: {world_name}, chunks: {len(chunk_coords)}")
        self.canvas.clear()
        try:
            # Validate the existence of the region folder
            region_folder = get_region_folder(worlds_directory, world_name)
            print(f"Region folder found: {region_folder}")

            with self.canvas:
                for chunk_x, chunk_z in chunk_coords:
                    try:
                        print(f"Processing chunk ({chunk_x}, {chunk_z})")
                        # Convert chunk coordinates to region coordinates
                        region_coords = tools.chunk_to_region(chunk_x, chunk_z)
                        region_path = Path(region_folder) / f"r.{region_coords[0]}.{region_coords[1]}.mca"

                        # Validate the existence of the region file
                        if not region_path.exists():
                            print(f"Warning: Region file not found: {region_path}")
                            continue

                        # Load the region
                        region = Region(region_folder, region_coords)

                        # Get the chunk from the region
                        chunk_coord = (chunk_x % 32, chunk_z % 32)
                        chunk = region.get_chunk(chunk_coord)
                        if chunk is None:
                            print(f"Warning: Failed to render chunk {chunk_coord}: Invalid or missing chunk data.")
                            continue

                        # Iterate through the blocks in reverse Y-level order
                        for x in range(16):
                            for z in range(16):
                                world_x = chunk_x * 16 + x
                                world_z = chunk_z * 16 + z

                                found_block = False  # Flag to track if a non-air block is found
                                for y in range(320, -65, -1):  # From Y=320 to Y=-64
                                    # Validate Y-level
                                    y_section = y // 16
                                    if y_section < MIN_SECTION or y_section > MAX_SECTION:
                                        continue  # Skip invalid Y-levels

                                    block = editor.get_block(world_x, y, world_z)
                                    block_name = block.name()  # Correctly call the name method
                                    if block_name in ["air", "cave_air", "minecraft:air", "minecraft:cave_air"]:
                                        # Skip air blocks
                                        continue

                                    # Debug: Print block name
                                    print(f"Block found at ({world_x}, {y}, {world_z}): {block_name}")

                                    # Look up the block's color
                                    color = editor.colormap.get(block_name, None)
                                    if color is None:
                                        print(f"Warning: Color not found for block '{block_name}', using default color.")
                                        color = [0, 0, 1, 1]  # Default to blue

                                    # Draw the block's color
                                    Color(*[c / 255 for c in color])
                                    rect_x = self.pos[0] + world_x * scale
                                    rect_z = self.pos[1] + world_z * scale
                                    Rectangle(pos=(rect_x, rect_z), size=(scale, scale))
                                    print(f"Drew block at ({world_x}, {y}, {world_z}) with color {color}")
                                    found_block = True
                                    break  # Stop descending once a non-air block is found

                                if not found_block:
                                    print(f"No non-air block found for ({world_x}, {world_z})")
                    except Exception as e:
                        print(f"Warning: Failed to render chunk ({chunk_x}, {chunk_z}): {e}")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def visualize_area(self, coords, radius):
        """
        Visualizes a bounding box on the map viewer based on coordinates and radius.
        """
        try:
            area = tools.get_area(None, coords, radius)

            # Convert area coordinates to relative positions
            x_min, z_min = area[0]
            x_max, z_max = area[1]

            with self.canvas:
                Color(1, 0, 0, 0.3)  # Red for bounding box
                Rectangle(pos=(self.pos[0] + x_min, self.pos[1] + z_min),
                          size=(x_max - x_min, z_max - z_min))
        except Exception as e:
            print(f"Error visualizing area: {e}")


class MainWindow(FloatLayout):
    def __init__(self):
        super().__init__()
        
        

        # Background image setup
        self.bg_image = Image(source="C:\\Users\\zombi\\Documents\\Capstone Project\\images\\6104142.png", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg_image)  # Add background image first to make it appear behind other widgets

        # Center Title
        title_label = Label(
            text="Minecraft World Editor",
            size_hint=(2, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 1},
            font_size=64,
            color=(1, 1, 1, 1)
        )
        self.add_widget(title_label)

        # Top-Left Buttons and Descriptions
        top_left_layout = BoxLayout(orientation="vertical", spacing=20, size_hint=(0.2, None), height=120)
        top_left_layout.pos_hint = {"x": 0.05, "top": 0.94}  # Adjusted for top-left corner

        # World Merger Button
        merger_button = Button(text="World Merger", size_hint=(1, None), height=40)
        merger_button.bind(on_press=self.show_merger_inputs)
        merger_description = Label(
            text="Choose certain chunks from a Source world\n and place them in a Destination world.",
            size_hint=(1, None),
            height=30,
            font_size=32,  
            color=(1, 1, 1, 1)
        )
        top_left_layout.add_widget(merger_button)
        top_left_layout.add_widget(merger_description)

        # Fill Blocks Button
        fill_blocks_button = Button(text="Fill Blocks", size_hint=(1, None), height=40)
        fill_blocks_button.bind(on_press=self.show_fill_blocks_inputs)
        fill_blocks_description = Label(
            text="Choose a block from minecraft and\n fill a specific area with those chosen blocks.",
            size_hint=(1, None),
            height=30,
            font_size=32,  
            color=(1, 1, 1, 1)
        )
        top_left_layout.add_widget(fill_blocks_button)
        top_left_layout.add_widget(fill_blocks_description)

        # Add the layout to the FloatLayout
        self.add_widget(top_left_layout)


        # Scrollable Content Layout for Inputs
        self.scroll_view = ScrollView(size_hint=(0.9, 0.6), pos_hint={"center_x": 0.5, "center_y": 0.4})
        self.content_layout = BoxLayout(
            orientation='vertical',
            padding=[20, 20, 20, 20],
            spacing=15,
            size_hint_y=None
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        self.scroll_view.add_widget(self.content_layout)
        self.add_widget(self.scroll_view)

            # Input Section Placeholder
        self.input_layout = None  # Will be populated dynamically


        

    def create_labeled_spinner(self, label_text, values, description):
        """
        Helper function to create a spinner with title and description.
        """
        container = BoxLayout(orientation='vertical', spacing=24, size_hint=(1, None), height=120)
        label = Label(text=label_text, size_hint=(1, None), height=30, font_size=32)
        spinner = Spinner(values=values, size_hint=(1, None), height=40, font_size=32)  # Shorter scroller button height
        description_label = Label(text=description, size_hint=(1, None), height=40, font_size=24, color=(0.7, 0.7, 0.7, 1))

        container.add_widget(label)
        container.add_widget(spinner)
        container.add_widget(description_label)
        return container, spinner
    
    def clear_content(self):
        """Clear dynamic content from both input_layout and right_layout."""
        # Clear widgets in input_layout
        if self.input_layout:
            for child in list(self.input_layout.children):  # Clear all child widgets in input_layout
                self.input_layout.remove_widget(child)
            self.remove_widget(self.input_layout)  # Remove input_layout from the parent layout
            self.input_layout = None

        # Clear widgets in right_layout (if you want spinners and dynamic widgets removed)
        if hasattr(self, 'right_layout') and self.right_layout:
            for child in list(self.right_layout.children):  # Clear all child widgets in right_layout
                self.right_layout.remove_widget(child)


    def create_labeled_input(self, label_text, hint_text, description):
        """
        Helper function to create a labeled input with larger font size and positioning on the left.
        """
        container = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, None), height=105)
        
        # Title label
        label = Label(
            text=label_text, 
            size_hint=(1, None), 
            height=40, 
            font_size=32, 
            color=(1, 1, 1, 1)
        )
        
        # Description label
        description_label = Label(
            text=description, 
            size_hint=(1, None), 
            height=30, 
            font_size=24, 
            color=(0.7, 0.7, 0.7, 1)
        )
        
        # Input field
        input_field = TextInput(
            hint_text=hint_text, 
            size_hint=(1, None), 
            height=50, 
            font_size=32
        )
        
        # Add widgets in the desired order
        container.add_widget(label)
        container.add_widget(description_label)
        container.add_widget(input_field)
        
        return container, input_field


    def show_merger_inputs(self, instance):
        self.clear_content()

        # Dynamically populate the list of worlds
        def get_world_folders():
            return [
                folder
                for folder in os.listdir(worlds_directory)
                if os.path.isdir(os.path.join(worlds_directory, folder))
            ]

        worlds = get_world_folders()  # Get the latest list of world folders dynamically

        # Layout for inputs on the left side
        self.input_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(0.4, None), height=700)
        self.input_layout.pos_hint = {"x": 0.05, "y": 0.05}  # Positioned lower to avoid overlap

        # Top-Left Buttons and Descriptions
        top_left_layout = BoxLayout(orientation="vertical", spacing=10, size_hint=(0.2, None), height=150)
        top_left_layout.pos_hint = {"x": 0.05, "top": 1}  # Positioned in the top-left corner

        # Add top-left layout to FloatLayout
        self.add_widget(top_left_layout)

        # Right-Side Layout for Source and Destination Worlds
        self.right_layout = BoxLayout(orientation='vertical', spacing=36, size_hint=(0.4, None), height=800)
        self.right_layout.pos_hint = {"x": 0.6, "top": 0.95}  # Positioned on the right side

        # Title and Description above selections
        title_label = Label(
            text="World Selection",
            size_hint=(1, None),
            height=50,
            font_size=36,
            color=(1, 1, 1, 1)
        )
        description_label = Label(
            text="Select the source and destination worlds for chunk merging.",
            size_hint=(1, None),
            height=45,
            font_size=32,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.right_layout.add_widget(title_label)
        self.right_layout.add_widget(description_label)

        # Source world selection spinner
        source_container, self.source_path_input = self.create_labeled_spinner(
            "Source World Path:",
            worlds,  # Replace with actual options
            "Select the source world."
        )
        self.source_path_input.bind(text=self.update_source_map_viewer)  # Bind to update source map viewer
        self.right_layout.add_widget(source_container)

        # Source map viewer positioned directly below the spinner
        self.source_map_viewer = ChunkMapViewer(size_hint=(1, None), height=200)  # Define fixed height
        self.right_layout.add_widget(self.source_map_viewer)

        # Destination world selection spinner
        destination_container, self.destination_path_input = self.create_labeled_spinner(
            "Destination World Path:",
            worlds,  # Replace with actual options
            "Select the destination world."
        )
        self.destination_path_input.bind(text=self.update_destination_map_viewer)  # Bind to update destination map viewer
        self.right_layout.add_widget(destination_container)

        # Destination map viewer positioned directly below the spinner
        self.destination_map_viewer = ChunkMapViewer(size_hint=(1, None), height=200)  # Define fixed height
        self.right_layout.add_widget(self.destination_map_viewer)

        # Add right layout to FloatLayout
        self.add_widget(self.right_layout)

        # Chunk coordinate inputs with larger font size
        # Source Start Coordinates
        source_start_x, self.source_start_chunk_x_input = self.create_labeled_input(
            "Source Start Chunk X:",
            "Enter X coordinate",
            "The Starting X axis chunk coordinate."
        )
        source_start_z, self.source_start_chunk_z_input = self.create_labeled_input(
            "Source Start Chunk Z:",
            "Enter Z axis chunk coordinate.",
            "The Starting Z axis chunk coordinate."
        )
        self.input_layout.add_widget(source_start_x)
        self.input_layout.add_widget(source_start_z)

        # Source End Coordinates
        source_end_x, self.source_end_chunk_x_input = self.create_labeled_input(
            "Source End Chunk X:",
            "Enter X coordinate",
            "The Ending X axis chunk coordinate."
        )
        source_end_z, self.source_end_chunk_z_input = self.create_labeled_input(
            "Source End Chunk Z:",
            "Enter Z axis chunk coordinate.",
            "The Ending Z axis chunk coordinate."
        )
        self.input_layout.add_widget(source_end_x)
        self.input_layout.add_widget(source_end_z)

        # Destination Start Coordinates
        destination_start_x, self.destination_start_chunk_x_input = self.create_labeled_input(
            "Destination Start Chunk X:",
            "Enter X coordinate",
            "The Starting X axis chunk coordinate for the destination."
        )
        destination_start_z, self.destination_start_chunk_z_input = self.create_labeled_input(
            "Destination Start Chunk Z:",
            "Enter Z axis chunk coordinate.",
            "The Starting Z axis chunk coordinate for the destination."
        )
        self.input_layout.add_widget(destination_start_x)
        self.input_layout.add_widget(destination_start_z)

        # Destination End Coordinates
        destination_end_x, self.destination_end_chunk_x_input = self.create_labeled_input(
            "Destination End Chunk X:",
            "Enter X coordinate",
            "The Ending X axis chunk coordinate for the destination."
        )
        destination_end_z, self.destination_end_chunk_z_input = self.create_labeled_input(
            "Destination End Chunk Z:",
            "Enter Z axis chunk coordinate.",
            "The Ending Z axis chunk coordinate for the destination."
        )
        self.input_layout.add_widget(destination_end_x)
        self.input_layout.add_widget(destination_end_z)

        # Bind axis inputs to update map viewers
        self.source_start_chunk_x_input.bind(text=lambda instance, value: self.update_source_map_viewer(self.source_path_input, self.source_path_input.text))
        self.source_start_chunk_z_input.bind(text=lambda instance, value: self.update_source_map_viewer(self.source_path_input, self.source_path_input.text))
        self.source_end_chunk_x_input.bind(text=lambda instance, value: self.update_source_map_viewer(self.source_path_input, self.source_path_input.text))
        self.source_end_chunk_z_input.bind(text=lambda instance, value: self.update_source_map_viewer(self.source_path_input, self.source_path_input.text))

        # Bind axis inputs to update destination map viewer
        self.destination_start_chunk_x_input.bind(text=lambda instance, value: self.update_destination_map_viewer(self.destination_path_input, self.destination_path_input.text))
        self.destination_start_chunk_z_input.bind(text=lambda instance, value: self.update_destination_map_viewer(self.destination_path_input, self.destination_path_input.text))
        self.destination_end_chunk_x_input.bind(text=lambda instance, value: self.update_destination_map_viewer(self.destination_path_input, self.destination_path_input.text))
        self.destination_end_chunk_z_input.bind(text=lambda instance, value: self.update_destination_map_viewer(self.destination_path_input, self.destination_path_input.text))

        # Run merger button
        merge_button = Button(text="Run Chunk Merger", size_hint=(1, None), height=50, font_size=32)
        merge_button.bind(on_press=self.run_merger)
        self.input_layout.add_widget(merge_button)

        # Add result label
        self.result_label = Label(text="", size_hint=(1, None), height=50, font_size=32)
        self.input_layout.add_widget(self.result_label)

        # Add input layout to FloatLayout (on the left side)
        self.add_widget(self.input_layout)






    def show_fill_blocks_inputs(self, instance):
        self.clear_content()

        def get_world_folders():
            return [
                folder
                for folder in os.listdir(worlds_directory)
                if os.path.isdir(os.path.join(worlds_directory, folder))
            ]

        worlds = get_world_folders()  # Fetch world folders dynamically

        self.input_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(0.4, None), height=700)
        self.input_layout.pos_hint = {"x": 0.05, "y": 0.05}

        # Right-Side Layout for Source
        self.right_layout = BoxLayout(orientation='vertical', spacing=36, size_hint=(0.3, None), height=700)
        self.right_layout.pos_hint = {"x": 0.65, "top": 0.95}  

        title_label = Label(
            text="World Selection",
            size_hint=(1, None),
            height=50,
            font_size=32,
            color=(1, 1, 1, 1)
        )
        description_label = Label(
            text="Select the source world for block placement.",
            size_hint=(1, None),
            height=40,
            font_size=24,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.right_layout.add_widget(title_label)
        self.right_layout.add_widget(description_label)

        # Spinner for selecting the world folder
        source_container, self.source_path_input = self.create_labeled_spinner(
            "Source World Path:",
            worlds,
            "Select the world where blocks will be placed."
        )
        self.right_layout.add_widget(source_container)
        self.add_widget(self.right_layout)

        # Input fields for block type and coordinates
        block_type_container, self.block_type_input = self.create_labeled_input(
            "Block Type:",
            "Enter block type (e.g., gold_block)",
            "Specify the type of block."
        )
        self.input_layout.add_widget(block_type_container)

        start_coords_container, self.start_coords_input = self.create_labeled_input(
            "Start Coordinates (x, y, z):",
            "Enter start coordinates (e.g., 10,64,10)",
            "Specify the starting point."
        )
        self.input_layout.add_widget(start_coords_container)

        end_coords_container, self.end_coords_input = self.create_labeled_input(
            "End Coordinates (x, y, z):",
            "Enter end coordinates (e.g., 20,70,20)",
            "Specify the ending point."
        )
        self.input_layout.add_widget(end_coords_container)

        fill_button = Button(text="Fill Blocks", size_hint=(1, None), height=50, font_size=32)
        fill_button.bind(on_press=self.fill_blocks)
        self.input_layout.add_widget(fill_button)

        self.result_label = Label(text="", size_hint=(1, None), height=50, font_size=32)
        self.input_layout.add_widget(self.result_label)

        self.add_widget(self.input_layout)




    def run_merger(self, instance):
        try:
            # Construct paths to the source and destination worlds
            source_world_path = os.path.join(worlds_directory, self.source_path_input.text)
            destination_world_path = os.path.join(worlds_directory, self.destination_path_input.text)
            
            # Validate the existence of region folders
            source_region_folder = os.path.join(source_world_path, "region")
            destination_region_folder = os.path.join(destination_world_path, "region")
            
            if not os.path.exists(source_region_folder):
                self.result_label.text = f"Error: Source region folder not found at {source_region_folder}"
                return
            
            if not os.path.exists(destination_region_folder):
                self.result_label.text = f"Error: Destination region folder not found at {destination_region_folder}"
                return

            chunk_size = [16, 320, 16]  # Default chunk dimensions

            # Parse source starting and ending chunk coordinates
            source_start_chunk_coords = (
                int(self.source_start_chunk_x_input.text or 0),
                int(self.source_start_chunk_z_input.text or 0)
            )
            source_end_chunk_coords = (
                int(self.source_end_chunk_x_input.text or 0),
                int(self.source_end_chunk_z_input.text or 0)
            )

            # Parse destination starting chunk coordinates
            destination_start_chunk_coords = (
                int(self.destination_start_chunk_x_input.text or 0),
                int(self.destination_start_chunk_z_input.text or 0)
            )

            # Run the merger
            result = merge_worlds(
                source_world_path,
                destination_world_path,
                chunk_size,
                source_start_chunk_coords,
                source_end_chunk_coords,
                destination_start_chunk_coords  # Pass destination start coordinates
            )

            self.result_label.text = result
        except ValueError:
            self.result_label.text = "Please enter valid numeric values for chunk coordinates."
        except Exception as e:
            self.result_label.text = f"Error: {e}"



    def fill_blocks(self, instance):
        # Retrieve user inputs
        source_world_path = self.source_path_input.text
        block_type = self.block_type_input.text.strip()
        start_coords_text = self.start_coords_input.text.strip()
        end_coords_text = self.end_coords_input.text.strip()

        try:
                                    # Construct paths to the source and destination worlds
            source_world_path = os.path.join(worlds_directory, self.source_path_input.text)
            
            # Validate the existence of region folders
            source_region_folder = os.path.join(source_world_path, "region")
            
            if not os.path.exists(source_region_folder):
                self.result_label.text = f"Error: Source region folder not found at {source_region_folder}"
                return
            

            # Parse coordinates
            start_coords = tuple(map(int, start_coords_text.split(',')))
            end_coords = tuple(map(int, end_coords_text.split(',')))

            # Load the world
            editor = Editor(source_world_path)

            # Define the block type dynamically
            custom_block = Block(block_type)

            # Set the blocks
            for x in range(start_coords[0], end_coords[0] + 1):
                for y in range(start_coords[1], end_coords[1] + 1):
                    for z in range(start_coords[2], end_coords[2] + 1):
                        editor.set_block(custom_block, x, y, z)

            # Save the world
            editor.done()
            self.result_label.text = "Blocks filled successfully!"

        except Exception as e:
            self.result_label.text = f"Error: {e}"

    def update_source_map_viewer(self, spinner, selected_world):
        """
        Updates the map viewer for the source world when a new world is selected and renders surface blocks.
        """
        if selected_world:
            try:
                # Construct the path to the source world
                source_world_path = os.path.join(worlds_directory, selected_world)
                source_region_folder = os.path.join(source_world_path, "region")

                # Validate the existence of the source region folder
                if not os.path.exists(source_region_folder):
                    print(f"Error: Source region folder not found at {source_region_folder}")
                    return

                # Retrieve starting and ending chunk coordinates from user input
                start_chunk_x = int(self.source_start_chunk_x_input.text or 0)
                start_chunk_z = int(self.source_start_chunk_z_input.text or 0)
                end_chunk_x = int(self.source_end_chunk_x_input.text or 4)
                end_chunk_z = int(self.source_end_chunk_z_input.text or 4)

                # Calculate area dimensions
                dx = end_chunk_x - start_chunk_x + 1
                dz = end_chunk_z - start_chunk_z + 1

                # Use tools.py method to get chunk area
                regions, _, _ = tools.get_chunk_area(start_chunk_x * 16, start_chunk_z * 16, dx * 16, dz * 16)

                # Prepare chunk coordinates for rendering
                chunk_coords = []
                for region, chunks in regions.items():
                    for chunk_x, chunk_z in chunks:
                        chunk_coords.append((chunk_x, chunk_z))

                # Load the editor for the selected world
                editor = Editor(source_world_path)

                # Render surface blocks on the source map viewer
                self.source_map_viewer.draw_surface_blocks(editor, selected_world, chunk_coords, scale=10)

                # Ensure spinners are on top
                self.remove_widget(self.source_path_input)
                self.add_widget(self.source_path_input)

            except Exception as e:
                print(f"Error updating source map viewer: {e}")

    def update_destination_map_viewer(self, spinner, selected_world):
        """
        Updates the map viewer for the destination world when a new world is selected and renders surface blocks.
        """
        if selected_world:
            try:
                # Construct the path to the destination world
                destination_world_path = os.path.join(worlds_directory, selected_world)
                destination_region_folder = os.path.join(destination_world_path, "region")

                # Validate the existence of the destination region folder
                if not os.path.exists(destination_region_folder):
                    print(f"Error: Destination region folder not found at {destination_region_folder}")
                    return

                # Retrieve starting and ending chunk coordinates from user input
                start_chunk_x = int(self.destination_start_chunk_x_input.text or 0)
                start_chunk_z = int(self.destination_start_chunk_z_input.text or 0)
                end_chunk_x = int(self.destination_end_chunk_x_input.text or 4)
                end_chunk_z = int(self.destination_end_chunk_z_input.text or 4)

                # Calculate area dimensions
                dx = end_chunk_x - start_chunk_x + 1
                dz = end_chunk_z - start_chunk_z + 1

                # Use tools.py method to get chunk area
                regions, _, _ = tools.get_chunk_area(start_chunk_x * 16, start_chunk_z * 16, dx * 16, dz * 16)

                # Prepare chunk coordinates for rendering
                chunk_coords = []
                for region, chunks in regions.items():
                    for chunk_x, chunk_z in chunks:
                        chunk_coords.append((chunk_x, chunk_z))

                # Load the editor for the selected world
                editor = Editor(destination_world_path)

                # Render surface blocks on the destination map viewer
                self.destination_map_viewer.draw_surface_blocks(editor, selected_world, chunk_coords, scale=10)

                # Ensure spinners are on top
                self.remove_widget(self.destination_path_input)
                self.add_widget(self.destination_path_input)

            except Exception as e:
                print(f"Error updating destination map viewer: {e}")


class MyApp(App):
    def build(self):
        self.title = "Minecraft World Editor"
        return MainWindow()

if __name__ == '__main__':
    MyApp().run()

import logging

# Initialize logger
L = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def chunk_location(self, chunk_x: int, chunk_z: int) -> list:
    b_off = self.header_offset(chunk_x, chunk_z)
    off = int.from_bytes(self.data[b_off : b_off + 3], byteorder="big")
    sectors = self.data[b_off + 3]
    L.debug(f"Chunk {chunk_x}/{chunk_z} offset: {off}, sectors: {sectors}")
    return (off, sectors)

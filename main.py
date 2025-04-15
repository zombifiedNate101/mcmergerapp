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
    
from mcmerger.merger import merge_worlds  # Import the merger module
from pyblock.editor import Editor
from pyblock.block import Block

Window.size = (1280, 720)

# Define the base directory where all Minecraft worlds are stored
worlds_directory = os.path.normpath("C:/Users/zombi/Documents/Capstone Project/minecraft_worlds_tests")


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
        top_left_layout = BoxLayout(orientation="vertical", spacing=10, size_hint=(0.2, None), height=120)
        top_left_layout.pos_hint = {"x": 0.05, "top": 0.95}  # Adjusted for top-left corner

        # World Merger Button
        merger_button = Button(text="World Merger", size_hint=(1, None), height=40)
        merger_button.bind(on_press=self.show_merger_inputs)
        merger_description = Label(
            text="Combine chunks from different worlds.",
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
            text="Fill specific areas with chosen blocks.",
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

    def clear_content(self):
        """Clear the current input layout."""
        if self.input_layout:
            self.remove_widget(self.input_layout)
            self.input_layout = None

    def create_labeled_spinner(self, label_text, values, description):
        """
        Helper function to create a spinner with title and description.
        """
        container = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None), height=120)
        label = Label(text=label_text, size_hint=(1, None), height=30, font_size=18)
        spinner = Spinner(values=values, size_hint=(1, None), height=40, font_size=18)  # Shorter scroller button height
        description_label = Label(text=description, size_hint=(1, None), height=40, font_size=16, color=(0.7, 0.7, 0.7, 1))

        container.add_widget(label)
        container.add_widget(spinner)
        container.add_widget(description_label)
        return container, spinner

    def create_labeled_input(self, label_text, hint_text, description):
        """
        Helper function to create a labeled input with larger font size and positioning on the left.
        """
        container = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None), height=100)
        label = Label(text=label_text, size_hint=(1, None), height=40, font_size=32, color=(1, 1, 1, 1))
        input_field = TextInput(hint_text=hint_text, size_hint=(1, None), height=60, font_size=32)
        description_label = Label(text=description, size_hint=(1, None), height=40, font_size=24, color=(0.7, 0.7, 0.7, 1))

        container.add_widget(label)
        container.add_widget(input_field)
        container.add_widget(description_label)
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

        # Right-Side Layout for Scrollers and Buttons
        right_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(0.3, None), height=600)
        right_layout.pos_hint = {"x": 0.7, "top": 0.95}  # Positioned on the right side

        # Title and Description above scrollers
        title_label = Label(
            text="World Selection",
            size_hint=(1, None),
            height=50,
            font_size=32,
            color=(1, 1, 1, 1)
        )
        description_label = Label(
            text="Select the source and destination worlds for chunk merging.",
            size_hint=(1, None),
            height=40,
            font_size=24,
            color=(0.7, 0.7, 0.7, 1)
        )
        right_layout.add_widget(title_label)
        right_layout.add_widget(description_label)

        # Source world path scroller
        source_container, self.source_path_input = self.create_labeled_spinner(
            "Source World Path:",
            worlds,  # Replace with actual options
            "Select the source world from which chunks will be copied."
        )
        self.source_path_input.size_hint = (1, None)  # Shorter button length
        self.source_path_input.height = 40  # Adjust height for shorter buttons
        right_layout.add_widget(source_container)

        # Destination world path scroller
        destination_container, self.destination_path_input = self.create_labeled_spinner(
            "Destination World Path:",
            worlds,  # Replace with actual options
            "Select the destination world to which chunks will be copied."
        )
        self.destination_path_input.size_hint = (1, None)  # Shorter button length
        self.destination_path_input.height = 40  # Adjust height for shorter buttons
        right_layout.add_widget(destination_container)

        # Add right layout to FloatLayout
        self.add_widget(right_layout)

        # Chunk coordinate inputs with larger font size
        # Source Start Coordinates
        source_start_x, self.source_start_chunk_x_input = self.create_labeled_input(
            "Source Start Chunk X:",
            "Enter X coordinate",
            "Starting X chunk coordinate."
        )
        source_start_z, self.source_start_chunk_z_input = self.create_labeled_input(
            "Source Start Chunk Z:",
            "Enter Z coordinate",
            "Starting Z chunk coordinate."
        )
        self.input_layout.add_widget(source_start_x)
        self.input_layout.add_widget(source_start_z)

        # Source End Coordinates
        source_end_x, self.source_end_chunk_x_input = self.create_labeled_input(
            "Source End Chunk X:",
            "Enter X coordinate",
            "Ending X chunk coordinate."
        )
        source_end_z, self.source_end_chunk_z_input = self.create_labeled_input(
            "Source End Chunk Z:",
            "Enter Z coordinate",
            "Ending Z chunk coordinate."
        )
        self.input_layout.add_widget(source_end_x)
        self.input_layout.add_widget(source_end_z)

        # Destination Start Coordinates
        destination_start_x, self.destination_start_chunk_x_input = self.create_labeled_input(
            "Destination Start Chunk X:",
            "Enter X coordinate",
            "Starting X chunk coordinate."
        )
        destination_start_z, self.destination_start_chunk_z_input = self.create_labeled_input(
            "Destination Start Chunk Z:",
            "Enter Z coordinate",
            "Starting Z chunk coordinate."
        )
        self.input_layout.add_widget(destination_start_x)
        self.input_layout.add_widget(destination_start_z)

        # Destination End Coordinates
        destination_end_x, self.destination_end_chunk_x_input = self.create_labeled_input(
            "Destination End Chunk X:",
            "Enter X coordinate",
            "Ending X chunk coordinate."
        )
        destination_end_z, self.destination_end_chunk_z_input = self.create_labeled_input(
            "Destination End Chunk Z:",
            "Enter Z coordinate",
            "Ending Z chunk coordinate."
        )
        self.input_layout.add_widget(destination_end_x)
        self.input_layout.add_widget(destination_end_z)

        # Run merger button
        merge_button = Button(text="Run Merger", size_hint=(1, None), height=50, font_size=32)
        merge_button.bind(on_press=self.run_merger)
        self.input_layout.add_widget(merge_button)

        # Add result label
        self.result_label = Label(text="", size_hint=(1, None), height=50, font_size=32)
        self.input_layout.add_widget(self.result_label)

        # Add input layout to FloatLayout (on the left side)
        self.add_widget(self.input_layout)





    def show_fill_blocks_inputs(self, instance):
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

        # Right-Side Layout for Scrollers and Title
        right_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(0.3, None), height=700)
        right_layout.pos_hint = {"x": 0.65, "top": 0.95}  # Positioned higher to accommodate spinner visibility

        # Title and Description above scrollers
        title_label = Label(
            text="World Selection",
            size_hint=(1, None),
            height=50,
            font_size=32,
            color=(1, 1, 1, 1)
        )
        description_label = Label(
            text="Select the source world you want to place blocks in.",
            size_hint=(1, None),
            height=40,
            font_size=24,
            color=(0.7, 0.7, 0.7, 1)
        )
        right_layout.add_widget(title_label)
        right_layout.add_widget(description_label)

        # Source world path scroller (visible and functional)
        source_container, self.source_path_input = self.create_labeled_spinner(
            "Source World Path:",
            worlds,
            "Select the world where blocks will be placed."
        )
        self.source_path_input.size_hint = (1, None)
        self.source_path_input.height = 40  # Shorter scroller button length
        right_layout.add_widget(source_container)

        # Add right layout to FloatLayout
        self.add_widget(right_layout)

        # Block type input
        block_type_container, self.block_type_input = self.create_labeled_input(
            "Block Type:",
            "Enter block type (e.g., gold_block)",
            "Specify the type of block to fill the area."
        )
        self.input_layout.add_widget(block_type_container)

        # Start coordinates input
        start_coords_container, self.start_coords_input = self.create_labeled_input(
            "Start Coordinates (x, y, z):",
            "Enter start coordinates (e.g., 10,64,10)",
            "Specify the starting point for block filling."
        )
        self.input_layout.add_widget(start_coords_container)

        # End coordinates input
        end_coords_container, self.end_coords_input = self.create_labeled_input(
            "End Coordinates (x, y, z):",
            "Enter end coordinates (e.g., 20,70,20)",
            "Specify the ending point for block filling."
        )
        self.input_layout.add_widget(end_coords_container)

        # Fill blocks button
        fill_button = Button(text="Fill Blocks", size_hint=(1, None), height=50, font_size=32)
        fill_button.bind(on_press=self.fill_blocks)
        self.input_layout.add_widget(fill_button)

        # Add result label (position adjusted to align properly)
        self.result_label = Label(text="", size_hint=(1, None), height=50, font_size=32, pos_hint={"x": 0.05, "y": 0.5})
        self.input_layout.add_widget(self.result_label)

        # Add the input layout to the FloatLayout
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

            # Parse starting and ending chunk coordinates
            start_chunk_coords = (
                int(self.source_start_chunk_x_input.text or 0),
                int(self.source_start_chunk_z_input.text or 0)
            )
            end_chunk_coords = (
                int(self.source_end_chunk_x_input.text or 0),
                int(self.source_end_chunk_z_input.text or 0)
            )

            # Run the merger
            result = merge_worlds(
                source_world_path,
                destination_world_path,
                chunk_size,
                start_chunk_coords,
                end_chunk_coords
            )

            self.result_label.text = result
        except ValueError:
            self.result_label.text = "Please enter valid numeric values for chunk coordinates."



    def fill_blocks(self, instance):
        # Retrieve user inputs
        source_world_path = self.source_path_input.text
        block_type = self.block_type_input.text.strip()
        start_coords_text = self.start_coords_input.text.strip()
        end_coords_text = self.end_coords_input.text.strip()

        try:
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

class MyApp(App):
    def build(self):
        self.title = "Minecraft World Editor"
        return MainWindow()

if __name__ == '__main__':
    MyApp().run()

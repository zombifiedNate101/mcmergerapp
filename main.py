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

        # Default Message Description
        self.default_message = Label(
            text="Welcome to the Minecraft World Editor!\nChoose a button to get started:\nWorld Merger: Combine chunks from different worlds.\nFill Blocks: Fill a specific area with chosen blocks.",
            size_hint=(0.8, None),
            height=120,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            font_size=18,
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.default_message)

        # Option Buttons Layout
        self.option_layout = BoxLayout(
            orientation='horizontal',
            spacing=40,
            size_hint=(0.8, None),
            height=80,
            pos_hint={"center_x": 0.5, "y": 0.85}
        )
        merger_button = Button(text="World Merger", font_size=22, size_hint=(0.5, None), height=60)
        merger_button.bind(on_press=self.show_merger_inputs)
        self.option_layout.add_widget(merger_button)

        fill_blocks_button = Button(text="Fill Blocks", font_size=22, size_hint=(0.5, None), height=60)
        fill_blocks_button.bind(on_press=self.show_fill_blocks_inputs)
        self.option_layout.add_widget(fill_blocks_button)
        self.add_widget(self.option_layout)

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

    def create_labeled_spinner(self, label_text, values, description):
        container = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None), height=120)
        label = Label(text=label_text, size_hint=(1, None), height=30, font_size=24, color=(1, 1, 1, 1))
        spinner = Spinner(values=values, size_hint=(1, None), height=50, font_size=20)
        description_label = Label(text=description, size_hint=(1, None), height=40, font_size=16, color=(0.7, 0.7, 0.7, 1))

        container.add_widget(label)
        container.add_widget(spinner)
        container.add_widget(description_label)
        return container, spinner

    def clear_content(self):
        self.content_layout.clear_widgets()
        self.default_message.text = ""

    def create_labeled_input(self, label_text, hint_text, description):
        """
        Helper function to create a labeled input with description.
        """
        container = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None), height=120)
        label = Label(text=label_text, size_hint=(1, None), height=30, font_size=20, color=(1, 1, 1, 1))
        input_field = TextInput(hint_text=hint_text, size_hint=(1, None), height=50, font_size=18)
        description_label = Label(text=description, size_hint=(1, None), height=40, font_size=16, color=(0.7, 0.7, 0.7, 1))

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

        source_container, self.source_path_input = self.create_labeled_spinner(
            "Source World Path:",
            worlds,  # Replace with actual options
            "Select the source world from which chunks will be copied."
        )
        self.content_layout.add_widget(source_container)

        destination_container, self.destination_path_input = self.create_labeled_spinner(
            "Destination World Path:",
            worlds,  # Replace with actual options
            "Select the destination world to which chunks will be copied."
        )
        self.content_layout.add_widget(destination_container)

        source_start_chunk_container_x, self.source_start_chunk_x_input = self.create_labeled_input(
            "Source Start Chunk X:",
            "Enter the starting X chunk coordinate for the source world",
            "This specifies the starting chunk's X-coordinate."
        )
        source_start_chunk_container_z, self.source_start_chunk_z_input = self.create_labeled_input(
            "Source Start Chunk Z:",
            "Enter the starting Z chunk coordinate for the source world",
            "This specifies the starting chunk's Z-coordinate."
        )
        self.content_layout.add_widget(source_start_chunk_container_x)
        self.content_layout.add_widget(source_start_chunk_container_z)

        source_end_chunk_container_x, self.source_end_chunk_x_input = self.create_labeled_input(
            "Source End Chunk X:",
            "Enter the ending X chunk coordinate for the source world",
            "This specifies the ending chunk's X-coordinate."
        )
        source_end_chunk_container_z, self.source_end_chunk_z_input = self.create_labeled_input(
            "Source End Chunk Z:",
            "Enter the ending Z chunk coordinate for the source world",
            "This specifies the ending chunk's Z-coordinate."
        )
        self.content_layout.add_widget(source_end_chunk_container_x)
        self.content_layout.add_widget(source_end_chunk_container_z)

        destination_start_chunk_container_x, self.destination_start_chunk_x_input = self.create_labeled_input(
            "Destination Start Chunk X:",
            "Enter the starting X chunk coordinate for the destination world",
            "This specifies the starting chunk's X-coordinate in the destination."
        )
        destination_start_chunk_container_z, self.destination_start_chunk_z_input = self.create_labeled_input(
            "Destination Start Chunk Z:",
            "Enter the starting Z chunk coordinate for the destination world",
            "This specifies the starting chunk's Z-coordinate in the destination."
        )
        self.content_layout.add_widget(destination_start_chunk_container_x)
        self.content_layout.add_widget(destination_start_chunk_container_z)

        destination_end_chunk_container_x, self.destination_end_chunk_x_input = self.create_labeled_input(
            "Destination End Chunk X:",
            "Enter the ending X chunk coordinate for the destination world",
            "This specifies the ending chunk's X-coordinate in the destination."
        )
        destination_end_chunk_container_z, self.destination_end_chunk_z_input = self.create_labeled_input(
            "Destination End Chunk Z:",
            "Enter the ending Z chunk coordinate for the destination world",
            "This specifies the ending chunk's Z-coordinate in the destination."
        )
        self.content_layout.add_widget(destination_end_chunk_container_x)
        self.content_layout.add_widget(destination_end_chunk_container_z)

        merge_button = Button(text="Run Merger", size_hint=(0.5, None), height=60, font_size=22)
        merge_button.bind(on_press=self.run_merger)
        self.content_layout.add_widget(merge_button)

        self.result_label = Label(text="", size_hint=(1, None), height=40, font_size=18, color=(1, 1, 1, 1))
        self.content_layout.add_widget(self.result_label)

    def show_fill_blocks_inputs(self, instance):
        self.clear_content()

        source_container, self.source_path_input = self.create_labeled_input(
            "Source World Path:",
            "Enter the path to the source world folder",
            "This is the world where blocks will be filled."
        )
        self.content_layout.add_widget(source_container)

        block_type_container, self.block_type_input = self.create_labeled_input(
            "Block Type:",
            "Enter the block type (e.g., gold_block)",
            "Specify the type of block to fill the area with."
        )
        self.content_layout.add_widget(block_type_container)

        start_coords_container, self.start_coords_input = self.create_labeled_input(
            "Start Coordinates (x, y, z):",
            "Enter start coordinates (e.g., 10,64,10)",
            "Specify the starting point for block filling."
        )
        self.content_layout.add_widget(start_coords_container)

        end_coords_container, self.end_coords_input = self.create_labeled_input(
            "End Coordinates (x, y, z):",
            "Enter end coordinates (e.g., 20,70,20)",
            "Specify the ending point for block filling."
        )
        self.content_layout.add_widget(end_coords_container)

        fill_button = Button(text="Fill Blocks", size_hint=(0.5, None), height=60, font_size=22)
        fill_button.bind(on_press=self.fill_blocks)
        self.content_layout.add_widget(fill_button)

        self.result_label = Label(text="", size_hint=(1, None), height=40, font_size=18, color=(1, 1, 1, 1))
        self.content_layout.add_widget(self.result_label)

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

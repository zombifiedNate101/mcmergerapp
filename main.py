import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from mcmerger.merger import merge_worlds  # Import the merger module

Window.size = (1280, 720)

class MainWindow(BoxLayout):
    def __init__(self):
        super().__init__(orientation='vertical')
        
        # Set up the background colors
        with self.canvas.before:
            Color(0.6, 0.4, 0.2, 1)  # Brown
            self.rect1 = Rectangle(pos=self.pos, size=(self.width, self.height * 0.33))
            Color(0, 1, 0, 1)  # Green
            self.rect2 = Rectangle(pos=(self.x, self.height * 0.15), size=(self.width, self.height * 0.15))
            Color(0.68, 0.85, 0.9, 1)  # Blue
            self.rect3 = Rectangle(pos=(self.x, self.height * 0.66), size=(self.width, self.height * 0.33))
        
        self.bind(size=self._update_rectangles, pos=self._update_rectangles)

        # Input fields for source and destination paths
        self.add_widget(Label(text="Source World Path:"))
        self.source_path_input = TextInput(hint_text="Enter source world path")
        self.add_widget(self.source_path_input)

        self.add_widget(Label(text="Destination World Path:"))
        self.destination_path_input = TextInput(hint_text="Enter destination world path")
        self.add_widget(self.destination_path_input)

        # Input fields for chunk size and range
        self.add_widget(Label(text="Chunks X Range:"))
        self.chunks_x_input = TextInput(hint_text="Enter number of chunks in X direction (default: 10)")
        self.add_widget(self.chunks_x_input)

        self.add_widget(Label(text="Chunks Z Range:"))
        self.chunks_z_input = TextInput(hint_text="Enter number of chunks in Z direction (default: 10)")
        self.add_widget(self.chunks_z_input)

        # Run Merger Button
        self.merge_button = Button(text="Run Merger")
        self.merge_button.bind(on_press=self.run_merger)
        self.add_widget(self.merge_button)

        # Label for feedback
        self.result_label = Label(text="")
        self.add_widget(self.result_label)

    def _update_rectangles(self, *args):
        # Adjust rectangle sizes when window is resized
        self.rect1.size = (self.width, self.height * 0.33)
        self.rect2.size = (self.width, self.height * 0.33)
        self.rect2.pos = (self.x, self.height * 0.33)
        self.rect3.size = (self.width, self.height * 0.33)
        self.rect3.pos = (self.x, self.height * 0.66)

    def run_merger(self, instance):
        # Retrieve user inputs
        source_world_path = self.source_path_input.text
        destination_world_path = self.destination_path_input.text
        try:
            chunk_size = [
                int(16),
                int(320),
                int(16),
            ]
            chunks_x = int(self.chunks_x_input.text or 10)
            chunks_z = int(self.chunks_z_input.text or 10)

            # Run the merger logic from the separate module
            result = merge_worlds(source_world_path, destination_world_path, chunk_size, chunks_x, chunks_z)
            self.result_label.text = result
        except ValueError:
            self.result_label.text = "Please enter valid numeric values for chunk size and ranges."

class MyApp(App):
    def build(self):
        self.title = "Minecraft World Merger"
        return MainWindow()

app = MyApp()
app.run()

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json
import random


class BoxRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Box Recommender - 3D Stencil Placement")
        self.box_dimensions = {"length": 50, "width": 50, "height": 50}  # Default box size
        self.stencils = []  # List of stencil data
        self.setup_ui()

    def setup_ui(self):
        # Left panel for stencil palette and controls
        self.left_panel = tk.Frame(self.root, padx=10, pady=10)
        self.left_panel.pack(side="left", fill="y")

        tk.Label(self.left_panel, text="Stencil Palette").pack()
        self.add_stencil_button = tk.Button(
            self.left_panel, text="Add Stencil", command=self.add_stencil
        )
        self.add_stencil_button.pack(pady=5)

        self.load_config_button = tk.Button(
            self.left_panel, text="Load Box Config", command=self.load_box_config
        )
        self.load_config_button.pack(pady=5)

        self.edit_box_button = tk.Button(
            self.left_panel, text="Edit Box Dimensions", command=self.edit_box_dimensions
        )
        self.edit_box_button.pack(pady=5)

        # Canvas for 3D box rendering
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side="right", fill="both", expand=True)
        self.fig = plt.figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection="3d")

        self.canvas = None

        self.update_box()

    def update_box(self):
        """Update the 3D rendering of the box and stencils."""
        self.ax.clear()
        self.draw_box()

        for stencil in self.stencils:
            self.draw_stencil(stencil)

        # Refresh the canvas
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = tk.Canvas(self.canvas_frame)
        self.canvas.pack(fill="both", expand=True)
        canvas_widget = self.fig.canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

    def draw_box(self):
        """Draw the 3D box."""
        l, w, h = self.box_dimensions.values()

        # Draw the edges of the box
        vertices = [
            [0, 0, 0], [l, 0, 0], [l, w, 0], [0, w, 0],  # Bottom vertices
            [0, 0, h], [l, 0, h], [l, w, h], [0, w, h]   # Top vertices
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom edges
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top edges
            (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
        ]

        for edge in edges:
            start, end = edge
            self.ax.plot(
                [vertices[start][0], vertices[end][0]],
                [vertices[start][1], vertices[end][1]],
                [vertices[start][2], vertices[end][2]],
                color="black"
            )

        # Add filled faces
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front face
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right face
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back face
            [vertices[3], vertices[0], vertices[4], vertices[7]],  # Left face
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom face
            [vertices[4], vertices[5], vertices[6], vertices[7]]   # Top face
        ]
        self.ax.add_collection3d(Poly3DCollection(faces, alpha=0.2, facecolors="blue"))

    def draw_stencil(self, stencil):
        """Draw a stencil in the 3D box."""
        x, y, z = stencil["position"]
        l, w, h = stencil["dimensions"]
        color = self.get_stencil_color(stencil)

        vertices = [
            [x, y, z],
            [x + l, y, z],
            [x + l, y + w, z],
            [x, y + w, z],
            [x, y, z + h],
            [x + l, y, z + h],
            [x + l, y + w, z + h],
            [x, y + w, z + h]
        ]
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[1], vertices[2], vertices[6], vertices[5]],
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            [vertices[3], vertices[0], vertices[4], vertices[7]],
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]]
        ]
        self.ax.add_collection3d(Poly3DCollection(faces, alpha=0.5, facecolors=color))

    def get_stencil_color(self, stencil):
        """Determine the color of the stencil based on its fit."""
        x, y, z = stencil["position"]
        l, w, h = stencil["dimensions"]
        box_l, box_w, box_h = self.box_dimensions.values()

        if x + l <= box_l and y + w <= box_w and z + h <= box_h:
            return "green"  # Fits perfectly
        elif x + l > box_l or y + w > box_w or z + h > box_h:
            return "red"  # Exceeds dimensions
        else:
            return "yellow"  # Close to exceeding

    def load_box_config(self):
        """Load box configuration from a JSON file."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                config = json.load(file)
            self.box_dimensions = config.get("box_dimensions", self.box_dimensions)
            self.update_box()
            messagebox.showinfo("Success", "Box configuration loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load box configuration: {e}")

    def edit_box_dimensions(self):
        """Edit the dimensions of the box."""
        try:
            l = float(simpledialog.askstring("Edit Box", "Enter box length:", initialvalue=self.box_dimensions["length"]))
            w = float(simpledialog.askstring("Edit Box", "Enter box width:", initialvalue=self.box_dimensions["width"]))
            h = float(simpledialog.askstring("Edit Box", "Enter box height:", initialvalue=self.box_dimensions["height"]))
            self.box_dimensions = {"length": l, "width": w, "height": h}
            self.update_box()
        except Exception:
            messagebox.showerror("Error", "Invalid dimensions entered.")

    def delete_stencil(self, stencil_id):
        """Delete a stencil by ID."""
        self.stencils = [s for s in self.stencils if s["id"] != stencil_id]
        self.update_box()


if __name__ == "__main__":
    root = tk.Tk()
    app = BoxRecommenderApp(root)
    root.mainloop()

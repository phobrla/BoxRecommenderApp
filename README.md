# Box Recommender App

Box Recommender is a Python desktop application for 3D visualization and interactive placement of "stencils" (rectangular prisms) inside a configurable box. The interface allows users to edit box dimensions, add and visualize stencils, and load box configurations from JSON files.

## Features

- **3D Visualization:** View a box and its contents in 3D using `matplotlib`.
- **Interactive UI:** Edit box dimensions, add stencils, and load configurations with a GUI built in `tkinter`.
- **Stencil Placement:** Add stencils with positions and dimensions; see if they fit inside the box (color-coded).
- **Load Configurations:** Import box settings from JSON files.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/phobrla/BoxRecommenderApp.git
   cd BoxRecommenderApp
   ```

2. **Set up a virtual environment (recommended):**
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install matplotlib
   ```

   > **Note:** You must also have `tkinter` installed. On many systems, it's included with Python, but see troubleshooting below if you encounter import errors.

## Usage

Run the application:

```sh
python box_recommender.py
```

- Use the left panel to add stencils, load box configurations, or edit box dimensions.
- The right panel displays a 3D view of the box and placed stencils.
- Stencils are color-coded:
  - **Green:** Fits inside the box
  - **Red:** Exceeds box dimensions
  - **Yellow:** Nearly exceeds dimensions

## Configuration Files

Box configurations can be loaded from a JSON file with the following structure:

```json
{
  "box_dimensions": {
    "length": 100,
    "width": 80,
    "height": 60
  }
}
```

## Troubleshooting

### Tkinter Import Error

If you encounter this error:

```
Traceback (most recent call last):
  File "/Users/phobrla/Documents/GitHub/BoxRecommenderApp/box_recommender.py", line 1, in <module>
    import tkinter as tk
  File "/opt/homebrew/Cellar/python@3.13/3.13.2/Frameworks/Python.framework/Versions/3.13/lib/python3.13/tkinter/__init__.py", line 38, in <module>
    import _tkinter # If this fails your Python may not be configured for Tk
    ^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named '_tkinter'
```

The error message:

```
ModuleNotFoundError: No module named '_tkinter'
```

means your Python installation does not have Tkinter (the GUI library) installed or configured properly. This is common on some macOS and Linux systems, especially when Python is installed via Homebrew.

### How to fix

#### Homebrew Python on macOS

1. **Install Tk:**
   ```sh
   brew install tcl-tk
   ```

2. **Note Homebrew's caveats:**  
   After installing, Homebrew will print some instructions. Take note of the path to tcl-tk. For example, you might see something like:
   ```
   For compilers to find tcl-tk you may need to set:
     export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
     export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
   ```

3. **Reinstall Python with Tk support:**  
   You need to tell Python where Tk is. Try reinstalling Python with the correct flags:
   ```sh
   brew reinstall python@3.13 --with-tcl-tk
   ```
   (Note: If `--with-tcl-tk` is not available, see below.)

4. **Set Environment Variables:**  
   Add these to your `.zshrc` or `.bash_profile` (replace path as needed):
   ```sh
   export PATH="/opt/homebrew/opt/python@3.13/bin:$PATH"
   export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
   export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
   export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"
   ```

5. **Restart your terminal and try again:**  
   Open a new terminal and run your script again.

#### Alternative: Use Python from python.org

The official Python installer for macOS from [python.org](https://www.python.org/downloads/mac-osx/) comes with Tkinter pre-installed and working out-of-the-box.

#### Check Tkinter

To check if Tkinter is working, try:

```sh
python3 -m tkinter
```

If a small window pops up, Tkinter is working.

#### Summary

- Install `tcl-tk` with Homebrew.
- Set environment variables.
- Consider the official python.org installer if you continue to have issues.

---

### Using a Virtual Python Environment

If you are using a virtual environment (recommended):

```sh
source myenv/bin/activate
```

all Python packages you install will go into that environment, keeping them separate from your system Python. To resolve your Tkinter issue, follow these steps:

1. **Check if Tkinter is available in your venv**
   ```sh
   python -m tkinter
   ```
   If a window pops up, Tkinter is installed and working.

2. **If you get the same error (`no module named '_tkinter'`):**

   - On macOS (especially with Homebrew Python): Homebrew Python often does **not** include Tkinter by default. The virtual environment inherits whatever is available in the system Python it was created from. You need to ensure the base Python (used to create the venv) has Tkinter.

   **Fix:**
   1. Exit your venv:
      ```sh
      deactivate
      ```
   2. Install Tcl/Tk (if not already):
      ```sh
      brew install tcl-tk
      ```
   3. Reinstall Python and create a new venv using the correct flags:
      ```sh
      brew install python
      ```
      Or (if already installed):
      ```sh
      brew reinstall python
      ```
   4. Set environment variables so Python finds Homebrew’s Tk: Add these to your `~/.zshrc` or `~/.bash_profile`:
      ```sh
      export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
      export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
      export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"
      export PATH="/opt/homebrew/opt/python@3.13/bin:$PATH"
      ```
      Then:
      ```sh
      source ~/.zshrc  # or source ~/.bash_profile
      ```
   5. Create a new venv with the fixed Python:
      ```sh
      python3 -m venv myenv
      source myenv/bin/activate
      python -m pip install --upgrade pip
      ```
   6. Test Tkinter again:
      ```sh
      python -m tkinter
      ```

#### Summary

- Tkinter is not a pip package—you need a Python built with Tk support.
- The venv inherits from your system Python; fix your system Python, then recreate the venv.
- If on macOS, prefer the official python.org installer for easiest Tkinter support.

Let me know if you want step-by-step for your particular OS or encounter any errors!

## License

MIT License

---

*Developed by phobrla*

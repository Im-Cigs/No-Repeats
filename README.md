# No-Repeats
This tool is designed for those who frequently download large amounts of 'Homework.' As your collection grows, managing and protecting against duplicate files can become increasingly challenging. This script helps you efficiently identify and eliminate duplicates, ensuring your files remain organized and clutter-free.


For example, if you point it to your Downloads folder, it will compare each file against the others in that folder and its subfolders to identify any duplicates.

## Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)(It comes with python and is auto installed with the latest python versions)


## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/no-repeats.git
   cd no-repeats

2. **Create a virtual environment** (Optinal but recommended)
   ```sh
   python -m venv venv

3. **activate the virtual environment**
   On Windows:
   ```sh
   venv\Scripts\activate
   ```
   On MacOs/Linux:
   ```sh
   source venv/bin/activate
   
4. **Install requirments**
   ```sh
   pip install -r requirements.txt
   
5. **Configuration**
   Locate where it is installed and edit "settings.json".
   You want to change PUT DIR HERE in "directory": "PUT DIR HERE" to the location of your "Homework" folder, For Example: {
                                                                                                                            "directory": "C:\special"
                                                                                                                           }


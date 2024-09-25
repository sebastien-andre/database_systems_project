# Database Systems Project
## By Sebastien Lee and Ian Pruitt
This repository contains source code for the Database Systems Project.

## Setup 

```bash
git clone https://github.com/sebastien-andre/database_systems_project.git
cd database_systems_project
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

#### Generating UML Diagrams
To generate UML diagrams from `.txt` files:

- **For a specific `.txt` file:**
  ```bash
  python diagramming.py my_diagram.txt
  ```

- **For all `.txt` files in a directory:**
  ```bash
  python diagramming.py all ./path/to/directory
  ```

The generated PNG files will be saved in the `png` folder in the same directory.

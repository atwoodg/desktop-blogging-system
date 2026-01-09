# Desktop Blogging System (Course Project)
 
## Overview
This project implements a blogging system in Python by using the unittest framework, CRUD operations, file persistence, and a PyQt6 GUI.

![Demo](https://github.com/atwoodg/desktop-blogging-system/blob/main/Animation.gif)

## Features
- Login/logout
- Create, search, update, and delete blogs and posts.
- Persistence using a DAO layer (JSON and Pickle storage).
- Graphical user interface in PyQt6.
- Unittest testing.

## Tech Stack
- Python 3.9.23
- PyQt6
- Unittest

## Installation
Clone repo and install required dependencies:

```bash
git clone https://github.com/atwoodg/desktop-blogging-system.git
cd desktop-blogging-system

#Windows:
py -m venv .venv
.\.venv\Scripts\activate

#macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## How to use
Running the system:
```bash
python -m blogging.gui.blogging_gui
```
User: user
Password: 123456

## Tests
From the project root folder (`group078/`):
```bash
python -m unittest discover -s tests -p "*_test.py" -v
python -m unittest -v ./tests/controller_test.py 
python -m unittest -v ./tests/integration_test.py
```

## Credits
- Contributors: Gabriel Atwood, Michael Chen, Roberto Bittencourt
- Course: SENG 265 (Software Development Methods)



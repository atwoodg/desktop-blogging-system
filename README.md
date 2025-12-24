# Blogging System Assignment 
**Course:** SENG 265 (Software Engineering Fundamentals)  
**Team:** Group 078  
**Author:** Gabriel Atwood, Michael Chen  
**Date:** November 2025  

---

## 🧭 Overview
This project implements a blogging system with Python in three parts.
1. Uses the unittesting framework and CRUD operations to build three main classes:
- **Blog** – represents a single blog and manages its posts.  
- **Post** – represents an individual blog post with title, text, creation, and update timestamps.  
- **Controller** – manages user login, blog creation/deletion, and post operations.
2. Implements DAO persistence for saving and loading files.
- **BlogEncoder** - Saves blog as JSON strings.
- **BlogDecoder** - Loads blog as JSON strings.
- **BlogDAOJSON** - Stores a blog's collection of posts in JSON.
- **BlogDAOPickle** - Stores a blog's collection of posts in binary mode using the pickle library.
3. Implements a GUI for the blogging system.
- **BloggingGUI** - Main window for the graphical user interface.
- **Dashboard** - Dashboard to navigate blog and posts. User can Search, Create, Retrieve, Update, and Delete blogs and posts.
- **Login** - GUI for login screen passed to BloggingGUI.


All logic follows object-oriented design principles and passes all unit tests supplied with each assignment.

---

## ⚙️ How to Run Tests
From the project root folder (`group078/`):

```bash
#1
python -m unittest discover -s tests -p "*_test.py" -v

#2
python3 -m unittest -v ./tests/controller_test.py 
python3 -m unittest -v ./tests/integration_test.py

#3
python3 -m blogging gui 



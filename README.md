# Assignment 3 – Blogging System  
**Course:** SENG 265 (Software Engineering Fundamentals)  
**Team:** Group 078  
**Author:** Gabriel Atwood, Michael Chen  
**Date:** November 2025  

---

## 🧭 Overview
This project implements a simple blogging controller system in Python.  
It includes three main classes:
- **Blog** – represents a single blog and manages its posts.  
- **Post** – represents an individual blog post with title, text, creation, and update timestamps.  
- **Controller** – manages user login, blog creation/deletion, and post operations.

All logic follows object-oriented design principles and passes all unit tests supplied with the assignment.

---

## ⚙️ How to Run Tests
From the project root folder (`group078/`):

```bash
python -m unittest discover -s tests -p "*_test.py" -v

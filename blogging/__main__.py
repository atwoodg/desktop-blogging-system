# blogging/__main__.py
# Commit 1: enable GUI mode

import sys

try:
    from PyQt6.QtWidgets import QApplication
    from blogging.gui.blogging_gui import BloggingGUI
except:
    QApplication = None
    BloggingGUI = None


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "gui":
        if QApplication is None:
            print("PyQt6 not installed.")
            return
        app = QApplication(sys.argv)
        win = BloggingGUI()
        win.show()
        app.exec()
        return

    print("Usage:")
    print("  python3 -m blogging gui")


if __name__ == "__main__":
    main()

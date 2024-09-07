from tkinter import Tk, N, S, E, W
from .window import MainWindow
from .controls import Control
from .maze import Maze


class App(MainWindow, Control):
    def __init__(self, title, width, height):
        self._root = Tk()
        self._root.title(title)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        super().__init__(self._root, width, height)
        super(MainWindow, self).__init__(self._root, width/3)

        super().grid(row=0, column=0, columnspan=4, sticky=(N, S, W, E))
        super(MainWindow, self).grid(row=0, column=4, sticky=E)
        self.maze: Maze = None

        self._root.bind('<Return>', self._create_maze_bind)

    def _create_maze_bind(self, *args):
        self.create_maze()

    def wait_for_close(self):
        self._is_running = True
        while self._is_running:
            self.redraw()
        print("window closed")

    def close(self):
        self.interrupt_maze()
        self._is_running = False

import time
from typing import Optional
from tkinter import Tk, IntVar, N, S, E, W
from tkinter import ttk
from .window import MainWindow, Point
from .maze import Maze

MAZE_POS = Point(10, 10)


class Control:
    def __init__(self, root: Tk, width: int):
        self._frame = ttk.Frame(root, width=width)
        self._spinners = ttk.Frame(self._frame)
        self._spinners.grid(row=0, column=0, rowspan=10, sticky=(N, S))
        self._buttons = ttk.Frame(self._frame)
        self._buttons.grid(row=10, column=0, sticky=(N, S))
        self.maze_is_solved = False
        self.maze: Optional[Maze] = None
        self._create_buttons()

    def create_maze(self):
        rows = self.maze_rows.get()
        cols = self.maze_cols.get()
        cell_size = self.maze_cell_size.get()
        self.interrupt_maze()
        while not self.maze_is_solved and self.maze is not None:
            time.sleep(0.01)
        self.launch_b.state(['disabled'])
        self.reset_b.state(['disabled'])
        self.maze = Maze(MAZE_POS, rows, cols, cell_size, cell_size, self)
        self.clear()
        self.maze.draw()
        self.maze_is_solved = False
        self.launch_b.state(['!disabled'])
        self.reset_b.state(['!disabled'])

    def solve_maze(self):
        if self.maze is None:
            return
        if self.maze_is_solved:
            self.reset_maze()
        self.maze_is_solved = self.maze.solve()

    def reset_maze(self):
        if self.maze is None:
            return
        # if self.maze_is_being_solved:
        self.interrupt_maze()
        self.maze_is_solved = False
        # new_cell_size = self.cellsize_b.get()
        # self.maze._cell_size_x = new_cell_size
        # self.maze._cell_size_y = new_cell_size
        self.maze.clear()

    def interrupt_maze(self):
        if self.maze is None:
            return
        self.maze.interrupted = True
        # time.sleep(1)

    def grid(self, *args, **kwargs):
        self._frame.grid(*args, **kwargs)

    def clear(self):
        pass

    def _create_buttons(self):
        self.maze_rows = IntVar(value=10)
        self.maze_cols = IntVar(value=10)
        self.maze_cell_size = IntVar(value=50)
        self.cols_b = ttk.Spinbox(
            self._spinners, from_=1, to=50, textvariable=self.maze_cols)
        self.rows_b = ttk.Spinbox(
            self._spinners, from_=1, to=50, textvariable=self.maze_rows)
        self.cellsize_b = ttk.Spinbox(
            self._spinners, from_=20, to=100, textvariable=self.maze_cell_size)

        self.create_b = ttk.Button(
            self._buttons, text="Create maze", command=self.create_maze)
        self.launch_b = ttk.Button(
            self._buttons, text="Launch solver", command=self.solve_maze)
        self.reset_b = ttk.Button(
            self._buttons, text="Reset maze", command=self.reset_maze)
        self.interrupt_b = ttk.Button(
            self._buttons, text="Interrupt", command=self.interrupt_maze)

        self.cols_b.grid(row=0, column=1, sticky=(N, S), padx=5, pady=5)
        self.rows_b.grid(row=1, column=1, sticky=N, padx=5, pady=5)
        self.cellsize_b.grid(row=0, column=0, sticky=N, padx=5, pady=5)

        self.create_b.grid(row=0, column=0, padx=5, pady=5)
        self.launch_b.grid(row=0, column=1, padx=5, pady=5)
        self.reset_b.grid(row=0, column=2, padx=5, pady=5)
        self.interrupt_b.grid(row=1, column=1, padx=5, pady=5)


class App(MainWindow, Control):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        super(MainWindow, self).__init__(self._root, width/3)

        super().grid(row=0, column=0, columnspan=4, sticky=(N, S, W, E))
        super(MainWindow, self).grid(row=0, column=4, sticky=E)
        self.maze: Maze = None

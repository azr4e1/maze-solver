import time
from typing import Optional
from tkinter import Tk, IntVar, N, S, E, W, StringVar
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
        self.error_val.set('')
        rows = self.maze_rows.get()
        cols = self.maze_cols.get()
        cell_size = self.maze_cell_size.get()
        self.launch_b.state(['disabled'])
        self.reset_b.state(['disabled'])
        self.maze = Maze(MAZE_POS, rows, cols, cell_size, cell_size, self)
        self.clear()
        try:
            self.maze.draw()
            self.maze_is_solved = False
        except RecursionError:
            self.error_val.set('maze is too large; try to set lower values')
            self.redraw()
            return
        self.launch_b.state(['!disabled'])
        self.reset_b.state(['!disabled'])

    def solve_maze(self):
        if self.maze is None:
            return
        if self.maze_is_solved:
            self.reset_maze()
        self.create_b.state(['disabled'])
        self.reset_b.state(['disabled'])
        self.maze_is_solved = self.maze.solve()
        self.create_b.state(['!disabled'])
        self.reset_b.state(['!disabled'])

    def reset_maze(self):
        if self.maze is None:
            return
        self.interrupt_maze()
        self.maze_is_solved = False
        self.maze.clear()

    def interrupt_maze(self):
        if self.maze is None:
            return
        self.maze.interrupt()

    def grid(self, *args, **kwargs):
        self._frame.grid(*args, **kwargs)

    def clear(self):
        ...

    def redraw(self):
        ...

    def _create_buttons(self):
        self.maze_rows = IntVar(value=10)
        self.maze_cols = IntVar(value=10)
        self.maze_cell_size = IntVar(value=50)
        self.error_val = StringVar(value="")
        self.error_l = ttk.Label(
            self._spinners, textvariable=self.error_val, foreground='red', font='TkSmallCaptionFont')
        ttk.Label(self._spinners, text="Columns").grid(
            column=1, row=0, padx=5, pady=(5, 0))
        ttk.Label(self._spinners, text="Rows").grid(
            column=1, row=2, padx=5, pady=(5, 0))
        ttk.Label(self._spinners, text="Cell Size").grid(
            column=0, row=0, padx=5, pady=(5, 0))
        self.cols_b = ttk.Spinbox(
            self._spinners, from_=2, to=50, textvariable=self.maze_cols)
        self.rows_b = ttk.Spinbox(
            self._spinners, from_=2, to=50, textvariable=self.maze_rows)
        self.cellsize_b = ttk.Spinbox(
            self._spinners, from_=10, to=100, textvariable=self.maze_cell_size)

        self.cols_b.state(['readonly'])
        self.rows_b.state(['readonly'])
        self.cellsize_b.state(['readonly'])

        self.create_b = ttk.Button(
            self._buttons, text="Create maze", command=self.create_maze, default='active')
        self.launch_b = ttk.Button(
            self._buttons, text="Launch solver", command=self.solve_maze)
        self.reset_b = ttk.Button(
            self._buttons, text="Reset maze", command=self.reset_maze)
        self.interrupt_b = ttk.Button(
            self._buttons, text="Interrupt", command=self.interrupt_maze)

        self.cols_b.grid(row=1, column=1, sticky=(N, S), padx=5, pady=(0, 5))
        self.rows_b.grid(row=3, column=1, sticky=N, padx=5, pady=(0, 5))
        self.cellsize_b.grid(row=1, column=0, sticky=N,
                             padx=5, rowspan=2, pady=(0, 5))
        self.error_l.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.create_b.grid(row=0, column=0, padx=5, pady=5)
        self.launch_b.grid(row=0, column=1, padx=5, pady=5)
        self.reset_b.grid(row=0, column=2, padx=5, pady=5)
        self.interrupt_b.grid(row=1, column=1, padx=5, pady=5)

        self.launch_b.state(['disabled'])
        self.reset_b.state(['disabled'])


class App(MainWindow, Control):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)
        super(MainWindow, self).__init__(self._root, width/3)

        super().grid(row=0, column=0, columnspan=4, sticky=(N, S, W, E))
        super(MainWindow, self).grid(row=0, column=4, sticky=E)
        self.maze: Maze = None

        self._root.bind('<Return>', self._create_maze_bind)

    def _create_maze_bind(self, *args):
        self.create_maze()

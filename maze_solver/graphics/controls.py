from typing import Optional
from abc import ABC, abstractmethod
from tkinter import Tk, IntVar, N, S, E, W, StringVar
from tkinter import ttk
from .window import Point
import time

from .maze import Maze


class Control(ABC):
    def __init__(self, root: Tk, width: int, maze_pos: Point):
        self._frame = ttk.Frame(root, width=width)
        self._spinners = ttk.Frame(self._frame)
        self._spinners.grid(row=0, column=0, rowspan=10, sticky=(N, S))
        self._buttons = ttk.Frame(self._frame)
        self._buttons.grid(row=10, column=0, sticky=(N, S))
        self.maze_is_solved = False
        self.maze: Optional[Maze] = None
        self.start = 0
        self.maze_pos = maze_pos
        self._create_buttons()

    def create_maze(self):
        self.error_val.set('')
        self._reset_timer()
        self._update_scrollsize()
        rows = self.maze_rows.get()
        cols = self.maze_cols.get()
        cell_size = self.maze_cell_size.get()
        self.interrupt_b.state(['!disabled'])
        self.create_b.state(['disabled'])
        self.launch_b.state(['disabled'])
        self.reset_b.state(['disabled'])
        self.maze = Maze(self.maze_pos, rows, cols, cell_size,
                         cell_size, self, 1/self.maze_speed.get())
        self.clear()
        try:
            self.maze.draw()
            self.maze_is_solved = False
        except RecursionError:
            self.error_val.set('maze is too large; try to set lower values')
            self.redraw()
            self.create_b.state(['!disabled'])
            return

        if self.maze.interrupted:
            self.create_b.state(['!disabled'])
            return

        self.launch_b.state(['!disabled'])
        self.reset_b.state(['!disabled'])
        self.create_b.state(['!disabled'])

    def solve_maze(self):
        self._reset_timer()
        if self.maze is None:
            return
        if self.maze_is_solved or self.maze.manual_solution:
            self.reset_maze()

        self.create_b.state(['disabled'])
        self.reset_b.state(['disabled'])
        self.launch_b.state(['disabled'])

        # task = Thread(target=self._launch_timer)
        # task.start()
        self.maze._cells[0][0].change_color_pressed()
        self.maze_is_solved = self.maze.solve()
        # task.join()

        self.create_b.state(['!disabled'])
        self.reset_b.state(['!disabled'])
        self.launch_b.state(['!disabled'])

    def reset_maze(self):
        self._reset_timer()
        if self.maze is None:
            return
        self.interrupt_maze()
        self.maze_is_solved = False
        cell_size = self.maze_cell_size.get()
        if cell_size != self.maze._cell_size_x:
            self.maze.resize(cell_size,
                             cell_size)
            self._update_scrollsize()
        self.maze.clear()

    def interrupt_maze(self):
        if self.maze is None:
            return
        self.maze.interrupt()
        self.create_b.state(['!disabled'])

    def grid(self, *args, **kwargs):
        self._frame.grid(*args, **kwargs)

    def _set_speed_callback(self, x):
        if self.maze is not None:
            speed = 1 / float(x)
            self.maze.speed = speed
        self.maze_speed.set(int(float(x)))

    def _update_timer(self):
        if self.maze is None:
            return
        self.timer.set(f"{(time.time_ns() - self.start) / 1000000000:.2f}")
        self.redraw()

    def _reset_timer(self):
        self.start = time.time_ns()
        self.timer.set("0.00")

    def _create_buttons(self):
        self.maze_rows = IntVar(value=10)
        self.maze_cols = IntVar(value=10)
        self.maze_cell_size = IntVar(value=50)
        self.maze_speed = IntVar(value=20)
        self.error_val = StringVar(value="")
        self.timer = StringVar(value="0.00")

        self.timer_l = ttk.Label(
            self._spinners, textvariable=self.timer)
        self.error_l = ttk.Label(
            self._spinners, textvariable=self.error_val, foreground='red',
            font='TkSmallCaptionFont')

        ttk.Label(self._spinners, text="Cell Size").grid(
            column=0, row=0, padx=5, pady=5)
        ttk.Label(self._spinners, text="Columns").grid(
            column=0, row=1, padx=5, pady=5)
        ttk.Label(self._spinners, text="Rows").grid(
            column=0, row=2, padx=5, pady=5)
        ttk.Label(self._spinners, text="Speed").grid(
            column=0, row=3, padx=5, pady=5)
        ttk.Label(self._spinners, text="Seconds:").grid(
            column=0, row=4, padx=5, pady=5)

        ttk.Label(self._spinners, textvariable=self.maze_cell_size).grid(
            column=2, row=0, padx=5, pady=5)
        ttk.Label(self._spinners, textvariable=self.maze_cols).grid(
            column=2, row=1, padx=5, pady=5)
        ttk.Label(self._spinners, textvariable=self.maze_rows).grid(
            column=2, row=2, padx=5, pady=5)
        ttk.Label(self._spinners, textvariable=self.maze_speed).grid(
            column=2, row=3, padx=5, pady=5)

        self.cellsize_b = ttk.Scale(
            self._spinners, from_=10, to=99, variable=self.maze_cell_size,
            command=lambda x: self.maze_cell_size.set(int(float(x))))
        self.cols_b = ttk.Scale(
            self._spinners, from_=2, to=50, variable=self.maze_cols,
            command=lambda x: self.maze_cols.set(int(float(x))))
        self.rows_b = ttk.Scale(
            self._spinners, from_=2, to=50, variable=self.maze_rows,
            command=lambda x: self.maze_rows.set(int(float(x))))
        self.speed_b = ttk.Scale(
            self._spinners, from_=1, to=100, variable=self.maze_speed,
            command=self._set_speed_callback)

        self.create_b = ttk.Button(
            self._buttons, text="Create maze", command=self.create_maze, default='active')
        self.launch_b = ttk.Button(
            self._buttons, text="Launch solver", command=self.solve_maze)
        self.reset_b = ttk.Button(
            self._buttons, text="Reset maze", command=self.reset_maze)
        self.interrupt_b = ttk.Button(
            self._buttons, text="Interrupt", command=self.interrupt_maze)

        self.cellsize_b.grid(row=0, column=1, sticky=N, padx=5, pady=5)
        self.cols_b.grid(row=1, column=1, sticky=N, padx=5, pady=5)
        self.rows_b.grid(row=2, column=1, sticky=N, padx=5, pady=5)
        self.speed_b.grid(row=3, column=1, sticky=N, padx=5, pady=5)
        self.timer_l.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        self.error_l.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        self.create_b.grid(row=0, column=0, padx=5, pady=5)
        self.reset_b.grid(row=1, column=0, padx=5, pady=5)
        self.launch_b.grid(row=0, column=1, padx=5, pady=5)
        self.interrupt_b.grid(row=1, column=1, padx=5, pady=5)

        self.launch_b.state(['disabled'])
        self.reset_b.state(['disabled'])
        self.interrupt_b.state(['disabled'])

    @abstractmethod
    def clear(self):
        ...

    @abstractmethod
    def redraw(self):
        ...

    @abstractmethod
    def _update_scrollsize(self):
        ...

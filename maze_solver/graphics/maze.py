from __future__ import annotations
from typing import Optional, Callable, TypeAlias, Any
from tkinter import Event
import time
import random

from .window import Line, Point, MainWindow

Callback: TypeAlias = Callable[Event, Any]


FRAME_TIME = 0.05
CELL_COLOR = 'black'
SLEEP_FRAME = 0.001


class Cell:
    def __init__(self,
                 win: MainWindow,
                 pos1: Point,
                 pos2: Point,
                 lwall: bool = True,
                 rwall: bool = True,
                 uwall: bool = True,
                 dwall: bool = True,
                 # visited: bool = False,
                 ):

        self._pos1 = pos1
        self._pos2 = pos2
        self._win = win
        self._id = None
        self._callbacks = []
        self._blank_color = self._win._canvas['background']
        self.visited = False
        self.manual_visited = False
        self.lwall = lwall
        self.rwall = rwall
        self.uwall = uwall
        self.dwall = dwall

    def draw(self, color: str):
        if self._win is None:
            return

        self._id = self._win._canvas.create_rectangle(self._pos1.x, self._pos1.y,
                                                      self._pos2.x, self._pos2.y,
                                                      fill=self._blank_color,
                                                      outline=self._blank_color)
        for event, callback in self._callbacks:
            self._win._canvas.tag_bind(
                self._id, event, callback, add=True)
        # self._win._canvas.tag_bind(
        #     self._id, '<Button-1>', self.change_color_pressed, add=True)

        lline = Line(self._pos1, Point(self._pos1.x, self._pos2.y))
        rline = Line(Point(self._pos2.x, self._pos1.y), self._pos2)
        uline = Line(self._pos1, Point(self._pos2.x, self._pos1.y))
        dline = Line(Point(self._pos1.x, self._pos2.y), self._pos2)

        for w, l in [(self.lwall, lline),
                     (self.rwall, rline),
                     (self.uwall, uline),
                     (self.dwall, dline)]:
            clr = color if w else self._blank_color
            self._win.draw_line(l, clr)

    def draw_move(self, to_cell: Cell,
                  undo: bool = False,
                  correct: bool = False):
        if self._win is None:
            return

        point1 = self.get_center()
        point2 = to_cell.get_center()
        color = 'gray'
        if undo:
            color = 'red'
        if correct:
            color = 'green'
        self._win.draw_line(Line(point1, point2), color)

    def get_center(self):
        x = (self._pos1.x + self._pos2.x) / 2
        y = (self._pos1.y + self._pos2.y) / 2

        return Point(x, y)

    def register_event(self, event: str, callback: Callback):
        self._callbacks.append((event, callback))

    def change_color_pressed(self, e: Optional[Event] = None, undo: bool = False, correct: bool = False, blank: bool = False):
        if self._id is None:
            return
        # self.pressed = False if self.pressed else True
        color = 'yellow'
        if undo:
            color = 'red'
        if correct:
            color = 'green'
        if blank:
            color = self._blank_color
        self._win._canvas.itemconfig(self._id, fill=color)


class Maze:
    def __init__(
            self,
            pos: Point,
            num_rows: int,
            num_cols: int,
            cell_size_x: int,
            cell_size_y: int,
            win: MainWindow,
            speed: float = FRAME_TIME,
            seed: Optional[int] = None):
        self._posn = pos
        self._rows = num_rows
        self._cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self.interrupted = False
        self.speed = speed
        self._last_ij = (0, 0)
        self._solution_stack = [(0, 0)]
        self.manual_solution = False

        random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        self._win._canvas.bind('<B1-Motion>', self._next_cell_mousedrag)
        curr_x = self._posn.x
        for coln in range(self._cols):
            rows = []
            curr_y = self._posn.y
            for rown in range(self._rows):
                point1 = Point(curr_x, curr_y)

                # update curr_y
                curr_y += self._cell_size_y
                point2 = Point(curr_x + self._cell_size_x, curr_y)

                cell = Cell(self._win, point1, point2)
                cell.register_event(
                    '<Button-1>', self._next_cell_callback(coln, rown))
                rows.append(cell)
            self._cells.append(rows)
            curr_x += self._cell_size_x

    def resize(self, new_cell_size, new_pos):
        self._cell_size_x = new_cell_size
        self._cell_size_y = new_cell_size
        self._posn = new_pos

        curr_x = self._posn.x
        for coln in range(self._cols):
            curr_y = self._posn.y
            for rown in range(self._rows):
                point1 = Point(curr_x, curr_y)

                # update curr_y
                curr_y += self._cell_size_y
                point2 = Point(curr_x + self._cell_size_x, curr_y)

                self._cells[coln][rown]._pos1 = point1
                self._cells[coln][rown]._pos2 = point2
            curr_x += self._cell_size_x

    def draw(self):
        for i in range(self._cols):
            for j in range(self._rows):
                if self.interrupted:
                    return
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def clear(self, clear_solution=True):
        self._solution_stack = [(0, 0)]
        self._win.clear()
        for i in range(self._cols):
            for j in range(self._rows):
                self._draw_cell(i, j)
        if clear_solution:
            self.interrupted = False
            self._reset_cells_visited()
            self.manual_solution = False

    def _draw_cell(self, i, j):
        cell: Cell = self._cells[i][j]
        cell.draw(CELL_COLOR)
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].lwall = False
        self._draw_cell(0, 0)

        self._cells[self._cols-1][self._rows-1].rwall = False
        self._draw_cell(self._cols-1, self._rows-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            if self.interrupted:
                return
            adjacents = list(filter(lambda x: (0 <= x[0] < self._cols)
                                    and (0 <= x[1] < self._rows)
                                    and not self._cells[x[0]][x[1]].visited,
                                    [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]))
            if len(adjacents) == 0:
                return

            next = random.choice(adjacents)
            self._break_walls_between_cells(i, j, next[0], next[1])
            self._break_walls_r(next[0], next[1])

    def _break_walls_between_cells(self, cur_i, cur_j, next_i, next_j):
        if cur_i > next_i:
            self._cells[cur_i][cur_j].lwall = False
            self._cells[next_i][next_j].rwall = False
        elif cur_i < next_i:
            self._cells[cur_i][cur_j].rwall = False
            self._cells[next_i][next_j].lwall = False
        elif cur_j > next_j:
            self._cells[cur_i][cur_j].uwall = False
            self._cells[next_i][next_j].dwall = False
        else:
            self._cells[cur_i][cur_j].dwall = False
            self._cells[next_i][next_j].uwall = False
        self._draw_cell(cur_i, cur_j)
        self._draw_cell(next_i, next_j)

    def _animate(self, sleep: int = 0):
        if self._win is None:
            return

        self._win.redraw()
        slept = 0
        while slept < sleep:
            self._win._update_timer()
            self._win.redraw()
            time.sleep(SLEEP_FRAME)
            slept += SLEEP_FRAME

    def _reset_cells_visited(self):
        for i in range(self._cols):
            for j in range(self._rows):
                self._cells[i][j].visited = False
                self._cells[i][j].manual_visited = False

        self._last_ij = (0, 0)
        self._cells[0][0].change_color_pressed()

    def solve(self):
        self.interrupted = False
        solution = self._solve_r(0, 0)
        self.interrupt()
        self._win._root.event_generate('<<SolverStop>>')
        return solution

    def _solve_r(self, i, j):
        self._animate(self.speed)
        if self.interrupted:
            return True
        end_cell = (self._cols-1, self._rows-1)
        curr = (i, j)
        curr_cell = self._cells[i][j]

        self._cells[i][j].visited = True
        if curr == end_cell:
            return True

        valid_directions = self._get_valid_directions(i, j)
        for next in valid_directions:
            next_cell = self._cells[next[0]][next[1]]
            curr_cell.draw_move(next_cell)
            is_winning = self._solve_r(*next)
            if is_winning:
                correct = True if not self.interrupted else False
                curr_cell.draw_move(next_cell, correct=correct)
                return True
            curr_cell.draw_move(next_cell, undo=True)

        return False

    def interrupt(self):
        self.interrupted = True

    def _next_cell_callback(self, i, j):
        def inner(e: Event):
            if not self.manual_solution:
                self.manual_solution = True
                self._win._root.event_generate('<<SolverLaunch>>')
            end_cell = (self._cols-1, self._rows-1)
            prev_cell: Cell = self._cells[self._last_ij[0]][self._last_ij[1]]
            curr_cell: Cell = self._cells[i][j]
            valid_directions = self._get_valid_directions(
                *self._last_ij, manual=True)
            if (i, j) not in valid_directions:
                return
            if (i, j) in valid_directions and not self.interrupted:
                # prev_cell.draw_move(curr_cell)
                prev_cell.manual_visited = True
                curr_cell.manual_visited = True

                curr_cell.change_color_pressed()
                self._last_ij = (i, j)
                self._solution_stack.append((i, j))
                if self._last_ij == end_cell:
                    self.interrupt()
                    self._win._root.event_generate('<<SolverStop>>')
                    self._draw_stacked_solution(correct=True, undo=True)
                    return
            if not self.interrupted and (len(valid_directions) == 0
               or len(self._get_valid_directions(i, j, manual=True)) == 0):
                self.interrupt()
                self._draw_stacked_solution(correct=False, undo=True)
                return
        return inner

    def _next_cell_mousedrag(self, e: Event):
        pos = self._get_cell_pos(e.x, e.y)
        if pos is None:
            return

        i, j = pos
        curr_cell: Cell = self._cells[i][j]
        center = curr_cell.get_center()
        if (i, j) != self._last_ij:
            self._win._canvas.event_generate(
                '<Button-1>', x=center.x+4, y=center.y+4)

    def _get_valid_directions(self, i, j, manual: bool = False):
        curr_cell = self._cells[i][j]
        adjacents = {(i+1, j): 'r', (i-1, j): 'l',
                     (i, j+1): 'd', (i, j-1): 'u'}
        valid_directions = filter(lambda x: (0 <= x[0] < self._cols)
                                  and (0 <= x[1] < self._rows),
                                  adjacents.keys())
        if manual:
            valid_directions = filter(
                lambda x: not self._cells[x[0]][x[1]].manual_visited,
                valid_directions)
        else:
            valid_directions = filter(
                lambda x: not self._cells[x[0]][x[1]].visited,
                valid_directions)
        valid_directions = filter(
            lambda x: not getattr(curr_cell, adjacents[x]+'wall', False),
            valid_directions)

        return list(valid_directions)

    def _get_cell_pos(self, x, y):
        j = round((y - self._posn.y) // self._cell_size_y)
        i = round((x - self._posn.x) // self._cell_size_x)

        if i < 0 or i >= self._cols:
            return None
        if j < 0 or j >= self._rows:
            return None

        return (i, j)

    def _draw_stacked_solution(self, correct: bool, undo: bool):
        for el in self._solution_stack:
            cell: Cell = self._cells[el[0]][el[1]]
            cell.change_color_pressed(undo=undo, correct=correct)

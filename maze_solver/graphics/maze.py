from __future__ import annotations
from typing import Optional
import time
import random

from .window import Line, Point, MainWindow


FRAME_TIME = 0.05
CELL_COLOR = 'black'


class Cell:
    def __init__(self,
                 win: MainWindow,
                 pos1: Point,
                 pos2: Point,
                 lwall: bool = True,
                 rwall: bool = True,
                 uwall: bool = True,
                 dwall: bool = True,
                 visited: bool = False):
        self._pos1 = pos1
        self._pos2 = pos2
        self._win = win
        self.lwall = lwall
        self.rwall = rwall
        self.uwall = uwall
        self.dwall = dwall
        self.visited = visited

    def draw(self, color: str):
        if self._win is None:
            return

        blank_color = self._win._canvas['background']

        lline = Line(self._pos1, Point(self._pos1.x, self._pos2.y))
        rline = Line(Point(self._pos2.x, self._pos1.y), self._pos2)
        uline = Line(self._pos1, Point(self._pos2.x, self._pos1.y))
        dline = Line(Point(self._pos1.x, self._pos2.y), self._pos2)

        for w, l in [(self.lwall, lline),
                     (self.rwall, rline),
                     (self.uwall, uline),
                     (self.dwall, dline)]:
            clr = color if w else blank_color
            self._win.draw_line(l, clr)

    def draw_move(self, to_cell: Cell,
                  undo: bool = False,
                  correct: bool = False):
        if self._win is None:
            return

        point1 = Point((self._pos1.x + self._pos2.x) / 2,
                       (self._pos1.y + self._pos2.y) / 2)
        point2 = Point((to_cell._pos1.x + to_cell._pos2.x) / 2,
                       (to_cell._pos1.y + to_cell._pos2.y) / 2)
        color = 'gray'
        if undo:
            color = 'red'
        if correct:
            color = 'blue'
        self._win.draw_line(Line(point1, point2), color)


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

        random.seed(seed)
        self._create_cells()

    def _create_cells(self):
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
                rows.append(cell)
            self._cells.append(rows)
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

    def clear(self):
        self._reset_cells_visited()
        self.interrupted = False
        self._win.clear()
        for i in range(self._cols):
            for j in range(self._rows):
                self._draw_cell(i, j)

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
        time.sleep(sleep)

    def _reset_cells_visited(self):
        for i in range(self._cols):
            for j in range(self._rows):
                self._cells[i][j].visited = False

    def solve(self):
        self.interrupted = False
        return self._solve_r(0, 0)

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

        adjacents = {(i+1, j): 'r', (i-1, j): 'l',
                     (i, j+1): 'd', (i, j-1): 'u'}
        valid_directions = filter(lambda x: (0 <= x[0] < self._cols)
                                  and (0 <= x[1] < self._rows),
                                  adjacents.keys())
        valid_directions = filter(
            lambda x: not self._cells[x[0]][x[1]].visited,
            valid_directions)
        valid_directions = filter(
            lambda x: not getattr(curr_cell, adjacents[x]+'wall', False),
            valid_directions)
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

from tkinter import Tk, BOTH, Canvas
import time

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.title = ""
        self.height = height
        self.width = width
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2)

class Cell():
    def __init__(self, left_wall, top_wall, right_wall, bot_wall, win):
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self._left_wall = left_wall
        self._top_wall = top_wall
        self._right_wall = right_wall
        self._bot_wall = bot_wall
        self._win = win

    def draw(self):
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._left_wall, self._top_wall), Point(self._right_wall, self._top_wall)), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._right_wall, self._top_wall), Point(self._right_wall, self._bot_wall)), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._left_wall, self._bot_wall), Point(self._right_wall, self._bot_wall)), "black")
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._left_wall, self._top_wall), Point(self._left_wall, self._bot_wall)), "black")
    
    def draw_move(self, to_cell, undo=False):
        cell1_center = Point((self._left_wall + self._right_wall) / 2, (self._top_wall + self._bot_wall) / 2)
        cell2_center = Point((to_cell._left_wall + to_cell._right_wall) / 2, (to_cell._top_wall + to_cell._bot_wall) / 2)
        line = Line(cell1_center, cell2_center)
        if undo:
            color = "red"
        else:
            color = "gray"
        line.draw(self._win.canvas, color)

class Maze():
    def __init__(
        self,
        left_wall,
        top_wall,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self._left_wall = left_wall
        self._top_wall = top_wall
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
    
    def _create_cells(self):
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                left_wall = self._left_wall + j * self._cell_size_x
                top_wall = self._top_wall + i * self._cell_size_y
                right_wall = left_wall + self._cell_size_x
                bot_wall = top_wall + self._cell_size_y
                self._cells.append(Cell(left_wall, top_wall, right_wall, bot_wall, self._win))
        self._draw_cells()
        
    
    def draw_cells(self, i, j):
        for cell in self._cells:
            cell.draw()
        self.animate()
    
    def animate(self):
        while True:
            self._win.redraw()
            time.sleep(0.5)


def main():
    win = Window(800, 600)
    cell1 = Cell(10, 10, 50, 50, win)
    cell2 = Cell(50, 10, 90, 50, win)
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2)
    win.wait_for_close()

    print("Window closed")


main()
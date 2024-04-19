from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.configure(bg="#323232")
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
        self.visited = False

    def draw(self):
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._left_wall, self._top_wall), Point(self._right_wall, self._top_wall)), "black")
        else:
            self._win.draw_line(Line(Point(self._left_wall, self._top_wall), Point(self._right_wall, self._top_wall)), "#323232")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._right_wall, self._top_wall), Point(self._right_wall, self._bot_wall)), "black")
        else:   
            self._win.draw_line(Line(Point(self._right_wall, self._top_wall), Point(self._right_wall, self._bot_wall)), "#323232")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._left_wall, self._bot_wall), Point(self._right_wall, self._bot_wall)), "black")
        else:
            self._win.draw_line(Line(Point(self._left_wall, self._bot_wall), Point(self._right_wall, self._bot_wall)), "#323232")
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._left_wall, self._top_wall), Point(self._left_wall, self._bot_wall)), "black")
        else:
            self._win.draw_line(Line(Point(self._left_wall, self._top_wall), Point(self._left_wall, self._bot_wall)), "#323232")
    
    def draw_move(self, to_cell, undo=False):
        cell1_center = Point((self._left_wall + self._right_wall) / 2, (self._top_wall + self._bot_wall) / 2)
        cell2_center = Point((to_cell._left_wall + to_cell._right_wall) / 2, (to_cell._top_wall + to_cell._bot_wall) / 2)
        line = Line(cell1_center, cell2_center)
        if undo:
            color = "#323232"
        else:
            color = "red"
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
        seed=None,
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
        if seed is not None:
            random.seed(seed)
    
    def _create_cells(self):
        for row in range(self._num_rows):
            colList = []
            for col in range(self._num_cols):
                
                left_wall = self._left_wall + col * self._cell_size_x
                top_wall = self._top_wall + row * self._cell_size_y
                right_wall = left_wall + self._cell_size_x
                bot_wall = top_wall + self._cell_size_y
                cell = Cell(left_wall, top_wall, right_wall, bot_wall, self._win)
                colList.append(cell)
            self._cells.append(colList)
        
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                self.draw_cells(row, col)
        
    
    def draw_cells(self,row,col):
        cell = self._cells[row][col]
        cell.draw()
        self.animate()
    
    def animate(self):
        self._win.redraw()
        time.sleep(.5)
    
    def _break_entrance_and_exit_walls(self):
        self._cells[0][0].has_left_wall = False
        self._cells[self._num_rows - 1][self._num_cols - 1].has_right_wall = False
        self.draw_cells(0,0)
        self.draw_cells(self._num_rows - 1, self._num_cols - 1)
    
    def _get_unvisited_neighbors(self, row, col):
        neighbors = []
        if row > 0 and not self._cells[row - 1][col].visited:
            neighbors.append(("top", row - 1, col))
        if row < self._num_rows - 1 and not self._cells[row + 1][col].visited:
            neighbors.append(("bot", row + 1, col))
        if col > 0 and not self._cells[row][col - 1].visited:
            neighbors.append(("left", row, col - 1))
        if col < self._num_cols - 1 and not self._cells[row][col + 1].visited:
            neighbors.append(("right",row, col + 1))
        return neighbors
    
    def _break_walls(self, row, col):
        cell = self._cells[row][col]
        cell.visited = True
        while True:
            neighbors = self._get_unvisited_neighbors(row, col)
            if len(neighbors) > 0:
                random_neighbor = random.choice(neighbors)
                
                if random_neighbor[0] == "top":
                    self._cells[row][col].has_top_wall = False
                    self._cells[random_neighbor[1]][random_neighbor[2]].has_bottom_wall = False
                elif random_neighbor[0] == "bot":
                    self._cells[row][col].has_bottom_wall = False
                    self._cells[random_neighbor[1]][random_neighbor[2]].has_top_wall = False
                elif random_neighbor[0] == "left":
                    self._cells[row][col].has_left_wall = False
                    self._cells[random_neighbor[1]][random_neighbor[2]].has_right_wall = False
                elif random_neighbor[0] == "right":
                    self._cells[row][col].has_right_wall = False
                    self._cells[random_neighbor[1]][random_neighbor[2]].has_left_wall = False
                
                self.draw_cells(row, col)
                self.draw_cells(random_neighbor[1], random_neighbor[2])
                
                self._break_walls(random_neighbor[1], random_neighbor[2])
            else:
                self.draw_cells(row, col)
                return
            
    def _reset_visited(self):
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                self._cells[row][col].visited = False

    def solve(self):
        return self.solve_recursive(0, 0)
    
    def solve_recursive(self, row, col):
        self.animate()
        self._cells[row][col].visited = True
        if row == self._num_rows - 1 and col == self._num_cols - 1:
            return True
        neighbors = self._get_unvisited_neighbors(row, col)
        for neighbor in neighbors:
            cell = self._cells[row][col]
            neighbor_cell = self._cells[neighbor[1]][neighbor[2]]
            if neighbor[0] == "top" and not cell.has_top_wall:
                cell.draw_move(neighbor_cell)
                if self.solve_recursive(neighbor[1], neighbor[2]):
                    return True
                else:
                    cell.draw_move(neighbor_cell, undo=True)
            elif neighbor[0] == "bot" and not cell.has_bottom_wall:
                cell.draw_move(neighbor_cell)
                if self.solve_recursive(neighbor[1], neighbor[2]):
                    return True
                else:
                    cell.draw_move(neighbor_cell, undo=True)
            elif neighbor[0] == "left" and not cell.has_left_wall:
                cell.draw_move(neighbor_cell)
                if self.solve_recursive(neighbor[1], neighbor[2]):
                    return True
                else:
                    cell.draw_move(neighbor_cell, undo=True)
            elif neighbor[0] == "right" and not cell.has_right_wall:
                cell.draw_move(neighbor_cell)
                if self.solve_recursive(neighbor[1], neighbor[2]):
                    return True
                else:
                    cell.draw_move(neighbor_cell, undo=True)
        return False




    def solve_easy(self):
        self._cells[0][0].draw_move(self._cells[self._num_rows - 1][self._num_cols - 1])


def maze():
    win = Window(800, 600)
    m = Maze(10, 10, 4, 4, 200, 200, win)
    m._break_entrance_and_exit_walls()
    m._break_walls(0, 0)
    m._reset_visited()
    m.solve()
    win.wait_for_close()
    print("Window closed")


maze()
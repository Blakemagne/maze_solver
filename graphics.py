from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="#1a1a2e", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            try:
                self.redraw()
            except:
                # Window was closed
                break
        print("window closed...")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
    
    def clear_canvas(self):
        self.__canvas.delete("all")

    def close(self):
        self.__running = False
        if self.__root:
            self.__root.quit()
            self.__root.destroy()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(
        self,
        p1,
        p2,
    ):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black", width=2):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=width
        )

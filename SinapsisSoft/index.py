from tkinter import ttk
from tkinter import *

class Product:
    def __init__(self, window):
        self.wind = window
        self.wind.title('Sinapsis Soft')
        
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
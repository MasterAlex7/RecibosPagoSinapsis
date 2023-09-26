from tkinter import ttk
from tkinter import *
import tkinter as tk
import pymysql.cursors
from tkinter import messagebox

class Product:
    # ... (tu código existente)

    def __init__(self, window):
        self.wind = window
        self.wind.title('Sinapsis Soft')

        # Crear el Notebook (pestañas)
        self.notebook = ttk.Notebook(self.wind)
        self.notebook.grid(row=0, column=0, columnspan=3, pady=20)

        # Pestaña para registrar cliente
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Registrar Cliente')
        self.create_register_tab(self.tab1)

        # Pestaña para mostrar lista de clientes
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Lista de Clientes')

    def create_register_tab(self, tab):
        frame = LabelFrame(tab, text='Registrar nuevo cliente')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text='Numero de Contrato: ').grid(row=1, column=0)
        self.numContrato = Entry(frame)
        self.numContrato.grid(row=1, column=1)

        Label(frame, text='Nombre Cliente: ').grid(row=2, column=0)
        self.nomCliente = Entry(frame)
        self.nomCliente.grid(row=2, column=1)

        Label(frame, text='Saldo: ').grid(row=3, column=0)
        self.saldo = Entry(frame)
        self.saldo.grid(row=3, column=1)

        Label(frame, text='Mensualidades: ').grid(row=4, column=0)
        self.mensua = Entry(frame)
        self.mensua.grid(row=4, column=1)

        ttk.Button(frame, text='Guardar Cliente').grid(row=5, columnspan=2, sticky=W + E)
        #ttk.Button(frame, text='Generar Recibo de Pago').grid(row=5, column=2, sticky=W + E)

        self.tree = ttk.Treeview(tab, height=10, columns=("","","",""))
        self.tree.grid(row=5, column=0, columnspan=2)
        self.tree.heading('#0', text='Numero de Contrato', anchor=CENTER)
        self.tree.heading('#1', text='Nombre', anchor=CENTER)
        self.tree.heading('#2', text='Saldo Anterior', anchor=CENTER)
        self.tree.heading('#3', text='Saldo Actual', anchor=CENTER)
        self.tree.heading('#4', text='Mensualidades', anchor=CENTER)

        ttk.Button(tab, text='Borrar').grid(row=6, column=0, sticky=W + E)
        ttk.Button(tab, text='Editar').grid(row=6, column=1, sticky=W + E)



if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()

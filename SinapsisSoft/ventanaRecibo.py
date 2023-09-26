from tkinter import ttk
from tkinter import *
import tkinter as tk
import pymysql.cursors
from tkinter import messagebox

class Product:
    dbHost = 'localhost'
    dbPort = 3306
    dbUser = 'root'
    dbPassword = 'Alexelpro27'
    dbName = 'sinapsis_clients'

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
        self.notebook.add(self.tab2, text='Crear Recibo')
        self.create_recibo_tab(self.tab2)

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

        ttk.Button(frame, text='Guardar Cliente',command=self.add_clients).grid(row=5, columnspan=2, sticky=W + E)
        #ttk.Button(frame, text='Generar Recibo de Pago').grid(row=5, column=2, sticky=W + E)

        self.tree = ttk.Treeview(tab, height=10, columns=("","","",""))
        self.tree.grid(row=5, column=0, columnspan=2)
        self.tree.heading('#0', text='Numero de Contrato', anchor=CENTER)
        self.tree.heading('#1', text='Nombre', anchor=CENTER)
        self.tree.heading('#2', text='Saldo Anterior', anchor=CENTER)
        self.tree.heading('#3', text='Saldo Actual', anchor=CENTER)
        self.tree.heading('#4', text='Mensualidades', anchor=CENTER)

        ttk.Button(tab, text='Borrar', command=self.delete_clients).grid(row=6, column=0, sticky=W + E)
        ttk.Button(tab, text='Editar').grid(row=6, column=1, sticky=W + E)
        
        self.get_clients()

    def create_recibo_tab(self, tab):
        frame = LabelFrame(tab, text='Nuevo Abono')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.etiquetaNombre= Label(frame)
        self.etiquetaNombre.grid(row=1, column=1)

        Label(frame, text='Numero de Contrato: ').grid(row=2, column=0)
        self.numContratoRecibo = Entry(frame)
        self.numContratoRecibo.grid(row=2, column=1)

        ttk.Button(frame, text='Buscar').grid(row=2,column=3, columnspan=2, sticky=W + E)

        Label(frame, text='Cantidad Recibida: ').grid(row=3, column=0)
        self.cantidadRecibida = Entry(frame)
        self.cantidadRecibida.grid(row=3, column=1)

        Label(frame, text='Mensualidad Recibida: ').grid(row=4, column=0)
        self.mensualidadRecibida = Entry(frame)
        self.mensualidadRecibida.grid(row=4, column=1)

        Label(frame, text='Abono: ').grid(row=5, column=0)
        self.abono = Entry(frame)
        self.abono.grid(row=5, column=1)

        Label(frame, text='Descuento: ').grid(row=6, column=0)
        self.descuento = Entry(frame)
        self.descuento.grid(row=6, column=1)

        Label(frame, text='Recibio: ').grid(row=7, column=0)
        self.nombreAcreedor = Entry(frame)
        self.nombreAcreedor.grid(row=7, column=1)

        ttk.Button(frame, text='Crear Recibo').grid(row=8, columnspan=2, sticky=W + E)
        #ttk.Button(frame, text='Generar Recibo de Pago').grid(row=5, column=2, sticky=W + E)

        self.tree2 = ttk.Treeview(tab, height=7, columns=("",))
        self.tree2.grid(row=5, column=0, columnspan=2)
        self.tree2.heading('#0', text='Nombre', anchor=CENTER)
        self.tree2.heading('#1', text='Numero de Contrato', anchor=CENTER)
        
        ttk.Button(tab, text='Seleccionar', command=self.select_register).grid(row=6, column=0, sticky=W + E)

        self.get_clientsRecibo()

    def run_query(self,query,parameters = ()):
        MysqlCnx = pymysql.connect(host=self.dbHost,port=self.dbPort,
                                user=self.dbUser,
                                password=self.dbPassword,
                                db=self.dbName,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        cursor = MysqlCnx.cursor()
        cursor.execute(query,parameters)
        response=cursor.fetchall()
        return response
    
    def run_query_add(self,query,parameters = ()):
        MysqlCnx = pymysql.connect(host=self.dbHost,port=self.dbPort,
                                user=self.dbUser,
                                password=self.dbPassword,
                                db=self.dbName,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        cursor = MysqlCnx.cursor()
        cursor.execute(query,parameters)
        MysqlCnx.commit()
    
    def get_clients(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #Obetniendo datos y pintandolos
        query = 'SELECT * FROM cliente'
        response = self.run_query(query)
        for row in response:
            #print(row)
            self.tree.insert('',0,text = row['num_contrato'], values = (row['nombre_cliente'],row['saldo_anterior'],row['saldo_actual'],row['total_mensualidades']))
            
    def get_clientsRecibo(self):
        records = self.tree2.get_children()
        for element in records:
            self.tree2.delete(element)

        #Obetniendo datos y pintandolos
        query = 'SELECT num_contrato,nombre_cliente FROM cliente'
        response = self.run_query(query)
        for row in response:
            #print(row)
            self.tree2.insert('',0,text = row['nombre_cliente'], values = (row['num_contrato']))

    def validation(self):
        return len(self.numContrato.get()) != 0 and len(self.nomCliente.get()) != 0 and len(self.saldo.get()) != 0 and len(self.mensua.get()) != 0
    
    def add_clients(self):
        try:
            if self.validation():
                query = 'INSERT INTO cliente (num_contrato, nombre_cliente, saldo_anterior, saldo_actual, total_mensualidades) values(%s,%s, %s, %s, %s)'
                parameters = (self.numContrato.get(),self.nomCliente.get(),self.saldo.get(),self.saldo.get(),self.mensua.get())
                self.run_query_add(query,parameters)
                #print('Datos guardados')
                messagebox.showinfo("Éxito", "Datos guardados correctamente")
            else:
                #print('Error al guardar datos')
                messagebox.showinfo("Fracaso", "Datos Erroneos")
        except pymysql.Error as e:
            #print("Error al guardar los datos: ", e)
            messagebox.showerror("Error", "Error al guardar los datos")
        self.get_clients()
        self.get_clientsRecibo()
        self.numContrato.delete(0,END)
        self.nomCliente.delete(0,END)
        self.saldo.delete(0,END)
        self.mensua.delete(0,END)

    def delete_clients(self):
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            #print('Seleccione un registro')
            messagebox.showinfo("Fracaso", "Seleccione un registro")
            return
        numContrato = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM cliente WHERE num_contrato = %s'
        self.run_query_add(query,(numContrato,))
        #print('Registro Eliminado')
        messagebox.showinfo("Éxito", "Registro Eliminado")
        self.get_clientsRecibo()
        self.get_clients()

    def select_register(self):
        try:
            self.numContratoRecibo.delete(0,END)
            self.tree2.item(self.tree2.selection())['values'][0]
            numContrato = self.tree2.item(self.tree2.selection())['values'][0]
            nomCliente = self.tree2.item(self.tree2.selection())['text']
            self.numContratoRecibo.insert(0, numContrato)
            self.etiquetaNombre.config(text=f'{nomCliente}')
        except IndexError as e:
            #print('Seleccione un registro')
            messagebox.showinfo("Fracaso", "Seleccione un registro")
            return


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()

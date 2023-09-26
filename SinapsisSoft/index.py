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

        frame = LabelFrame(self.wind, text = 'Registrar nuevo cliente')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        Label(frame, text = 'Numero de Contrato: ').grid(row = 1, column = 0)
        self.numContrato = Entry(frame)
        self.numContrato.grid(row = 1, column = 1)

        Label(frame, text = 'Nombre Cliente: ').grid(row = 2, column = 0)
        self.nomCliente = Entry(frame)
        self.nomCliente.grid(row = 2, column = 1)

        Label(frame, text = 'Saldo: ').grid(row = 3, column = 0)
        self.saldo = Entry(frame)
        self.saldo.grid(row = 3, column = 1)

        Label(frame, text = 'Mensualidades: ').grid(row = 4, column = 0)
        self.mensua = Entry(frame)
        self.mensua.grid(row = 4, column = 1)

        ttk.Button(frame, text = 'Guardar Cliente',command=self.add_clients).grid(row = 5, columnspan = 2, sticky = W + E)
        ttk.Button(text = 'Generar Recibo de Pago').grid(row = 5, column = 2, sticky = W + E)

        self.tree = ttk.Treeview(height = 10, columns = ("","","",""))
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Numero de Contrato', anchor = CENTER)
        self.tree.heading('#1', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#2', text = 'Saldo Anterior', anchor = CENTER)
        self.tree.heading('#3', text = 'Saldo Actual', anchor = CENTER)
        self.tree.heading('#4', text = 'Mensualidades', anchor = CENTER)

        ttk.Button(text = 'Borrar', command=self.delete_clients).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar').grid(row = 5, column = 1, sticky = W + E)

        self.get_clients()

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
        self.get_clients()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
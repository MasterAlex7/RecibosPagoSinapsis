from tkinter import ttk
from tkinter import *
import tkinter as tk
import pymysql.cursors
from tkinter import messagebox
import datetime
from pdfGenerator import receiveGenerate

class Product:
    dbHost = 'localhost'
    dbPort = 3306
    dbUser = 'root'
    dbPassword = 'Alexelpro27'
    dbName = 'sinapsis_clients'
    arrayDatos = {}

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

        Label(frame, text='*Numero de Contrato: ').grid(row=2, column=0)
        self.numContratoRecibo = Entry(frame)
        self.numContratoRecibo.grid(row=2, column=1)

        ttk.Button(frame, text='Buscar',command=self.search_client).grid(row=2,column=3, columnspan=2, sticky=W + E)

        Label(frame, text='*Cantidad Recibida: ').grid(row=3, column=0)
        self.cantidadRecibida = Entry(frame)
        self.cantidadRecibida.grid(row=3, column=1)

        Label(frame, text='*Mensualidad Recibida: ').grid(row=4, column=0)
        self.mensualidadRecibida = Entry(frame)
        self.mensualidadRecibida.grid(row=4, column=1)

        Label(frame, text='*Abono: ').grid(row=5, column=0)
        self.abono = Entry(frame)
        self.abono.grid(row=5, column=1)

        Label(frame, text='Descuento: ').grid(row=6, column=0)
        self.descuento = Entry(frame)
        self.descuento.grid(row=6, column=1)

        Label(frame,text='* Campos obligatorios', fg='red').grid(row=8, column=0)
        ttk.Button(frame, text='Crear Recibo',command=self.create_recibo).grid(row=9, columnspan=2, sticky=W + E)
        #ttk.Button(frame, text='Generar Recibo de Pago').grid(row=5, column=2, sticky=W + E)

        self.tree2 = ttk.Treeview(tab, height=7, columns=("",))
        self.tree2.grid(row=5, column=0, columnspan=2)
        self.tree2.heading('#0', text='Nombre', anchor=CENTER)
        self.tree2.heading('#1', text='Numero de Contrato', anchor=CENTER)
        
        ttk.Button(tab, text='Seleccionar', command=self.select_register).grid(row=6, column=0, sticky=W + E)

        self.get_clientsRecibo()

    def run_query(self,query,parameters = ()):
        print("Entro a run query")
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
            numContratoRecibo = self.tree2.item(self.tree2.selection())['values'][0]
            self.nomClienteRecibo = self.tree2.item(self.tree2.selection())['text']
            self.numContratoRecibo.insert(0, numContratoRecibo)
            self.etiquetaNombre.config(text=f'{self.nomClienteRecibo}')
            self.mensualidadRecibida.delete(0,END)
            self.abono.delete(0,END)
            self.descuento.delete(0,END)
            
            query = 'SELECT * FROM cliente WHERE num_contrato = %s'
            parameters = (self.numContratoRecibo.get())
            response = self.run_query(query,parameters)
            if len(response) == 0:
                messagebox.showinfo("Fracaso", "No se encontro el numero de contrato")
            else:
                query = 'SELECT mensualidad_recibida, abono, descuento FROM pago WHERE FK_ContratoCliente = %s ORDER BY fecha DESC LIMIT 1;'
                parameters = (self.numContratoRecibo.get())
                response = self.run_query(query,parameters)
                if len(response) == 0:
                    print("No hay pagos")
                else:
                    self.mensualidadRecibida.insert(0, response[0]['mensualidad_recibida']+1)
                    self.abono.insert(0, response[0]['abono'])
                    self.descuento.insert(0, response[0]['descuento'])
                #print(response)
        except IndexError as e:
            #print('Seleccione un registro')
            messagebox.showinfo("Fracaso", "Seleccione un registro")
            return
        
    def search_client(self):
        try:
            if len(self.numContratoRecibo.get()) != 0:
                self.mensualidadRecibida.delete(0,END)
                self.abono.delete(0,END)
                self.descuento.delete(0,END)
                print(self.numContratoRecibo.get())
                query = 'SELECT * FROM cliente WHERE num_contrato = %s'
                parameters = (self.numContratoRecibo.get())
                response = self.run_query(query,parameters)
                if len(response) == 0:
                    messagebox.showinfo("Fracaso", "No se encontro el numero de contrato")
                else:
                    self.etiquetaNombre.config(text=f'{response[0]["nombre_cliente"]}')
                    query = 'SELECT mensualidad_recibida, abono, descuento FROM pago WHERE FK_ContratoCliente = %s ORDER BY fecha DESC LIMIT 1;'
                    parameters = (self.numContratoRecibo.get())
                    response = self.run_query(query,parameters)
                    if len(response) == 0:
                        print("No hay pagos")
                    else:
                        self.mensualidadRecibida.insert(0, response[0]['mensualidad_recibida']+1)
                        self.abono.insert(0, response[0]['abono'])
                        self.descuento.insert(0, response[0]['descuento'])
            else:
                #print('Error al buscar datos')
                messagebox.showinfo("Fracaso", "No se ingreso un numero de contrato")
        except pymysql.Error as e:
            messagebox.showerror("Error", "Error al buscar los datos")

    def validationRecibo(self):
        return len(self.numContratoRecibo.get()) != 0 and len(self.cantidadRecibida.get()) != 0 and len(self.mensualidadRecibida.get()) != 0 and len(self.abono.get()) != 0

    def create_recibo(self):
        try:
            if self.validationRecibo():
                query = 'INSERT INTO pago (FK_ContratoCliente, cantidad_recibida, mensualidad_recibida, abono, descuento,fecha) values(%s,%s, %s, %s, %s,%s)'
                descuentoAux = self.descuento.get()
                if len(descuentoAux) == 0:
                    descuentoAux="0"
                else:
                    descuentoAux=self.descuento.get()
                parameters = (self.numContratoRecibo.get(),self.cantidadRecibida.get(),self.mensualidadRecibida.get(),self.abono.get(),descuentoAux,datetime.datetime.now())
                self.run_query_add(query,parameters)
                #print('Datos guardados')
                messagebox.showinfo("Éxito", "Datos guardados correctamente")
                receiveGenerate.crearPDF()
                self.numContratoRecibo.delete(0,END)
                self.cantidadRecibida.delete(0,END)
                self.mensualidadRecibida.delete(0,END)
                self.abono.delete(0,END)
                self.descuento.delete(0,END)
                self.etiquetaNombre.config(text=f'')
            else:
                #print('Error al guardar datos')
                messagebox.showinfo("Fracaso", "Por favor llene todos los campos obligatorios")
        except pymysql.Error as e:
            print("Error al guardar los datos: ", e)
            messagebox.showerror("Error", "Error al guardar los datos")



if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()

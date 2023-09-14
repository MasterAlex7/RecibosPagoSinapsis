from tkinter import ttk
from tkinter import *
import pymysql.cursors

class Product:
    dbHost = 'localhost'
    dbPort = 3306
    dbUser = 'root'
    dbPassword = 'Alexelpro27'
    dbName = 'sinapsis_clients'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Sinapsis Soft')

        frame = LabelFrame(self.wind, text = 'Registrar nuevo producto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 1)

        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        ttk.Button(frame, text = 'Guardar producto').grid(row = 3, columnspan = 2, sticky = W + E)

        self.tree = ttk.Treeview(height = 10, columns = ("","","",""))
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Numero de Contrato', anchor = CENTER)
        self.tree.heading('#1', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#2', text = 'Saldo Anterior', anchor = CENTER)
        self.tree.heading('#3', text = 'Saldo Actual', anchor = CENTER)
        self.tree.heading('#4', text = 'Mensualidades', anchor = CENTER)

        self.get_clients()

    def run_procedures(self,query,parameters = ()):
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
    
    def get_clients(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #Obetniendo datos y pintandolos
        query = 'SELECT * FROM cliente'
        response = self.run_procedures(query)
            
        
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
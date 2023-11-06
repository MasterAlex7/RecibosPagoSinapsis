import pymysql.cursors
import random
from datetime import datetime, timedelta


class insercionVarios:
    dbHost = 'localhost'
    dbPort = 3306
    dbUser = 'root'
    dbPassword = 'Alexelpro27'
    dbName = 'sinapsis_clients'
    fecha_inicio = datetime(2023, 1, 1)
    fecha_fin = datetime(2024, 12, 31)

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

    def insertarPagos(self):
        todas_las_fechas = [self.fecha_inicio + timedelta(days=i) for i in range((self.fecha_fin - self.fecha_inicio).days + 1)]
        random.shuffle(todas_las_fechas)
        for i in range(0,100):
            query = "INSERT INTO pago (FK_ContratoCliente, cantidad_recibida, mensualidad_recibida, abono, descuento, fecha) VALUES (%s, %s, %s, %s, %s, %s)"
            parameters = (123654, 1, 1, 1, 0,todas_las_fechas[i])
            self.run_query_add(query,parameters)

if __name__ == '__main__':
    insercionVarios().insertarPagos()
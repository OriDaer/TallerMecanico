import mysql.connector
import os
from datetime import datetime

class ConexionDB:
    def __init__(self):
        self.conn = None # Conexión a la base de datos
        self.cursor = None 
        self.conectar()

    def conectar(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root', 
            database='taller_mecanico',
            port=3306
        )
        if self.conn.is_connected(): # Verificar si la conexión es exitosa
            self.cursor = self.conn.cursor()

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

class Taller:
    def __init__(self):
        self.db = ConexionDB()

    def limpiar(self):# Limpia la consola  
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_principal(self):
        while True:
            print("""
--- Menú Principal ---
1. Clientes
2. Empleados
3. Vehículos
4. Repuestos
5. Ficha Técnica
6. Facturación
7. Salir
""")
            op = input("Seleccione una opción: ")
            if op == "1":
                self.menu_clientes()
            elif op == "2":
                self.menu_secundario("empleados")
            elif op == "3":
                self.menu_secundario("vehiculos")
            elif op == "4":
                self.menu_secundario("repuestos")
            elif op == "5":
                self.menu_ficha_tecnica()
            elif op == "6":
                self.menu_secundario("facturacion")
            elif op == "7":
                print("Saliendo...")
                self.db.cerrar()
                break
            else:
                print("Opción inválida.")

    def menu_secundario(self, tabla):
        while True:
            print(f"""
--- Menú {tabla} ---
1. Alta
2. Baja
3. Modificación
4. Consulta
5. Volver
""")
            op = input("Seleccione una opción: ")
            if op == "1":
                self.alta(tabla)
            elif op == "2":
                self.baja(tabla)
            elif op == "3":
                self.modificacion(tabla)
            elif op == "4":
                self.consulta(tabla)
            elif op == "5":
                break
            else:
                print("Opción inválida.")

    def menu_clientes(self):
        while True:
            print("""
--- Menú Clientes ---
1. Alta
2. Baja
3. Modificación
4. Consulta
5. Vehículos del Cliente
6. Volver
""")
            op = input("Seleccione una opción: ")
            if op == "1":
                self.alta("clientes")
            elif op == "2":
                self.baja("clientes")
            elif op == "3":
                self.modificacion("clientes")
            elif op == "4":
                self.consulta("clientes")
            elif op == "5":
                self.menu_vehiculos_cliente()
            elif op == "6":
                break
            else:
                print("Opción inválida.")

    def menu_vehiculos_cliente(self):
        while True:
            print("""
--- Vehículos del Cliente ---
1. Alta
2. Baja
3. Consulta
4. Volver
""")
            op = input("Seleccione una opción: ")
            if op == "1":
                self.alta_vehiculo_cliente()
            elif op == "2":
                self.baja("vehiculos")
            elif op == "3":
                self.consulta_vehiculos_cliente()
            elif op == "4":
                break
            else:
                print("Opción inválida.")

    def menu_ficha_tecnica(self):
        while True:
            print("""
--- Ficha Técnica ---
1. Alta
2. Baja
3. Consulta
4. Volver
""")
            op = input("Seleccione una opción: ")
            if op == "1":
                self.alta("ficha_tecnica")
            elif op == "2":
                self.baja("ficha_tecnica")
            elif op == "3":
                self.consulta_ficha_tecnica()
            elif op == "4":
                break
            else:
                print("Opción inválida.")

    def alta(self, tabla):
        if tabla == "clientes":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            consulta = "INSERT INTO clientes (nombre, apellido, dni, telefono, direccion) VALUES (%s,%s,%s,%s,%s)"
            self.db.cursor.execute(consulta, (nombre, apellido, dni, telefono, direccion))
        elif tabla == "empleados":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            puesto = input("Puesto: ")
            telefono = input("Teléfono: ")
            consulta = "INSERT INTO empleados (nombre, apellido, dni, puesto, telefono) VALUES (%s,%s,%s,%s,%s)"
            self.db.cursor.execute(consulta, (nombre, apellido, dni, puesto, telefono))
        elif tabla == "vehiculos":
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            anio = input("Año: ")
            patente = input("Patente: ")
            id_cliente = input("ID Cliente: ")
            if not self.existe_en_tabla("clientes", id_cliente):
                print("El cliente no existe.")
                return
            consulta = "INSERT INTO vehiculos (marca, modelo, anio, patente, id_cliente) VALUES (%s,%s,%s,%s,%s)"
            self.db.cursor.execute(consulta, (marca, modelo, anio, patente, id_cliente))
        elif tabla == "repuestos":
            nombre = input("Nombre: ")
            marca = input("Marca: ")
            precio = input("Precio: ")
            stock = input("Stock: ")
            consulta = "INSERT INTO repuestos (nombre, marca, precio, stock) VALUES (%s,%s,%s,%s)"
            self.db.cursor.execute(consulta, (nombre, marca, precio, stock))
        elif tabla == "ficha_tecnica":
            id_vehiculo = input("ID Vehículo: ")
            if not self.existe_en_tabla("vehiculos", id_vehiculo):
                print("El vehículo no existe.")
                return
            id_repuesto = input("ID Repuesto (opcional, puede dejar vacío): ")
            if id_repuesto and not self.existe_en_tabla("repuestos", id_repuesto):
                print("El repuesto no existe.")
                return
            id_cliente = input("ID Cliente: ")
            if not self.existe_en_tabla("clientes", id_cliente):
                print("El cliente no existe.")
                return
            descripcion = input("Descripción: ")
            fecha = input("Fecha (año-mes-día): ")
            if not self.validar_fecha(fecha):
                print("Fecha inválida.")
                return
            repuesto_val = id_repuesto if id_repuesto else None
            consulta = "INSERT INTO ficha_tecnica (id_vehiculo, id_repuesto, id_cliente, descripcion, fecha) VALUES (%s,%s,%s,%s,%s)"
            self.db.cursor.execute(consulta, (id_vehiculo, repuesto_val, id_cliente, descripcion, fecha))
        elif tabla == "facturacion":
            id_cliente = input("ID Cliente: ")
            if not self.existe_en_tabla("clientes", id_cliente):
                print("El cliente no existe.")
                return
            monto = input("Monto total: ")
            fecha = input("Fecha (año-mes-día): ")
            if not self.validar_fecha(fecha):
                print("Fecha inválida.")
                return
            consulta = "INSERT INTO facturacion (id_cliente, monto_total, fecha) VALUES (%s,%s,%s)"
            self.db.cursor.execute(consulta, (id_cliente, monto, fecha))
        else:
            print("Tabla no válida")
            return
        self.db.conn.commit()
        print("Registro agregado con éxito.")

    def baja(self, tabla):
        id_eliminar = input(f"ID a eliminar : ")
        if not self.existe_en_tabla(tabla, id_eliminar):
            print("Error, ID no existe.")
            return
        if tabla == "clientes":
            self.db.cursor.execute("DELETE FROM vehiculos WHERE id_cliente=%s", (id_eliminar,))
        self.db.cursor.execute(f"DELETE FROM {tabla} WHERE id=%s", (id_eliminar,))
        self.db.conn.commit()
        print("Registro eliminado.")

    def modificacion(self, tabla):
        id_modificar = input("ID a modificar: ")
        if not self.existe_en_tabla(tabla, id_modificar):
            print("ID no existe.")
            return
        if tabla == "clientes":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")
            consulta = "UPDATE clientes SET nombre=%s, apellido=%s, dni=%s, telefono=%s, direccion=%s WHERE id=%s"
            self.db.cursor.execute(consulta, (nombre, apellido, dni, telefono, direccion, id_modificar))
        elif tabla == "empleados":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            puesto = input("Puesto: ")
            telefono = input("Teléfono: ")
            consulta = "UPDATE empleados SET nombre=%s, apellido=%s, dni=%s, puesto=%s, telefono=%s WHERE id=%s"
            self.db.cursor.execute(consulta, (nombre, apellido, dni, puesto, telefono, id_modificar))
        elif tabla == "vehiculos":
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            anio = input("Año: ")
            patente = input("Patente: ")
            id_cliente = input("ID Cliente: ")
            if not self.existe_en_tabla("clientes", id_cliente):
                print("Cliente no existe.")
                return
            consulta = "UPDATE vehiculos SET marca=%s, modelo=%s, anio=%s, patente=%s, id_cliente=%s WHERE id=%s"
            self.db.cursor.execute(consulta, (marca, modelo, anio, patente, id_cliente, id_modificar))
        elif tabla == "repuestos":
            nombre = input("Nombre: ")
            marca = input("Marca: ")
            precio = input("Precio: ")
            stock = input("Stock: ")
            consulta = "UPDATE repuestos SET nombre=%s, marca=%s, precio=%s, stock=%s WHERE id=%s"
            self.db.cursor.execute(consulta, (nombre, marca, precio, stock, id_modificar))
        else:
            print("Tabla no válida para modificar.")
            return
        self.db.conn.commit()
        print("Registro modificado correctamente.")

    def consulta(self, tabla):
        while True:
            print("""
Consulta por:
1. General
2. Particular
3. Volver
""")
            op = input("Seleccione opción: ")
            if op == "1":
                self.consulta_general(tabla)
            elif op == "2":
                self.consulta_particular(tabla)
            elif op == "3":
                break
            else:
                print("Opción inválida.")

    def consulta_general(self, tabla):
        self.db.cursor.execute(f"SELECT * FROM {tabla}")
        filas = self.db.cursor.fetchall()
        if filas:
            for fila in filas:
                print(fila)
        else:
            print("No hay registros.")

    def consulta_particular(self, tabla):
        id_buscar = input("Ingrese ID: ")
        self.db.cursor.execute(f"SELECT * FROM {tabla} WHERE id=%s", (id_buscar,))
        fila = self.db.cursor.fetchone()
        if fila:
            print(fila)
        else:
            print("No encontrado.")

    def alta_vehiculo_cliente(self):
        print("Alta vehículo para cliente")
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        anio = input("Año: ")
        patente = input("Patente: ")
        id_cliente = input("ID Cliente: ")
        if not self.existe_en_tabla("clientes", id_cliente):
            print("Cliente no existe.")
            return
        consulta = "INSERT INTO vehiculos (marca, modelo, anio, patente, id_cliente) VALUES (%s,%s,%s,%s,%s)"
        self.db.cursor.execute(consulta, (marca, modelo, anio, patente, id_cliente))
        self.db.conn.commit()
        print("Vehículo agregado con éxito.")

    def consulta_vehiculos_cliente(self):
        id_cliente = input("ID Cliente: ")
        self.db.cursor.execute("""
            SELECT v.id, v.marca, v.modelo, v.anio, v.patente
            FROM vehiculos v
            WHERE v.id_cliente = %s
            """, (id_cliente,))
        filas = self.db.cursor.fetchall()
        if filas:
            for fila in filas:
                print(fila)
        else:
            print("No se encontraron vehículos para ese cliente.")

    def consulta_ficha_tecnica(self):
        while True:
            print("""
Consultar ficha técnica por:
1. Vehículo
2. Repuesto
3. Cliente
4. Volver
""")
            op = input("Seleccione opción: ")
            if op == "1":
                id_vehiculo = input("ID Vehículo: ")
                self.db.cursor.execute("SELECT * FROM ficha_tecnica WHERE id_vehiculo=%s", (id_vehiculo,))
                filas = self.db.cursor.fetchall()
                if filas:
                    for fila in filas:
                        print(fila)
                else:
                    print("No hay fichas para ese vehículo.")
            elif op == "2":
                id_repuesto = input("ID Repuesto: ")
                self.db.cursor.execute("SELECT * FROM ficha_tecnica WHERE id_repuesto=%s", (id_repuesto,))
                filas = self.db.cursor.fetchall()
                if filas:
                    for fila in filas:
                        print(fila)
                else:
                    print("No hay fichas para ese repuesto.")
            elif op == "3":
                id_cliente = input("ID Cliente: ")
                self.db.cursor.execute("SELECT * FROM ficha_tecnica WHERE id_cliente=%s", (id_cliente,))
                filas = self.db.cursor.fetchall()
                if filas:
                    for fila in filas:
                        print(fila)
                else:
                    print("No hay fichas para ese cliente.")
            elif op == "4":
                break
            else:
                print("Opción inválida.")

    def existe_en_tabla(self, tabla, id_buscar):# Verifica si un ID existe en una tabla
        self.db.cursor.execute(f"SELECT id FROM {tabla} WHERE id=%s", (id_buscar,))
        return self.db.cursor.fetchone() is not None

    def validar_fecha(self, fecha_str):
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    taller = Taller()
    taller.limpiar()
    taller.menu_principal()

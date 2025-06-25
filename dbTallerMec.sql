#Creado desde mysql workbench :)
CREATE DATABASE IF NOT EXISTS taller_mecanico;
USE taller_mecanico;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    dni VARCHAR(20),
    telefono VARCHAR(20),
    direccion VARCHAR(200)
);

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    dni VARCHAR(20),
    puesto VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    anio INT,
    patente VARCHAR(20),
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

CREATE TABLE repuestos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    marca VARCHAR(100),
    precio DECIMAL(10,2),
    stock INT
);

CREATE TABLE ficha_tecnica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT,
    id_repuesto INT,
    id_cliente INT,
    descripcion TEXT,
    fecha DATE,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id),
    FOREIGN KEY (id_repuesto) REFERENCES repuestos(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

CREATE TABLE facturacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    monto_total DECIMAL(12,2),
    fecha DATE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

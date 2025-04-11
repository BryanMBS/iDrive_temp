create database Aliante;

use Aliante;

CREATE TABLE Productos (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO Productos (nombre, descripcion, precio, stock)
VALUES 
('Bomba de Aire de Alta Gama', 'Bomba de aire portátil con diseño elegante y tecnología avanzada', 500.00, 10 ),
('Guarda Polvo de Lujo', 'Guarda polvo de cuero premium, especialmente diseñado para autos deportivos', 200.00, 30),
('Tapas de Válvula de Oro', 'Tapas de válvula en oro de 18 quilates, diseño exclusivo para autos de lujo', 150.00,  20),
('Limpia Parabrisas Ultra', 'Limpia parabrisas de alta calidad con diseño de lujo', 80.00, 30);


SELECT producto_id, nombre, descripcion, precio, stock
FROM aliante.productos;
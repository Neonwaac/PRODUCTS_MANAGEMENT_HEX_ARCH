drop schema if exists mercancia060426;
create schema mercancia060426;
use mercancia060426;


create table producto(
idproducto int primary key auto_increment,
producto text,
marca text,
precio decimal(10, 2)
);

INSERT INTO producto (producto, marca, precio) 
VALUES 
('Teclado mecánico', 'Redragon', 150.00),
('Monitor 24 pulgadas', 'Samsung', 900.00);
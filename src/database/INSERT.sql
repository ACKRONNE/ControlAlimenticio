INSERT INTO pacientes VALUES (1,'Kimberly','Kardashian','West','F','paciente@gmail.com',555123456,'1234','1990-05-15','Noel'),
(2,'María','García','López','F','paciente2@email.com',555123457,'1234','1985-08-22','Ana'),
(3,'Carlos','Rodríguez','Martínez','M','paciente3@email.com',555123458,'1234','1998-02-10','Laura');

INSERT INTO especialistas VALUES (1,'Leonel','Messi','Rocusso','M','especialista@gmail.com',555987653,'1234','Nutricionista','Andres'),
(2,'Alejandro','Martínez','López','M','especialista2@email.com',555987654,'1234','Dietista','Carolina'),
(3,'Laura','Rodríguez','Sánchez','F','especialista3@email.com',555987655,'1234','Nutricionista','Juan');

INSERT INTO alimentos VALUES (1,'Proteina','Pollo',1),
(2,'Carbohidrato','Arroz',2),
(3,'Grasa','Aceite de Oliva',2),
(4,'Vegetal','Espinacas',3),
(5,'Fruta','Manzana',4),
(6,'Otros','Yogur Natural',5),
(7,'Bebida','Agua',1),
(8,'Dulce','Chocolate',2),
(9,'Otros','Papas Fritas',3),
(10,'Otros','Quinoa',11),
(11,'Proteina','Salmón',12),
(12,'Carbohidrato','Pasta',23),
(13,'Grasa','Aguacate',4),
(14,'Vegetal','Zanahorias',5),
(15,'Fruta','Plátano',2),
(16,'Bebida','Té Verde',2),
(17,'Dulce','Galletas',1),
(18,'Otros','Queso',4),
(19,'Otros','Atún en lata',2),
(20,'Carbohidrato','Batata',3),
(21,'Proteina','Huevos',5),
(22,'Fruta','Fresas',6),
(23,'Vegetal','Brócoli',2),
(24,'Grasa','Nueces',2),
(25,'Otros','Tofu',1);

INSERT INTO comidas VALUES (1,1,'2023-07-15 8:00:00','D','Mal','No me gusta'),
(1,1,'2023-07-15 12:00:00','A','Super','estuvo pesima '),
(1,2,'2023-03-15 8:00:00','D','Normal','todo el tiempo lo mismo'),
(1,2,'2023-03-15 12:00:00','A','Super','la combinacion estaba deliciosa');

INSERT INTO a_c VALUES (1,1,'2023-07-15 8:00:00',1),
(1,1,'2023-07-15 8:00:00',2),
(1,1,'2023-07-15 8:00:00',3),
(1,1,'2023-07-15 8:00:00',4),
(1,1,'2023-07-15 12:00:00',5),
(1,1,'2023-07-15 12:00:00',6),
(1,1,'2023-07-15 12:00:00',7),
(1,1,'2023-07-15 12:00:00',8),
(1,2,'2023-03-15 8:00:00',9),
(1,2,'2023-03-15 8:00:00',10),
(1,2,'2023-03-15 8:00:00',11),
(1,2,'2023-03-15 8:00:00',12),
(1,2,'2023-03-15 12:00:00',13),
(1,2,'2023-03-15 12:00:00',14),
(1,2,'2023-03-15 12:00:00',15),
(1,2,'2023-03-15 12:00:00',16);


Alimento(tipo="Proteina", nombre="Pechuga de pollo", cantidad=100)
Alimento(tipo="Proteina", nombre="Salmón", cantidad=100)
Alimento(tipo="Proteina", nombre="Huevo cocido", cantidad=1)
Alimento(tipo="Proteina", nombre="Tofu", cantidad=100)
Alimento(tipo="Proteina", nombre="Lentejas", cantidad=100)
Alimento(tipo="Proteina", nombre="Atún en agua", cantidad=100)
Alimento(tipo="Proteina", nombre="Yogur griego", cantidad=150)
Alimento(tipo="Carbohidrato", nombre="Arroz integral", cantidad=100)
Alimento(tipo="Carbohidrato", nombre="Avena", cantidad=40)
Alimento(tipo="Carbohidrato", nombre="Pan integral", cantidad=1)
Alimento(tipo="Carbohidrato", nombre="Quinoa", cantidad=100)
Alimento(tipo="Carbohidrato", nombre="Batata", cantidad=100)
Alimento(tipo="Carbohidrato", nombre="Pasta de trigo integral", cantidad=100)
Alimento(tipo="Grasa", nombre="Aguacate", cantidad=50)
Alimento(tipo="Grasa", nombre="Nueces", cantidad=30)
Alimento(tipo="Grasa", nombre="Aceite de oliva", cantidad=15)  # 1 cucharada
Alimento(tipo="Grasa", nombre="Mantequilla de maní", cantidad=20)
Alimento(tipo="Grasa", nombre="Semillas de chía", cantidad=15)
Alimento(tipo="Vegetal", nombre="Espinacas", cantidad=100)
Alimento(tipo="Vegetal", nombre="Brócoli", cantidad=100)
Alimento(tipo="Vegetal", nombre="Zanahoria", cantidad=100)
Alimento(tipo="Vegetal", nombre="Pimiento rojo", cantidad=100)
Alimento(tipo="Vegetal", nombre="Coliflor", cantidad=100)
Alimento(tipo="Vegetal", nombre="Tomate", cantidad=100)
Alimento(tipo="Fruta", nombre="Manzana", cantidad=1)
Alimento(tipo="Fruta", nombre="Plátano", cantidad=1)
Alimento(tipo="Fruta", nombre="Fresas", cantidad=150)
Alimento(tipo="Fruta", nombre="Naranja", cantidad=1)
Alimento(tipo="Fruta", nombre="Uvas", cantidad=100)
Alimento(tipo="Fruta", nombre="Piña", cantidad=100)
Alimento(tipo="Bebida", nombre="Agua", cantidad=250)      # 1 vaso
Alimento(tipo="Bebida", nombre="Leche desnatada", cantidad=250)
Alimento(tipo="Bebida", nombre="Jugo de naranja natural", cantidad=200)
Alimento(tipo="Bebida", nombre="Té verde", cantidad=250)
Alimento(tipo="Dulce", nombre="Chocolate negro (70%)", cantidad=30)
Alimento(tipo="Dulce", nombre="Galleta de avena", cantidad=1)
Alimento(tipo="Dulce", nombre="Helado de vainilla", cantidad=100)
Alimento(tipo="Otros", nombre="Barra de proteína", cantidad=1)
Alimento(tipo="Otros", nombre="Suplemento vitamínico", cantidad=1)
Alimento(tipo="Otros", nombre="Sopa de miso", cantidad=200)
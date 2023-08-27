CREATE TABLE alimento(
    id_alimento     numeric(3)      PRIMARY KEY,
    tipo            varchar(12)     NOT NULL        CHECK(tipo IN ('proteina','carbohidrato','vegetal','grasa','fruta','bebida','otro')),
    nombre          varchar(30)     NOT NULL,
    cantidad        numeric(2)      NOT NULL
);

CREATE TABLE persona(
    id_persona      numeric(3)      PRIMARY KEY,
    nombre          varchar(15)     NOT NULL,
    apellido        varchar(15)     NOT NULL,
    tipo            char(1)         NOT NULL        CHECK(tipo IN ('p','e')),
    sexo            char(1)         NOT NULL        CHECK(sexo IN ('m','f')),
    correo          text            NOT NULL        UNIQUE,
    telefono        numeric(12)     NOT NULL,
    contraseña      text            NOT NULL,
    fecha_nac       date,
    especialidad    varchar(30),
    id_espe         numeric(3)      REFERENCES persona(id_persona)
);

CREATE TABLE comida(
    id_comida       numeric(3)      NOT NULL,
    id_persona      numeric(3)      NOT NULL,   
    tipo            char(1)         NOT NULL        CHECK(tipo IN ('d','a','c','m')),
    satisfaccion    varchar(11)     CHECK(satisfaccion IN ('super','bien','normal','no muy bien','mal','cansado')),
    comentario      text,
    CONSTRAINT pk_det   PRIMARY KEY (id_persona,id_comida),
    CONSTRAINT fk_dc    FOREIGN KEY (id_persona)  REFERENCES  persona(id_persona)
);

CREATE TABLE hist_comida(
    id_comida       numeric(3)      NOT NULL,
    id_persona      numeric(3)      NOT NULL,   
    fecha_ini       date            NOT NULL,
    fecha_fin       date,
    CONSTRAINT pk_hist  PRIMARY KEY (id_comida, id_persona , fecha_ini),
    CONSTRAINT fk_hr    FOREIGN KEY (id_persona, id_comida)  REFERENCES  comida(id_persona, id_comida)
);

CREATE TABLE a_r(
    id_comida       numeric(3)      NOT NULL,
    id_persona      numeric(3)      NOT NULL,
    id_alimento     numeric(3)      NOT NULL,
    CONSTRAINT pk_ar    PRIMARY KEY (id_comida, id_persona, id_alimento),
    CONSTRAINT fk_ar    FOREIGN KEY (id_persona, id_comida)  REFERENCES  comida(id_persona, id_comida),
    CONSTRAINT fk_aa    FOREIGN KEY (id_alimento)   REFERENCES  alimento(id_alimento)
);

-- I N S E R T S

INSERT INTO persona
VALUES (1,'Juan','Perez','p','m','juan.perez@example.com',5551234567,'1234','1990-03-03',NULL,2),
(2,'Maria','Lopez','e','f','maria.lopez@example.com',4449876543,'1234',NULL,'nutricionista',NULL),
(3,'Luis','Garcia','p','m','luis.garcia@example.com',3334567890,'1234','1920-03-05',NULL,3),
(4,'Ana','Martinez','e','f','ana.martinez@example.com',2227891234,'1234',NULL,'nutricionista',NULL),
(5,'Carlos','Rodriguez','p','m','carlos.rodriguez@example.com',6663210987,'1234','1910-03-07',NULL,4),
(6,'Leonel','Messi','e','f','especialista@gmail.com',7779876543,'1234',NULL,'nutricionista',NULL),
(7,'Kim','Kardashian','p','m','paciente@gmail.com',8882345678,'1234','2000-03-09',NULL,6);

INSERT INTO alimento
VALUES (1,'proteina','carne',1),
(2,'carbohidrato','papas',4),
(3,'vegetal','champiñones',4),
(4,'grasa','aceite de oliva',1),
(5,'fruta','piña',2),
(6,'bebida','limonada',1),
(7,'otro','helado',1),
(8,'proteina','pollo',2),
(9,'carbohidrato','arroz',3),
(10,'vegetal','espinacas',2),
(11,'grasa','manteca de cerdo',1),
(12,'fruta','manzana',3),
(13,'bebida','agua',5),
(14,'otro','galletas',6),
(15,'proteina','pescado',1),
(16,'carbohidrato','pan',5),
(17,'vegetal','zanahorias',3),
(18,'grasa','aguacate',2),
(19,'fruta','fresa',7),
(20,'bebida','té',2),
(21,'proteina','huevo',2),
(22,'carbohidrato','avena',1),
(23,'fruta','plátano',1),
(24,'otro','yogur',1),
(25,'carbohidrato','pan integral',2),
(26,'proteina','queso',2),
(27,'grasa','mantequilla',1),
(28,'bebida','café',1),
(29,'carbohidrato','granola',1),
(30,'bebida','jugo de naranja',1);

INSERT INTO comida
VALUES (1,7,'d',NULL,NULL),
(2,7,'a',NULL,NULL),
(3,7,'c',NULL,NULL),
(4,7,'m',NULL,NULL),
(5,6,'d','mal','estuvo pesima '),
(6,6,'a','cansado','todo el tiempo lo mismo'),
(7,6,'c','super','la combinacion estaba deliciosa'),
(8,6,'m','bien','No tengo nada que decir');

INSERT INTO hist_comida
VALUES (1,7,'2023-07-15','2023-07-20'),
(2,7,'2023-06-10','2023-06-18'),
(3,7,'2023-08-01','2023-08-05'),
(4,7,'2023-04-22','2023-05-01'),
(5,6,'2023-03-15','2023-03-20'),
(6,6,'2023-07-01','2023-07-10'),
(7,6,'2023-08-20','2023-09-02'),
(8,6,'2023-08-21','2023-09-03');

INSERT INTO a_r
VALUES (1,7,22),
(1,7,23),
(1,7,21),
(1,7,28),
(2,7,8),
(2,7,9),
(2,7,10),
(2,7,18),
(2,7,13),
(3,7,15),
(3,7,25),
(3,7,17),
(3,7,4),
(4,7,12),
(4,7,24),
(5,6,21),
(5,6,25),
(5,6,18),
(5,6,20),
(6,6,1),
(6,6,2),
(6,6,3),
(6,6,4),
(6,6,5),
(6,6,6),
(6,6,7),
(7,6,15),
(7,6,16),
(7,6,10),
(7,6,11),
(8,6,19),
(8,6,30);

-- D R O P  T A B L E
DROP TABLE persona CASCADE;
DROP TABLE alimento CASCADE;
DROP TABLE comida CASCADE;
DROP TABLE hist_comida CASCADE;
DROP TABLE a_r CASCADE;

-- D R O P  T A B L E
TRUNCATE TABLE persona CASCADE;
TRUNCATE TABLE alimento CASCADE;
TRUNCATE TABLE comida CASCADE;
TRUNCATE TABLE hist_comida CASCADE;
TRUNCATE TABLE a_r CASCADE;
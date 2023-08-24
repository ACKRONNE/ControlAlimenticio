CREATE TABLE receta(
    id_receta       numeric(3)      PRIMARY KEY,
    tipo            char(1)         NOT NULL        CHECK(tipo IN ('d','a','c','m'))
);

CREATE TABLE alimento(
    id_alimento     numeric(3)      PRIMARY KEY,
    tipo            varchar(12)     NOT NULL        CHECK(tipo IN ('proteina','carbohidrato','vegetal','grasa','fruta','bebida','otro')),
    nombre          varchar(30)     NOT NULL,
    cantidad        numeric(2)
);

CREATE TABLE persona(
    id_persona      numeric(3)      PRIMARY KEY,
    nombre          varchar(15)     NOT NULL,
    apellido        varchar(15)     NOT NULL,
    tipo            char(1)         NOT NULL        CHECK(tipo IN ('p','e')),
    sexo            char(1)         NOT NULL        CHECK(sexo IN ('m','f')),
    correo          text            NOT NULL        UNIQUE,
    direccion       text            NOT NULL,
    telefono        numeric(12)     NOT NULL,
    contraseña      text            NOT NULL,
    fecha_nac       date,
    especialidad    varchar(30),
    id_espe         numeric(3)      REFERENCES persona(id_persona)
);

CREATE TABLE hist_receta(
    id_receta       numeric(3)      NOT NULL,
    fecha_ini       date            NOT NULL,
    fecha_fin       date,
    CONSTRAINT pk_hist  PRIMARY KEY (id_receta,fecha_ini),
    CONSTRAINT fk_hr    FOREIGN KEY (id_receta)  REFERENCES  receta(id_receta)
);

CREATE TABLE det_comida(
    id_receta       numeric(3)      NOT NULL,
    id_cliente      numeric(3)      NOT NULL,   
    satisfaccion    varchar(11)     CHECK(satisfaccion IN ('super','bien','normal','no muy bien','mal','cansado')),
    comentario      text,
    CONSTRAINT pk_det   PRIMARY KEY (id_cliente,id_receta),
    CONSTRAINT fk_dr    FOREIGN KEY (id_receta)   REFERENCES  receta(id_receta),
    CONSTRAINT fk_dc    FOREIGN KEY (id_cliente)  REFERENCES  persona(id_persona)
);

CREATE TABLE a_r(
    id_receta       numeric(3)      NOT NULL,
    id_alimento     numeric(3)      NOT NULL,
    CONSTRAINT pk_ar    PRIMARY KEY (id_receta,id_alimento),
    CONSTRAINT fk_ar    FOREIGN KEY (id_receta)     REFERENCES  receta(id_receta),
    CONSTRAINT fk_aa    FOREIGN KEY (id_alimento)   REFERENCES  alimento(id_alimento)
);

-- I N S E R T S

INSERT INTO receta
VALUES (1,'d'),
    (2,'a'),
    (3,'c'),
    (4,'m'),
    (5,'d'),
    (6,'a'),
    (7,'c');

INSERT INTO persona
VALUES (1,'Juan','Perez','p','m','juan.perez@example.com','Calle 123, Ciudad',555-123-4567,'abc123456','1990-03-03','NULL',NULL),
       (2,'Maria','Lopez','e','f','maria.lopez@example.com','Avenida X, Pueblo',444-987-6543,'passw0rd','1990-03-03','nutricionista',NULL),
       (3,'Luis','Garcia','p','m','luis.garcia@example.com','Carretera Y, Villa',333-456-7890,'123qwe!@#','1990-03-03','NULL',NULL),
       (4,'Ana','Martinez','e','f','ana.martinez@example.com','Camino Z, Ciudad',222-789-1234,'mysecurepassword','1990-03-03','nutricionista',NULL),
       (5,'Carlos','Rodriguez','p','m','carlos.rodriguez@example.com','Plaza 456, Pueblo',666-321-0987,'password123','1990-03-03','NULL',NULL),
       (6,'Laura','Hernandez','e','f','laura.hernandez@example.com','Calle 789, Villa',777-987-6543,'securepass!@#','1990-03-03','nutricionista',NULL),
       (7,'Andres','Gomez','p','m','andres.gomez@example.com','Avenida 12, Ciudad',888-234-5678,'987poiuytr','1990-03-03','NULL',NULL),
       (8,'Paciente','Gomez','p','m','paciente@gmail.com','Avenida 12, Ciudad',888-234-5678,'1234','1990-03-03','NULL',NULL),
       (9,'Especialista','Gomez','e','f','especialista@gmail.com','Avenida 12, Ciudad',888-234-5678,'1234','1990-03-03','NULL',NULL);

INSERT INTO alimento
VALUES (1,'proteina','carne',1),
(2,'carbohidrato','papas',4),
(3,'vegetal','champiñones',4),
(4,'grasa','aceite de oliva',1),
(5,'fruta','piña',2),
(6,'bebida','limonada',1),
(7,'otro','helado',1);

INSERT INTO hist_receta
VALUES (1,'2023-07-15','2023-07-20'),
(2,'2023-06-10','2023-06-18'),
(3,'2023-08-01','2023-08-05'),
(4,'2023-04-22','2023-05-01'),
(5,'2023-03-15','2023-03-20'),
(6,'2023-07-01','2023-07-10'),
(7,'2023-08-20','2023-09-02');

INSERT INTO det_comida
VALUES (1,1,'super','Me siento comodo con la comida'),
       (2,3,'bien','no me encanto la combinacion de alimentos'),
       (3,5,'normal','esta ok'),
       (4,7,'no muy bien','no es mi comida favorita'),
       (5,1,'mal','estuvo pesima '),
       (6,3,'cansado','todo el tiempo lo mismo'),
       (7,5,'super','la combinacion estaba deliciosa');

INSERT INTO a_r
VALUES (1,1),
(1,2),
(1,3),
(2,1),
(2,2),
(2,3),
(2,4),
(3,2),
(3,3),
(4,7),
(5,5),
(5,3),
(6,1),
(6,2),
(6,3),
(6,4),
(6,5),
(7,1),
(7,2),
(7,3),
(7,4),
(7,5),
(7,6),
(7,7);


-- D R O P  T A B L E
DROP TABLE receta CASCADE;
DROP TABLE persona CASCADE;
DROP TABLE alimento CASCADE;
DROP TABLE hist_receta CASCADE;
DROP TABLE det_comida CASCADE;
DROP TABLE a_r CASCADE;

-- D R O P  T A B L E
TRUNCATE TABLE receta CASCADE;
TRUNCATE TABLE persona CASCADE;
TRUNCATE TABLE alimento CASCADE;
TRUNCATE TABLE hist_receta CASCADE;
TRUNCATE TABLE det_comida CASCADE;
TRUNCATE TABLE a_r CASCADE;
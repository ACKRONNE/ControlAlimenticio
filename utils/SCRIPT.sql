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
    telefono        numeric(12)     NOT NULL,
    contraseña      text            NOT NULL,
    fecha_nac       date,
    especialidad    varchar(30),
    id_espe         numeric(3)      REFERENCES persona(id_persona)
);

CREATE TABLE comida(
    id_comida       numeric(3)      NOT NULL,
    id_persona      numeric(3)      NOT NULL,   
    tipo            char(1)         NOT NULL        CHECK(tipo IN ('d','a','c','m'))
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
    CONSTRAINT fk_hr    FOREIGN KEY (id_comida)  REFERENCES  comida(id_comida),
    CONSTRAINT fk_hp    FOREIGN KEY (id_persona)  REFERENCES  persona(id_persona)
);

CREATE TABLE a_r(
    id_comida       numeric(3)      NOT NULL,
    id_persona      numeric(3)      NOT NULL,
    id_alimento     numeric(3)      NOT NULL,
    CONSTRAINT pk_ar    PRIMARY KEY (id_comida, id_persona, id_alimento),
    CONSTRAINT fk_ar    FOREIGN KEY (id_comida)     REFERENCES  comida(id_comida),
    CONSTRAINT fk_aa    FOREIGN KEY (id_alimento)   REFERENCES  alimento(id_alimento),
    CONSTRAINT fk_hp    FOREIGN KEY (id_persona)  REFERENCES  persona(id_persona)
);

-- I N S E R T S

INSERT INTO persona
VALUES (1,'Juan','Perez','p','m','juan.perez@example.com',555-123-4567,'1234',32935,'NULL',2),
       (2,'Maria','Lopez','e','f','maria.lopez@example.com',444-987-6543,'1234',34397,'nutricionista',2),
       (3,'Luis','Garcia','p','m','luis.garcia@example.com',333-456-7890,'1234',7370,'NULL',3),
       (4,'Ana','Martinez','e','f','ana.martinez@example.com',222-789-1234,'1234',29286,'nutricionista',4),
       (5,'Carlos','Rodriguez','p','m','carlos.rodriguez@example.com',666-321-0987,'1234',3719,'NULL',4),
       (6,'Leonel','Messi','e','f','especialista@gmail.com',777-987-6543,'1234',11025,'nutricionista',6),
       (7,'Kim','Kardashian','p','m','paciente@gmail.com',888-234-5678,'1234',36594,'NULL',6);

INSERT INTO alimento
VALUES (1,'proteina','carne',1),
(2,'carbohidrato','papas',4),
(3,'vegetal','champiñones',4),
(4,'grasa','aceite de oliva',1),
(5,'fruta','piña',2),
(6,'bebida','limonada',1),
(7,'otro','helado',1);

INSERT INTO hist_comida
VALUES (1,'2023-07-15','2023-07-20'),
       (2,'2023-06-10','2023-06-18'),
       (3,'2023-08-01','2023-08-05'),
       (4,'2023-04-22','2023-05-01'),
       (1,'2023-03-15','2023-03-20'),
       (2,'2023-07-01','2023-07-10'),
       (3,'2023-08-20','2023-09-02');

INSERT INTO comida
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
DROP TABLE persona CASCADE;
DROP TABLE alimento CASCADE;
DROP TABLE hist_comida CASCADE;
DROP TABLE comida CASCADE;
DROP TABLE a_r CASCADE;

-- D R O P  T A B L E
TRUNCATE TABLE persona CASCADE;
TRUNCATE TABLE alimento CASCADE;
TRUNCATE TABLE hist_comida CASCADE;
TRUNCATE TABLE comida CASCADE;
TRUNCATE TABLE a_r CASCADE;
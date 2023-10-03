-- Database: pokemon

-- DROP DATABASE pokemon;

CREATE DATABASE pokemon
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE pokemon
    IS 'Тестовое задание по REST API';
----------------------------------------------------------------------------------------------------------------	
-- Table: public.species

-- DROP TABLE public.species;

CREATE TABLE public.species
(
    pokemon_id integer NOT NULL,
    name character varying(40) COLLATE pg_catalog."default" NOT NULL,
    characteristic_eng character varying(500) COLLATE pg_catalog."default",
    characteristic_rus character varying(500) COLLATE pg_catalog."default",
    CONSTRAINT species_pkey PRIMARY KEY (pokemon_id)
);

ALTER TABLE public.species
    OWNER to postgres;

COMMENT ON COLUMN public.species.pokemon_id
    IS 'Идентификатор вида покемона';

COMMENT ON COLUMN public.species.name
    IS 'Название вида покемона';
	
COMMENT ON COLUMN public.species.characteristic_eng
    IS 'Характеристика вида покемона (на английском)';
	
COMMENT ON COLUMN public.species.characteristic_rus
    IS 'Характеристика вида покемона (на русском)';

		
-- Table: public.evolution

-- DROP TABLE public.evolution;

CREATE TABLE public.evolution
(
    pokemon_id  integer NOT NULL, 
    species_path  character varying(90) COLLATE pg_catalog."default" NOT NULL,
    parent_species_id integer,
    evolution_chain integer NOT NULL,
    CONSTRAINT evolution_pkey PRIMARY KEY (pokemon_id)
);

ALTER TABLE public.evolution
    ADD CONSTRAINT evolution_fk1 FOREIGN KEY (pokemon_id)
    REFERENCES public.species (pokemon_id) MATCH FULL
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE public.evolution
    OWNER to postgres;
	
COMMENT ON COLUMN public.evolution.pokemon_id
    IS 'Идентификатор вида покемона';

COMMENT ON COLUMN public.evolution.species_path
    IS 'Ссылка на вид покемона species. Данная ступень эволюции';
	
COMMENT ON COLUMN public.evolution.parent_species_id
    IS 'Идентификатор вида покемона Предыдущая ступень эволюции';

COMMENT ON COLUMN public.evolution.evolution_chain
    IS 'Идентификатор цепочки для группировки';
	
--------------------------------------------------------------------------------------------------------
---Функция чтения данных из БД


#Запро требуемых данных из БД

# изначально
#SELECT
#		t2.name as pokemon_name, t2.characteristic_rus as pokemon_characteristic_rus, t2.characteristic_eng as pokemon_characteristic_eng, t3.parent_name, t3.parent_characteristic_rus, t3.parent_characteristic_eng
#	FROM
#		species t2, (SELECT t1.pokemon_id, t2.pokemon_id as parent_id, t2.name as parent_name, t2.characteristic_rus as parent_characteristic_rus, t2.characteristic_eng as parent_characteristic_eng  FROM evolution t1 FULL JOIN species t2 ON t2.pokemon_id = t1.parent_species_id) t3
#	WHERE
#		t2.pokemon_id = t3.pokemon_id
#	;


# конечное	
SELECT
		t2.name as pokemon_name, 
		COALESCE (t2.characteristic_rus, t2.characteristic_eng, NULL) as pokemon_characteristic, t3.parent_name, COALESCE (t3.parent_characteristic_rus, t3.parent_characteristic_eng, NULL) as parent_characteristic
	FROM
		species t2, (SELECT t1.pokemon_id, t2.pokemon_id as parent_id, t2.name as parent_name, t2.characteristic_rus as parent_characteristic_rus, t2.characteristic_eng as parent_characteristic_eng  FROM evolution t1 FULL JOIN species t2 ON t2.pokemon_id = t1.parent_species_id) t3
	WHERE
		t2.pokemon_id = t3.pokemon_id
	;


# функция запроса требуемых данных с БД

# изначадьно
#CREATE OR REPLACE  FUNCTION data_about_pokemons()
#	RETURNS TABLE(pokemon_name character, pokemon_characteristic_rus character, pokemon_characteristic_eng character, parent_name character, parent_characteristic_rus character, parent_characteristic_eng character) AS
#$$
#	DECLARE
#	ls RECORD;
#BEGIN
#	FOR ls IN EXECUTE 'SELECT
#		t2.name as pokemon_name, t2.characteristic_rus as pokemon_characteristic_rus, t2.characteristic_eng as pokemon_characteristic_eng, t3.parent_name, t3.parent_characteristic_rus, t3.parent_characteristic_eng
#	FROM
#		species t2, (SELECT t1.pokemon_id, t2.pokemon_id as parent_id, t2.name as parent_name, t2.characteristic_rus as parent_characteristic_rus, t2.characteristic_eng as parent_characteristic_eng  FROM evolution t1 FULL JOIN species t2 ON t2.pokemon_id = t1.parent_species_id) t3
#	WHERE
#		t2.pokemon_id = t3.pokemon_id'
#	LOOP
#		pokemon_name = ls.pokemon_name;
#		pokemon_characteristic_rus = ls.pokemon_characteristic_rus;
#		pokemon_characteristic_eng = ls.pokemon_characteristic_eng;
#		parent_name = ls.parent_name;
#		parent_characteristic_rus = ls.parent_characteristic_rus;
#		parent_characteristic_eng = ls.parent_characteristic_eng;	
#		RETURN next;
#	END LOOP;
#END;
#$$
#LANGUAGE 'plpgsql' VOLATILE;


# конечное
CREATE OR REPLACE  FUNCTION data_about_pokemons()
	RETURNS TABLE(pokemon_name character, pokemon_characteristic character, parent_name character, parent_characteristic character) AS
$$
	DECLARE
	ls RECORD;
BEGIN
	FOR ls IN EXECUTE 'SELECT
		t2.name as pokemon_name, 
		COALESCE (t2.characteristic_rus, t2.characteristic_eng, NULL) as pokemon_characteristic, t3.parent_name, COALESCE (t3.parent_characteristic_rus, t3.parent_characteristic_eng, NULL) as parent_characteristic
	FROM
		species t2, (SELECT t1.pokemon_id, t2.pokemon_id as parent_id, t2.name as parent_name, t2.characteristic_rus as parent_characteristic_rus, t2.characteristic_eng as parent_characteristic_eng  FROM evolution t1 FULL JOIN species t2 ON t2.pokemon_id = t1.parent_species_id) t3
	WHERE
		t2.pokemon_id = t3.pokemon_id
	;'
	LOOP
		pokemon_name = ls.pokemon_name;
		pokemon_characteristic = ls.pokemon_characteristic;
		parent_name = ls.parent_name;
		parent_characteristic= ls.parent_characteristic;
		RETURN next;
	END LOOP;
END;
$$
LANGUAGE 'plpgsql' VOLATILE;

# запуск функция запроса требуемых данных с БД
SELECT * FROM data_about_pokemons();


# запуск функция запроса требуемых данных с БД и сохранение данных в файле pokemonsData.csv
C:\Program Files\PostgreSQL\15\bin>psql -U postgres -d pokemon -c "\COPY (select * from data_about_pokemons()) TO 'C:\New\pokemonsData.csv' CSV HEADER DELIMITER ',';"




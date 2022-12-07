query_create_basic_data = """
Create table basic_data_1
(
	id		INT NOT NULL auto_increment,
    serial VARCHAR(100) not null,
    name	VARCHAR(100),
    species VARCHAR(100),
    weight INT unsigned not null default 0,
    height INT unsigned not null default 0,
    primary key (id),
    unique key serial_unique (serial),
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NOT NULL DEFAULT current_timestamp
) ENGINE = InnoDB;
"""

query_create_ability = """
create table ability_1
(
	id		INT NOT NULL auto_increment,
    serial	VARCHAR(100) not null,
    name	VARCHAR(100),
    ability VARCHAR(100) not null,
    slot INT,
    ability_order INT,
    created_at timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp NOT NULL DEFAULT current_timestamp,
    primary key (id)
) ENGINE = InnoDB;
"""

query_inject_basic_data = """
    INSERT INTO basic_data_1 (name,serial,species,weight,height)
    values (%(name)s,%(serial)s,%(species)s,%(weight)s,%(height)s)
"""

query_inject_ability = """
    INSERT INTO ability_1 (name,serial,ability,slot,ability_order)
    values (%(name)s,%(serial)s,%(ability)s,%(slot)s,%(ability_order)s)
"""

query_ability = """
    Select * from ability_1 where ability = "%(delete_ability)s";
"""

query_temp_table_pokedex = """
with pokedex as (Select 
	bd.name, 
    bd.serial, 
    skill_1.ability as ability_1, 
    skill_2.ability as ability_2, 
    skill_3.ability as ability_3,
    bd.species,
    bd.weight,
    bd.height
from basic_data_1 bd 
left join 
	ability_1 skill_1 
    on bd.serial = skill_1.serial 
    and skill_1.ability_order = 1 
left join 
	ability_1 skill_2 
    on bd.serial = skill_2.serial 
    and skill_2.ability_order = 2 
left join 
	ability_1 skill_3 
	on bd.serial = skill_3.serial 
    and skill_3.ability_order = 3 )
select * from pokedex
"""

query_ability_1 = f"""
{query_temp_table_pokedex} where ability_1 is not null and ability_2 is null;
"""

query_ability_2 = f"""
{query_temp_table_pokedex} where ability_2 is not null and ability_3 is null;
"""

query_ability_3 = f"""
{query_temp_table_pokedex} where ability_3 is not null;
"""

query_rank_ability_asc = f"""
{query_temp_table_pokedex} order by ability_2 IS NULL asc,ability_3 IS NULL asc
"""
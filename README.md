# pokemon
Scripting exercise to consume pokeapi

## How to Run in Local 
### Prerequisites
1. Python installed (>= 3.7)
2. `pip` (or `pip3`), `virtualenv` installed
3. Clone this repo
4. Run `virtualenv .` => this will create python virtual env in that directory (so it doesn't messed up with other python environment, if you have any others)
6. Run `source bin/activate` => activate newly created virtual env on macOs user. If you Windows user, Run `Scripts\activate.bat`
7. Install required lib => `pip3 install -r requirements.txt`

### Migrate Data to MySQL
1. Make sure you have already mysql server. Then the config you'll change on config.py
2. Then create table basic_data_1 and ability_1. Open query.py, copy query create table to CLI / IDE your mysql server, then running the query
3. Run `python migrate_to_mysql.py`

### Step by Step
1. Run `python main.py -p` to get all pokedex data within suitable columns with acceptance criteria
2. Use `-f args` or `--filtering args` to specify the default filtering on pokedex data (args: ability_1, ability_2, ability_3, rank_ability_asc)
3. Use `-c args` or `--custom args` to get pokedex data with specify where condition. Plis user (ex: "serial='pidgeot18' limit 1")
4. Use `-d ability_name` or `--delete-ability ability_name` to delete the ability for all pokemon on pokedex
5. Use `-i "new_ability|'pokemon1','pokemon2',..'pokemon-n'"` or `--insert-ability "new_ability|'pokemon1','pokemon2',..'pokemon-n'` to insert new ability to several pokemon. Don't forget to use same command format
6. for filtering & custom command, csv file will be generated to "output" folder
7. After you finish, run `deactivate` to terminate the virtualenv

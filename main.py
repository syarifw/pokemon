import argparse
from config import *
from query import *
import pandas as pd
from mysql.connector import connect,Error
import arrow

CURRENT_DATETIME = arrow.utcnow().to('Asia/Jakarta').strftime("%d-%m-%Y %H%M%S")

# Create the parses
my_parser = argparse.ArgumentParser(prog='main.py',
                                    usage='%(prog)s -p',
                                    description='Run CLI of pokedex script')

# Add the arguments
my_parser.add_argument('-p','--pokedex', action='store_true')
my_parser.add_argument('-f','--filtering', action='store',
                        type=str)
my_parser.add_argument('-c','--custom', action='store',
                        type=str)
my_parser.add_argument('-d','--delete-ability', action='store',
                        type=str)
my_parser.add_argument('-i','--insert-ability', action='store',
                        type=str)

# Execute the parse_args() method
args = my_parser.parse_args()
pokedex = args.pokedex
filtering = args.filtering
custom = args.custom
delete_ability = args.delete_ability
insert_ability = args.insert_ability

output_columns = [
    "name",
    "serial",
    "ability_1",
    "ability_2",
    "ability_3",
    "species",
    "weight",
    "height"
]
ability_columns = [
    "id",
    "serial",
    "name",
    "ability",
    "slot",
    "ability_order",
    "created_at",
    "updated_at"
]
pd.set_option('display.width',None)

def query_pokedex(query,add_filename):
    my_cursor = my_db.cursor()
    my_cursor.execute(query)
    result = my_cursor.fetchall()

    data_df = pd.DataFrame(result,columns=output_columns)
    output_file_path = f'output/pokedex-{add_filename}-{CURRENT_DATETIME}.csv'
    data_df.to_csv(output_file_path,sep=',',index=False,encoding='utf-8')
    print(data_df)
    print(f"file {output_file_path} already created on output folder")

if args.pokedex:
    try:
        my_db = connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
    except Error as e:
        print("Something went wrong: {}".format(e))

    if args.filtering:
        if filtering == "ability_1":
            query_pokedex(query_ability_1,filtering)
        elif filtering == "ability_2":
            query_pokedex(query_ability_2,filtering)
        elif filtering == "ability_3":
            query_pokedex(query_ability_3,filtering)
        elif filtering == "rank_ability_asc":
            query_pokedex(query_rank_ability_asc,filtering)

    elif args.custom:
        query_pokedex(query_temp_table_pokedex+" where "+custom,custom)

    elif args.delete_ability:

        # Get All Pokemon Had delete_ability
        my_cursor = my_db.cursor()
        my_cursor.execute(f"Select * from ability_1 where ability in ('{delete_ability}') limit 1;")
        get_all_pokemon_had_ability = my_cursor.fetchall()
        pokemon_had_ability = pd.DataFrame(get_all_pokemon_had_ability,columns=ability_columns)
        print(pokemon_had_ability)

        for index,row in pokemon_had_ability.iterrows():
            
            # Get list of pokemon's ability which need to delete_ability
            serial = row["serial"]
            my_cursor.execute(f"Select COUNT(serial) as counter from ability_1 where serial = '{serial}';")
            result = my_cursor.fetchall()
            count_df = pd.DataFrame(result,columns=["counter"])
            print("Total ability: ",count_df["counter"][0])

            # Check is ability_order have same value with Total of pokemon's ability
            if row["ability_order"] != count_df["counter"][0]:
                
                # Get list of pokemon's ability which don't need to be delete
                my_cursor.execute(f"Select * from ability_1 where serial = '{serial}' and not ability_order = '{row['ability_order']}'")
                result = my_cursor.fetchall()
                update_df = pd.DataFrame(result,columns=ability_columns)
                print(update_df)
                for index,row_1 in update_df.iterrows():

                    # Construct data of list of pokemon's ability that need to update ability_order
                    update_ability_order = row_1['ability_order']
                    # if ability_order == 1, skip updating process.
                    if update_ability_order > 1:
                        new_ability_order = update_ability_order-1
                    else:
                        continue
                    update_ability = row_1['ability']
                    update_serial = row_1['serial']
                    print(f"UPDATE ability_1 set ability_order = {new_ability_order},updated_at = NOW() where serial = '{update_serial}' and ability = '{update_ability}'")
                    my_cursor.execute(f"UPDATE ability_1 set ability_order = {new_ability_order},updated_at = NOW() where serial = '{update_serial}' and ability = '{update_ability}'")
                    my_db.commit()
                
                # Execute delete_ability
                my_cursor.execute(f"DELETE from ability_1 where serial = '{serial}' and ability = '{delete_ability}' and ability_order = {row['ability_order']}")
                my_db.commit()
                
                print(f"record {serial} & {delete_ability} already deleted.")

            else:
                # Execute delete_ability without update ability_order cause the pokemon's ability are in the last sequence
                my_cursor.execute(f"DELETE from ability_1 where serial = '{serial}' and ability = '{delete_ability}' and ability_order = {row['ability_order']}")
                my_db.commit()
                print(f"record {serial} & {delete_ability} already deleted.")

    elif args.insert_ability:
        my_cursor = my_db.cursor()

        # Split argument to ability and serials
        new_ability,serials = insert_ability.split("|",1)
        serials = list(serials.split(','))

        for index_serial_insert in serials:

            # Get counter of serial and name of pokemon on ability_1 table
            my_cursor.execute(f"Select distinct COUNT(serial) as counter, name from ability_1 where serial in ({index_serial_insert})")
            count_ability = my_cursor.fetchall()

            # Construct to dataframe
            count_ability_df = pd.DataFrame(count_ability,columns=["counter","name"])

            # Get value of name & ability_order for newest injected ability
            injected_name = count_ability_df['name'][0]
            injected_ability_order = count_ability_df['counter'][0]+1

            #Inject to ability_1
            my_cursor.execute(f"INSERT INTO ability_1 (name,serial,ability,slot,ability_order) values ('{injected_name}',{index_serial_insert},'{new_ability}',0,{injected_ability_order}) ")
            my_db.commit()
            print(f"{index_serial_insert} with {new_ability} already injected.")

    else:
        query_pokedex(query_temp_table_pokedex,"")
    my_db.close()

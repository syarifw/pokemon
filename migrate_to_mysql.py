from mysql.connector import connect,Error
from config import *
from query import *

import requests

url_get_pokemon_list = "https://pokeapi.co/api/v2/pokemon/?limit=2000&offset=0"

response_pokemon_list = requests.get(url_get_pokemon_list).json()
# n=0
list_pokemon = response_pokemon_list["results"]
for index in list_pokemon:
    # if n <= 0:
    get_detail_pokemon = requests.get(index["url"]).json()

    #Inject to MySQL
    retry_count = 0
    retry_status = True
    while retry_status and retry_count < 3:
        try:
            mydb = connect(
                host=host,
                user=username,
                password=password,
                database=database
            )
            serial = get_detail_pokemon["name"]+str(get_detail_pokemon["id"])
            mycursor = mydb.cursor()

            # Inject to basic_data
            mycursor.execute(query_inject_basic_data,{
                'name':get_detail_pokemon["name"],
                'serial':serial,
                'species':get_detail_pokemon["species"]["name"],
                'weight':get_detail_pokemon["weight"],
                'height':get_detail_pokemon["height"]})
            ability_order = 1
            for index_1 in get_detail_pokemon["abilities"]:
                #Inject to ability
                mycursor.execute(query_inject_ability,{
                'name':get_detail_pokemon["name"],
                'serial':serial,
                'ability':index_1["ability"]["name"],
                'slot':index_1['slot'],
                'ability_order':ability_order})
                ability_order+=1
            # myresult = mycursor.fetchall()
            # print(myresult)
            print(f"{serial} with name: already injected")
            retry_status = False
        except Error as e:
            mydb.rollback()
            print(f"Failed to inject data: {e}")
            retry_count += 1
        finally:
            mydb.commit()
            if mydb.is_connected():
                mydb.close()
            # n+=1
print("MySQL Connection is closed.")


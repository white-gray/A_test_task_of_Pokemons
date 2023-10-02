from BD_Postgress import BD_Postgress
from ReadPokemon import ReadPokemon

# определение количества покемонов
url = "https://pokeapi.co/api/v2/pokemon-species"
pokemons = ReadPokemon().pokemonGET(url)
theNumberOfPokemons = pokemons['count']



# рассмотрение каждого покемона, и сбор нужных данных
for pokemonNumber in range(1,theNumberOfPokemons+1):
    print("читается покемон ", pokemonNumber)
    url = "https://pokeapi.co/api/v2/pokemon-species/"+str(pokemonNumber)
    # print("\n---------------------------------------------------------------------------------\nread from ", url)
    pokemonData = ReadPokemon().pokemonGET(url)

    pokemon_id = pokemonNumber
    # print("\tpokemon_id = ", pokemon_id)

    name = pokemonData['name']
    # print("\tего имя: ", name)

    species_path = url

    characteristicEng = ""
    # characteristicEng = "characteristicEng" + str(pokemonNumber) # использовалось при тестировании
    for charchacteristics in pokemonData['flavor_text_entries']:
        if not "en" in charchacteristics.get('language').get('name'):
            # print("----------------------------------------------", charchacteristics.get('language').get('name'))
            continue
        characteristicEng += charchacteristics.get('flavor_text', " ")
    characteristicEng = characteristicEng.replace('\n', ' | ') #замена переноса строк на разделители для экономии места на экране при отображении инфо
    characteristicEng = characteristicEng.replace('\'', '') #удалени кавычек
    characteristicEng = characteristicEng.replace('\"', '') #удалени кавычек
    characteristicEng = characteristicEng.replace('é', 'e') # во избежание SQL ОШИБКА:  для символа с последовательностью байт 0xc3 0xa9 из кодировки "UTF8" нет эквивалента в "WIN1251"
    if len(characteristicEng) > 499:                        # от разработчика API ограничение на 500 символов при переводе
        characteristicEng = characteristicEng[:499]
    characteristicRus = ReadPokemon().pokemonTranslate(characteristicEng).get('responseData').get('translatedText')
    # characteristicRus = "characteristicRus" + str(pokemonNumber) # использовалось при тестировании
    if characteristicRus == "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY. NEXT AVAILABLE IN  10 HOURS 24 MINUTES 13 SECONDS VISIT HTTPS:\/\/MYMEMORY.TRANSLATED.NET\/DOC\/USAGELIMITS.PHP TO TRANSLATE MORE":
        characteristicRus = "у переводчика нерабочее время"
    if len(characteristicRus) > 499:                        # от разработчика API ограничение на 500 символов при переводе
        characteristicRus = characteristicRus[:499]
    # print("\t==============  characteristicEng=\n\t\t\t",characteristicEng, "\n\t======================\n")
    # print("\t==============  characteristicRus=\n\t\t\t",characteristicRus, "\n\t======================\n")

    if pokemonData['evolves_from_species']:
        parent_species_ids = pokemonData['evolves_from_species'].get('url').split('/')
        # print("\n\tFrom ", pokemonData['evolves_from_species'].get('url'))
        parent_species_id = parent_species_ids[-2]
    else:
        parent_species_id="NULL"
        # print("\n\tFrom parent_species_id=\"\"")


    # print("\tparent_species_id: ", parent_species_id)

    evolution_chains = pokemonData['evolution_chain'].get('url').split('/')
    # print("\n\tFrom ", pokemonData['evolution_chain'].get('url'))
    evolution_chain= evolution_chains[-2]
    # print("\t\t\tevolution_chain: ", evolution_chain)


    # print("длина characteristicEng = ", len(characteristicEng))
    # print("длина characteristicRus = ", len(characteristicRus))

    print("заливка в БД полученных данных")  # использовалось при тестировании
    #заливка в БД полученных данных
    insertData = str(pokemon_id) + ", '" + name + "', '" + characteristicEng + "', '" + characteristicRus + "'"
    # print("insertData = ", insertData)
    BD_Postgress().insert('species',"pokemon_id, name, characteristic_eng, characteristic_rus",insertData)

    # print("\tparent_species_id: ", parent_species_id)

    insertData = str(pokemon_id) + ", '" + species_path + "', " + str(parent_species_id) + ", " + evolution_chain
    # print("insertData = ", insertData)
    BD_Postgress().insert('evolution', "pokemon_id, species_path, parent_species_id, evolution_chain",insertData)








#
# print(f"Состав БД teble evolution: ")
# for i in BD_Postgress().selectAll('evolution'):
#     print("\t", i[0])
#
# print(f"Состав БД teble species: ")
# for i in BD_Postgress().selectAll('species'):
#     print("\t", i)
#
# print(f"Состав строки из БД teble species: ")
# for i in BD_Postgress().select('species', "id", 4):
#     print("\t", i)
#
#





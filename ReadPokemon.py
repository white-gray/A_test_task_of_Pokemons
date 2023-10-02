import json
import urllib3


class ReadPokemon:

    # def __init__(self,url):
    #     self.url = url


    def readGET(self, url):
        http = urllib3.PoolManager()
        try:
            response = http.request('GET', url)
            data = json.loads(response.data.decode('utf-8'))
            # print("\n_____\n\t","loaded date from BD pokemon:- ", data,"\n")
        except IOError as io:
            print("\n!!!!!\n\tERROR при чтении данных с сайта\n")

        finally:
            return data


    def readTranslate(self, text):
        http = urllib3.PoolManager()
        url = "https://api.mymemory.translated.net/get?q="+text+"&langpair=en|ru"
        # print("urlTranslate = ", url)
        try:
            response = http.request('GET', url)
            data = json.loads(response.data.decode('utf-8'))
            # print("\n_____\n\t","loaded date from BD pokemon:- ", data,"\n")
        except IOError as io:
            print("\n!!!!!\n\tERROR при чтении данных с сайта\n", io)

        finally:
            return data


    def pokemonGET(self, url):
        return ReadPokemon().readGET(url)

    def pokemonTranslate(self, text):
        return ReadPokemon().readTranslate(text)

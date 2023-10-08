import sys
from sys import argv
import datetime
from pathlib import Path
import os



# проверка, что при запуске скрипта не было введено слишком много параметров
if len(argv) > 2:
    sys.exit('\nОжидается только один аргумент: путь папки в которую выложить информацию о покемонах. \n\tЭто может быть '
          'путь с именем диска (C:/Pokemons), или путь относительно той папки, где сейчас находится скрипт (путь '
          'должен начиниться со знака . )'
          '\n\tПри отсутствии аргумента, файл с  информацией о покемонах будет выложен в ту '
          'папку, откуда запускается данный скрипт\n')

# если при запустке скрипта на было введено параметров (в качестве папки размещения отчета принимается текущай папка из которой запущен скрипт)
elif len(argv) == 1:
    filepath = ""

# если при запустке скрипта параметром была указана папка, здесь она определяется
else:
    try:
        filepath = argv[1]
        if not Path(filepath).exists():  # определение возможных ошибок при написании пути файла
            sys.exit("Данной папки не существует") # выход. т.к. указали неверное имя папки
        filePathList = filepath.split(":")
        if len(filePathList) > 1 and not filePathList[1]:
            sys.exit("При указании коння диска надо закончить символом \"\\\"")  # выход, т.к. указали не полное имя диска
        else:
            filepath = Path(filepath)
    except OSError:
        sys.exit("Ошибка в пути файла!")  # выход, т.к. указали неверный путь к файлу

# создание имени файла
filename = "Покемоны " + datetime.datetime.now().strftime("%d.%m.%Y %H_%M_%S") + ".csv"
# определение имени файла и пути
fullFileName = Path(filepath, filename)
# print("fullFileName = ", fullFileName)

# определени пути в файле psql
if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "linux3":
    # предполагается что там по-умолчанию расшарена папка м PostgreSQL. Не проверял.
    psqlPath = ""
elif sys.platform == "darwin":
    # предполагается что там по-умолчанию расшарена папка м PostgreSQL. Не проверял.
    psqlPath = ""
elif sys.platform == "win32":
    # проверяется в какой папке расположен psql, и запоминается путь
    # изначально предполагается что PostgreSQL расположен станлартно в папке c:\Program Files\PostgreSQL\версия\
    # опредеояется какая версия PostgreSQL установлена
    try:
        with os.scandir("c:\\Program Files\\PostgreSQL\\") as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    psqlPath = Path("C:\\","Progra~1","PostgreSQL",entry.name,"bin", "psql")
                    # print("entry.name = ", entry.name) # использовалось при написании приложения
                    # print("psqlPath = ", psqlPath)  # использовалось при написании приложения
    except FileNotFoundError:
        psqlPath = input("PostgreSQL не найден в обычном месте. Укажите папку в которой расположен файл psql.exe")
        if not psqlPath:
            print("сработает если у вас установлен PostgreSQL и папка с файлом psql.exe прописана в PATH" )
            psqlPath = ""
    except:
        print("неучтенная ошибка: ")
        sys.exit(1)

print("psqlPath = ", psqlPath)  # использовалось при написании приложения
command = str(psqlPath) + " -U postgres -d pokemon -c \"\\COPY (select * from data_about_pokemons()) TO '" + str(fullFileName) + "' CSV HEADER DELIMITER ',';\""
# чтение данных из таблицы и выгрухка файла с данными по покемонам
# print("command = ", command)
print("Данные по покемонам записаны в файл ", str(fullFileName))
os.system(command)
import psycopg2


from config import host, user, password, db_name, port



class BD_Postgress:

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        # port=port
    )
    connection.autocommit = True

    def select(self, table, colon, cell):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * from %s WHERE %s=%s;" % (table, colon, cell)
                )
                return{cursor.fetchone()}
        except IOError as io:
            print("\n!!!!!\n\tERROR to DB def select\n", io)
        # finally:
        #     print('fin')
        #     self.EndConnect(cursor)

    def selectAll(self, table):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * from %s ;" % (table)
                )
                return {cursor.fetchone()}
        except IOError as io:
            print("\n!!!!!\n\tERROR to DB def select\n")
        # finally:
        #     print('fin')
        #     self.EndConnect(cursor)

    def insert(self, table, colons, insertData):
        try:
            with self.connection.cursor() as cursor:
                # print("insertDataInBD = ", insertData)
                cursor.execute(
                    "INSERT INTO %s(%s) VALUES(%s);" % (table, colons, insertData)
                )
        except IOError as io:
            print("\n!!!!!\n\tERROR to DB def insert\n", io)
        # finally:
        #     self.EndConnect(cursor)

    # def EndConnect(self, cursor):
    #     if self.connection:
    #         cursor.close()
    #         self.connection.close()
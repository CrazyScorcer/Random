import sqlite3

connection = sqlite3.connect("practice.db")
cursor = connection.cursor()
while True:
    userInput = input("Input Command: ").upper()
    match userInput:
        case("EXIT"):
            break
        case("CREATE TABLE"):
            try:
                tableName = input("Input table name: ")
                # Get User input for amount of columns wanted in table
                while True:
                    try:
                        columnAmount = int(input("Input total number of columns: "))
                        if columnAmount < 0:
                            raise ValueError
                        break
                    except ValueError:
                        print("Invalid Input. Try Again.")
                # Contructs command string that will be execute to create table with columns
                columnCommandList = []
                for x in range(columnAmount):
                    currentColumnNumber = x+1
                    columnCreate = input(f"Input Column {currentColumnNumber} Name and Type:")
                    columnCommandList.append(columnCreate)
                columnCommand = ", ".join(columnCommandList)
                cursor.execute(f"CREATE TABLE {tableName} ({columnCommand})")
                connection.commit()
                print("Successfully Created Table")
            except Exception as e:
                print(e)
                print("Failed To Create Table")
        case("DELETE TABLE"):
            try:
                tableName = input("Input Table Name: ")
                cursor.execute(f"DROP TABLE {tableName}")
                connection.commit()
                print("Succesfully Deleted Table")
            except Exception as e:
                print(e)
                print("Failed To Delete Table")
        case("INSERT"):
            try:
                tableName = input("Input Table Name: ")
                pragma = cursor.execute(f"PRAGMA table_info({tableName})").fetchall()
                columnNum = 0
                for column in pragma:
                    columnNum += 1
                    print(f"Column {columnNum}: {list(column)[1]} {list(column)[2]}")
                columnValues = []
                sanitizerList = []
                for x in range(columnNum):
                    currentColumnNumber = x+1
                    #columninput = input(f"Input Column {currentColumnNumber} Value: ")
                    columnValues.append(input(f"Input Column {currentColumnNumber} Value: "))
                    sanitizerList.append("?")
                sanitizer = ",".join(sanitizerList)
                sanitizerTuple = sanitizer
                cursor.execute(f"INSERT INTO {tableName} VALUES({sanitizerTuple})",(tuple(columnValues)))
                connection.commit()
            except Exception as e:
                print(e)
                print("Failed to Insert Element")
        case _:
            print("Invalid Command")


connection.close()
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
                columnCommand = ""
                for x in range(columnAmount):
                    currentColumnNumber = x+1
                    columnCreate = input(f"Input column {currentColumnNumber} name and type:")
                    if x == 0:
                        columnCommand += columnCreate
                    else:
                        columnCommand += f", {columnCreate}"
                tableCreateCommand = f"CREATE TABLE {tableName} ({columnCommand})"
                print(tableCreateCommand)
                cursor.execute(tableCreateCommand)
                connection.commit()
                print("Successfully created table")
            except:
                print("Failed to create table")
        case("DELETE TABLE"):
            try:
                tableName = input("Input table name: ")
                cursor.execute(f"DROP TABLE {tableName}")
                print("Succesfully deleted table")
            except:
                print("Faild to delete table")
        case("INSERT"):
            #try:
                tableName = input("Input table name: ")
                pragma = cursor.execute(f"PRAGMA table_info({tableName})").fetchall()
                columnNum = 1
                for column in pragma:
                    print(f"Column {columnNum}: {list(column)[1]} {list(column)[2]}")
                    columnNum += 1
                
            #except:
                print("Failed to ")
        case _:
            print("Invalid Command")

connection.commit()
connection.close()
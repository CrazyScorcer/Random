import sqlite3
###Functions###
# Checks if Table already Exists in DB
def tableExists(tableName):
    return len(cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'").fetchall()) != 0
# Prints out Column Name and Type
def queryTableColumnInfo(tableName):
    pragma = cursor.execute(f"PRAGMA table_info({tableName})").fetchall()
    columnNum = 0
    #Prints out Column's Name and Type
    for column in pragma:
        columnNum += 1
        print(f"Column {columnNum}: {list(column)[1]} {list(column)[2]}")
    return columnNum
# Removes anything that isn't a Letter or a Number
def scrubInput(input):
    return ''.join(chr for chr in input if chr.isalnum())
def printMainCommands():
    print("""Commands:
        EXIT: Exit program
        CREATE TABLE: Create new table in Database
        DROP TABLE: DROP existing table from Database
        INSERT: Insert element into table
        DELETE: Delete element from table
        QUERY: Prints out info based on User Filters
        COMMANDS: Print out viable commands""")
###Main Program###
connection = sqlite3.connect("practice.db")
cursor = connection.cursor()
printMainCommands()
while True:
    userInput = input("Input Command: ").upper()
    match userInput:
        case("EXIT"):
            break
        case("CREATE TABLE"):
            try:
                tableName = scrubInput(input("Input table name: "))
                if(tableExists(tableName)):
                    print(f"{tableName} Already Exists")
                    continue
                # Get User Input for amount of columns wanted in table
                while True:
                    try:
                        columnAmount = int(input("Input total number of columns: "))
                        if columnAmount <= 0:
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
        case("DROP TABLE"):
            try:
                tableName = scrubInput(input("Input Table Name: "))
                if(not tableExists(tableName)):
                    print(f"{tableName} Doesn't Exists")
                    continue
                cursor.execute(f"DROP TABLE {tableName}")
                connection.commit()
                print("Succesfully Dropped Table")
            except Exception as e:
                print(e)
                print("Failed To Drop Table")
        case("INSERT"):
            try:
                tableName = scrubInput(input("Input Table Name: "))
                if(not tableExists(tableName)):
                    print(f"{tableName} Doesn't Exists")
                    continue
                columnNum = queryTableColumnInfo(tableName)
                columnValues = []
                sanitizerList = []
                for x in range(columnNum):
                    currentColumnNumber = x+1
                    columnValues.append(input(f"Input Column {currentColumnNumber} Value: "))
                    sanitizerList.append("?")
                sanitizer = ",".join(sanitizerList) # Contains "?" of Column Total for sanitization
                cursor.execute(f"INSERT INTO {tableName} VALUES({sanitizer})",tuple(columnValues))
                connection.commit()
                print(f"Successfully Inserted Element into {tableName}")
            except Exception as e:
                print(e)
                print("Failed to Insert Element")
        case("DELETE"):
            try:
                tableName = scrubInput(input("Input Table Name: "))
                if(not tableExists(tableName)):
                    print(f"{tableName} Doesn't Exists")
                    continue
                columnName = scrubInput(input("Input Column Name:"))
                elementName = input("Input Element Value:")
                cursor.execute(f"DELETE FROM {tableName} WHERE {columnName}=?", (elementName))
                connection.commit()              
            except Exception as e:
                print(e)
                print("Failed to Delete Element")
        case("QUERY"):
            try:
                tableName = scrubInput(input("Input Table Name: "))
                if(not tableExists(tableName)):
                    print(f"{tableName} Doesn't Exists")
                    continue

                columnNum = queryTableColumnInfo(tableName)
                columnName = scrubInput(input("Input Column Name: "))
                elementName = input("Input Element Name in Column: ")
                query = cursor.execute(f"SELECT * FROM {tableName} WHERE {columnName}=?", (elementName,)).fetchall()
                query = list(query[0])
                pragma = cursor.execute(f"PRAGMA table_info({tableName})").fetchall()
                columnHeaders = []
                for column in pragma:
                    columnHeaders.append(list(column)[1])    
                format_row = "{:>12}" * (len(columnHeaders)+ 1)
                print(format_row.format("", *columnHeaders))
                print(format_row.format("", *query))
                #for data in query:
                #    print(format_row.format(data))
            except Exception as e:
                print(e)
                print("Failed to Query")
        case("COMMANDS"):
            printMainCommands()
        case _:
            print("Invalid Command")

connection.close()

  

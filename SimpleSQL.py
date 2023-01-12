import sqlite3
import sys
###Functions###
# Checks if Table already Exists in DB
def tableExists(tableName):
    return len(cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'").fetchall()) != 0
# Prints out Column Name and Type; Return value mainly only used in Drop Table
def queryTableColumnInfo(tableName):
    pragma = cursor.execute(f"PRAGMA table_info({tableName})").fetchall()
    columnNum = 0
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
        ALTER: Add/Drop/Rename Columns in table
        EDIT: Change value of element
        QUERY: Prints out info based on User Filters
        COMMANDS: Print out viable commands""")
def printColumnCommands():
    print("""Commands:
        ADD: Add a new column to a table
        DROP: Drop a column from a table
        RENAME: Rename column
        COMMANDS: Print out valid commnads
        BACK: Return to Main""")
###Main Program###
connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()
while True:
    printMainCommands()
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
                cursor.execute(f"DELETE FROM {tableName} WHERE {columnName}=?", (elementName,))
                connection.commit()              
            except Exception as e:
                print(e)
                print("Failed to Delete Element")
        case("ALTER"):
            tableName = scrubInput(input("Input Table Name: "))
            if(not tableExists(tableName)):
                print(f"{tableName} Doesn't Exists")
                continue
            columnAmount = queryTableColumnInfo(tableName)
            columnName = scrubInput(input("Input Column Name: "))
            userInput = input("Input Command: ").upper()
            while True:
                printColumnCommands()
                match userInput:
                    case("ADD"):
                        try:
                            cursor.execute(f"ALTER TABLE {tableName} ADD {columnName}")
                        except Exception as e:
                            print(e)
                            print(f"Failed to add {columnName} to {tableName}")
                    case("DROP"):
                        try:
                            cursor.execute(f"ALTER TABLE {tableName} DROP COLUMN {columnName}")
                        except Exception as e:
                            print(e)
                            print(f"Failed to remove {columnName} from {tableName}")
                    case("RENAME"):
                        newColumnName = scrubInput(input("Input new Column Name: "))
                        try:
                            cursor.execute(f"ALETER TABLE {tableName} RENAME COLUMN {columnName} to {newColumnName}")
                        except Exception as e:
                            print(e)
                            print(f"Failed to change {columnName} to {newColumnName} in {tableName}")
                    case("COMMANDS"):
                        printColumnCommands()
                    case("BACK"):  
                        break
                    case _:
                        print("Invalid Command")
            connection.commit()
        case("EDIT"):
            try:
                tableName = scrubInput(input("Input Table Name: "))
                if(not tableExists(tableName)):
                    print(f"{tableName} Doesn't Exists")
                    continue

                columnNum = queryTableColumnInfo(tableName)
                columnFilterName = scrubInput(input("Input Filter Column Name: "))
                elementFilterName = input("Input Filter Element: ")
                userColumnInput = scrubInput(input("Input Column Name: "))
                userValueInput = input("Input New Value: ")
                cursor.execute(f"UPDATE {tableName} SET {userColumnInput} = ? WHERE {columnFilterName} = ?", (userValueInput,elementFilterName))
                connection.commit()
            except Exception as e:
                print(e)
                print("Failed to Edit Element")
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
                pragma = cursor.execute(f"PRAGMA table_info({tableName})").fetchall()
                columnHeaders = []
                for column in pragma:
                    columnHeaders.append(list(column)[1])
                format_row = "{:>12}" * (len(columnHeaders)+ 1)
                print(format_row.format("", *columnHeaders))
                for element in list(query):
                    print(format_row.format("", *element))
            except Exception as e:
                print(e)
                print("Failed to Query")
        case("COMMANDS"):
            printMainCommands()
        case _:
            print("Invalid Command")

connection.close()

  

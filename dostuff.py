import sqlite3

connection = sqlite3.connect("practice.db")
cursor = connection.cursor()
while True:
    userInput = input("Input Command: ").upper()

    if(userInput == "EXIT"):
        break
    cursor.execute("CREATE TABLE")

connection.commit()
connection.close()
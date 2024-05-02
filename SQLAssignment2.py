#*******Important Message*******
#Hi Evaluation Team,
#Please save the mbox.txt file at "D:" for proper execution of this code.

import sqlite3

FileName = str(input("Enter file name: "))  #Enter only file name
FileName = "D:/"+FileName   #Concatenate the path with the filename i.e. D:/
DomainNameDict = {}         #Take and empty Dictionary to save the domain names and their counts

with open(FileName,"r") as FileHandler:
#Open file for reading. This code does not require to close the file explicitly.
    for line in FileHandler:
        if line.startswith("From"):
        #*****Check if the line starts with "From". It ensures there is a domain name present in the line.
            i = 0
            length = len(line)
            DomainName = ""
            while i<length and line[i]!="\n":
                if line[i] == "@":
                #*****If line contains "@", move to the next character and keep taking next character until there is a space. This helps in cleaning the junk words and symbols and extracts only the required domain name.
                    i+=1
                    ch = line[i]
                    while i<length-1 and (ch!=" "):
                        DomainName = DomainName + ch
                        i+=1
                        ch = line[i]
                i+=1
            if DomainName in DomainNameDict:
            #If domain name is already present, add 1 to its count else create new one with initial count 1
                DomainNameDict[DomainName]+=1
            else:
                DomainNameDict[DomainName] = 1

print("\n\nDictionary Created.\n\n")
print(DomainNameDict)
print("\n\nSaving to Database...\n\n")

#*****Save the data to the Database*****

db = sqlite3.connect(":memory:")

cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS COUNTS(
ORG VARCHAR(50),
COUNT INTEGER
)''')

cursor.execute("DELETE FROM COUNTS")

for key in DomainNameDict:
    cursor.execute("INSERT INTO COUNTS(ORG,COUNT) VALUES(\"" + key + "\"," + str(DomainNameDict[key]) + ")")

cursor.execute("SELECT * FROM COUNTS")
#Fetch all rows from the result set
rows = cursor.fetchall()
#Print each row
for row in rows:
    print(row[0]," ",row[1])

db.commit()
db.close()
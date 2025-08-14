import sqlite3

connection = sqlite3.connect("academy.db")
cur = connection.cursor()

def createDB():
    connection = sqlite3.connect("academy.db")

def createTable():
    connection = sqlite3.connect("academy.db")
    cur.execute(
        """
        CREATE TABLE Invoice(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        status INT NOT NULL, 
        paid_at DATE NULLABLE,
        due_date DATE NOT NULL,
        FOREIGN KEY (id) REFERENCES InvoiceStatus(id)

        )
        """
        )
def deleteTable():
    cur.execute("DROP TABLE User")

def insertRow():
    cur.execute("INSERT INTO InvoiceStatus (id, status) VALUES (1, 'paid'), (2, 'open'), (3, 'uncollectible'), (4, 'void')")

    connection.commit() 

# cur.execute("DROP TABLE SubscriptionStatus")
res = cur.execute("SELECT * FROM Invoice")

print(res.description)
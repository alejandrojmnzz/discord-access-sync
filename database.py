import sqlite3

connection = sqlite3.connect("academy.db")
cur = connection.cursor()

def createDB():
    connection = sqlite3.connect("academy.db")

def createInvoiceTable():
    connection = sqlite3.connect("academy.db")
    cur.execute(
        """
        CREATE TABLE Invoice(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        status TEXT NOT NULL, 
        paid_at DATE NULLABLE,
        due_date DATE NOT NULL,
        FOREIGN KEY (status) REFERENCES InvoiceStatus(status)

        )
        """
        )

def createUserTable():
    connection = sqlite3.connect("academy.db")
    cur.execute(
        """
        CREATE TABLE User(
        id INT PRIMARY KEY,
        email TEXT NOT NULL,
        first_name TEXT NOT NULL, 
        last_name TEXT NOT NULL,
        discord_user_id TEXT DATE NOT NULL

        )
        """
        )
def createProfileTable():
    connection = sqlite3.connect("academy.db")
    cur.execute(
        """
        CREATE TABLE ProfileAcademy(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        academy_id INT NOT NULL, 
        FOREIGN KEY (user_id) REFERENCES User(id)
        )
        """
        )

        
def deleteTable():
    cur.execute("DROP TABLE Invoice")

def insertUserRow():
    cur.execute("""INSERT INTO User VALUES 
    (1, 'alejandro@gmail.com', 'Alejandro', 'Jiménez', 1379943138247839985),
    (2, 'miguel@gmail.com', 'Miguel', 'Gonzáles', 1390720076671357112),
    (3, 'javier@gmail.com', 'Javier', 'García', 1350129598943465513)
    """)
    connection.commit() 

def insertProfileRow():
    cur.execute("""INSERT INTO ProfileAcademy VALUES
    (1, 1, 30), (2, 2, 42), (3, 3, 42)
    """)
    connection.commit() 


def insertCohortRow():
    cur.execute("""INSERT INTO CohortUser VALUES 
    (1, 1, 36, 'postponed', 'financial_hold'),
    (2, 2, 48, 'higher_education', 'income_statement'),
    (3, 3, 23, 'secondary', 'balance_sheet')
    """)
    connection.commit() 

def insertSubscriptionRow():
    cur.execute("""INSERT INTO Subscription VALUES 
    (1, 1, 'canceled'),
    (2, 2, 'active'),
    (3, 3, 'past_due')
    """)
    connection.commit() 

def insertInvoiceRow():
    cur.execute("""INSERT INTO Invoice VALUES 
    (1, 1, 'uncollectible', null, '2025-07-30'),
    (2, 2, 'paid', '2025-07-12', '2025-07-30'), (3, 2, 'paid', '2025-08-04', '2025-08-30'), 
    (4, 3, 'paid', '2025-08-04', '2025-08-20'), (5, 3, 'open', null, '2025-08-13')
    """)
    connection.commit() 



# cur.execute("DROP TABLE SubscriptionStatus")
res = cur.execute("SELECT * FROM Invoice")


print(res.fetchall())

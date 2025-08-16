import sqlite3

# Se realiza una conexión a la base de datos creada y se crea un cursor de esa conexión para manejar consultas SQL
connection = sqlite3.connect("academy.db")
cur = connection.cursor()

# El resto de funciones encontradas en este archivo, son funciones que no se ejecutan nunca al correr la aplicación
# Estas funciones solo se utilizaron una vez de manera manual para crear la base de datos, crear tablas e insertar datos en ellas
# Sin embargo, son útiles como documentación para visualizar el modelo de cada una de las tablas y los datos que hay dentro de cada una

def createDB():
    connection = sqlite3.connect("academy.db")

def createUserTable():
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

def createCohortTable():
    cur.execute(
        """
        CREATE TABLE CohortUser(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        cohort_id INT NOT NULL, 
        educational_status TEXT NOT NULL,
        financial_status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(id)

        )
        """
        )

def createSubscriptionStatusTable():
    cur.execute("""
    CREATE TABLE SubscriptionStatus (
    id INT PRIMARY KEY,
    status VARCHAR(50) UNIQUE NOT NULL
    )
    """
    )

def createSubscriptionTable():
    cur.execute(
        """
        CREATE TABLE CohortUser(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        status TEXT NOT NULL, 
        FOREIGN KEY (status) REFERENCES InvoiceStatus(status),
        FOREIGN KEY (user_id) REFERENCES User(id)
        )
        """
        )

def createInvoiceStatusTable():
    cur.execute("""
    CREATE TABLE InvoiceStatus (
    id INT PRIMARY KEY,
    status_name VARCHAR(50) UNIQUE NOT NULL
    )
    """
    )

def createInvoiceTable():
    cur.execute(
        """
        CREATE TABLE Invoice(
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        status TEXT NOT NULL, 
        paid_at DATE NULLABLE,
        due_date DATE NOT NULL,
        FOREIGN KEY (status) REFERENCES InvoiceStatus(status),
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

def insertSubscriptionStatusRow():
    cur.execute("""INSERT INTO SubscriptionStatus (id, status) VALUES
    (1, 'active'),
    (2, 'trialing'),
    (3, 'past_due'),
    (4, 'canceled'),
    (5, 'paused'),
    (6, 'expired'),
    (7, 'unpaid')
    """)

def insertSubscriptionRow():
    cur.execute("""INSERT INTO Subscription VALUES 
    (1, 1, 'canceled'),
    (2, 2, 'active'),
    (3, 3, 'past_due')
    """)
    connection.commit() 

def insertInvoiceStatusRow():
    cur.execute("""INSERT INTO InvoiceStatus (id, status) VALUES
    (1, 'paid'),
    (2, 'open'),
    (3, 'uncollectible'),
    (4, 'void');
    """)

def insertInvoiceRow():
    cur.execute("""INSERT INTO Invoice VALUES 
    (1, 1, 'uncollectible', null, '2025-07-30'),
    (2, 2, 'paid', '2025-07-12', '2025-07-30'), (3, 2, 'paid', '2025-08-04', '2025-08-30'), 
    (4, 3, 'paid', '2025-07-04', '2025-07-30'), (5, 3, 'open', null, '2025-08-13')
    """)
    connection.commit() 
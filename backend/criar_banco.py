import sqlite3

def criar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marcas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pais TEXT NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS miniaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            escala TEXT NOT NULL,
            preco REAL NOT NULL,
            marca_id INTEGER NOT NULL,
            FOREIGN KEY (marca_id) REFERENCES marcas(id)
        )
    """)


    cursor.execute("INSERT INTO marcas (nome, pais) VALUES ('Hot Wheels', 'EUA')")
    cursor.execute("INSERT INTO marcas (nome, pais) VALUES ('Kyosho', 'Japão')")

    cursor.execute("""
        INSERT INTO miniaturas (modelo, escala, preco, marca_id) 
        VALUES ('Nissan GT-R R35', '1:64', 29.90, 1)
    """)
    cursor.execute("""
        INSERT INTO miniaturas (modelo, escala, preco, marca_id) 
        VALUES ('Ferrari F40', '1:18', 450.00, 2)
    """)

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_banco()

from app import app, db, Marca, Miniatura

with app.app_context():
    # cria todas as tabelas dos modelos, se ainda nao existirem
    db.create_all()

    # so popula se o banco estiver vazio
    if Marca.query.first() is None:
        hot_wheels = Marca(nome="Hot Wheels", pais="EUA")
        kyosho = Marca(nome="Kyosho", pais="Japão")

        db.session.add(hot_wheels)
        db.session.add(kyosho)
        db.session.commit()

        db.session.add(Miniatura(
            modelo="Nissan GT-R R35",
            escala="1:64",
            preco=29.90,
            marca_id=hot_wheels.id
        ))

        db.session.add(Miniatura(
            modelo="Ferrari F40",
            escala="1:18",
            preco=450.00,
            marca_id=kyosho.id
        ))

        db.session.commit()

    print("Banco criado com sucesso.")

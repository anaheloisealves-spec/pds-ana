from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Marca(db.Model):
    __tablename__ = "marcas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)

    miniaturas = db.relationship("Miniatura", backref="marca")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "pais": self.pais
        }


class Miniatura(db.Model):
    __tablename__ = "miniaturas"

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    escala = db.Column(db.String(20), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    marca_id = db.Column(
        db.Integer,
        db.ForeignKey("marcas.id"),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "modelo": self.modelo,
            "escala": self.escala,
            "preco": self.preco,
            "marca_id": self.marca_id,
            "marca_nome": self.marca.nome
        }


@app.route("/miniaturas", methods=["GET"])
def listar_miniaturas():
    marca_id = request.args.get("marca_id")

    if marca_id is not None:
        try:
            marca_id = int(marca_id)
        except (TypeError, ValueError):
            return jsonify({"erro": "marca_id invalido"}), 400

        miniaturas = Miniatura.query.filter_by(marca_id=marca_id).all()
    else:
        miniaturas = Miniatura.query.all()

    return jsonify([miniatura.to_dict() for miniatura in miniaturas]), 200


@app.route("/miniaturas/<int:miniatura_id>", methods=["GET"])
def buscar_miniatura(miniatura_id):
    miniatura = db.session.get(Miniatura, miniatura_id)

    if miniatura is None:
        return jsonify({"erro": "Miniatura nao encontrada"}), 404

    return jsonify(miniatura.to_dict()), 200


@app.route("/miniaturas", methods=["POST"])
def cadastrar_miniatura():
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["modelo", "escala", "preco", "marca_id"]
    if any(campo not in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe modelo, escala, preco e marca_id"}), 400

    marca = db.session.get(Marca, dados["marca_id"])

    if marca is None:
        return jsonify({"erro": "Marca nao encontrada"}), 404

    nova_miniatura = Miniatura(
        modelo=dados["modelo"],
        escala=dados["escala"],
        preco=dados["preco"],
        marca_id=marca.id
    )

    db.session.add(nova_miniatura)
    db.session.commit()

    resposta = {
        "id": nova_miniatura.id,
        "modelo": nova_miniatura.modelo,
        "escala": nova_miniatura.escala,
        "preco": nova_miniatura.preco,
        "marca_id": nova_miniatura.marca_id
    }

    return jsonify(resposta), 201


@app.route("/miniaturas/<int:miniatura_id>", methods=["PUT"])
def atualizar_miniatura(miniatura_id):
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["modelo", "escala", "preco", "marca_id"]
    if any(campo not in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe modelo, escala, preco e marca_id"}), 400

    miniatura = db.session.get(Miniatura, miniatura_id)

    if miniatura is None:
        return jsonify({"erro": "Miniatura nao encontrada"}), 404

    marca = db.session.get(Marca, dados["marca_id"])

    if marca is None:
        return jsonify({"erro": "Marca nao encontrada"}), 404

    miniatura.modelo = dados["modelo"]
    miniatura.escala = dados["escala"]
    miniatura.preco = dados["preco"]
    miniatura.marca_id = marca.id

    db.session.commit()

    resposta = {
        "id": miniatura.id,
        "modelo": miniatura.modelo,
        "escala": miniatura.escala,
        "preco": miniatura.preco,
        "marca_id": miniatura.marca_id
    }

    return jsonify(resposta), 200


@app.route("/miniaturas/<int:miniatura_id>", methods=["DELETE"])
def deletar_miniatura(miniatura_id):
    miniatura = db.session.get(Miniatura, miniatura_id)

    if miniatura is None:
        return jsonify({"erro": "Miniatura nao encontrada"}), 404

    db.session.delete(miniatura)
    db.session.commit()

    return jsonify({"mensagem": "Miniatura removida com sucesso"}), 200


@app.route("/marcas/<int:marca_id>", methods=["GET"])
def buscar_marca(marca_id):
    marca = db.session.get(Marca, marca_id)

    if marca is None:
        return jsonify({"erro": "Marca nao encontrada"}), 404

    dados = marca.to_dict()

    if request.args.get("miniaturas", "").lower() in ("1", "true", "sim"):
        dados["miniaturas"] = [miniatura.to_dict() for miniatura in marca.miniaturas]

    return jsonify(dados), 200


@app.route("/marcas/<int:marca_id>/miniaturas", methods=["GET"])
def listar_miniaturas_da_marca(marca_id):
    marca = db.session.get(Marca, marca_id)

    if marca is None:
        return jsonify({"erro": "Marca nao encontrada"}), 404

    return jsonify([miniatura.to_dict() for miniatura in marca.miniaturas]), 200


if __name__ == "__main__":
    app.run(debug=True)

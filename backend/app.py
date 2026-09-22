from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("banco.db")

@app.route("/miniaturas", methods=["GET"])
def listar_miniaturas():
    marca_id = request.args.get("marca_id")
    
    conexao = conectar()
    cursor = conexao.cursor()
    
    query = """
        SELECT miniaturas.id, miniaturas.modelo, miniaturas.escala, 
               miniaturas.preco, miniaturas.marca_id, marcas.nome
        FROM miniaturas
        INNER JOIN marcas ON miniaturas.marca_id = marcas.id
    """
    
    if marca_id is not None:
        query += " WHERE miniaturas.marca_id = ?"
        cursor.execute(query, (marca_id,))
    else:
        cursor.execute(query)
        
    linhas = cursor.fetchall()
    conexao.close()
    
    miniaturas = []
    for linha in linhas:
        miniaturas.append({
            "id": linha[0],
            "modelo": linha[1],
            "escala": linha[2],
            "preco": linha[3],
            "marca_id": linha[4],
            "marca_nome": linha[5]
        })
        
    return jsonify(miniaturas), 200

@app.route("/miniaturas/<int:miniatura_id>", methods=["GET"])
def buscar_miniatura(miniatura_id):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT miniaturas.id, miniaturas.modelo, miniaturas.escala, 
               miniaturas.preco, miniaturas.marca_id, marcas.nome
        FROM miniaturas
        INNER JOIN marcas ON miniaturas.marca_id = marcas.id
        WHERE miniaturas.id = ?
    """, (miniatura_id,))
    
    linha = cursor.fetchone()
    conexao.close()
    
    if linha is None:
        return jsonify({"erro": "Miniatura nao encontrada"}), 404
        
    miniatura = {
        "id": linha[0],
        "modelo": linha[1],
        "escala": linha[2],
        "preco": linha[3],
        "marca_id": linha[4],
        "marca_nome": linha[5]
    }
    
    return jsonify(miniatura), 200

@app.route("/miniaturas", methods=["POST"])
def cadastrar_miniatura():
    dados = request.get_json()
    
    campos_obrigatorios = ["modelo", "escala", "preco", "marca_id"]
    if not dados or any(campo not in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe modelo, escala, preco e marca_id"}), 400
        
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute(
        "INSERT INTO miniaturas (modelo, escala, preco, marca_id) VALUES (?, ?, ?, ?)",
        (dados["modelo"], dados["escala"], dados["preco"], dados["marca_id"])
    )
    conexao.commit()
    
    novo_id = cursor.lastrowid
    conexao.close()
    
    resposta = {
        "id": novo_id,
        "modelo": dados["modelo"],
        "escala": dados["escala"],
        "preco": dados["preco"],
        "marca_id": dados["marca_id"]
    }
    
    return jsonify(resposta), 201

@app.route("/miniaturas/<int:miniatura_id>", methods=["PUT"])
def atualizar_miniatura(miniatura_id):
    dados = request.get_json()
    
    campos_obrigatorios = ["modelo", "escala", "preco", "marca_id"]
    if not dados or any(campo not in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe modelo, escala, preco e marca_id"}), 400
        
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute(
        "UPDATE miniaturas SET modelo = ?, escala = ?, preco = ?, marca_id = ? WHERE id = ?",
        (dados["modelo"], dados["escala"], dados["preco"], dados["marca_id"], miniatura_id)
    )
    conexao.commit()
    
    if cursor.rowcount == 0:
        conexao.close()
        return jsonify({"erro": "Miniatura nao encontrada"}), 404
        
    conexao.close()
    
    resposta = {
        "id": miniatura_id,
        "modelo": dados["modelo"],
        "escala": dados["escala"],
        "preco": dados["preco"],
        "marca_id": dados["marca_id"]
    }
    
    return jsonify(resposta), 200

@app.route("/miniaturas/<int:miniatura_id>", methods=["DELETE"])
def deletar_miniatura(miniatura_id):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("DELETE FROM miniaturas WHERE id = ?", (miniatura_id,))
    conexao.commit()
    
    if cursor.rowcount == 0:
        conexao.close()
        return jsonify({"erro": "Miniatura nao encontrada"}), 404
        
    conexao.close()
    
    return jsonify({"mensagem": "Miniatura removida com sucesso"}), 200

if __name__ == "__main__":
    app.run(debug=True)

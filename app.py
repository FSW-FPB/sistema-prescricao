from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['clinica']

# Endpoint para criar uma nova prescrição
@app.route('/prescricoes', methods=['POST'])
def criar_prescricao():
    dados = request.json
    dados['id'] = str(ObjectId())  # Gera um ID único
    db.prescricoes.insert_one(dados)

    # Convertendo o ID gerado em string para o retorno
    dados['_id'] = dados['id']
    return jsonify(dados), 201

# Endpoint para obter todas as prescrições
@app.route('/prescricoes', methods=['GET'])
def obter_prescricoes():
    prescricoes = list(db.prescricoes.find())
    for prescricao in prescricoes:
        prescricao['_id'] = str(prescricao['_id'])  # Converter ObjectId para string
    return jsonify(prescricoes), 200

# Endpoint para obter uma prescrição específica
@app.route('/prescricoes/<id>', methods=['GET'])
def obter_prescricao(id):
    prescricao = db.prescricoes.find_one({"id": id})
    if prescricao:
        prescricao['_id'] = str(prescricao['_id'])  # Converter ObjectId para string
        return jsonify(prescricao), 200
    return jsonify({'error': 'Prescrição não encontrada'}), 404

# Endpoint para atualizar uma prescrição existente
@app.route('/prescricoes/<id>', methods=['PUT'])
def atualizar_prescricao(id):
    dados = request.json
    resultado = db.prescricoes.update_one({"id": id}, {"$set": dados})
    if resultado.matched_count > 0:
        return jsonify({'message': 'Prescrição atualizada com sucesso'}), 200
    return jsonify({'error': 'Prescrição não encontrada'}), 404

# Endpoint para deletar uma prescrição
@app.route('/prescricoes/<id>', methods=['DELETE'])
def deletar_prescricao(id):
    resultado = db.prescricoes.delete_one({"id": id})
    if resultado.deleted_count > 0:
        return jsonify({'message': 'Prescrição deletada com sucesso'}), 200
    return jsonify({'error': 'Prescrição não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)

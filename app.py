from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import csv
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['clinica']

@app.route('/prescricoes', methods=['POST'])
def criar_prescricao():
    dados = request.json
    medicamentos = dados.get('medicamentos', [])

    # Verifica se os campos obrigatórios estão presentes
    if not all(key in dados for key in ("paciente_id", "medico_id", "medicamentos")):
        return jsonify({'error': 'Campos obrigatórios: paciente_id, medico_id e medicamentos'}), 400

    # A data e hora atual no momento em que a requisição é recebida
    dados['data_prescricao'] = datetime.utcnow().isoformat()  # Usando UTC para garantir uniformidade

    # Adiciona informações detalhadas de cada medicamento
    medicamentos_detalhados = []
    for med in medicamentos:
        nome_medicamento = med.get("nome")
        if nome_medicamento:
            # Busca o medicamento no arquivo CSV pelo nome
            dados_medicamento = consultar_medicamento(nome_medicamento)
            if "error" in dados_medicamento:
                return jsonify({'error': dados_medicamento["error"]}), 404
            # Agora o 'nome' vai dentro de 'informacoes_medicamento'
            med['informacoes_medicamento'] = dados_medicamento
            # Removendo o campo 'nome' da raiz do medicamento
            del med['nome']
            medicamentos_detalhados.append(med)

    dados['medicamentos'] = medicamentos_detalhados

    # Insere um ID único para a prescrição
    dados['_id'] = ObjectId()  # Gera automaticamente um ID
    db.prescricoes.insert_one(dados)

    # Converte o ID gerado em string para o retorno
    dados['_id'] = str(dados['_id'])
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
    try:
        # Converte o id recebido para ObjectId
        prescricao = db.prescricoes.find_one({"_id": ObjectId(id)})
        if prescricao:
            prescricao['_id'] = str(prescricao['_id'])  # Converter ObjectId para string
            return jsonify(prescricao), 200
        return jsonify({'error': 'Prescrição não encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para atualizar parcialmente uma prescrição
@app.route('/prescricoes/<prescricao_id>', methods=['PATCH'])
def atualizar_prescricao(prescricao_id):
    dados = request.json

    # Cria um dicionário com os campos que podem ser atualizados
    campos_para_atualizar = {}

    # Verifica se o campo 'paciente_id' foi fornecido
    if 'paciente_id' in dados:
        campos_para_atualizar['paciente_id'] = dados['paciente_id']

    # Verifica se o campo 'medicamentos' foi fornecido
    if 'medicamentos' in dados:
        medicamentos_detalhados = []
        for med in dados['medicamentos']:
            nome_medicamento = med.get("nome")
            if nome_medicamento:
                # Consulta o medicamento no arquivo CSV
                dados_medicamento = consultar_medicamento(nome_medicamento)
                if "error" in dados_medicamento:
                    return jsonify({'error': dados_medicamento["error"]}), 404
                # Agora o 'nome' vai dentro de 'informacoes_medicamento'
                med['informacoes_medicamento'] = dados_medicamento
                # Removendo o campo 'nome' da raiz do medicamento
                del med['nome']
                medicamentos_detalhados.append(med)
        campos_para_atualizar['medicamentos'] = medicamentos_detalhados

    # Se nenhum campo válido for fornecido para atualização, retorna um erro
    if not campos_para_atualizar:
        return jsonify({'error': 'Nenhum campo para atualizar fornecido'}), 400

    # Realiza a atualização no banco de dados
    resultado = db.prescricoes.update_one(
        {"_id": ObjectId(prescricao_id)},  # Filtro pela ID da prescrição
        {"$set": campos_para_atualizar}  # Atualiza apenas os campos fornecidos
    )

    # Verifica se a prescrição foi encontrada e atualizada
    if resultado.matched_count == 0:
        return jsonify({'error': 'Prescrição não encontrada'}), 404

    return jsonify({'message': 'Prescrição atualizada com sucesso'}), 200

# Endpoint para deletar uma prescrição
@app.route('/prescricoes/<prescricao_id>', methods=['DELETE'])
def deletar_prescricao(prescricao_id):
    # Tenta excluir a prescrição com o ID fornecido
    resultado = db.prescricoes.delete_one({"_id": ObjectId(prescricao_id)})

    # Verifica se algum documento foi excluído
    if resultado.deleted_count == 0:
        return jsonify({'error': 'Prescrição não encontrada'}), 404

    return jsonify({'message': 'Prescrição deletada com sucesso'}), 200


@app.route('/medicamentos', methods=['GET'])
def get_all_medicamentos():
    medicamentos = []
    try:
        with open('medicamentos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                nome_medicamento = row[1].strip().upper()
                tipo_medicamento = row[7].strip() if row[7].strip() else "Tipo não disponível"
                medicamentos.append({
                    "nome": nome_medicamento,
                    "tipo": tipo_medicamento
                })
        return jsonify(medicamentos), 200
    except FileNotFoundError:
        return jsonify({"error": "Arquivo medicamentos.csv não encontrado"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Função para consultar medicamentos diretamente no arquivo CSV
def consultar_medicamento(nome):
    try:
        with open('medicamentos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                # O nome do medicamento está na segunda coluna (index 1)
                nome_medicamento = row[1].strip().upper()  # Remove espaços e ignora case sensitivity
                # O tipo do medicamento está na oitava coluna (index 7)
                tipo_medicamento = row[7].strip()

                # Comparando o nome fornecido com o nome do medicamento no CSV
                if nome_medicamento == nome.upper():
                    return {
                        "nome": nome_medicamento,
                        "tipo": tipo_medicamento if tipo_medicamento else "Tipo não disponível"
                    }
        return {"error": "Medicamento não encontrado"}
    except FileNotFoundError:
        return {"error": "Arquivo medicamentos.csv não encontrado"}
    except Exception as e:
        return {"error": str(e)}


@app.route('/medicamentos/busca', methods=['GET'])
def buscar_medicamento_por_nome():
    nome = request.args.get('search')  # Obtém o parâmetro 'search' da query string

    if not nome:
        return jsonify({'error': 'Parâmetro "search" é obrigatório'}), 400

    try:
        medicamentos_encontrados = []
        with open('medicamentos.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                nome_medicamento = row[1].strip().upper()  # Nome do medicamento
                tipo_medicamento = row[7].strip()  # Tipo do medicamento

                # Verifica se o nome buscado é um fragmento do nome do medicamento
                if nome.upper() in nome_medicamento:
                    medicamentos_encontrados.append({
                        "nome": nome_medicamento,
                        "tipo": tipo_medicamento if tipo_medicamento else "Tipo não disponível"
                    })

        # Se não encontrar nenhum medicamento, retorna erro
        if not medicamentos_encontrados:
            return jsonify({'error': 'Nenhum medicamento encontrado com esse nome'}), 404

        return jsonify(medicamentos_encontrados), 200

    except FileNotFoundError:
        return jsonify({"error": "Arquivo medicamentos.csv não encontrado"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

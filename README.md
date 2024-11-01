
# API de Prescrição Médica

Este projeto define uma API para gerenciar prescrições médicas em uma clínica. Utiliza o framework Flask para criar endpoints HTTP que permitem a criação e recuperação de prescrições, além de interagir com o MongoDB para armazenamento dos dados.

## Tecnologias Utilizadas
- **Flask**: Framework web para criação da API.
- **pymongo**: Biblioteca para interação com o banco de dados MongoDB.
- **bson**: Biblioteca para manipulação de objetos do MongoDB, como o `ObjectId`.

## Configuração Inicial

1. Certifique-se de que o MongoDB está instalado e em execução em `localhost` na porta `27017`.
2. Instale as dependências do projeto:
   ```bash
   pip install flask pymongo bson
   ```

3. Execute o servidor Flask:
   ```bash
   python app.py
   ```

A API estará disponível em `http://localhost:5000`.

## Endpoints

### `POST /prescricoes`
- **Descrição**: Cria uma nova prescrição médica com os dados fornecidos no corpo da requisição.
- **Requisição**:
  - Formato: JSON
  - Campos esperados: Variável, de acordo com as informações de uma prescrição.
- **Resposta**:
  - Retorna um JSON com os dados da prescrição criada, incluindo o `id` gerado.

### `GET /prescricoes`
- **Descrição**: Recupera todas as prescrições armazenadas no banco de dados.
- **Resposta**:
  - Retorna uma lista de prescrições em formato JSON, cada uma contendo as informações detalhadas.

### `GET /prescricoes/<id>`
- **Descrição**: Recupera uma prescrição específica com base no `id` fornecido na URL.
- **Parâmetros**:
  - `id`: String representando o identificador único da prescrição.
- **Resposta**:
  - Retorna um JSON com os dados da prescrição solicitada ou um erro se o `id` não for encontrado.

## Exemplo de Uso

### Criar uma nova prescrição
```bash
 http://localhost:5000/prescricoes
```

### Recuperar todas as prescrições
```bash
 http://localhost:5000/prescricoes
```

### Recuperar uma prescrição específica
```bash
http://localhost:5000/prescricoes/<id>
```

---

Este README cobre as principais funcionalidades e exemplos de uso para a API de prescrição médica.

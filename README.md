
# API de Prescrição Médica

Este projeto define uma API para gerenciar prescrições médicas em uma clínica. Utiliza o framework Flask para criar endpoints HTTP que permitem a criação, atualização, recuperação e exclusão de prescrições, além de interagir com o MongoDB para armazenamento dos dados. A API também permite consultar medicamentos a partir de um arquivo CSV.

## Tecnologias Utilizadas
- **Flask**: Framework web para criação da API.
- **pymongo**: Biblioteca para interação com o banco de dados MongoDB.
- **bson**: Biblioteca para manipulação de objetos do MongoDB, como o `ObjectId`.
- **csv**: Para manipulação e leitura de arquivos CSV que contêm dados sobre medicamentos.
- **datetime**: Para manipulação de data e hora.

## Configuração Inicial

1. Certifique-se de que o MongoDB está instalado e em execução em `localhost` na porta `27017`.
2. Instale as dependências do projeto:
   ```bash
   pip install flask pymongo bson
   ```

3. Prepare o arquivo `medicamentos.csv` com os dados dos medicamentos na mesma pasta do projeto.
4. Execute o servidor Flask:
   ```bash
   python app.py
   ```

A API estará disponível em `http://localhost:5000`.

## Endpoints

### `POST /prescricoes`
- **Descrição**: Cria uma nova prescrição médica com os dados fornecidos no corpo da requisição.
- **Requisição**:
  - Formato: JSON
  - Campos esperados:
    - `paciente_id`: ID do paciente.
    - `medico_id`: ID do médico.
    - `medicamentos`: Lista de medicamentos prescritos (com nome e outros dados).
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

### `PATCH /prescricoes/<prescricao_id>`
- **Descrição**: Atualiza parcialmente uma prescrição existente com base no `prescricao_id`.
- **Requisição**:
  - Formato: JSON
  - Campos esperados:
    - `paciente_id`: ID do paciente (opcional).
    - `medicamentos`: Lista de medicamentos a ser atualizada (opcional).
- **Resposta**:
  - Retorna uma mensagem indicando se a atualização foi bem-sucedida ou se a prescrição não foi encontrada.

### `DELETE /prescricoes/<prescricao_id>`
- **Descrição**: Exclui uma prescrição existente com base no `prescricao_id`.
- **Resposta**:
  - Retorna uma mensagem indicando se a prescrição foi excluída com sucesso ou se não foi encontrada.

### `GET /medicamentos`
- **Descrição**: Recupera todos os medicamentos disponíveis no arquivo `medicamentos.csv`.
- **Resposta**:
  - Retorna uma lista de medicamentos em formato JSON.

### `GET /medicamentos/busca`
- **Descrição**: Busca medicamentos no arquivo `medicamentos.csv` com base em um nome fornecido na query string.
- **Parâmetros**:
  - `search`: Nome do medicamento ou parte dele.
- **Resposta**:
  - Retorna uma lista de medicamentos encontrados que correspondem ao nome fornecido.

## Exemplo de Uso

### Criar uma nova prescrição
```bash
POST http://localhost:5000/prescricoes
Content-Type: application/json
{
  "paciente_id": 1,
  "medico_id": 1,
  "doenca": "Dor de cabeça",
  "CID": "C70",
  "medicamentos": [
    {
      "nome": "DORALGINA", 
      "dosagem": "50mg", 
      "frequencia": "a cada 24 horas"
    },
    {
      "nome": "DORALGINA DIPCAF", 
      "dosagem": "25mg", 
      "frequencia": "a cada 16 horas"
    }
  ]
}
```

### Recuperar todas as prescrições
```bash
GET http://localhost:5000/prescricoes
```

### Recuperar uma prescrição específica
```bash
GET http://localhost:5000/prescricoes/<id>
```

### Atualizar uma prescrição existente
```bash
PATCH http://localhost:5000/prescricoes/<prescricao_id>
Content-Type: application/json
{
  "paciente_id": 1,
  "medico_id": 1,
  "doenca": "CÓLERA",
  "CID": "A00",
  "medicamentos": [
    {
      "nome": "PARACETAMOL", 
      "dosagem": "500mg", 
      "frequencia": "a cada 8 horas"
    },
    {
      "nome": "DIPIRONA", 
      "dosagem": "25ml", 
      "frequencia": "a cada 12 horas"
    }
  ]
}
```

### Excluir uma prescrição existente
```bash
DELETE http://localhost:5000/prescricoes/<prescricao_id>
```

### Buscar todos os medicamentos
```bash
GET http://localhost:5000/medicamentos
```

### Buscar medicamentos por nome
```bash
GET http://localhost:5000/medicamentos/busca?search=Paracetamol
```

## Membros do Projeto

| Nome            | Foto                                                                                                                   | Perfil                                             |
|-----------------|------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| **DaniloGnome** | <img src="https://avatars.githubusercontent.com/u/127751001?v=4" width="45" height="45" style="border-radius: 50%;" /> | [Perfil do GitHub](https://github.com/DaniloGnome) |
| **Reed0ne**     | <img src="https://avatars.githubusercontent.com/u/115191418?v=4" width="45" height="45" style="border-radius: 50%;" /> | [Perfil do GitHub](https://github.com/Reed0ne)     |

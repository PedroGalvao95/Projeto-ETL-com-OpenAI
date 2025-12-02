# Instala as bibliotecas necessárias
pip install pandas requests openai

import pandas as pd
import requests
import json
import openai

# URL base da API da Santander Dev Week 2023
# Você pode usar a URL oficial ou sua própria (se tiver deployado)
[cite_start]sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app' [cite: 39]

# SUA CHAVE DA API OpenAI (Obtenha em: https://platform.openai.com/account/api-keys)
# Necessária para a etapa de Transformação (IA Generativa)
# Substitua 'SUA_API_KEY_AQUI' pela sua chave real.
openai_api_key = 'SUA_API_KEY_AQUI'

# Configura a chave da OpenAI
openai.api_key = openai_api_key

# Carrega os IDs dos usuários a partir do arquivo CSV
try:
    [cite_start]df = pd.read_csv('SDW2023.csv') [cite: 46]
    [cite_start]user_ids = df['UserID'].tolist() [cite: 46]
    print(f"IDs de usuários extraídos: {user_ids}")
except FileNotFoundError:
    print("Erro: O arquivo 'SDW2023.csv' não foi encontrado. Certifique-se de que ele está no diretório correto.")
    user_ids = []

# Função para buscar os dados de um único usuário na API
[cite_start]def get_user(id): [cite: 55]
    [cite_start]response = requests.get(f'{sdw2023_api_url}/users/{id}') [cite: 56]
    # Retorna o JSON do usuário se o status for 200 (OK), senão retorna None
    [cite_start]return response.json() if response.status_code == 200 else None [cite: 56]

# Busca os dados de todos os usuários
# Apenas usuários com dados válidos (response.status_code == 200) são incluídos
[cite_start]users = [user for id in user_ids if (user := get_user(id)) is not None] [cite: 57]

print("\n--- Dados dos Usuários Extraídos ---")
print(json.dumps(users, indent=2))

# Função para gerar a mensagem de marketing usando a API do OpenAI
[cite_start]def generate_ai_news(user): [cite: 155]
    # O conteúdo da mensagem é construído com base no nome do usuário
    [cite_start]prompt = f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos." [cite: 171]
    
    [cite_start]completion = openai.ChatCompletion.create( [cite: 156]
        [cite_start]model="gpt-4", [cite: 157]
        messages=[
            {
                # Define o papel da IA como especialista em marketing bancário
                "role": "system",
                [cite_start]"content": "Você é um especialista em marketing bancário." [cite: 164]
            },
            {
                # Envia o prompt de criação da mensagem
                "role": "user",
                [cite_start]"content": prompt [cite: 171]
            }
        ]
    )
    # Retorna o conteúdo da mensagem, removendo as aspas que a IA pode incluir
    [cite_start]return completion.choices[0].message.content.strip('"') [cite: 172]

# Gera a mensagem para cada usuário e armazena na lista 'news'
print("\n--- Mensagens Geradas pela IA ---")
for user in users:
    [cite_start]news = generate_ai_news(user) [cite: 174]
    print(f"Para {user['name']}: {news}")
    
    # Adiciona a nova mensagem à lista 'news' do objeto usuário
    [cite_start]user['news'].append({ [cite: 176]
        [cite_start]"icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg", [cite: 178]
        [cite_start]"description": news [cite: 178]
    })

# Função para atualizar os dados do usuário na API
def update_user(user):
    headers = {'Content-Type': 'application/json'}
    # Envia os dados atualizados para o endpoint PUT
    [cite_start]response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", headers=headers, data=json.dumps(user)) [cite: 37]
    return response.status_code == 200

# Envia a atualização para cada usuário
print("\n--- Carga (Load) dos Dados na API ---")
for user in users:
    if update_user(user):
        print(f"Usuário {user['name']} (ID: {user['id']}) atualizado com sucesso na API.")
    else:
        print(f"Erro ao atualizar o usuário {user['name']} (ID: {user['id']}) na API.")
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import base64

def create_graphql_client():
    # Configuração do cliente GraphQL
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql',
        verify=True,
        retries=3,
    )
    
    return Client(transport=transport, fetch_schema_from_transport=True)

def load_project_structure(file_path: str):
    # Cria o cliente GraphQL
    client = create_graphql_client()
    
    # Lê o arquivo JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Para cada módulo no JSON
    for module_name, module_data in data.items():
        # Prepara os dados do módulo
        module_payload = {
            "name": module_name,
            "data": module_data
        }
        
        # Converte para string JSON
        module_json = json.dumps(module_payload)
        
        # Define a mutation
        mutation = gql('''
        mutation AddModule($data: String!) {
            addModule(data: $data)
        }
        ''')
        
        # Executa a mutation
        try:
            result = client.execute(
                mutation,
                variable_values={"data": module_json}
            )
            print(f"Módulo {module_name} adicionado com sucesso: {result}")
        except Exception as e:
            print(f"Erro ao adicionar módulo {module_name}: {e}")

if __name__ == "__main__":
    # Primeiro instale as dependências necessárias
    # pip install gql requests
    
    # Execute o carregamento
    load_project_structure('project_structure.json')
import json
import base64

try:
    # Lê o arquivo JSON
    with open('project_structure.json', 'r', encoding='utf-8') as file:
        print("Arquivo aberto com sucesso")
        json_data = file.read()
        print(f"Tamanho dos dados lidos: {len(json_data)} caracteres")

    # Verifica se o JSON é válido
    json_obj = json.loads(json_data)
    print("JSON é válido")

    # Converte o JSON para string e codifica em base64
    json_string = json.dumps(json_obj)
    json_base64 = base64.b64encode(json_string.encode()).decode()

    # Cria a mutation com o JSON em base64
    mutation = f'''mutation {{
  loadProjectData(data: "{json_base64}")
}}'''
    
    # Salva a mutation em um arquivo
    with open('mutation.txt', 'w', encoding='utf-8') as f:
        f.write(mutation)
        print("\nMutation salva em 'mutation.txt'")

except Exception as e:
    print(f"Erro: {str(e)}")
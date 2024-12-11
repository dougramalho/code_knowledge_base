import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from .schema.queries import Query, Mutation

print("Iniciando a aplicação...")

# Criar o schema GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Criar a aplicação FastAPI
app = FastAPI()

# Adicionar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL do seu app React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar e adicionar o router GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

print("Configuração concluída, iniciando o servidor...")

if __name__ == "__main__":
    print("Executando o servidor...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
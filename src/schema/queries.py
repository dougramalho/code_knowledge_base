import strawberry
from typing import Optional
from .types import Project, Module, Namespace, CodeClass, CodeMember
from ..services.knowledge_service import KnowledgeService

knowledge_service = KnowledgeService()

@strawberry.type
class Query:
    @strawberry.field
    def project(self) -> Project:
        return knowledge_service.get_project()
    
    @strawberry.field
    def module(self, name: str) -> Optional[Module]:
        project = knowledge_service.get_project()
        return next((m for m in project.modules if m.name == name), None)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_module(self, data: str) -> bool:
        try:
            import json
            module_data = json.loads(data)
            knowledge_service.add_module(module_data)
            return True
        except Exception as e:
            print(f"Error adding module: {e}")
            return False
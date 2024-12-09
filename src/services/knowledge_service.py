from typing import List, Dict, Any
from ..schema.types import CodeEntity, ProjectStructure

class KnowledgeService:
    def __init__(self):
        self.project_data: Dict[str, Any] = {}

    def load_project_structure(self, json_data: Dict[str, Any]) -> None:
        self.project_data = json_data

    def get_entities(self) -> List[CodeEntity]:
        entities = []
        for class_name, class_data in self.project_data.items():
            entities.append(
                CodeEntity(
                    name=class_name,
                    type=class_data.get("type", "unknown"),
                    raw_code=str(class_data.get("raw", ""))
                )
            )
        return entities
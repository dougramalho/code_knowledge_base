from typing import Dict, List, Optional, Any
from ..schema.types import Project, Module, Namespace, CodeClass, CodeMember, Dependency

class KnowledgeService:
    def __init__(self):
        self.project_data: Dict[str, Any] = {}

    def add_module(self, module_data: Dict[str, Any]) -> Module:
        # Processa o módulo e seus namespaces
        module_name = module_data["name"]
        namespace = self.process_node(module_data.get("data", {}))
        
        module = Module(
            name=module_name,
            namespaces=namespace.namespaces,
            classes=namespace.classes
        )
        
        # Armazena no project_data
        self.project_data[module_name] = module_data.get("data", {})
        
        return module

    def process_node(self, node_data: Dict) -> Namespace:
        classes = []
        namespaces = []
        
        for name, content in node_data.items():
            if isinstance(content, dict):
                if "type" in content:
                    # É uma classe
                    class_obj = self.process_class_data(name, content)
                    if class_obj:
                        classes.append(class_obj)
                else:
                    # É um namespace
                    sub_namespace = self.process_node(content)
                    sub_namespace.name = name
                    namespaces.append(sub_namespace)
        
        return Namespace(
            name="",
            classes=classes,
            namespaces=namespaces
        )

    def process_class_data(self, class_name: str, class_data: Dict) -> Optional[CodeClass]:
        if not isinstance(class_data, dict) or "type" not in class_data:
            return None
            
        members = []
        for member_name, member_data in class_data.get("members", {}).items():
            dependencies = []
            for dep in member_data.get("dependencies", []):
                dependencies.append(Dependency(
                    type=dep["type"],
                    method=dep["method"]
                ))
            
            members.append(CodeMember(
                name=member_name,
                type=member_data["type"],
                raw_code=member_data.get("raw"),
                dependencies=dependencies
            ))
        
        return CodeClass(
            name=class_name,
            type=class_data["type"],
            members=members
        )

    def get_project(self) -> Project:
        modules = []
        for module_name, module_data in self.project_data.items():
            namespace = self.process_node(module_data)
            modules.append(Module(
                name=module_name,
                namespaces=namespace.namespaces,
                classes=namespace.classes
            ))
        return Project(modules=modules)
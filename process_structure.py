import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Dependency:
    type: str
    method: str

@dataclass
class CodeMember:
    name: str
    type: str
    raw_code: Optional[str]
    dependencies: List[Dependency]

@dataclass
class CodeClass:
    name: str
    type: str
    members: List[CodeMember]

@dataclass
class Namespace:
    name: str
    classes: List[CodeClass]
    namespaces: List['Namespace']

@dataclass
class Module:
    name: str
    namespaces: List[Namespace]
    classes: List[CodeClass]  # Classes diretamente no módulo

def process_class_data(class_name: str, class_data: Dict) -> Optional[CodeClass]:
    """Processa os dados de uma classe individual"""
    if isinstance(class_data, dict) and "type" in class_data:
        members = []
        
        # Processa os membros da classe
        for member_name, member_data in class_data.get("members", {}).items():
            dependencies = []
            
            # Processa as dependências
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
            name=class_name,  # Agora o nome da classe não inclui o namespace
            type=class_data["type"],
            members=members
        )
    return None

def process_node(node_data: Dict, namespace_name: str = "") -> Namespace:
    """Processa um nó e retorna um namespace com suas classes e sub-namespaces"""
    classes = []
    namespaces = []
    
    for name, content in node_data.items():
        if isinstance(content, dict):
            if "type" in content:
                # É uma classe
                class_obj = process_class_data(name, content)  # Passa apenas o nome da classe
                if class_obj:
                    classes.append(class_obj)
            else:
                # É um namespace
                sub_namespace = process_node(content, name)
                namespaces.append(sub_namespace)
    
    return Namespace(
        name=namespace_name,
        classes=classes,
        namespaces=namespaces
    )

def load_project_structure(file_path: str) -> List[Module]:
    """Carrega e processa a estrutura completa do projeto"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modules = []
    
    # Processa cada módulo principal
    for module_name, module_data in data.items():
        print(f"\nProcessando módulo: {module_name}")
        
        namespace = process_node(module_data)
        
        module = Module(
            name=module_name,
            namespaces=namespace.namespaces,
            classes=namespace.classes
        )
        modules.append(module)
    
    return modules

def print_structure(modules: List[Module]):
    """Imprime a estrutura de forma hierárquica"""
    print("\n=== Estrutura do Projeto ===")
    
    for module in modules:
        print(f"\nMódulo: {module.name}")
        
        if module.classes:
            print("  Classes:")
            for class_ in module.classes:
                print(f"    - {class_.name}")
                print(f"      Membros: {len(class_.members)}")
        
        def print_namespace(namespace: Namespace, level: int):
            indent = "  " * level
            print(f"{indent}Namespace: {namespace.name}")
            
            if namespace.classes:
                print(f"{indent}  Classes:")
                for class_ in namespace.classes:
                    print(f"{indent}    - {class_.name}")
                    print(f"{indent}      Membros: {len(class_.members)}")
            
            for sub_namespace in namespace.namespaces:
                print_namespace(sub_namespace, level + 1)
        
        for namespace in module.namespaces:
            print_namespace(namespace, 1)

if __name__ == "__main__":
    modules = load_project_structure('project_structure.json')
    print_structure(modules)
from typing import List, Optional
import strawberry

@strawberry.type
class Dependency:
    type: str
    method: str

@strawberry.type
class CodeMember:
    name: str
    type: str
    raw_code: Optional[str] = None
    dependencies: List[Dependency] = strawberry.field(default_factory=list)

@strawberry.type
class CodeClass:
    name: str
    type: str
    members: List[CodeMember] = strawberry.field(default_factory=list)

@strawberry.type
class Namespace:
    name: str
    classes: List[CodeClass] = strawberry.field(default_factory=list)
    namespaces: List['Namespace'] = strawberry.field(default_factory=list)

@strawberry.type
class Module:
    name: str
    namespaces: List[Namespace] = strawberry.field(default_factory=list)
    classes: List[CodeClass] = strawberry.field(default_factory=list)

@strawberry.type
class Project:
    modules: List[Module] = strawberry.field(default_factory=list)
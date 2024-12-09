from typing import List, Optional
import strawberry

@strawberry.type
class CodeEntity:
    name: str
    type: str
    dependencies: List[str] = strawberry.field(default_factory=list)
    raw_code: Optional[str] = None

@strawberry.type
class ProjectStructure:
    entities: List[CodeEntity]
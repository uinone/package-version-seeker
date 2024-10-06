from enum import Enum

class ModuleType(Enum):
    VERSION_EXIST = 1
    VERSION_EMPTY = 2
    JUST_COMMENT = 3
    VERSION_EXIST_WITH_COMMENT = 4
    VERSION_EMPTY_WITH_COMMENT = 5
    NEWLINE = 6

class Module:
    def __init__(self, project_name:str, project_version:str, comment:str, module_type:ModuleType):
        self.project_name = project_name
        self.project_version = project_version
        self.comment = comment
        self.module_type = module_type
    
    @classmethod
    def parse_content(cls, content:str):
        if len(content) == 0:
            return Module(
                project_name=None,
                project_version=None,
                comment=None,
                module_type=ModuleType.NEWLINE
            )

        if content[0] == "#":
            return Module(
                project_name=None,
                project_version=None,
                comment=content,
                module_type=ModuleType.JUST_COMMENT
            )

        content = content.strip()

        project_name = None
        project_version = None
        module_type = None
        comment = None

        # Check comment existence
        if content.find("#") != -1:
            comment_start_idx = content.find("#")
            comment = content[comment_start_idx:]
            content = content[:comment_start_idx]
            content = content.strip()

        # Check project version existence
        split_prefix_candidate = [content.find("<"), content.find("="), content.find(">")]
        split_prefix_candidate.sort()

        postive_index = -1
        for cand in split_prefix_candidate:
            if cand > 0:
                postive_index = cand
                break

        # Version empty
        if postive_index == -1: 
            if comment is None:
                module_type = ModuleType.VERSION_EMPTY
            else:
                module_type = ModuleType.VERSION_EMPTY_WITH_COMMENT
            project_name = content.strip()
        
        # Version exist
        else:
            if comment is None:
                module_type = ModuleType.VERSION_EXIST
            else:
                module_type = ModuleType.VERSION_EXIST_WITH_COMMENT
            
            project_name = content[:postive_index].strip()
            project_version = content[postive_index:]
            
        return Module(
            project_name=project_name,
            project_version=project_version,
            comment=comment,
            module_type=module_type
        )
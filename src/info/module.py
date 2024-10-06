from enum import Enum

class ModuleType(Enum):
    NEWLINE = 0
    VERSION_EXIST = 1
    VERSION_EMPTY = 2
    JUST_COMMENT = 3
    VERSION_EXIST_WITH_COMMENT = 4
    VERSION_EMPTY_WITH_COMMENT = 5

class Module:
    def __init__(self, project_name:str, project_option:str, project_version:str, comment:str, module_type:ModuleType):
        self.project_name = project_name
        self.project_option = project_option
        self.project_version = project_version
        self.comment = comment
        self.module_type = module_type
    
    def __repr__(self) -> str:
        if self.module_type == ModuleType.NEWLINE:
            return ""

        if self.module_type == ModuleType.JUST_COMMENT:
            return self.comment

        repr_text = self.project_name + (self.project_option if self.project_option is not None else "") + (self.project_version if self.project_version is not None else "")
        if self.module_type.name.endswith("WITH_COMMENT"):
            repr_text += self.comment
        
        return repr_text
    
    @classmethod
    def parse_content(cls, content:str):
        if len(content) == 0:
            return Module(
                project_name=None,
                project_option=None,
                project_version=None,
                comment=None,
                module_type=ModuleType.NEWLINE
            )

        if content[0] == "#":
            return Module(
                project_name=None,
                project_option=None,
                project_version=None,
                comment=content,
                module_type=ModuleType.JUST_COMMENT
            )

        content = content.strip()

        project_name = None
        project_option = None
        project_version = None
        module_type = None
        comment = None

        # Check comment existence
        if content.find("#") != -1:
            comment_start_idx = content.find("#")

            # Check additional spaces
            temp_idx = comment_start_idx-1
            while content[temp_idx] == " ":
                temp_idx -= 1
            temp_idx += 1

            comment_start_idx = temp_idx

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
            project_version = "".join(content[postive_index:].split(" ")) # Trim some spaces around project version
            
        if project_name.find("[") != -1:
            project_option = project_name[project_name.find("["):]
            project_name = project_name[:project_name.find("[")]
            
        return Module(
            project_name=project_name,
            project_option=project_option,
            project_version=project_version,
            comment=comment,
            module_type=module_type
        )
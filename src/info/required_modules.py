from .history import ReleaseHistory
from .module import Module, ModuleType

from typing import Optional

class RequiredModules:
    def __init__(self, infos:list[Module]):
        self.infos = infos

    def __repr__(self) -> str:
        repr_text = ""

        for info in self.infos:
            repr_text += info.__repr__() + "\n"
        
        return repr_text[:-1]
    
    def _fill_empty_versions(self, target_project:str, target_project_version:str):
        module_with_empty_version = []

        # Aggregating
        for idx, info in enumerate(self.infos):
            if (info.module_type == ModuleType.VERSION_EMPTY) or (info.module_type == ModuleType.VERSION_EMPTY_WITH_COMMENT):
                module_with_empty_version.append(idx)
        
        target_project_release_hist = ReleaseHistory.get_project_release_history(target_project)
        target_datetime = target_project_release_hist.get_datetime_by_version(target_project_version)

        if target_datetime is None:
            return None

        target_datetime = target_datetime["datetime"]

        for idx in module_with_empty_version:
            module_name = self.infos[idx].project_name
            release_hist = ReleaseHistory.get_project_release_history(module_name)
            closest_version = release_hist.get_closest_version_by_datetime(target_datetime)
            self.infos[idx].project_version = closest_version

        return self
    
    def export(self, path:str):
        with open(path, "w") as f:
            f.write(self.__repr__())

    @classmethod
    def get_requirement_text(cls, path:str, target_project:str, target_project_version:str) -> Optional[ReleaseHistory]:
        required_modules:list[Module] = []

        try:
            with open(path, "r") as f:
                for line in f.read().split("\n"):
                    required_modules.append(Module.parse_content(line))
            
            return RequiredModules(infos=required_modules)._fill_empty_versions(target_project, target_project_version)
        except Exception as e:
            print(f"[FAILED]\n{e}")
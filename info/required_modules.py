from .history import ReleaseHistory

from typing import Optional

class RequiredModules:
    def __init__(self, infos:dict):
        self.infos = infos

    def __repr__(self) -> str:
        repr_text = ""

        for k, v in self.infos.items():
            if v is None:
                repr_text += k
                repr_text += "\n"
            else:
                repr_text += k + v
                repr_text += "\n"
        
        return repr_text[:-1]
    
    def _fill_empty_versions(self, target_project:str, target_project_version:str):
        module_with_empty_version = {}

        # Aggregating
        for k, v in self.infos.items():
            if v is None:
                module_with_empty_version[k] = None
        
        target_project_release_hist = ReleaseHistory.get_project_release_history(target_project)
        target_datetime = target_project_release_hist.get_datetime_by_version(target_project_version)

        if target_datetime is None:
            return None

        target_datetime = target_datetime["datetime"]

        for module_name in module_with_empty_version.keys():
            release_hist = ReleaseHistory.get_project_release_history(module_name)
            closest_version = release_hist.get_closest_version_by_datetime(target_datetime)
            module_with_empty_version[module_name] = closest_version
        
        self.infos.update(module_with_empty_version)

        return self
    
    def export(self, path:str):
        with open(path, "w") as f:
            f.write(self.__repr__())


    @classmethod
    def get_requirement_text(cls, path:str, target_project:str, target_project_version:str) -> Optional[ReleaseHistory]:
        required_module_infos = {}
        try:
            with open(path, "r") as f:
                required_module_names = [module_name for module_name in f.read().split("\n") if not(module_name.startswith("#")) and len(module_name) > 0]
                
                for module_name in required_module_names:
                    split_prefix_candidate = [module_name.find("<"), module_name.find("="), module_name.find(">")]
                    split_prefix_candidate.sort()

                    postive_index = -1
                    for cand in split_prefix_candidate:
                        if cand > 0:
                            postive_index = cand
                            break

                    if postive_index == -1:
                        required_module_infos[module_name] = None
                    else:
                        required_module_infos[module_name[:postive_index]] = module_name[postive_index:]
            
            return RequiredModules(infos=required_module_infos)._fill_empty_versions(target_project, target_project_version)
        except Exception as e:
            print(f"[FAILED]\n{e}")
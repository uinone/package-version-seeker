import requests
from bs4 import BeautifulSoup

from datetime import datetime

from typing import Optional

class ReleaseHistory:
    def __init__(self, project_name:str, release_history:dict):
        self.project_name = project_name
        self.version_to_datetime = release_history

    def get_closest_version_by_datetime(self, target_datetime: datetime) -> str:
        target_timestamp = target_datetime.timestamp()

        minimum_diff = -1
        closest_version = None
        for k,v in self.version_to_datetime.items():
            diff = target_timestamp - v["datetime"].timestamp()
            if diff < 0:
                continue
            if (closest_version is None) or (diff < minimum_diff):
                minimum_diff = diff
                closest_version = k
                break
        
        # See https://github.com/uinone/package-version-seeker/issues/1
        if closest_version is None:
            versions = list(self.version_to_datetime.keys())
            closest_version = versions[-1] # Get oldest version

        return f"=={closest_version}"
    
    def get_datetime_by_version(self, version:str) -> Optional[datetime]:
        try:
            dt = self.version_to_datetime[version]
            return dt
        except KeyError:
            print(f"version '{version}' does not exist in {self.project_name}'s release history\nCheck 'https://pypi.org/project/{self.project_name}/#history'")
            return None

    def __repr__(self) -> str:
        return f"[Project] {self.project_name}"

    @classmethod
    def get_project_release_history(cls, project_name:str):
        release_history_url = f"https://pypi.org/project/{project_name}/#history"

        release_history_response = requests.get(release_history_url)
        soup = BeautifulSoup(release_history_response.text, "html.parser")

        time_line = soup.find(name="div", attrs="release-timeline")
        
        releases = time_line.findAll(name="div", attrs="release")

        release_history = {}
        for release in releases:
            version = release.find(name="p", attrs="release__version").text.strip().split("\n")[0]
            dt = release.find(name="time").attrs["datetime"].split("+")[0]
            release_history[version] = {"datetime": datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")}
        
        return ReleaseHistory(
            project_name=project_name,
            release_history=release_history
        )
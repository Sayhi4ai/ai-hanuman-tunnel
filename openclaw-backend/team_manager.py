from typing import Dict, List
from app.integrations.opscaptain import opscaptain

class TeamManager:
    def __init__(self):
        self.teams: Dict[str, List[str]] = {}

    def create_team(self, team_id: str):
        if team_id not in self.teams:
            self.teams[team_id] = []
            opscaptain.log_event("team_created", {"team_id": team_id})

    def add_agent(self, team_id: str, agent_id: str):
        self.create_team(team_id)
        if agent_id not in self.teams[team_id]:
            self.teams[team_id].append(agent_id)
            opscaptain.log_event("team_member_added", {
                "team_id": team_id,
                "agent_id": agent_id,
            })

    def get_team(self, team_id: str) -> List[str]:
        return self.teams.get(team_id, [])

team_manager = TeamManager()

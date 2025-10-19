export interface Mission {
  challenge_id: string;
  riddle: string;
  action: string;
  challenge_name: string;
  code_offered: number;
  code_needed: number;
  agent_needed: string;
  assigned_at: number;
}

export interface AgentProfile {
  _id: string;
  sub: string;
  email: string;
  name: string;
  current_mission: Mission;
  previous_missions: Mission[];
  uuid: string;
  agent: string;
  summary: string;
}

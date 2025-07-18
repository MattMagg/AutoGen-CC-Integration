#!/usr/bin/env python3
"""
Register custom agents in AutoGen Studio database
This script properly adds agents to the Component Library
"""

import asyncio
import json
import requests
from pathlib import Path
from autogenstudio.database import DatabaseManager
from autogenstudio.datamodel import Agent, Model, Tool, Team

# AutoGen Studio API endpoint
STUDIO_API_BASE = "http://localhost:8080/api"

def register_model():
    """Register our Claude model in AutoGen Studio"""
    model_data = {
        "name": "Claude Opus via Wrapper",
        "model": "claude-opus-4-20250514",
        "api_type": "openai",
        "base_url": "http://localhost:8000/v1",
        "description": "Claude Opus 4 accessed through local OpenAI-compatible wrapper"
    }
    
    # Check if model exists
    response = requests.get(f"{STUDIO_API_BASE}/models")
    if response.status_code == 200:
        models = response.json()
        for model in models:
            if model.get("model") == model_data["model"]:
                print(f"✓ Model already registered: {model_data['name']}")
                return model["id"]
    
    # Register new model
    response = requests.post(f"{STUDIO_API_BASE}/models", json=model_data)
    if response.status_code == 200:
        model_id = response.json()["id"]
        print(f"✅ Registered model: {model_data['name']} (ID: {model_id})")
        return model_id
    else:
        print(f"❌ Failed to register model: {response.text}")
        return None

def register_agent(agent_config, model_id):
    """Register an agent in AutoGen Studio"""
    agent_data = {
        "name": agent_config["name"],
        "description": agent_config["description"],
        "system_message": agent_config["system_message"],
        "model_id": model_id,
        "type": "assistant",
        "config": {
            "temperature": agent_config.get("model_client", {}).get("temperature", 0.5),
            "max_tokens": agent_config.get("model_client", {}).get("max_tokens", 4096)
        }
    }
    
    # Check if agent exists
    response = requests.get(f"{STUDIO_API_BASE}/agents")
    if response.status_code == 200:
        agents = response.json()
        for agent in agents:
            if agent.get("name") == agent_data["name"]:
                print(f"✓ Agent already registered: {agent_data['name']}")
                return agent["id"]
    
    # Register new agent
    response = requests.post(f"{STUDIO_API_BASE}/agents", json=agent_data)
    if response.status_code == 200:
        agent_id = response.json()["id"]
        print(f"✅ Registered agent: {agent_data['name']} (ID: {agent_id})")
        return agent_id
    else:
        print(f"❌ Failed to register agent: {response.text}")
        return None

def register_team(team_config, agent_ids):
    """Register a team in AutoGen Studio"""
    team_data = {
        "name": team_config["name"],
        "description": team_config["description"],
        "participants": agent_ids,
        "type": "roundrobin",
        "config": {
            "termination_condition": {
                "type": "combination",
                "conditions": [
                    {"type": "text_mention", "text": "APPROVED"},
                    {"type": "max_messages", "max_messages": 15}
                ]
            }
        }
    }
    
    # Check if team exists
    response = requests.get(f"{STUDIO_API_BASE}/teams")
    if response.status_code == 200:
        teams = response.json()
        for team in teams:
            if team.get("name") == team_data["name"]:
                print(f"✓ Team already registered: {team_data['name']}")
                return team["id"]
    
    # Register new team
    response = requests.post(f"{STUDIO_API_BASE}/teams", json=team_data)
    if response.status_code == 200:
        team_id = response.json()["id"]
        print(f"✅ Registered team: {team_data['name']} (ID: {team_id})")
        return team_id
    else:
        print(f"❌ Failed to register team: {response.text}")
        return None

def use_database_direct():
    """Alternative: Register directly in the database"""
    print("\n🔧 Using direct database registration...")
    
    # Initialize database
    db = DatabaseManager(
        engine_uri="sqlite:///autogen04202.db",
        base_dir=str(Path(__file__).parent)
    )
    
    # Create model
    model = Model(
        name="Claude Opus Wrapper",
        model="claude-opus-4-20250514",
        api_type="openai",
        base_url="http://localhost:8000/v1",
        description="Claude Opus via local wrapper"
    )
    
    # Create agents from our configs
    agents = []
    
    # Load individual agent config
    agent_config_path = Path(__file__).parent / "configs" / "test_agent_config.json"
    if agent_config_path.exists():
        with open(agent_config_path, 'r') as f:
            config = json.load(f)
            agent = Agent(
                name=config["name"],
                description=config["description"],
                system_message=config["system_message"],
                type="assistant",
                model_id=model.id
            )
            agents.append(agent)
    
    # Load team config
    team_config_path = Path(__file__).parent / "team.json"
    if team_config_path.exists():
        with open(team_config_path, 'r') as f:
            team_config = json.load(f)
            for participant in team_config["participants"]:
                agent = Agent(
                    name=participant["name"],
                    description=participant["description"],
                    system_message=participant["system_message"],
                    type="assistant",
                    model_id=model.id
                )
                agents.append(agent)
    
    print(f"✅ Created {len(agents)} agents in database")
    return model, agents

def main():
    """Main registration function"""
    print("🚀 AutoGen Studio Agent Registration")
    print("=" * 50)
    
    # Check if AutoGen Studio is running
    try:
        response = requests.get(f"{STUDIO_API_BASE}/health")
        if response.status_code == 200:
            print("✅ AutoGen Studio API is accessible")
            use_api = True
        else:
            print("⚠️ AutoGen Studio API not responding, using direct database")
            use_api = False
    except:
        print("⚠️ Cannot connect to AutoGen Studio API, using direct database")
        use_api = False
    
    if use_api:
        # Register via API
        print("\n📝 Registering components via API...")
        
        # Register model
        model_id = register_model()
        if not model_id:
            print("Failed to register model, aborting")
            return
        
        # Register agents
        agent_ids = []
        
        # Load and register team agents
        team_path = Path(__file__).parent / "team.json"
        if team_path.exists():
            with open(team_path, 'r') as f:
                team_config = json.load(f)
                
            for participant in team_config["participants"]:
                agent_id = register_agent(participant, model_id)
                if agent_id:
                    agent_ids.append(agent_id)
        
        # Register team
        if agent_ids and team_path.exists():
            register_team(team_config, agent_ids)
    else:
        # Use direct database registration
        use_database_direct()
    
    print("\n✨ Registration complete!")
    print("\n💡 Next steps:")
    print("1. Refresh the AutoGen Studio UI")
    print("2. Check the Component Library in Team Builder")
    print("3. Your agents should now appear!")
    print("4. If not visible, restart AutoGen Studio")

if __name__ == "__main__":
    main()
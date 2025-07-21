#!/usr/bin/env python3
"""
Import Claude-configured team into AutoGen Studio
This creates a properly formatted team configuration that AutoGen Studio can understand
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Claude wrapper configuration
CLAUDE_MODEL_CONFIG = {
    "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
    "component_type": "model",
    "version": 1,
    "component_version": 1,
    "description": "Claude Opus via local OpenAI wrapper",
    "label": "Claude Opus Wrapper",
    "config": {
        "model": "claude-opus-4-20250514",
        "base_url": "http://localhost:8000/v1",
        "api_key": "not-needed"
    }
}

# Create a simple test team with Claude
CLAUDE_TEST_TEAM = {
    "provider": "autogen_agentchat.teams.RoundRobinGroupChat",
    "component_type": "team",
    "version": 1,
    "component_version": 1,
    "description": "Test team using Claude wrapper for development",
    "label": "Claude Development Team",
    "config": {
        "participants": [
            {
                "provider": "autogen_agentchat.agents.AssistantAgent",
                "component_type": "agent",
                "version": 1,
                "component_version": 1,
                "description": "Architecture and design specialist",
                "label": "Claude Architect",
                "config": {
                    "name": "architect",
                    "model_client": CLAUDE_MODEL_CONFIG,
                    "workbench": {
                        "provider": "autogen_core.tools.StaticWorkbench",
                        "component_type": "workbench",
                        "version": 1,
                        "component_version": 1,
                        "description": "A workbench that provides a static set of tools",
                        "label": "StaticWorkbench",
                        "config": {"tools": []}
                    },
                    "model_context": {
                        "provider": "autogen_core.model_context.UnboundedChatCompletionContext",
                        "component_type": "chat_completion_context",
                        "version": 1,
                        "component_version": 1,
                        "description": "An unbounded chat completion context",
                        "label": "UnboundedChatCompletionContext",
                        "config": {}
                    },
                    "description": "System architect for design and planning",
                    "system_message": "You are a software architect. Design clean, scalable solutions and provide implementation guidance.",
                    "model_client_stream": False,
                    "reflect_on_tool_use": False,
                    "tool_call_summary_format": "{result}",
                    "metadata": {}
                }
            },
            {
                "provider": "autogen_agentchat.agents.AssistantAgent",
                "component_type": "agent",
                "version": 1,
                "component_version": 1,
                "description": "Code implementation specialist",
                "label": "Claude Developer",
                "config": {
                    "name": "developer",
                    "model_client": CLAUDE_MODEL_CONFIG,
                    "workbench": {
                        "provider": "autogen_core.tools.StaticWorkbench",
                        "component_type": "workbench",
                        "version": 1,
                        "component_version": 1,
                        "description": "A workbench that provides a static set of tools",
                        "label": "StaticWorkbench",
                        "config": {"tools": []}
                    },
                    "model_context": {
                        "provider": "autogen_core.model_context.UnboundedChatCompletionContext",
                        "component_type": "chat_completion_context",
                        "version": 1,
                        "component_version": 1,
                        "description": "An unbounded chat completion context",
                        "label": "UnboundedChatCompletionContext",
                        "config": {}
                    },
                    "description": "Developer who implements clean, efficient code",
                    "system_message": "You are a senior developer. Write clean, efficient, and well-tested code following best practices.",
                    "model_client_stream": False,
                    "reflect_on_tool_use": False,
                    "tool_call_summary_format": "{result}",
                    "metadata": {}
                }
            }
        ],
        "termination_condition": {
            "provider": "autogen_agentchat.base.OrTerminationCondition",
            "component_type": "termination",
            "version": 1,
            "component_version": 1,
            "label": "OrTerminationCondition",
            "config": {
                "conditions": [
                    {
                        "provider": "autogen_agentchat.conditions.TextMentionTermination",
                        "component_type": "termination",
                        "version": 1,
                        "component_version": 1,
                        "description": "Terminate on TERMINATE",
                        "label": "TextMentionTermination",
                        "config": {"text": "TERMINATE"}
                    },
                    {
                        "provider": "autogen_agentchat.conditions.MaxMessageTermination",
                        "component_type": "termination",
                        "version": 1,
                        "component_version": 1,
                        "description": "Max 10 messages",
                        "label": "MaxMessageTermination",
                        "config": {"max_messages": 10, "include_agent_event": False}
                    }
                ]
            }
        },
        "emit_team_events": False
    }
}

def insert_team_to_db():
    """Insert the Claude team directly into the AutoGen Studio database"""
    db_path = Path(__file__).parent.parent / "autogen04202.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return False
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert the team
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO team (created_at, updated_at, user_id, version, component)
            VALUES (?, ?, ?, ?, ?)
        """, (now, now, "guestuser@gmail.com", "0.0.1", json.dumps(CLAUDE_TEST_TEAM)))
        
        conn.commit()
        team_id = cursor.lastrowid
        print(f"✅ Successfully added Claude Development Team (ID: {team_id})")
        
        # Also insert into gallery for visibility
        gallery_entry = {
            "type": "component",
            "id": f"claude_team_{team_id}",
            "component": CLAUDE_TEST_TEAM
        }
        
        cursor.execute("""
            INSERT INTO gallery (created_at, updated_at, user_id, version, config)
            VALUES (?, ?, ?, ?, ?)
        """, (now, now, "guestuser@gmail.com", "0.0.1", json.dumps(gallery_entry)))
        
        conn.commit()
        print("✅ Added team to gallery")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error inserting team: {e}")
        return False

def main():
    print("🚀 Importing Claude team into AutoGen Studio")
    print("=" * 50)
    
    if insert_team_to_db():
        print("\n✨ Import complete!")
        print("\n💡 Next steps:")
        print("1. Refresh the AutoGen Studio UI")
        print("2. Look for 'Claude Development Team' in the Playground")
        print("3. Test the team with a simple task")
    else:
        print("\n❌ Import failed")

if __name__ == "__main__":
    main()
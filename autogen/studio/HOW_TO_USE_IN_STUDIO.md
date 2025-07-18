# 🎯 How to Use Custom Agents in AutoGen Studio

## Understanding AutoGen Studio's Build Interface

The **Team Builder** in AutoGen Studio works differently than expected:
- The **Component Library** shows generic agent TYPES (AssistantAgent, UserProxyAgent, etc.)
- You don't see your custom agents there - that's normal!
- Instead, you configure agents with your custom settings

## Step-by-Step Guide

### Method 1: Manual Configuration in Team Builder

1. **Go to Team Builder** (http://localhost:8080/build)

2. **Create a New Team**
   - Click "New Team"
   - Name it: "Test Development Team"

3. **Add Agents from Component Library**
   - Drag "AssistantAgent" from the Component Library
   - Drop it in the team workspace
   - Configure it:
     - Name: `test_architect`
     - System Message: (copy from our configs)
     - Model: `claude-opus-4-20250514`
     - Base URL: `http://localhost:8000/v1`
     - Temperature: `0.7`

4. **Repeat for Other Agents**
   - Add another AssistantAgent for `test_developer`
   - Add another for `test_reviewer`

5. **Configure Team Settings**
   - Set termination condition to OrTerminationCondition
   - Add TextMentionTermination with "APPROVED"
   - Add MaxMessageTermination with 15 messages

6. **Save and Run**
   - Click "Run" to test your team

### Method 2: Use in Playground (Easier!)

1. **Go to Playground** (http://localhost:8080/playground)

2. **Start New Session**
   - Click "New Session" or "+"

3. **Configure Default Agents**
   - Any default agent can use your Claude model
   - In agent settings, set:
     - Model: `claude-opus-4-20250514`
     - Base URL: `http://localhost:8000/v1`
     - API Type: `OpenAI`

4. **Use Your Agents**
   - The agents will now use Claude instead of OpenAI!

### Method 3: Import Workflow (Recommended)

1. **Go to Playground**

2. **Import Workflow**
   - Look for "Import" or "Load" button
   - Select: `/Users/mac-main/autogen-claude-integration/autogen/myapp/test_workflow.json`

3. **Start Using**
   - Your test team is now available!

## 🔧 Troubleshooting

### Agents Not Working?
1. **Check Model Configuration**
   ```
   Model: claude-opus-4-20250514
   Base URL: http://localhost:8000/v1
   API Type: OpenAI
   API Key: (leave empty or 'not-needed')
   ```

2. **Verify Wrapper is Running**
   ```bash
   curl http://localhost:8000/v1/models
   ```

3. **Check Console for Errors**
   - Open browser developer tools (F12)
   - Check Console tab for errors

### Build Interface Confusion?
- The Component Library shows agent TYPES, not instances
- You create instances by dragging types and configuring them
- Your custom system messages make them specialized

## 📝 Example Test Prompts

Once your agents are configured:

**For Testing Tasks:**
- "Create unit tests for a login function that validates email and password"
- "Design a test strategy for a payment processing system"
- "Write integration tests for a REST API with authentication"

**For Team Collaboration:**
- "Help me create a comprehensive test suite for a todo app with CRUD operations"
- "Review and improve this test code: [paste code]"
- "What's the best testing strategy for a microservices architecture?"

## 🚀 Pro Tips

1. **Save Your Teams**
   - After configuring in Team Builder, save the team
   - You can reuse it in future sessions

2. **Model Settings**
   - Higher temperature (0.7-0.9) for creative tasks (architect)
   - Lower temperature (0.3-0.5) for precise tasks (developer)
   - Medium temperature (0.5-0.7) for review tasks

3. **Use Playground for Quick Tests**
   - Playground is faster for testing
   - Team Builder is better for complex workflows

## ✅ Success Indicators

You'll know it's working when:
- Agents respond with Claude's style
- No OpenAI API errors in console
- Responses are relevant to your prompts
- Team collaboration flows smoothly

Remember: AutoGen Studio is a UI layer - the real work happens through your configured agents using the Claude wrapper!
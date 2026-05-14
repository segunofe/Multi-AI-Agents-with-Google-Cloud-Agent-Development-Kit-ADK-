# Multi-AI-Agents-with-Google-Cloud-Agent-Development-Kit-ADK

Four (4) AI- Agents in one System 
## Goal: Repair and deploy broken AI Agents to check and fix errors to ensure data accuracy

Scenario (Problem): Previous engineer left the agent definition incomplete which supposed to use Google Search to find real-time travel information but currently has no tools enabled. 


## Technical Requirement 1: I must use Vertex AI by configuring the .env file - No API Keys

### Here you go: my .env file
```
GOOGLE_GENAI_USE_VERTEXAI=true

GOOGLE_CLOUD_PROJECT=your-provided-project-id

GOOGLE_CLOUD_LOCATION=global

MODEL=gemini-1.5-flash
```

### Task 1. Install ADK and set up your environment

Step 1: Update PATH: 

```
export PATH=$PATH:"/home/${USER}/.local/bin"
python3 -m pip install google-adk
```

Step 2: Authenticate to Google Cloud and set up credentials 
```
gcloud auth application-default login
```
Step 3: Download source code: 

```
gcloud storage cp gs://qwiklabs-gcp-03-2323e1b2f558-bucket/adk_project.zip .

unzip adk_project.zip

cd adk_project

pip install -r requirements.txt
```

### Task 2. Initialize and Configure the Travel Scout (my_google_search_agent)

- Modify agent.py to enable the google_search tool. (Tip: Pass tools=[google_search] in the Agent definition).

- Locate the line in agent.py and Modify the Agent Definition

#### Example modification in agent.py
```
agent = Agent(
    tools=[google_search]      # <--- Add this line here
)
```

### Task 3. Verify the agent via the CLI

#### Navigate to your project directory if you aren't already there

```
cd ~/adk_project

# Run the specific agent
adk run my_google_search_agent

```

### Task 4. Enforce structured standards
Request: Wants strict JSON object containing just capital city nit free-form text
```
GOOGLE_GENAI_USE_VERTEXAI=true

GOOGLE_CLOUD_PROJECT=your-provided-project-id

GOOGLE_CLOUD_LOCATION=global

MODEL=gemini-1.5-flash
```
Modify model's resoinse format in code to ensure Booking Engine receives only JSON object

# Inside your agent.py logic
```
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(
    "What is the capital of Japan?",
    generation_config={"response_mime_type": "application/json"}
)
```
3. Modify agent.py to:

- Define a Pydantic model CountryCapital (Tip: inherit from BaseModel and define a field capital: str).
- 
- Enforce this schema by passing it as the output_schema argument in the Agent definition.
- 
- Disable transfers by setting disallow_transfer_to_parent=True and disallow_transfer_to_peers=True in the agent definition.
- 
- Set Model: Ensure you use the latest Flash model: model_name


# Updated agent.py
```
from pydantic import BaseModel

# 1. Define the Pydantic model
class CountryCapital(BaseModel):
    capital: str

# 2. Update the Agent definition
geo_validator = Agent(
    name="geo_validator",
    model="gemini-1.5-flash",  # The latest stable Flash model
    instructions="Identify the capital city of the provided destination.",
    
    # Enforce the structured JSON schema
    output_schema=CountryCapital,
    
    # 3. Disable transfers to keep the agent focused on this specific task
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)
```
# verify that the agent returns only JSON
adk run geo_validator

Test Input: France
Expected Output: {"capital": "Paris"}



### Task 5. Deploy the Brochure Auditor

The crown jewel of Cymbal Travel is the Brochure Auditor (llm_auditor), a sequential multi-agent system designed to ensure marketing accuracy.

Step 1: .env
```
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
MODEL=gemini-1.5-flash
```
Step 2: Modify agent.py to Restore the Pipeline: llm_auditor is lead agent (supervisor) and needs both critic_agent and reviser_agent in its sub_agents list to complete the workflow

#### 1. Ensure the reviser is imported
```
from agents.critic import critic_agent
from agents.reviser import reviser_agent  # <--- Uncomment this line
```
#### 2. Update the Lead Agent (Auditor) definition
```
llm_auditor = Agent(
    name="llm_auditor",
    model="gemini-1.5-flash",
    instructions="""
    You are the Brochure Auditor. 
    First, send the marketing claim to the critic_agent to verify facts.
    Second, send the claim and the critic's feedback to the reviser_agent 
    to produce a corrected version of the text.
    """,
    # 3. Add both agents to the sub_agents list
    sub_agents=[critic_agent, reviser_agent] 
)
```
Verify fix by  submitting a false claim for auditing: adk run llm_auditor

Test Prompt: Double check this: You can take a direct train from Hawaii to Japan.

Note: This was the note I took from my Professional Cloud Architect Course with Google Cloud 

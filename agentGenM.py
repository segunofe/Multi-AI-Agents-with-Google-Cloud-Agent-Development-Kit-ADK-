# Example modification in agent.py
agent = Agent(
    model="gemini-2.5-flash",  # or your specific model version
    instructions="You are a helpful research assistant.",
    tools=[google_search]      # <--- Add this line here
)

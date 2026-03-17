import os
from langchain_groq import ChatGroq

# Print API key to verify it is loaded
print("Loaded GROQ_API_KEY:", repr(os.getenv("GROQ_API_KEY")))

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY").strip(),
    temperature=0.2
)

# Send test prompt
response = llm.invoke("Say hello in one sentence.")

print("\nModel Response:")
print(response.content)
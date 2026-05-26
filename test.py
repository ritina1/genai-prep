import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
# Make your first LLM call
response = client.chat.completions.create(
 model="llama-3.3-70b-versatile",
 messages=[
 {"role": "system", "content": "You are a helpful AI tutor."},
 {"role": "user", "content": "Explain what an LLM is in 3 simple sentences."}
 ],
 temperature=0.7,
)

print("=" * 50)
print("AI Response:")
print("=" * 50)
print(response.choices[0].message.content)
print("=" * 50)
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_ai(prompt, system="You are a helpful AI.", temp=0.7):
 """Helper function - sends prompt to Groq, returns response."""
 response = client.chat.completions.create(
 model="llama-3.3-70b-versatile",
 messages=[
 {"role": "system", "content": system},
 {"role": "user", "content": prompt}
 ],
 temperature=temp,
 )
 return response.choices[0].message.content


# ===== EXPERIMENT 1: Temperature =====
print("\n" + "="*60)
print("EXP 1: Temperature controls randomness")
print("="*60)

prompt = "Write a one-sentence story about a dragon."

print("\n--- Temperature 0 (predictable) ---")
print(ask_ai(prompt, temp=0))

print("\n--- Temperature 0 again (should be ~same) ---")
print(ask_ai(prompt, temp=0))

print("\n--- Temperature 1.5 (creative, random) ---")
print(ask_ai(prompt, temp=1.5))

print("\n--- Temperature 1.5 again (should be different) ---")
print(ask_ai(prompt, temp=1.5))


# ===== EXPERIMENT 2: System Prompts =====
print("\n" + "="*60)
print("EXP 2: System prompts change AI personality")
print("="*60)

question = "Explain what a database is in one sentence."

print("\n--- As a Pirate ---")
print(ask_ai(question, system="You are a pirate. Reply only in pirate speak with 'Arrr!'"))

print("\n--- As a 5-year-old ---")
print(ask_ai(question, system="You are a 5-year-old explaining to other kids."))

print("\n--- As a Strict Professor ---")
print(ask_ai(question, system="You are a strict university professor giving a formal lecture."))


# ===== EXPERIMENT 3: Zero-shot vs Few-shot =====
print("\n" + "="*60)
print("EXP 3: Examples help the AI learn the pattern")
print("="*60)

print("\n--- ZERO-SHOT (no examples) ---")
print(ask_ai("Classify this review as POSITIVE or NEGATIVE: 'Food was cold and the staff rude.'"))

print("\n--- FEW-SHOT (with examples) ---")
few_shot = """Classify reviews as POSITIVE or NEGATIVE.

Review: 'Best meal of my life!'
Answer: POSITIVE

Review: 'Waited 2 hours for cold food.'
Answer: NEGATIVE

Review: 'Food was cold and staff rude.'
Answer:"""
print(ask_ai(few_shot))


# ===== EXPERIMENT 4: Chain-of-Thought =====
print("\n" + "="*60)
print("EXP 4: 'Think step by step' improves reasoning")
print("="*60)

math_problem = "A shop sells 23 apples Monday, 47 Tuesday, and twice Monday's count on Wednesday. Total apples?"

print("\n--- WITHOUT step-by-step ---")
print(ask_ai(math_problem))

print("\n--- WITH 'think step by step' ---")
print(ask_ai(math_problem + " Let's think step by step."))


# ===== EXPERIMENT 5: Structured JSON Output =====
print("\n" + "="*60)
print("EXP 5: Forcing structured output (interview-relevant!)")
print("="*60)

extract_prompt = """Extract info from this text and return ONLY valid JSON.

Text: "Ritina is 26 years old, lives in Kolkata, works as a SQL developer at TechCorp."

Return JSON with keys: name, age, city, job, company. No explanation."""

print(ask_ai(extract_prompt, system="You return only valid JSON. No markdown formatting."))


print("\n" + "="*60)
print("🎉 Day 1 experiments complete!")
print("="*60)
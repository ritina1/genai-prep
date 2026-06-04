1.Thanks, that's a strong overview. Let me dig in. You said you used text-embedding-ada-002 and stored vectors in Azure AI Search. When a new query comes in and you do the similarity search — how does that search actually find the right results? Walk me through what's happening mathematically when it matches the query to stored documents."

"When a new query arrives, I embed it using the same model — text-embedding-ada-002 — that I used to embed the stored documents. So now both the query and the documents are vectors in the same space, in this case 1536 dimensions.
The search then computes cosine similarity between the query vector and each stored vector. Cosine similarity measures the angle between two vectors — a score close to 1 means they point in nearly the same direction, so they're semantically similar; a score near 0 means unrelated.
It returns the top-k documents with the highest similarity — usually k=3 to 5.
The key point is this works on meaning, not keywords. So a query like 'casual leave allotment for this year' will match a stored document about 'annual leave entitlement' because their embeddings are close in vector space — even though the exact words don't overlap. That's the whole advantage of semantic search over traditional keyword search.
And at scale, Azure AI Search doesn't compare against every vector one by one — it uses an approximate nearest neighbor algorithm called HNSW to find the closest vectors fast."

2."You chose GPT-4o-mini for generating responses. Why GPT-4o-mini specifically — why not the full GPT-4o or another model? Walk me through that decision."

"Three reasons. First, cost — GPT-4o-mini is significantly cheaper than GPT-4o, which matters for a WhatsApp assistant handling high message volume.
Second, latency — it's faster, and WhatsApp users expect near-instant replies like a normal chat. Mini kept response times low.
Third, and most important — because I'm using RAG, the model doesn't need deep built-in knowledge. The relevant context is retrieved from Azure AI Search and injected into the prompt, so the model's only job is to read that context and form a clean answer. That's well within GPT-4o-mini's capability. I benchmarked it against the baseline and it performed well for our attendance and policy queries.
If we'd needed heavier reasoning, I'd tier it — use mini for most queries and escalate to GPT-4o only for complex ones. But for this use case, mini was the right cost-quality balance."

3.Let's talk about quality. You mentioned a 25 to 30 percent improvement over the baseline. How exactly did you measure that? Walk me through your evaluation method."

"I set up a comparative evaluation. First, I built a test set of question-answer pairs — domain-specific questions about attendance records, historical conversations, and company policies — the kind of thing the model couldn't know from pretraining.
Then I ran each question through two systems: one was GPT-4o-mini with RAG — retrieving context from Azure AI Search and injecting it — and the other was GPT-4o-mini alone, with no retrieval, relying only on its pretrained knowledge.
I scored both sets of answers on relevance and accuracy against the known correct answer. For scoring I used a mix of manual review and LLM-as-judge, where a stronger model rated each answer on a scale.
The RAG system consistently produced more accurate, context-grounded answers — roughly 25 to 30 percent better on relevance and fewer incorrect answers — and the gap was biggest exactly where you'd expect: the domain-specific questions the base model had no knowledge of."

4."Here's a design scenario. You're building a RAG system that serves multiple clients — multiple companies — on the same application. Hard requirement: one client's documents must never be retrieved when a user from a different client asks a question. How would you design that?"

"This is a multi-tenant data isolation problem. I'd approach it at two levels.
First, the data layer. Every document gets tagged with a client_id in its metadata when it's indexed. Then at retrieval time, before the vector search runs, I apply a metadata filter so the search only ever looks at documents matching the current user's client_id. So even though all clients share the same index, the filter guarantees a query only retrieves that client's documents. Azure AI Search supports this kind of metadata filtering on vector queries.
For stricter isolation — say a banking or healthcare client that demands physical separation — I'd give each client their own separate index or even a separate vector DB instance. More expensive and more to manage, but complete isolation at the infrastructure level. So it's a tiered approach: shared index with metadata filtering for most clients, dedicated index for high-security clients.
Second, the security layer on top. Each client authenticates with their own API key, which maps to their client_id — so the filter is driven by who's authenticated, not by anything the user can manipulate in their query. And I'd add audit logging — every query logged with its client_id — so we can prove isolation for compliance.
The key principle: never rely on the user's input to enforce isolation. The client_id comes from the authenticated session, and the filter is applied server-side before retrieval."

5.Beyond instructing the model to 'answer only from context,' what specific prompt engineering techniques do you know, and when would you use each?

a.Zero-shot Prompting

No examples given.

Translate English to French:
Hello
b. Few-shot Prompting

Examples provided.

English: Hello
French: Bonjour

English: Thank you
French:
c. Chain-of-Thought Prompting

Ask model to think step-by-step.

Solve step-by-step:
If 2 apples cost 10...

d.system prompt:
<!-- prompt = f"""
You are an HR assistant.

Answer ONLY from the given context.

Context:
{retrieved_context}

Question:
{question}
""" -->
You are an HR assistant

Defines role.

Helps model behave professionally.

Answer ONLY from given context

Prevents hallucination.

Context

Retrieved chunk from vector DB.

Question

Actual user query.

1. System Role

The system message tells the model:

"How should you behave?"

Example:

{
    "role": "system",
    "content": "You are a helpful Python tutor."
}

This sets the behavior.

2. User Role

This is the actual question from the user.

Example:

{
    "role": "user",
    "content": "Explain Python list comprehension."
}
3. Assistant Role

Represents previous responses from the AI.

Example:

{
    "role": "assistant",
    "content": "List comprehension is a concise way to create lists."
}

messages = [
    {
        "role": "system",
        "content": """
        You are an HR assistant.
        Answer only from the provided context.
        If the answer is not found, say:
        'Information not available.'
        """
    },
    {
        "role": "user",
        "content": """
        Context:
        Employees get 20 casual leaves annually.

        Question:
        How many leaves are allowed?
        """
    }
]

5.What was the hardest technical challenge you faced, and how did you solve it?

Here's how to approach this one — it's a classic, and they'll almost certainly ask it. The key is to pick a real, specific challenge from your project, not a generic one.

Let me give you a few options based on what you actually built, then you pick the one that's most true for you.

🎯 Option 1: Hallucination / answer grounding (strongest, ties to your 25-30%)

"The hardest challenge was making sure the model answered only from our retrieved data and didn't fall back on its pretrained knowledge — because for attendance records and company policies, the model's own knowledge was either wrong or nonexistent.

Early on, even with RAG, the model would sometimes blend in its own assumptions and give confident but incorrect answers. I solved it through a combination: strict prompt instructions telling the model to answer only from the provided context and to say 'I don't have that information' when the context didn't cover it, setting temperature to 0 for factual queries to reduce confabulation, and structuring the prompt so retrieved context was clearly separated from the question.

Then I validated it with comparative testing — RAG versus LLM-only — and confirmed the grounded approach was 25 to 30 percent more accurate on domain-specific questions. That testing loop is how I knew the fix actually worked, not just felt better."




****Good — let's clear up top-k and cosine similarity with simple examples. These two go together, so I'll explain both and show how they work as a team. No jargon. 🙂

Part 1: Cosine Similarity
What it measures: how similar two pieces of text are in meaning, as a number between -1 and 1.

Close to 1 = very similar meaning
Around 0 = unrelated
Close to -1 = opposite

How it works: Every piece of text becomes a list of numbers (a vector/embedding). Cosine similarity measures the angle between two vectors. Small angle = pointing the same direction = similar meaning.
Simple example
Imagine your stored documents and a user question, each turned into a similarity score against the question:
User asks: "How many casual leaves do I get?"
Now compare it against your stored documents:
Stored documentCosine similarity score"Casual leave entitlement is 7 days per year"0.91 ← very similar"Annual leave is 20 days per year"0.68 ← somewhat similar"Office opens at 9 AM"0.12 ← unrelated"Overtime is paid at 1.5x rate"0.09 ← unrelated
See how the system scores each document? The casual leave doc scores highest (0.91) because it's closest in meaning to the question — even though the question says "casual leaves" and the doc says "casual leave entitlement." The words aren't identical, but the meaning is, so the score is high.
That's the magic — it matches on meaning, not exact words.

Part 2: Top-k
What it means: After scoring every document, you don't send all of them to the LLM — you pick the top k highest-scoring ones. "k" is just a number you choose, usually 3 to 5.
Continuing the example
From the scores above, if you set k = 3, you take the 3 highest-scoring documents:
✅ "Casual leave entitlement is 7 days per year" (0.91)
✅ "Annual leave is 20 days per year" (0.68)
✅ "Office opens at 9 AM" (0.12)
(You take the top 3 by score, even if the 3rd one is weak.)
Then only those 3 get injected into the prompt as context for the LLM. The LLM reads them and answers: "You get 7 casual leaves per year."
Why not send all documents?

Too much text → overflows the context window
Costs more → more tokens = more money
Adds noise → irrelevant docs can confuse the model

So top-k keeps it focused: just the most relevant few.
Why 3 to 5 specifically?
It's a sweet spot:

k too small (k=1) → might miss relevant info if the answer spans multiple docs
k too large (k=20) → too much noise, higher cost, slower
k = 3 to 5 → usually enough context to answer well, without the downsides

You tune this number based on testing — that's a design choice you can mention in the interview.

Putting it together (the full picture)
User question: "How many casual leaves do I get?"
 │
 ▼
1. Embed the question → vector
 │
 ▼
2. Cosine similarity: score the question against EVERY stored doc
 (0.91, 0.68, 0.12, 0.09, ...)
 │
 ▼
3. Top-k: pick the 3 highest-scoring docs
 │
 ▼
4. Inject those 3 docs into the prompt as context
 │
 ▼
5. LLM reads the context → answers: "You get 7 casual leaves per year"

🎤 How to say it in the interview (simple version)

"Cosine similarity gives each document a score from 0 to 1 based on how close its meaning is to the user's question — 1 means very similar. Top-k means after scoring all the documents, I take the k highest-scoring ones — usually 3 to 5 — and send only those to the LLM as context. I don't send all documents because that's expensive and adds noise. Top-k keeps the context focused on what's most relevant."


Does that make it clear? Want me to show the actual numbers behind how cosine similarity is calculated (the math), or is the meaning-and-scoring intuition enough for the interview? For Capgemini, the intuition above is usually enough — but I can show the formula with a tiny example if you want to be extra ready. 💪You said: meaning of hnswmeaning of hnsw1:53 AMClaude responded: Good — HNSW is one of those terms that sounds scary but the idea is simple.Good — HNSW is one of those terms that sounds scary but the idea is simple. Let me break it down. 🙂

What HNSW stands for
Hierarchical Navigable Small World (graphs)
Don't worry about the long name. Here's what it actually does:

The problem it solves
Imagine you have 1 million stored documents (vectors). A user asks a question.
The naive way: Compare the question against all 1 million documents one by one, calculate cosine similarity for each, then pick the top matches.
Problem: That's 1 million calculations for every single query. Too slow. With millions of vectors, this takes seconds — users won't wait.

What HNSW does instead
HNSW is a smart shortcut algorithm that finds the closest matches without checking every single vector. It checks only a small fraction and still finds the right answers.
It does this by organizing the vectors into a layered map (like a graph), where each vector is connected to its nearest neighbors. To search, it navigates this map efficiently — jumping toward the answer instead of checking everything.

Simple analogy 🗺️
Imagine you're looking for a specific house in a huge city.
Naive way: Knock on every single door in the city until you find it. (= comparing against every vector)
HNSW way: You use a map with zoom levels:

Top level (zoomed out): "Which neighborhood?" → jump to the right area fast
Middle level: "Which street?" → narrow down
Bottom level (zoomed in): "Which house?" → find the exact one

You skip 99% of the city and go straight to the right area. That's HNSW — it navigates from coarse to fine, layer by layer, instead of brute-force searching.

The key trade-off (worth mentioning in interview)
HNSW is "approximate" nearest neighbor search.

It's massively faster (milliseconds instead of seconds)
But it's approximate — occasionally it might miss the absolute closest match and give you the 2nd closest instead

For RAG, this trade-off is fine — the 2nd or 3rd closest document is usually just as useful as context. You trade a tiny bit of accuracy for huge speed gains. That's a good deal.

Where it's used
Almost every production vector database uses HNSW internally:

Azure AI Search (what you used) ✅
Pinecone
ChromaDB
FAISS
Weaviate

So when you say "Azure AI Search uses HNSW," you're saying it uses the industry-standard fast search method.

🎤 How to say it in the interview (simple, confident version)

"HNSW stands for Hierarchical Navigable Small World graphs. It's the algorithm vector databases use to search quickly. Instead of comparing the query against every stored vector one by one — which is too slow at scale — HNSW organizes vectors into a layered graph and navigates it efficiently, going from a coarse search to a fine one. It's an approximate nearest neighbor method, so it trades a tiny bit of accuracy for a massive speed gain — which is a good trade-off for RAG, because the approximate top results are still highly relevant."


📝 What you really need to remember for the interview (if you forget everything else):

It's how vector DBs search fast at scale
It doesn't check every vector — uses a layered graph to jump to the answer
It's approximate — trades tiny accuracy for big speed
Azure AI Search (and most vector DBs) use it

That's enough. They won't ask you to implement HNSW — they just want to know you understand why vector search is fast. 🙂
Want me to explain the layered-graph part visually, or is the analogy clear enough? 💪

View SILPAMOY’s profileSILPAMOY KANJILAL, #OPEN_TO_WORK
SILPAMOY KANJILAL   2:03 AM
What does "multi-tenant" mean?
Tenant = a separate customer/client/company using your app.
Multi-tenant = one single application serving many different clients at the same time.
Simple analogy 🏢
Think of an apartment building:

One building (your application)
Many tenants/families living in it (different client companies)
Each family has their own locked apartment — they can't walk into someone else's home

Multi-tenant data isolation = making sure Client A can NEVER see Client B's data, even though they share the same building (app).

*****
roject Deep-Dive

Walk me through your WhatsApp RAG project end to end.
What was your specific contribution?
Hardest technical challenge and how you solved it?
If you rebuilt it today, what would you change?
How did you handle the audio/Whisper part?
How did you handle conversation history?
Why Azure AI Search over other vector DBs?
Why GPT-4o-mini over GPT-4o?
How did you measure the 25-30% improvement?
How did prompt engineering reduce hallucinations?

RAG

What is RAG and why use it?
Explain the indexing phase vs retrieval phase.
What chunking strategies exist? When use each?
Why is chunk overlap important?
Your retrieval returns irrelevant chunks — how do you debug?
What is reranking? When would you add it?
RAG vs fine-tuning — when each?
What is hybrid search?

Embeddings & Search

What is an embedding?
Explain cosine similarity. Why cosine over Euclidean?
What is top-k and how do you choose k?
What is HNSW?
What is text-embedding-ada-002? Its dimensions?

Prompting & Models

Prompt engineering techniques and when to use each.
What is temperature? 0 vs high?
How do you force valid JSON output?
How do you reduce hallucinations? (list techniques)
What is a system prompt vs user prompt?

Agents

What is an AI agent vs a plain LLM?
Explain the ReAct pattern.
What is function calling / tool use?
What agent frameworks do you know?
When use an agent vs simple RAG?

Evaluation & Production

How do you evaluate a RAG system?
What is LLM-as-Judge?
How would you scale to 100,000 users?
How do you optimize cost?
How do you optimize latency?

System Design

Design a multi-tenant RAG system with client data isolation.
Design a customer support chatbot for e-commerce.
How would you add memory to a chatbot?
Chatbot gives wrong answers — how do you investigate?

Concepts

How do transformers work? Why replaced RNN/LSTM?
What is self-attention (high level)?
What is tokenization? Why does it affect cost?
What is a context window? What if input exceeds it?
What is quantization (INT8/INT4)?
What is LoRA / QLoRA?
What is prompt injection? How to defend?
How do you handle PII in an LLM system?

Coding

Write a text chunking function with overlap.
Write cosine similarity from scratch.
Write an embedding generation function (Azure OpenAI).
Write a RAG prompt template.
Call an LLM and safely parse JSON output.
Find top-k most similar vectors to a query.
SQL: employees late more than 3 times this month.
Python: count word frequency in a string.

HR / Behavioral

Tell me about yourself.
Why Capgemini?
Why transition into GenAI?
Where do you see yourself in 3 years?
Biggest strength / weakness?
How do you keep up with fast-moving GenAI?
Why were you laid off?
Do you have questions for us?


Want me to fire these one at a time as a mock (you answer, I give feedback), or leave you to drill solo? Either way — you've put in the work. Saturday you've got this. 💪
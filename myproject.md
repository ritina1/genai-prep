In my previous project, I worked on an AI-powered WhatsApp assistant for attendance and employee support. The solution was built using Azure OpenAI, Azure AI Search (Vector Search), GPT-4o-mini, and OpenAI Whisper for speech-to-text transcription. 

The primary objective was to process user voice messages, maintain conversation history, and provide context-aware responses using Retrieval-Augmented Generation (RAG).

When a user sends an audio message through WhatsApp, the audio is first transcribed into text using Whisper. After transcription, I generated embeddings using the text-embedding-ada-002 model and stored them in Azure AI Search along with metadata such as user ID, timestamp, message category, and conversation context.

One of my key responsibilities was implementing the embedding generation pipeline, vector indexing, similarity search, and prompt engineering workflow. The goal was to enable semantic retrieval rather than traditional keyword-based search.

Whenever a new user query arrives, the query is converted into an embedding and a vector similarity search is performed against Azure AI Search. The system retrieves the most relevant historical conversations and knowledge-base documents based on semantic similarity.

The retrieved context is then injected into a structured prompt and sent to GPT-4o-mini. Through prompt engineering, we instructed the model to answer only from retrieved context and avoid generating unsupported information. This significantly reduced hallucinations and improved answer reliability.

To evaluate the effectiveness of the RAG architecture, we performed comparative testing between responses generated using only the LLM's pretrained knowledge and responses generated using retrieved enterprise data. During internal testing, the RAG-based approach consistently produced more contextually relevant and accurate answers for attendance-related and policy-related queries.

Compared to the baseline LLM-only approach, we observed approximately 25-30% improvement in response relevance and reduction in incorrect answers for domain-specific questions. This was particularly noticeable when users asked questions related to historical conversations, attendance records, or company-specific policies that were not part of the model's pretrained knowledge.

The complete workflow was:

WhatsApp User → Audio Message → Whisper Transcription → Embedding Generation (text-embedding-ada-002) → Azure AI Search → Vector Similarity Search → Context Retrieval → Prompt Engineering → GPT-4o-mini → Final Response.

This project provided hands-on experience with Azure OpenAI, embeddings, vector databases, RAG architecture, prompt engineering, semantic search, hallucination reduction, and production-scale chatbot development.




##


If they ask:

"How did you measure the 25–30% improvement?"

You can answer:

We created a validation set of frequently asked attendance and HR-related questions. We compared answers generated using only GPT-4o-mini versus answers generated using RAG. We manually evaluated relevance, factual correctness, and context alignment. The RAG-based responses consistently performed better for company-specific questions.

That answer sounds much more like a real GenAI engineer than someone who only knows the theory.
Without RAG (Only GPT-4o-mini)

Suppose your company attendance policy says:

Employees can regularize attendance within 3 days.

But this policy is not part of GPT's training data.

User asks:

How many days do I have to regularize my attendance?
GPT Only

GPT might answer:

Most companies allow attendance regularization within 7 days.

or

Usually attendance can be regularized within a week.

This is called hallucination because GPT is guessing.

With RAG
Step 1: Document Stored
Attendance Policy:
Employees can regularize attendance within 3 days.

Stored in Azure AI Search as embeddings.

Step 2: User Question
How many days do I have to regularize my attendance?
Step 3: Similarity Search

Azure AI Search retrieves:

Employees can regularize attendance within 3 days.
Step 4: Prompt Sent to GPT
System:
You are an attendance assistant.
Answer only from provided context.

Context:
Employees can regularize attendance within 3 days.

Question:
How many days do I have to regularize my attendance?
Step 5: GPT Response
Employees can regularize attendance within 3 days.

Correct answer.

How to Explain Improvement

Interviewer: "What improvement did RAG provide?"

You can say:

For company-specific questions, GPT alone sometimes generated generic answers because it did not know our internal policies. After implementing RAG using Azure AI Search, the model retrieved actual company documents before generating responses. During internal testing, we observed significantly better accuracy and relevance for attendance and policy-related queries.

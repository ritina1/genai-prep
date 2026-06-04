1.NLP:IT IS An field of ai it helps computer to understand,analyze,generate the hyman language like text,speech etc
example :chatgpt,spam detection,siri and all

2.flow of NLP:
Human Text
   ↓  
Tokenization
   ↓
Text Processing
   ↓
Understanding Meaning
   ↓
Prediction/Response

3.Tokenization: Breaking text into smaller parts like machine learning theer is 2 token machine and learning

4.stemming:reducing words to root form like playing->play.

5.Lemmatization:converting words to meaningful root form. Example:better->good.

6.NER(Named entity recognition):Finding name in text 
like :ritina works at accenture    here ritina ->name,accenture->organization.

7.sentimental analysis: detects emotion in text like 
the product is amazing ->positive statement

8.Artificial Neuron
      ↓
Neural Network
      ↓
Deep Learning
      ↓
Transformer Architecture
      ↓
LLMs (GPT, Gemini, Llama)

9.neuron :receive signals,process information,pass signals forward
artificial neuron it received tge input processed it and give the output like 
Input:
Hours studied
Attendance
Assignments
output: pass or fail.

10.when many artificial neuron are connected together it is called neural network.
structure:input layer,hidden layer ,output
Example: Cat Detection
Suppose input image is given.
Input Layer:Receives pixels.
Hidden Layers:
First layer learns:edges
Second layer learns:ears,eyes
Third layer learns:full cat face
output layer:cat predict chatgpt

11.deep learning:when neural network has many hidden layer

12.transformer:it is the deep learning architecture to understand the text and the relationship between the words 
example:The animal didn’t cross the road because it was tired. here it understand it means animal.it used attention mechanism and parallel processing,like I went to the bank for deposit the money here using attebtion it focuses the bank is the financial bank and I love cricket here parallely it process that 3 words .Attention helps the model focus on important words and understand contextual relationships.

13.llm:it is huge model built using transformer architecture trained on huge datasets.

14.Artificial Neuron
      ↓
Neural Network
      ↓
Deep Learning
      ↓
Transformer Architecture
      ↓
LLMs (GPT, Gemini, Llama)

15.real transformer flow:
Input Sentence
   ↓
Tokenization
   ↓
Embeddings
   ↓
Self-Attention
   ↓
Parallel Processing
   ↓
Context Understanding
   ↓
Prediction

15.Complete Architecture
WhatsApp User
      ↓
Audio Message
      ↓
Speech-to-Text
      ↓
Transcription
      ↓
Embedding Model
      ↓
Azure AI Search (Vector DB)
      ↓
User Query
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
Relevant Conversations/Documents
      ↓
Prompt Engineering
      ↓
GPT-4o-mini
      ↓
Response

16.
Q: Why did you choose text-embedding-ada-002?
Strong Interview Answer

We chose text-embedding-ada-002 because it provided a good balance between embedding quality, cost, latency, and integration with Azure OpenAI. Our use case required semantic search over historical conversations and knowledge-base content, and ada-002 generated high-quality embeddings that worked well for vector similarity search in Azure AI Search.
like : how many casual lives 
and what is the casual leaves allotmemnt diff words same meNING
17.
What exactly does Ada-002 produce?

Answer:

It converts text into a high-dimensional vector representation that captures semantic meaning. These vectors can then be compared using similarity metrics such as cosine similarity.

18.
what is azure open ai?
Azure OpenAI is a Microsoft-managed service that provides access to OpenAI models such as GPT and embedding models through Azure, offering enterprise-grade security, scalability, monitoring, and integration with other Azure services.

19.Q: Why did you choose GPT-4o-mini?
Strong Interview Answer

We chose GPT-4o-mini because it provided a good balance between response quality, latency, and cost. Our WhatsApp assistant handled a large number of user interactions, so we needed a model that could generate accurate responses while keeping API costs and response times manageable.
Our use case was:

Attendance queries
Employee support
FAQ responses
RAG-based retrieval

The difficult knowledge retrieval was handled by Azure AI Search.

The LLM mainly needed to:

understand the question
use retrieved context
generate a natural answer

GPT-4o-mini was sufficient for that.

20.If Interviewer Asks:
Why not GPT-4o?

Answer:

GPT-4o generally provides stronger reasoning capabilities, but our use case focused on retrieving company-specific information and generating conversational responses. GPT-4o-mini met our quality requirements while offering lower latency and lower operational cost.
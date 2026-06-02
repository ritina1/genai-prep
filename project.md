azure vector store endpoijt and api key die vector search kra jai ,ekta kre container banano jai,chatbot er questopn and answer store kra jai,(14),index kra mane database e save 
azure vector serach library te 
top p parameter   search krar time e use kra hoi ,top q 
gpt-generative pretrained transformer(3.5)-fine tuning (labeled data model training )
azure open ai ,azure model data model r api key die use kratam 
azure portal e model ki kre deploy krbo ? use kre nijer kaje use ki kr ekrbo 
azure portal model,

project idea-chatbot type(33 min)  
role question answer question tate audio support kre ,question gulo asche vector store e store hoe jachhe automatically ,question ta user voice on kre send krlo pathalo ami otake open ai use kre text krlam die vector store e store kre dilam question hisebe,prompt kre pathie dilam gpt 4 o mini rkache ,

search client e 



ki ki search krte pre attendance data store ache ki na ?
kno absent dekhache esb jiges krbo sourav da ke?

1.Why not store text directly?

Answer:

Storing text alone enables keyword search. Using embeddings allows semantic search, where similar meanings can be found even when different words are used.

Example:

Attendance correction
Attendance regularization
Fix attendance issue

2.What Is Happening Internally?
Very simple explanation:

Text
 ↓
Tokenization
 ↓
Neural Network
 ↓
Vector Representation

The model has been trained on massive text datasets and has learned relationships between words and concepts.
So:
leave
vacation
holiday

end up relatively close in vector space.

3.If the interviewer asks: "What exactly is the role of GPT here?"

Say:

Azure AI Search retrieves relevant information, but it does not generate answers. GPT-4o-mini reads the retrieved context, understands the user's question, and generates a natural language response. The vector database acts as the knowledge source, while the LLM acts as the reasoning and response generation engine

4.If the interviewer asks: "Why not use SQL?"

Say:

SQL works well for exact matching, but our users ask the same question in many different ways. We needed semantic similarity search, which is why we used embeddings and Azure AI Search.

5.If the interviewer asks: "Where is RAG used in the flow?"

Say:

RAG starts after the user query arrives. The query is converted into an embedding, relevant information is retrieved from the vector database, and that retrieved context is sent to GPT-4o-mini before generating the final response.
import streamlit as st
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFacePipeline , HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

def load_model(model_type, model_name): #created function to load and work on model 
    if model_type == "Closed-Source (Groq)":
        if model_name == "Groq-LLaMA2":
            return ChatGroq(model_name="llama3-8b-8192")
        elif model_name == "Groq-Mistral":
            return ChatGroq(model_name="mixtral-8x7b-32768")
    

    elif model_type == "Open-Source":    
        if model_name == "HuggingFace - API":
            llm = HuggingFaceEndpoint(repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
            return ChatHuggingFace(llm=llm)
        elif model_name == "HuggingFace - Local":
            llm = HuggingFacePipeline.from_model_id(
                model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                task='text-generation',
                pipeline_kwargs=dict(temperature=0.5, max_new_tokens=100)
            )
            return ChatHuggingFace(llm=llm)

    return None
def chattemp_create(chat_history, user_input):
    chat_template=ChatPromptTemplate.from_messages([
    ('system', 'you are a helpful AI expert'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{topic}')
])
    return chat_template.invoke({"chat_history":chat_history,"topic":user_input})
    

load_dotenv()
# Initialising Chat History
if "chat_history_local" not in st.session_state:
    st.session_state.chat_history_local = []

st.header('LangChain Q&A Assistant')

#To select Model Type
model_type = st.selectbox("Choose Model Type:", ["Closed-Source (Groq)", "Open-Source"])

# To select Model Name
if model_type == "Open-Source":
    model_name = st.selectbox("Choose Open-Source Model:", ["HuggingFace - API", "HuggingFace - Local"])
else:
    model_name = st.selectbox("Choose Groq Model:", ["Groq-LLaMA2", "Groq-Mistral"])

user_input = st.text_input("Ask a question:")

if user_input:
    # Load selected model dynamically
    model = load_model(model_type, model_name)
   
   #Append model response as Human Message
    st.session_state.chat_history_local.append(HumanMessage(user_input))

    # Run model using chat history 
    result = model.invoke(st.session_state.chat_history_local)

    #Append model response as AIMessage
    st.session_state.chat_history_local.append(AIMessage(result.content))

    # Display the response
    st.write(result.content)

    # displaying chat history
    if st.checkbox("Show Chat History"):
        for msg in st.session_state.chat_history_local:
            role = "Human" if isinstance(msg, HumanMessage) else "AI"
            st.write(f"**{role}**: {msg.content}")

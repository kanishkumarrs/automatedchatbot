from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st

system_prompt = """You are a helpful assistant that determines if a user's question requires web scraping and provides responses in a strict JSON format:

{
    "needs_web_scraping": "Yes/No",
    "response": "answer_if_no_scraping_needed"
}

Rules:
- If web scraping is needed: needs_web_scraping = "Yes" and response = ""
- If no scraping needed: needs_web_scraping = "No" and provide the answer in response field
- Always maintain this JSON structure
- Consider the full conversation history when responding"""

groq_api=st.secrets["GROQ_API_KEY"]

def chat_with_history():
    chat = ChatGroq(
        api_key=groq_api,
        model_name="mixtral-8x7b-32768"
    )
    
    # Initialize messages list with system prompt
    messages = [SystemMessage(content=system_prompt)]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        # Add user message to history
        messages.append(HumanMessage(content=user_input))
        
        # Get response while passing full history
        response = chat.invoke(messages)
        
        # Add assistant response to history
        messages.append(response)
        
        print("Assistant:", response.content)
    
    return messages
chat_with_history()
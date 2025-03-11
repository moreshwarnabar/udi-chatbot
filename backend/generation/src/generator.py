import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class GeneratorAgent():
    def __init__(self, model: str = "llama-3.3-70b-versatile") -> None:
        self.llm = ChatGroq(model=model)
        self.generator_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a seasoned Customer Support Representative. "
                "You answer customer queries in a live-chat environment. "
                "Answer the following query based on the provided context. "
                "Context: {context} "
                "If the context is insufficient, ask for clarification or "
                "suggest alternative support channels. "
                "Your response should be short, concise, and professional. "
            )),
            ("user", "Query: {query}")
        ])
        self.formatter_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a seasoned Support Quality Assurance Specialist. "
                "You check the response from the customer support representative "
                "to ensure it is short, direct, and professional. "
                "Ensure the response is clear, concise, and well-structured. "
                "Query: {query} "
                "Format it with markdown syntax for easy readability using bullet points "
                "or spacing where necessary. "
            )),
            ("user", "Response: {response}")
        ])

    def generate_response(self, query: str, context: str) -> str:
        response = self.llm.invoke(
            self.generator_prompt.format(query=query, context=context)
        )

        return response.content
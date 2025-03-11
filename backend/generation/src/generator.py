from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

class GeneratorAgent():
    def __init__(self, model: str = "llama-3.3-70b-versatile") -> None:
        self.llm = ChatGroq(model=model)
        self.generator_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a seasoned Customer Support Representative. "
                "You answer customer queries in a live-chat environment. "
                "Your response should acknowledge the customer's query in a "
                "natural way. It should use a friendly and approachable tone, "
                "without being verbose and academic. The response should not exceed"
                "5 sentences. Answer the following query based on the provided context. "
                "Context: {context} "
                "If the context is insufficient, ask for clarification or "
                "suggest alternative support channels. Format your response in "
                "markdown for easy readability using bullet points where necessary. "
            )),
            ("user", "Query: {query}")
        ])

    def generate_response(self, query: str, context: str) -> str:
        response = self.llm.invoke(
            self.generator_prompt.format(query=query, context=context)
        )
        print(f"Response: {response.content}")

        return response.content
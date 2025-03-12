import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.response import Response, ContentBlock

class GeneratorAgent():
    def __init__(self, model: str = "llama-3.3-70b-versatile") -> None:
        self.llm = ChatGroq(model=model)
        self.generator_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a friendly Customer Support Representative. "
                "You answer customer queries in a live-chat environment. "
                "You are known for your friendly and approachable manner. "
                "Your response should acknowledge the customer's query in a "
                "natural way. It should use a friendly and approachable tone, "
                "without being verbose and academic. The response should not exceed "
                "5 sentences. End your response in a way that engages the customer to ask "
                "more questions. Answer the following query based on the provided context "
                "and formatting instructions. "
                "Context: {context} "
                "Formatting Instructions: {instructions}"
                "If the context is insufficient, ask for clarification or "
                "suggest alternative support channels. Your response should be formatted "
                "as per the following JSON format: \n "
                "{{\n"
                "  \"response\": [\n"
                "    {{ \"content\": \"text\" }}, \n"
                "    {{ \"content\": [\n"
                "      {{ \"text\": \"bullet\" }},\n"
                "      {{ \"text\": \"bullet\", \"subpoints\": [\n"
                "        {{ \"text\": \"nested bullet\" }}\n"
                "      ] }}\n"
                "    ] }}\n "
                "    {{ \"content\": \"text\" }}, \n"
                "  ]\n"
                "}}"
            )),
            ("user", "Query: {query}")
        ])

    def generate_response(self, query: str, context: str) -> str:
        parser = PydanticOutputParser(pydantic_object=Response)

        response = self.llm.invoke(
            self.generator_prompt.format_prompt(
                query=query, context=context, instructions=parser.get_format_instructions()
            )
        )
        
        try:
            resp_json = json.loads(response.content)
            val_resp = Response(**resp_json)
            return val_resp.model_dump_json()
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error decoding JSON: {e}")
            return self.generate_response(query, context)
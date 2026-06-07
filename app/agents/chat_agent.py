from app.core.llm import llm
from app.core.logger import logger


class ChatAgent:

    async def execute(self, query: str):
        logger.info("ChatAgent started", query=query)
        response = await llm.invoke(query)
        logger.info("ChatAgent completed", response_length=len(response))
        return response


chat_agent = ChatAgent()

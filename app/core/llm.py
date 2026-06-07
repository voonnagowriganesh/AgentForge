from groq import AsyncGroq

from app.core.config import get_settings
from app.core.logger import logger

settings = get_settings()
client = AsyncGroq(api_key=settings.GROQ_API_KEY)


class GroqLLM:

    async def invoke(self, prompt: str, temperature: float = 0.1):
        logger.info(
            "llm_invoke_start",
            model=settings.MODEL_NAME,
            prompt_length=len(prompt),
            temperature=temperature,
        )

        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )

        result = response.choices[0].message.content
        logger.info(
            "llm_invoke_result",
            response_length=len(result),
            response_preview=result[:200],
        )

        return result


llm = GroqLLM()

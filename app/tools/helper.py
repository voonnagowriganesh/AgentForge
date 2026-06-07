from app.tools.registry import TOOLS
from app.core.logger import logger


def get_available_tools():

    tools_text = []

    logger.info("get_avaible_tools function started executing")

    for name, meta in TOOLS.items():

        tools_text.append(f"- {name}: {meta['description']}")

    logger.info(f"list of tools_text : {tools_text}")

    return "\n".join(tools_text)

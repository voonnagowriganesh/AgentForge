from app.core.logger import logger
import re


def parse_math_query(query: str):
    logger.info("parse_math_query_started", query=query)

    query = query.lower()
    numbers = re.findall(r"\d+", query)
    logger.info("extracted_math_numbers", numbers=numbers)

    if len(numbers) < 2:
        logger.info("parse_math_query_skipped", reason="not_enough_numbers")
        return None

    a = numbers[0]
    b = numbers[1]

    if "add" in query or "addition" in query:
        expression = f"{a}+{b}"
        logger.info("parse_math_query_result", expression=expression)
        return expression

    if "subtract" in query:
        expression = f"{a}-{b}"
        logger.info("parse_math_query_result", expression=expression)
        return expression

    if "multiply" in query:
        expression = f"{a}*{b}"
        logger.info("parse_math_query_result", expression=expression)
        return expression

    if "divide" in query:
        expression = f"{a}/{b}"
        logger.info("parse_math_query_result", expression=expression)
        return expression

    logger.info("parse_math_query_skipped", reason="unknown_operation")
    return None

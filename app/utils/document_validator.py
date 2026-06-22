from app.core.logger import logger

# MIN_DOCUMENT_LENGTH = 100


# def is_valid_document_result(result: str) -> bool:

#     if not result:
#         return False

#     result = result.strip()

#     if len(result) < MIN_DOCUMENT_LENGTH:
#         return False

#     invalid_patterns = [
#         "TABLE OF CONTENTS",
#     ]

#     matches = 0

#     for pattern in invalid_patterns:
#         if pattern.lower() in result.lower():
#             matches += 1

#     if matches >= 1:
#         logger.info(
#             "document_validation_failed",
#             reason="too_many_noise_patterns",
#         )

#         return False

#     return True

MIN_DOCUMENT_LENGTH = 100


def is_valid_document_result(result: str) -> bool:

    if not result:
        return False

    result = result.strip()

    if len(result) < MIN_DOCUMENT_LENGTH:
        return False

    return True

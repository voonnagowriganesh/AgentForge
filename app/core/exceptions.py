class AgentException(Exception):
    pass


class ToolNotFoundException(AgentException):
    pass


class PlannerException(AgentException):
    pass


class RouterException(AgentException):
    pass


class InvalidPlanException(Exception):
    pass


class LLMResponseException(Exception):
    pass

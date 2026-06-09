import ast
import operator

from app.schemas.tool_response import ToolResponse

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def evaluate(node):

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):

        left = evaluate(node.left)
        right = evaluate(node.right)

        return OPERATORS[type(node.op)](left, right)

    raise ValueError("Invalid expression")


def calculate(expression: str):

    tree = ast.parse(expression, mode="eval")

    result = evaluate(tree.body)

    return ToolResponse(
        success=True,
        tool="calculator",
        result=result,
    ).model_dump()

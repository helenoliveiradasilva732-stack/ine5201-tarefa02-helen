"""Calculadora de operações básicas com interface gráfica."""

import ast
import operator
import math
from typing import Union


Numero = Union[int, float]
OPERADORES_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
OPERADORES_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _avaliar_no(no: ast.AST) -> Numero:
    if isinstance(no, ast.Expression):
        return _avaliar_no(no.body)
    if isinstance(no, ast.Constant) and type(no.value) in (int, float):
        if isinstance(no.value, float) and not math.isfinite(no.value):
            raise ValueError("Número inválido")
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in OPERADORES_BINARIOS:
        esquerda = _avaliar_no(no.left)
        direita = _avaliar_no(no.right)
        if isinstance(no.op, ast.Div) and direita == 0:
            raise ValueError("Não é possível dividir por zero")
        return OPERADORES_BINARIOS[type(no.op)](esquerda, direita)
    if isinstance(no, ast.UnaryOp) and type(no.op) in OPERADORES_UNARIOS:
        return OPERADORES_UNARIOS[type(no.op)](_avaliar_no(no.operand))
    raise ValueError("Expressão inválida")


def calcular(expressao: str) -> Numero:
    """Calcula uma expressão usando apenas +, -, * e /."""
    try:
        arvore = ast.parse(expressao, mode="eval")
        resultado = _avaliar_no(arvore)
    except (SyntaxError, OverflowError) as erro:
        raise ValueError("Expressão inválida") from erro
    if isinstance(resultado, float) and not math.isfinite(resultado):
        raise ValueError("Resultado inválido")
    return resultado

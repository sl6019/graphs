from functools import singledispatch
import expressions


class TreeNode:

    def __init__(self, value, *children):
        self.value = value
        self.children = children

    def __repr__(self):
        return f"{type(self).__name__}{(self.value,) + self.children}"

    def __str__(self):
        childstring = ",".join(map(str, self.children))
        return f"{self.value!s} -> ({childstring})"


def postvisitor(tree, fn):  # 比较常用的格式
    """Visit the tree from its end verticies."""
    return fn(tree, *(postvisitor(c, fn) for c in tree.children))


# **kwargs 版本
def postvisitor(expr, fn, **kwargs):  # noqa F811
    '''Traverse an Expression in postorder applying a function to every node.

    Parameters
    ----------
    expr: Expression
        The expression to be visited.
    fn: function(node, *o, **kwargs)
        A function to be applied at each node. The function should take the
        node to be visited as its first argument, and the results of visiting
        its operands as any further positional arguments. Any additional
        information that the visitor requires can be passed in as keyword
        arguments.
    **kwargs:
        Any additional keyword arguments to be passed to fn.
    '''
    return fn(expr,
              *(postvisitor(c, fn, **kwargs) for c in expr.operands),
              **kwargs)


def previsitor(tree, fn, fn_parent=None):
    """不常用."""
    fn_out = fn(tree, fn_parent)
    for child in tree.children:
        previsitor(child, fn, fn_out)


@singledispatch
def evaluate(expr, *o, **kwargs):
    """Evaluate an expression node.

    Parameters
    ----------
    expr: Expression
        The expression node to be evaluated.
    *o: numbers.Number
        The results of evaluating the operands of expr.
    **kwargs:
        Any keyword arguments required to evaluate specific
        types of expression.
    symbol_map: dict
        A dictionary mapping Symbol names to numerical values, for example:

        {'x': 1}
    """
    raise NotImplementedError(
        f"Cannot evaluate a {type(expr).__name__}")


@evaluate.register(expressions.Number)
def _(expr, *o, **kwargs):
    return expr.value


@evaluate.register(expressions.Symbol)
def _(expr, *o, symbol_map, **kwargs):
    return symbol_map[expr.value]


@evaluate.register(expressions.Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@evaluate.register(expressions.Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@evaluate.register(expressions.Mul)
def _(expr, *o, **kwargs):
    return o[0] * o[1]


@evaluate.register(expressions.Div)
def _(expr, *o, **kwargs):
    return o[0] / o[1]


@evaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    return o[0] ** o[1]

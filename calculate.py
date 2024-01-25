import ast
import astor
import inspect


def rewrite(func, args, subs):
    source = inspect.getsource(func)
    tree = ast.parse(source)

    def remove_decorators(node):
        for function in [n for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]:
            function.decorator_list = []

    remove_decorators(tree)

    class SourceReturner(ast.NodeTransformer):
        def visit_Return(self, node):
            self.generic_visit(node)

            return_expr = astor.to_source(node.value).strip()

            if subs:
                for arg_name, arg_value in zip(func.__code__.co_varnames, args):
                    return_expr = return_expr.replace(arg_name, str(arg_value))

            if return_expr.startswith('(') and return_expr.endswith(')'):
                return_expr = return_expr[1:-1]

            node.value = ast.Constant(return_expr)
            return node

    tree = SourceReturner().visit(tree)
    ast.fix_missing_locations(tree)

    return astor.to_source(tree)


def clean_expression(expr: str):
    return expr.replace("\n", "").replace("\r", "").replace("\t", "")


def evaluate_expression(expr):
    class ExpressionEvaluator(ast.NodeTransformer):
        def visit_Call(self, node):
            evaluated_args = [eval(astor.to_source(arg).strip())
                              for arg in node.args]
            node.args = [ast.Constant(value=arg) for arg in evaluated_args]
            return node

    tree = ast.parse(clean_expression(expr), mode='eval')

    transformed_tree = ExpressionEvaluator().visit(tree)

    return astor.to_source(transformed_tree).strip()


def calculate(func, args, eval=True, subs=True):
    if eval and not subs:
        raise ValueError('Cannot evaluate without substituting')

    rewritten_function_code = rewrite(func, args, subs)

    local_namespace = {}
    exec(rewritten_function_code, globals(), local_namespace)
    modified_func = local_namespace[func.__name__]

    expr = modified_func(*args)
    if eval:
        expr = evaluate_expression(expr)
        if expr.startswith('(') and expr.endswith(')'):
            expr = expr[1:-1]
    return expr

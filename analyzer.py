from tree import build_tree, tree_to_list_levels, tree_to_set
from calculate import calculate
import functools


def trace(stack):
    def decorator(func):
        depth = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal depth
            stack.append({"parameters": args, "depth": depth})
            depth += 1
            result = func(*args, **kwargs)
            depth -= 1
            return result

        return wrapper
    return decorator


def analyze(func, stack):
    func = func.__wrapped__

    stack_list = [[i["depth"], i["parameters"]] for i in stack]
    root = build_tree(stack_list)

    para_dict = {}
    para_list = list(tree_to_set(root))
    for i in para_list:
        para_dict[i] = calculate(func, i)

    system_stack = []

    curr = f"mystery({', '.join([str(j) for j in root.value])})"

    levels = tree_to_list_levels(root)

    bracket = False
    for level in levels:
        if len(stack) > 0 and stack[-1] != curr:
            system_stack.append(curr)

        for i in range(len(level) - 1, -1, -1):
            if bracket:
                curr = curr.replace(
                    f"mystery({', '.join([str(j) for j in level[i][0]])})", f"({para_dict[level[i][0]]}")
            else:
                curr = curr.replace(
                    f"mystery({', '.join([str(j) for j in level[i][0]])})", para_dict[level[i][0]])

    for i in range(len(para_list) - 1, -1, -1):
        if bracket:
            curr = curr.replace(
                f"mystery({', '.join([str(j) for j in para_list[i]])})", f"({para_dict[para_list[i]]}")
        else:
            curr = curr.replace(
                f"mystery({', '.join([str(j) for j in para_list[i]])})", para_dict[para_list[i]])

    if len(stack) > 0 and stack[-1] != curr:
        system_stack.append(curr)
    system_stack.append(str(eval(curr)))

    print("\n= ".join(system_stack))

    return system_stack

from collections import deque


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []


def build_tree(preorder_list):
    if not preorder_list:
        return None

    root = TreeNode(preorder_list[0][1])
    stack = [(0, root)]

    for depth, value in preorder_list[1:]:
        while stack and stack[-1][0] >= depth:
            stack.pop()

        new_node = TreeNode(value)
        if stack:
            stack[-1][1].children.append(new_node)

        stack.append((depth, new_node))

    return root


def print_tree(node, level=0):
    if node:
        print('  ' * level + str(node.value))
        for child in node.children:
            print_tree(child, level + 1)


def tree_to_list_levels(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            is_leaf = len(node.children) == 0
            level.append((node.value, is_leaf))

            for child in node.children:
                queue.append(child)

        result.append(level)

    return result


def tree_to_set(root):
    if not root:
        return set()

    result = set()
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.add(node.value)

        for child in node.children:
            queue.append(child)

    return result

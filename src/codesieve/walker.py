from tree_sitter import Tree


def treewalk(node: Tree):
    cursor = node.walk()
    isroot = False

    while not isroot:
        yield cursor.node

        if cursor.goto_first_child():
            continue
        if cursor.goto_next_sibling():
            continue

        retracing = True

        while retracing:
            if not cursor.goto_parent():
                retracing = False
                isroot = True
            if cursor.goto_next_sibling():
                retracing = False

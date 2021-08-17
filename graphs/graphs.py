

class TreeNode:

    def __init__(self, value, *children):
        self.value = value
        self.children = children

    def __repr__(self):
        return f"{type(self).__name__}{(self.value,) + self.children}"

    def __str__(self):
        childstring = ",".join(map(str, self.children))
        return f"{self.value!s} -> ({childstring})"

class FamilyRelations:
    def __init__(self):
        self.relations = {
            "parent": [
                ("homer", "bart"), ("homer", "lisa"), ("homer", "maggie"),
                ("marge", "bart"), ("marge", "lisa"), ("marge", "maggie"),
                ("abraham", "homer"), ("mona", "homer"),
                ("clancy", "marge"), ("jacqueline", "marge")
            ]
        }

    def check_parent(self, parent, child):
        """Check if one is a parent of the other."""
        return (parent, child) in self.relations.get("parent", [])

    def check_grandparent(self, grandparent, grandchild):
        """Check if one is a grandparent of the other using parent relation."""
        possible_parents = {child for _, child in self.relations["parent"]}
        return any(
            self.check_parent(grandparent, parent) and self.check_parent(parent, grandchild)
            for parent in possible_parents
        )

    def verify_relation(self, relation_type, person1, person2):
        """General method to verify family relations."""
        if relation_type == "parent":
            return self.check_parent(person1, person2)
        elif relation_type == "grandparent":
            return self.check_grandparent(person1, person2)
        return False

family_tree = FamilyRelations()

test_cases = [
    ("grandparent", "abraham", "bart"),
    ("grandparent", "mona", "lisa"),
    ("parent", "homer", "bart"),
    ("grandparent", "marge", "bart")
]

for relation, x, y in test_cases:
    result = family_tree.verify_relation(relation, x, y)
    print(f"Is {x} a {relation} of {y}? {result}")

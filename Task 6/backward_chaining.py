class Proposition:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def __repr__(self):
        return f"{self.name}({', '.join(self.parameters)})"

class Implication:
    def __init__(self, result, premises):
        self.result = result
        self.premises = premises

    def __repr__(self):
        premise_repr = ', '.join(map(str, self.premises))
        return f"{self.result} if {premise_repr}"

def rebind_terms(proposition, bindings):
    substituted_terms = [bindings.get(term, term) for term in proposition.parameters]
    return Proposition(proposition.name, substituted_terms)

def align_terms(target, pattern):
    term_bindings = {}
    index = 0
    while index < len(target.parameters):
        target_param = target.parameters[index]
        pattern_param = pattern.parameters[index]
        if target_param.startswith('?'):
            term_bindings[target_param] = pattern_param
        if pattern_param.startswith('?'):
            term_bindings[pattern_param] = target_param
        elif target_param != pattern_param:
            return None
        index += 1
    return term_bindings

def check_match(goal, existing_fact):
    if goal.name != existing_fact.name:
        return False
    index = 0
    while index < len(goal.parameters):
        target_param = goal.parameters[index]
        fact_param = existing_fact.parameters[index]
        if not (target_param == fact_param or '?' in target_param):
            return False
        index += 1
    return True

def resolve_goal(implications, base_facts, query, current_bindings=None):
    if current_bindings is None:
        current_bindings = {}

    instantiated_query = rebind_terms(query, current_bindings)

    fact_index = 0
    while fact_index < len(base_facts):
        if check_match(instantiated_query, base_facts[fact_index]):
            print(f"Verified: {instantiated_query} from facts.")
            return True, current_bindings
        fact_index += 1

    impl_index = 0
    while impl_index < len(implications):
        implication = implications[impl_index]
        if implication.result.name == query.name:
            possible_bindings = align_terms(instantiated_query, implication.result)
            if possible_bindings:
                combined_bindings = {**current_bindings, **possible_bindings}
                print(f"Applying: {implication}")
                all_premises_hold = True
                premise_index = 0
                while premise_index < len(implication.premises):
                    premise = implication.premises[premise_index]
                    valid, new_bindings = resolve_goal(implications, base_facts, premise, combined_bindings)
                    if not valid:
                        all_premises_hold = False
                        break
                    combined_bindings.update(new_bindings)
                    premise_index += 1
                if all_premises_hold:
                    return True, combined_bindings
        impl_index += 1

    print(f"Failed to resolve: {instantiated_query}")
    return False, current_bindings

base_facts = [
    Proposition("parent", ["homer", "bart"]),
    Proposition("parent", ["homer", "lisa"]),
    Proposition("parent", ["homer", "maggie"]),
    Proposition("parent", ["marge", "bart"]),
    Proposition("parent", ["marge", "lisa"]),
    Proposition("parent", ["marge", "maggie"]),
    Proposition("parent", ["abraham", "homer"]),
    Proposition("parent", ["mona", "homer"]),
    Proposition("parent", ["clancy", "marge"]),
    Proposition("parent", ["jacqueline", "marge"])
]

implications = [
    Implication(Proposition("grandparent", ["?x", "?y"]), [
        Proposition("parent", ["?x", "?z"]),
        Proposition("parent", ["?z", "?y"])
    ])
]

query_goal = Proposition("grandparent", ["abraham", "bart"])

result, final_bindings = resolve_goal(implications, base_facts, query_goal)
print(f"Result: {result}, Bindings: {final_bindings}")

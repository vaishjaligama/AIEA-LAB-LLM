import swiplserver

def assert_prolog_data(prolog_thread, data, label):
    for item in data:
        command = f"assertz({item})" if label == "fact" else f"assertz(({item}))."
        print(f"Adding {label}: {command}")
        try:
            prolog_thread.query(command)
        except swiplserver.prologmqi.PrologError as e:
            print(f"Error while adding {label}: {e}")

def run_prolog_queries(prolog_thread, queries):
    for query in queries:
        command = f"{query}."
        print(f"Running Query: {command}")
        try:
            result = prolog_thread.query(command)
            print(f"Query: {query} -> Result: {result}")
        except swiplserver.prologmqi.PrologError as e:
            print(f"Error executing query '{query}': {e}")

if __name__ == "__main__":
    family_facts = [
        "parent(homer, bart)",
        "parent(homer, lisa)",
        "parent(homer, maggie)",
        "parent(marge, bart)",
        "parent(marge, lisa)",
        "parent(marge, maggie)",
        "parent(abraham, homer)",
        "parent(mona, homer)",
        "parent(clancy, marge)",
        "parent(jacqueline, marge)"
    ]

    family_rules = [
        "grandparent(X, Y) :- parent(X, Z), parent(Z, Y)"
    ]

    with swiplserver.PrologMQI() as mqi:
        with mqi.create_thread() as thread:
            assert_prolog_data(thread, family_facts, "fact")
            assert_prolog_data(thread, family_rules, "rule")

            test_queries = [
                "parent(homer, bart)",
                "parent(marge, maggie)",
                "grandparent(abraham, bart)",
                "grandparent(clancy, bart)",
                "grandparent(X, bart)"
            ]

            run_prolog_queries(thread, test_queries)

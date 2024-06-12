import openai
import swiplserver
import re
import tempfile

openai.api_key = ''


def convert_natural_language_to_prolog(prompt):
    """ Convert natural language descriptions into Prolog facts and rules using OpenAI's API. """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a skilled assistant tasked with translating English descriptions into Prolog syntax."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def extract_prolog_code(symbolic_response):
    """ Extracts Prolog code from a response, assuming it might be formatted within code blocks. """
    code_match = re.search(r'```prolog\n(.*?)\n```', symbolic_response, re.DOTALL)
    return code_match.group(1).strip() if code_match else symbolic_response.strip()

def run_prolog_queries(prolog_code):
    """ Runs Prolog queries using swiplserver and handles the temporary file creation. """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pl', delete=False) as temp_file:
        temp_file.write(prolog_code)
        file_path = temp_file.name

    queries = ["grandparent(abraham, bart)", "grandparent(X, bart)"]
    results = []

    with swiplserver.PrologMQI() as mqi:
        with mqi.create_thread() as thread:
            consult_command = f"consult('{file_path}')."
            print(f"Loading Prolog file: {consult_command}")
            thread.query(consult_command)

            for query in queries:
                result = execute_prolog_query(thread, query)
                results.append(result)

    return results

def execute_prolog_query(prolog_thread, query):
    """ Executes a single Prolog query and handles potential errors. """
    query_command = f"{query}."
    print(f"Executing Query: {query_command}")
    try:
        return prolog_thread.query(query_command)
    except swiplserver.prologmqi.PrologError as e:
        print(f"Error during query '{query_command}': {e}")

if __name__ == "__main__":
    prompt_description = "Translate the following problem into Prolog facts and rules: Homer is the father of Bart and Lisa. Marge is the mother of Bart and Lisa. Abraham is the father of Homer. Who are the grandparents of Bart?"
    symbolic_output = convert_natural_language_to_prolog(prompt_description)
    print("Symbolic Formulation:\n", symbolic_output)

    prolog_code = extract_prolog_code(symbolic_output)
    print("Extracted Prolog Code:\n", prolog_code)

    query_results = run_prolog_queries(prolog_code)
    print("Query Results:\n", query_results)

import openai
import swiplserver
import time

openai.api_key = ''

def translate_to_prolog(statement):
    prompt = [
        {"role": "system", "content": "You are a competent assistant."},
        {"role": "user", "content": f"Convert this sentence into a Prolog fact: '{statement}'"}
    ]
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt
            )
            prolog_statement = response['choices'][0]['message']['content'].strip()
            if not prolog_statement.endswith('.'):
                prolog_statement += '.'
            return prolog_statement
        except openai.error.RateLimitError:
            print("Exceeded API rate limit, retrying after 60 seconds...")
            time.sleep(60)

def execute_prolog_fact(fact):
    prolog_command = f"assertz({fact[:-1]})."
    try:
        with swiplserver.PrologMQI() as mqi:
            with mqi.create_thread() as thread:
                thread.query(prolog_command)
                results = thread.query(fact[:-1])
                return results
    except swiplserver.prologmqi.PrologError as error:
        print(f"Encountered a Prolog issue: {error}")

if __name__ == "__main__":
    input_sentence = "The cat is sleeping"
    prolog_fact = translate_to_prolog(input_sentence)
    print(f"Prolog Fact: {prolog_fact}")

    result = execute_prolog_fact(prolog_fact)
    if result:
        print("Fact successfully added and verified in Prolog.")
    else:
        print("Failed to add or verify the fact.")

import openai

openai.api_key = ''

def get_short_story(intro_line):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative writer."},
                {"role": "user", "content": f"Write a short story that starts with: '{intro_line}'"}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    intro_line = "On a chilly winter evening, an old man sat by the fireplace, knitting a scarf."

    short_story = get_short_story(intro_line)

    if short_story:
        print("\nGenerated Short Story:")
        print(short_story)

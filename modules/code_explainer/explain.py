import re

from openai import OpenAI

client = OpenAI(api_key='')


def explain_code_snippet(code):
    print("Inside explain")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a technical assistant, skilled in explaining code snippets in a "
                                          "simple way."},
            {"role": "user", "content": "Explain the code snippet below between %. Use a maximum of 5 bullet points and "
                                        "aim to explain the functionality at a high-level and any important concepts in "
                                        "the snippet, such as design patterns or known algorithms."
                                        "Code: % "+compress_code(code)+" %."}
        ]
    )

    return completion.choices[0].message.content


def compress_code(code):
    # Remove comments
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.S)
    # Remove spaces around operators and punctuations
    code = re.sub(r'\s*([{};=()\[\],])\s*', r'\1', code)
    # Replace multiple newlines and spaces with a single space
    code = re.sub(r'\s+', ' ', code)
    # Remove spaces before semicolons
    code = re.sub(r'\s*;', ';', code)
    # Strip leading/trailing whitespace
    code = code.strip()
    return code

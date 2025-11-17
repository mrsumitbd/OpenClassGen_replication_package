import sys
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from together import Together
import openai, backoff, os, ast, anthropic
from dotenv import load_dotenv
load_dotenv('../.env')

def extract_relevant_code_snippets(code, class_to_extract):
    tree = ast.parse(code)

    # adding parent info
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    relevant_snippet_with_parent_list = []

    for node in ast.walk(tree):
        if type(node).__name__ == "ClassDef":
            if node.name == class_to_extract:
                try:
                    parent = node.parent.name
                except:
                    parent = None
                relevant_snippet_with_parent_list.append((ast.get_source_segment(code, node, padded=True), parent))

    return relevant_snippet_with_parent_list[0][0]


def generate_with_claude(skeleton, model, reasoning=False):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    code_snippet = None

    # defining exponential backoff
    @backoff.on_exception(backoff.expo, anthropic.RateLimitError)
    def completions_with_backoff(**kwargs):
        return client.messages.create(**kwargs)

    if not reasoning:
        response = completions_with_backoff(
            model=model,
            max_tokens=8192,
            temperature=0.0,
            messages=[
                {
                    "role": "user",
                    "content": f"You are an expert Python programmer who can correctly implement complete Python classes based on the provided class skeleton. Implement the following class. Do not explain the code. The given class skeleton is as follows:\n{skeleton}"
                }
            ]
        )
        code_snippet = response.content[0].text

    else:
        response = completions_with_backoff(
            model=model,
            max_tokens=8192,
            temperature=1,
            thinking={
                "type": "enabled",
                "budget_tokens": 5000
            },
            messages=[
                {
                    "role": "user",
                    "content": f"You are an expert Python programmer who can correctly implement complete Python classes based on the provided class skeleton. Implement the following class. Do not explain the code. The given class skeleton is as follows:\n{skeleton}"
                }
            ]
        )
        for block in response.content:
            if block.type == "text":
                code_snippet = block.text

    return code_snippet


def generate_with_together(skeleton, model):
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

    response = client.chat.completions.create(
        model=model,
        temperature=0.0,
        messages=[
            {
                "role": "assistant",
                "content": "You are an expert Python programmer who can correctly implement complete Python classes based on the provided class skeleton."
            },
            {
                "role": "user",
                "content": f"Implement the following class. Do not explain the code. The given class skeleton is as follows:\n{skeleton}"
            }
        ]
    )
    code_snippet = response.choices[0].message.content

    return code_snippet


def generate_with_openai(skeleton, model):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # defining exponential backoff
    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    def completions_with_backoff(**kwargs):
        return client.chat.completions.create(**kwargs)

    response = completions_with_backoff(
        model=model,
        # reasoning={"effort": "low"},
        temperature=0.0,
        messages=[
            {
                "role": "developer",
                "content": "You are an expert Python programmer who can correctly implement complete Python classes based on the provided class skeleton."
            },
            {
                "role": "user",
                "content": f"Implement the following class. Do not explain the code. The given class skeleton is as follows:\n{skeleton}"
            }
        ]
    )
    code_snippet = response.choices[0].message.content

    return code_snippet

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_esg_question(question, dataframe):

    context = dataframe.to_string()

    prompt = f"""
    You are an ESG financial analyst.

    Here is the company ESG dataset:
    {context}

    Answer the question:
    {question}

    Provide a concise professional answer.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]

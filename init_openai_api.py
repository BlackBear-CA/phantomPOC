# Replace "your_openai_api_key" with your actual OpenAI API key
openai_api_key = "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"
llm = OpenAI(api_key=openai_api_key)

def generate_text(prompt):
    response = llm(prompt)
    return response


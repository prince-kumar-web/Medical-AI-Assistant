from llama_cpp import Llama


MODEL_PATH = "models/qwen/qwen2.5-1.5b-instruct-q4_k_m.gguf"


# Load model once
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
    verbose=False
)


def generate_health_response(user_message):

    prompt = f"""<|im_start|>system
You are a medical education assistant.

Rules:
- Give general educational information only.
- Do not diagnose the user.
- Do not prescribe personalized medicines.
- Do not claim certainty about a disease.
- If symptoms may indicate an emergency, advise seeking urgent professional medical care.
- Keep responses clear and concise.

<|im_end|>
<|im_start|>user
{user_message}
<|im_end|>
<|im_start|>assistant
"""

    output = llm(
        prompt,
        max_tokens=250,
        temperature=0.3,
        stop=["<|im_end|>"]
    )

    response = output["choices"][0]["text"].strip()

    return response
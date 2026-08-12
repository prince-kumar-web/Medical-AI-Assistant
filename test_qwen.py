from llama_cpp import Llama

MODEL_PATH = "models/qwen/qwen2.5-1.5b-instruct-q4_k_m.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8,
    verbose=False
)

prompt = """<|im_start|>system
You are a helpful medical education assistant.
Give general educational information only.
Do not diagnose or prescribe personalized treatment.
<|im_end|>
<|im_start|>user
I have a headache since yesterday. What general information can you give me?
<|im_end|>
<|im_start|>assistant
"""

output = llm(
    prompt,
    max_tokens=200,
    temperature=0.3,
    stop=["<|im_end|>"]
)

print("\n===== QWEN RESPONSE =====\n")
print(output["choices"][0]["text"])
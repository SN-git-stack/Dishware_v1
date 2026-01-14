import os
import argparse
import json
import urllib.request
import urllib.error
from agents.generation_agents import director_summarizer

def call_local_llm(messages, model="local-model", temperature=0.7):
    url = "http://localhost:1234/v1/chat/completions"
    payload = {"model": model, "messages": messages, "temperature": temperature, "stream": False}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.load(response)['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def read_file(filepath):
    if not os.path.exists(filepath): return ""
    with open(filepath, 'r', encoding='utf-8') as f: return f.read()

def generate_director_brief(cr_filepath):
    print(f"--- Generating Director's Brief ---")
    
    # 1. Load CR
    cr_content = read_file(cr_filepath)
    if not cr_content:
        print("CR File not found.")
        return

    # 2. Try to load Func Spec (if exists) for better context
    base, _ = os.path.splitext(cr_filepath)
    spec_path = f"{base}_FUNC_SPEC.md"
    spec_content = read_file(spec_path)
    
    context = f"CHANGE REQUEST:\n{cr_content}\n"
    if spec_content:
        print(f"Found associated Functional Spec: {os.path.basename(spec_path)}")
        context += f"\nFUNCTIONAL SPEC:\n{spec_content}"
    else:
        print("No Functional Spec found (generating update based on CR only).")

    # 3. Call Agent
    print("Consulting Director Summarizer...")
    messages = [
        {"role": "system", "content": director_summarizer.system_instruction},
        {"role": "user", "content": f"Generate Brief from:\n{context}"}
    ]
    brief_content = call_local_llm(messages)

    # 4. Save
    output_path = f"{base}_DIRECTOR_BRIEF.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(brief_content)
        
    print(f"\nSuccess! Brief created at:\n{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Director's Brief from a CR.")
    parser.add_argument("cr_file", help="Path to the CR file.")
    args = parser.parse_args()
    generate_director_brief(args.cr_file)

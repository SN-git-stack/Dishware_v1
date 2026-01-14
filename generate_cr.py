import os
import argparse
import json
import urllib.request
import urllib.error
import re
from agents.generation_agents import requirements_analyst

def call_local_llm(messages, model="local-model", temperature=0.7):
    """
    Sends a request to the local LLM server.
    """
    url = "http://localhost:1234/v1/chat/completions"
    payload = {
        "model": model, "messages": messages, "temperature": temperature, "stream": False
    }
    
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.load(response)
            return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def sanitize_filename(name):
    s = name.lower().replace(" ", "_")
    return re.sub(r'[^a-z0-9_-]', '', s)

def generate_cr(raw_input: str):
    print(f"--- Generating Change Request from Input ---")
    print(f"Input: {raw_input}\n")

    # Call AI
    print("Consulting Requirements Analyst Agent...")
    messages = [
        {"role": "system", "content": requirements_analyst.system_instruction},
        {"role": "user", "content": f"Raw Requirement:\n{raw_input}"}
    ]
    
    generated_content = call_local_llm(messages)
    
    # Extract Title to make filename
    match = re.search(r'\*\*CR Title:\*\* (.*)', generated_content)
    title = match.group(1).strip() if match else "generated_cr"
    
    # Create structure
    safe_title = sanitize_filename(title)
    base_dir = os.path.join("change_requests", safe_title)
    os.makedirs(base_dir, exist_ok=True)
    
    output_path = os.path.join(base_dir, f"{safe_title}.md")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(generated_content)
        
    print(f"\nSuccess! Change Request created at:\n{output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a CR from vague text.")
    parser.add_argument("input", help="The raw requirement text.")
    args = parser.parse_args()
    generate_cr(args.input)

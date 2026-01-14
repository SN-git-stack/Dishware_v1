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

def generate_cr(input_source: str) -> dict:
    """
    Generates a CR from a string or a file path. 
    Returns a dict with {"success": bool, "path": str, "error": str}.
    """
    # 1. Determine if input is a file path or raw text
    raw_input = input_source
    if os.path.exists(input_source) and (input_source.endswith(".txt") or input_source.endswith(".md")):
        print(f"Reading input from file: {input_source}")
        try:
            with open(input_source, "r", encoding="utf-8") as f:
                raw_input = f.read()
        except Exception as e:
            return {"success": False, "path": "", "error": f"Failed to read file: {e}"}

    print(f"--- Generating Change Request from Input ---")
    # print(f"Input Preview: {raw_input[:100]}...") 

    # 2. Call AI
    print("Consulting Requirements Analyst Agent...")
    messages = [
        {"role": "system", "content": requirements_analyst.system_instruction},
        {"role": "user", "content": f"Raw Requirement:\n{raw_input}"}
    ]
    
    generated_content = call_local_llm(messages)
    
    # 3. Extract Title
    match = re.search(r'\*\*CR Title:\*\* (.*)', generated_content)
    title = match.group(1).strip() if match else "generated_cr"
    
    # 4. Create structure
    safe_title = sanitize_filename(title)
    base_dir = os.path.join("change_requests", safe_title)
    os.makedirs(base_dir, exist_ok=True)
    
    output_path = os.path.join(base_dir, f"{safe_title}.md")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(generated_content)
        
    print(f"\nSuccess! Change Request created at:\n{output_path}")
    
    # Return structured data for Web View / API
    return {
        "success": True, 
        "path": output_path, 
        "base_dir": base_dir,
        "title": title
    }

# --- Web View Handler ---
def handle_web_request(text_content: str):
    """
    Entry point for future Web UI to submit text directly.
    """
    return generate_cr(text_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a CR from vague text or a .txt file.")
    parser.add_argument("input", help="The raw requirement text OR path to a .txt file.")
    args = parser.parse_args()
    
    result = generate_cr(args.input)
    if not result["success"]:
        print(f"Error: {result.get('error')}")
        exit(1)

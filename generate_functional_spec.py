import os
import argparse
import json
import urllib.request
import urllib.error
from agents.definitions import system_architect, qa_strategist
from agents.generation_agents import functional_spec_writer

# --- Copying Helper for now (Ideally move to utils.py) ---
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
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def consult_agent(agent, context_content):
    print(f"   > Consulting {agent.role_name}...")
    messages = [
        {"role": "system", "content": agent.system_instruction},
        {"role": "user", "content": f"Review this CR and provide your specific feedback (Constraints/Risks/Edge Cases):\n\n{context_content}"}
    ]
    return call_local_llm(messages)

def generate_functional_spec(cr_filepath):
    print(f"--- 1. Loading Change Request ---")
    if not os.path.exists(cr_filepath):
        print("File not found.")
        return
    cr_content = read_file(cr_filepath)
    print(f"Loaded: {os.path.basename(cr_filepath)}")

    print(f"\n--- 2. Consulting Experts (Architect & QA) ---")
    
    # Consult Architect
    architect_feedback = consult_agent(system_architect, cr_content)
    # Consult QA
    qa_feedback = consult_agent(qa_strategist, cr_content)

    print(f"\n--- 3. Synthesizing Functional Specification ---")
    print("   > Writing Document...")
    
    synthesis_context = f"""
    ORIGINAL CR:
    {cr_content}

    ARCHITECT FEEDBACK (Constraints/API):
    {architect_feedback}

    QA FEEDBACK (Edge Cases):
    {qa_feedback}
    """

    messages = [
        {"role": "system", "content": functional_spec_writer.system_instruction},
        {"role": "user", "content": f"Generate the Functional Specification based on these inputs:\n{synthesis_context}"}
    ]
    
    spec_content = call_local_llm(messages)

    # --- Generate Executive Summary for the Spec ---
    print("   > Generating Executive Summary...")
    summary_prompt = "Summarize this Functional Specification for a Lead Developer in 5 bullet points (Scope, Key Tech Changes, Risks)."
    summary_messages = [
        {"role": "system", "content": "You are a Technical Lead."},
        {"role": "user", "content": f"{summary_prompt}\n\nSPEC CONTENT:\n{spec_content}"}
    spec_content = call_local_llm(messages)

    # Save: Functional Spec (Detailed)
    base, _ = os.path.splitext(cr_filepath)
    path_spec = f"{base}_FUNC_SPEC.md"
    with open(path_spec, "w", encoding="utf-8") as f:
        f.write(f"# Functional Specification: {os.path.basename(cr_filepath)}\n\n")
        f.write(spec_content)
    print(f"\nSuccess! Detailed Spec created at:\n{path_spec}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Functional Spec from a CR.")
    parser.add_argument("cr_file", help="Path to the existing CR markdown file.")
    args = parser.parse_args()
    generate_functional_spec(args.cr_file)

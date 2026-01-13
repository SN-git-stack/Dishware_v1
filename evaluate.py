import os
import argparse
from agents.definitions import ALL_AGENTS, AgentPersona

def read_file(filepath):
    """Reads the content of the CR file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def load_knowledge_base(kb_dir: str) -> str:
    """Reads all markdown files from the knowledge base directory."""
    if not os.path.exists(kb_dir):
        return ""
    
    print(f"Loading Knowledge Base from: {kb_dir}")
    kb_content = []
    for filename in os.listdir(kb_dir):
        if filename.endswith(".md"):
            path = os.path.join(kb_dir, filename)
            content = read_file(path)
            kb_content.append(f"--- DOCUMENT: {filename} ---\n{content}\n")
    
    return "\n".join(kb_content)

import json
import urllib.request
import urllib.error

def call_local_llm(messages, model="local-model", temperature=0.7):
    """
    Sends a request to the local LLM server (compatible with OpenAI API).
    Default URL: http://localhost:1234/v1/chat/completions
    """
    url = "http://localhost:1234/v1/chat/completions"
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.load(response)
            return result['choices'][0]['message']['content']
    except urllib.error.URLError as e:
        return f"Error connecting to Local LLM at {url}: {e}. Is LMStudio/Ollama running?"

def get_ai_response(agent: AgentPersona, cr_content: str, kb_context: str) -> str:
    """
    Generates an AI response using the local LLM.
    """
    print(f"\n--- [Consulting {agent.role_name} via Local LLM] ---")
    
    system_prompt = f"""
{agent.system_instruction}

--- KNOWLEDGE BASE CONTEXT ---
Use the following context to check for violations or rules.
{kb_context}
"""

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": f"Evaluate this Change Request:\n\n{cr_content}"}
    ]
    
    return call_local_llm(messages)

def evaluate_cr(cr_filepath: str):
    print(f"Loading Change Request from: {cr_filepath}...")
    try:
        cr_content = read_file(cr_filepath)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Load RAG Context
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base")
    kb_context = load_knowledge_base(kb_path)
    if kb_context:
        print(f"Loaded {len(kb_context)} characters of context context.")

    print("\nStarting Multi-Agent Evaluation...\n" + "="*40)

    results = {}
    
    for agent in ALL_AGENTS:
        print(f"\n> Agent: {agent.role_name}")
        print(f"> Focus: {', '.join(agent.focus_areas)}")
        
        # Here we invoke the "AI" with Context
        response = get_ai_response(agent, cr_content, kb_context)
        
        results[agent.role_name] = response
        print(f"\n{response}\n" + "-"*40)

    print("\nEvaluation Complete.")
    
    # Save Report
    base, _ = os.path.splitext(cr_filepath)
    output_path = f"{base}_REPORT.md"
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(f"# Evaluation Report for {os.path.basename(cr_filepath)}\n\n")
        f.write(f"**Date**: {os.getcwd()}\n\n")
        
        for role, analysis in results.items():
            f.write(f"## {role}\n")
            f.write(analysis + "\n\n")
            
    print(f"Report saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a POS Change Request using AI Agents.")
    parser.add_argument("file", help="Path to the Change Request markdown file.")
    
    args = parser.parse_args()
    evaluate_cr(args.file)

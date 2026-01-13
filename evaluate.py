import os
import argparse
from agents.definitions import ALL_AGENTS, AgentPersona

def read_file(filepath):
    """Reads the content of the CR file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def simulate_llm_response(agent: AgentPersona, cr_content: str) -> str:
    """
    Mocks an LLM response. In a real system, this would call OpenAI/Gemini API.
    """
    print(f"\n--- [Simulating AI Evaluation for: {agent.role_name}] ---")
    # In a real scenario, we would send 'agent.system_instruction' + 'cr_content' to the model.
    
    # Mock logic for demonstration
    if "Product Owner" in agent.role_name:
        return f"""
**Decision**: Approve
**Reasoning**:
* Aligns with the roadmap for Q3.
* ROI is positive based on projected efficiency gains.
**Priority**: High
"""
    elif "Architect" in agent.role_name:
        return f"""
**Feasibility**: Yes, but with cautions.
**Architectural Impact**: Medium
**Technical Constraints**:
* Ensure offline sync logic handles conflict resolution (Last-Write-Wins is not enough).
"""
    elif "Security" in agent.role_name:
        return f"""
**Compliance Check**: Review Needed
**Security Risks**:
* If this involves customer data, we need to verify encryption at rest.
"""
    else:
        return f"**Analysis**: Looks reasonable. Proceed with standard {agent.role_name} checks."

def evaluate_cr(cr_filepath: str):
    print(f"Loading Change Request from: {cr_filepath}...")
    try:
        cr_content = read_file(cr_filepath)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\nStarting Multi-Agent Evaluation...\n" + "="*40)

    results = {}
    
    for agent in ALL_AGENTS:
        print(f"\n> Agent: {agent.role_name}")
        print(f"> Focus: {', '.join(agent.focus_areas)}")
        
        # Here we invoke the "AI"
        response = simulate_llm_response(agent, cr_content)
        
        results[agent.role_name] = response
        print(f"\n{response}\n" + "-"*40)

    print("\nEvaluation Complete.")
    
    # Save Report
    output_path = cr_filepath.replace(".md", "_REPORT.md")
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

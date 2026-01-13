# Dishware V1 - POS Change Request Evaluation System

This project implements a Multi-Agent System to evaluate Change Requests (CRs) for a Point of Sale (POS) application.

## 🧠 Project Memory / Context

**Goal**: Automate the initial review of features/requests using AI agents representing different stakeholders (Product Owner, Architect, Security, etc.).

### System Architecture
- **Orchestrator**: `evaluate.py` - Main script that loads a CR and queries agents.
- **Agents**: Defined in `agents/definitions.py`. Each has a specific persona and system prompt.
- **Input**: Markdown files in `templates/` format.
- **Output**: Markdown reports (e.g., `_REPORT.md`).

### Current Status (as of Jan 2026)
- The system uses a **Simulated LLM** (mocked responses) in `evaluate.py` to demonstrate the workflow.
- **TODO**: Replace `simulate_llm_response` with actual API calls to OpenAI/Gemini by adding an API key handling mechanism.

## 🚀 How to Run

1. **Install Python 3.x**
2. **Run Evaluation**:
   ```powershell
   python evaluate.py sample_cr.md
   ```

## Repository Structure
- `agents/`: Agent definitions.
- `templates/`: CR templates.
- `evaluate.py`: Main script.
- `sample_cr.md`: Example input.

## Future Plans
- [ ] Integrate real LLM API.
- [ ] Add PDF parsing support for legacy CRs.
- [ ] Create a Web UI for submission.

# Dishware V1 - POS Change Request Evaluation System

This project implements a Multi-Agent System to evaluate Change Requests (CRs) for a Point of Sale (POS) application.

## 🧠 Project Memory / Context

**Goal**: Automate the initial review of features/requests using AI agents representing different stakeholders (Product Owner, Architect, Security, etc.).

### System Architecture
- **Orchestration Layers**:
    1.  **Generation**: `generate_cr.py` & `generate_functional_spec.py` (Create content).
    2.  **Evaluation**: `evaluate.py` (Review content).
    3.  **Summarization**: `generate_director_brief.py` (Strategic view).
- **Agents**: Defined in `agents/definitions.py` (Evaluators) and `agents/generation_agents.py` (Creators).
- **Knowledge Base (RAG)**: `knowledge_base/` containing policy docs.
- **Web handlers**: `web_handlers.py` for future API integration.

### Current Status (Version 2.0 - Jan 2026)
- **Full Lifecycle Support**: From "Idea" -> "CR" -> "Spec" -> "Evaluation".
- **Context Aware**: Agents are configured for **C#/.NET Core & XML** architecture.
- **Director-Ready**: Dedicated scripts to generate high-level strategic briefs (`_DIRECTOR_BRIEF.md`).
- **Input Flexibility**: CLI accepts raw text or `.txt` files.

## 🚀 How to Run

1. **Create a Request**:
   ```powershell
   python create_cr.py "My New Feature"
   ```
   This creates `change_requests/my_new_feature/my_new_feature.md`.

2. **Run Evaluation**:
   ```powershell
   python evaluate.py change_requests/my_new_feature/my_new_feature.md
   ```

3. **View Report**:
   Open `change_requests/my_new_feature/my_new_feature_REPORT.md` to see the Director's Summary and Agent details.

## Repository Structure
- `agents/`: Agent personas.
- `change_requests/`: Database of CRs (one folder per CR).
- `knowledge_base/`: RAG context files.
- `templates/`: Templates.

## Future Plans
- [ ] Integrate real LLM API.
- [ ] Add PDF parsing support for legacy CRs.
- [ ] Create a Web UI for submission.

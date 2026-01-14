# POS Change Request System - User Manual

## 1. Prerequisites
Before running the scripts, ensure you have:
1.  **Python 3.8+** installed.
2.  **Local LLM Running**:
    - Recommended: **LM Studio** or **Ollama**.
    - Configuration: Must be running a local server at `http://localhost:1234`.
    - Note: If using a different port, update the `url` variable in the scripts.

---

## 2. Typical Workflow
The system is designed to support the lifecycle of a feature request from **Idea** to **Evaluation**.

### Step A: Generate a Change Request (CR)
*Turn a vague idea into a formal structure.*

**Command:**
```powershell
# Option 1: Direct Text
python generate_cr.py "We need a way to split bills by item."

# Option 2: From File (Recommended for long inputs)
python generate_cr.py my_feature_idea.txt
```
**Output:**
-   Creates: `change_requests/split_bills/split_bills.md`
-   Content: Structured CR with Business Value, UACs, and inferred Tech Context.

---

### Step B: Generate a Functional Specification
*Turn the CR into a detailed tech spec for developers.*

**Command:**
```powershell
python generate_functional_spec.py change_requests/split_bills/split_bills.md
```
**Process:**
1.  Consults **System Architect** (Checks C#/.NET alignment, XML Schema).
2.  Consults **QA Strategist** (Identifies edge cases).
3.  Synthesizes a full **Functional Specification**.

**Output:**
-   Creates: `change_requests/split_bills/split_bills_FUNC_SPEC.md`

---

### Step C: Generate a Director's Brief
*Get a high-level strategic summary for decision making.*

**Command:**
```powershell
python generate_director_brief.py change_requests/split_bills/split_bills.md
```
**Output:**
-   Creates: `change_requests/split_bills/split_bills_DIRECTOR_BRIEF.md`
-   Content: Traffic light verdict (Go/No-Go), Top Risks, Resource Estimates.

---

### Step D: Run Full Evaluation
*Run the full panel of 7 AI Agents (Privacy, DevOps, Architect, etc.) to grade the request.*

**Command:**
```powershell
python evaluate.py change_requests/split_bills/split_bills.md
```
**Output:**
-   Creates: `change_requests/split_bills/split_bills_REPORT.md`
-   Content: Detailed feedback from every agent persona.

---

## 3. Directory Structure
*   `agents/`: Definitions of AI Personas (modify `definitions.py` to change prompt behavior).
*   `change_requests/`: The database of all requests. Each feature gets its own folder.
*   `knowledge_base/`: Markdown files that the AI reads to understand constraints (e.g., "No Java", "PCI Compliance").
*   `templates/`: The blank Markdown templates used by the generator.

## 4. Troubleshooting
*   **"Connection Refused"**: Ensure your Local LLM is running and listening on port 1234.
*   **"File Not Found"**: Always use the relative path (e.g., `change_requests/...`) or absolute path when running scripts.

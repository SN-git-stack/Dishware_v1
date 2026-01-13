# Architectural Standards & Rules

## 1. Allowed Tech Stack
- **Platform**: **TCPOS** (Zucchetti).
- **Language**: **C#** (.NET 10). **NO PYTHON / NO JAVA** for core plugins.
- **Framework**: TCPOS Plugin Architecture / WPF for UI extensions.
- **Database**: 
    - **Server**: MSSQL / PostgreSQL.
    - **POS Local**: SQLite or TCPOS Local DB.

## 2. API Guidelines
- Plugin integrations must use **HttpClient** (typed clients preferred).
- All external calls must be strictly typed and async.
- Authentication via OAuth2 / API Key (securely stored).

## 3. Offline Capabilities
- **Crucial**: The POS MUST function 100% offline for core sales.
- **Sync Pattern**:
    - Use the TCPOS `OperationManager` or local queuing tables.
    - Background service (Worker) handles the "Store-and-Forward" once connectivity is restored.

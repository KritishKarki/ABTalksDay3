# Vector Database Overview: Chroma vs. Pinecone

## Comparison Table

| Feature | Chroma (Local / Embedded) | Pinecone (Managed / Cloud) |
| :--- | :--- | :--- |
| **Deployment** | Local / Embedded (runs in Python process) | Fully managed Cloud service |
| **Free-Tier Limits** | 100% Free & Open-source (limited only by local disk/RAM) | Starter tier: 1 project, limited storage/namespaces |
| **Latency** | Low latency (local in-memory/disk access, no network overhead) | Low network latency, depends on region and connection |
| **Ease of Setup** | Extremely easy (`pip install chromadb`, instant setup) | Easy (requires account sign-up, API keys, index config) |
| **Enterprise Access Control** | Handled at application level or custom database deployment wrappers | Native RBAC, API key permissions, namespaces, and metadata filtering |

---

## Enterprise Access Control Analysis

In a production enterprise deployment (e.g., controlling access per member or per insurance plan):
- **Chroma:** Does not natively enforce multi-tenant user access control out of the box in local mode. Access control must be managed at the application layer by filtering queries via metadata (e.g., `where={"plan_id": "plan_123"}`) or running isolated instances behind a secure API service.
- **Pinecone:** Provides built-in multi-tenancy capabilities using namespaces and fine-grained metadata filtering. Enterprise access rules can be enforced securely through backend service logic using API keys and scoped queries.

---

## Decision & Justification

**Chosen Database for this Program:** **ChromaDB**

**Reasoning:** ChromaDB is completely free, open-source, and runs entirely locally without requiring cloud API keys or external account management. It integrates seamlessly into standard Python workflows with zero configuration, making it the ideal lightweight choice for local development, rapid prototyping, and learning vector database fundamentals.
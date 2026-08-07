# Vector Query Test Documentation

## 1. Collection Status Check
- **Collection Name:** `coverage_kb`
- **Total Chunk Count (`collection.count()`):** 57 (verified against `knowledge_base.jsonl`)

---

## 2. Test Query
- **Test Question:** "Is physical therapy covered under the Silver plan?"
- **Top Results Requested (`n_results`):** 5

---

## 3. Query Results Comparison

### A. Unfiltered Vector Search
* **Execution:** Ran similarity query using embedding model without metadata constraints.
* **Observation:** Returned semantic matches across multiple plan types (e.g., Silver, Bronze, and Gold plan chunks were retrieved if they discussed physical therapy or coverage limits).
* **Finding:** Semantic similarity alone does not restrict context to a specific insurance tier.

### B. Filtered Vector Search (`where={"plan_type": "Silver"}`)
* **Execution:** Ran vector search with metadata filter `where={"plan_type": "Silver"}`.
* **Observation:** All 5 top-ranked returned results strictly belonged to `plan_type: Silver`.
* **Finding:** Metadata pre-filtering successfully isolated Silver plan coverage details and prevented cross-plan retrieval leaks.

---

## 4. Conclusion
Metadata filtering effectively scopes semantic vector search to specified document parameters, ensuring high precision for plan-specific retrieval tasks.
# Retrieval Engine Test Results

## Overview
This document logs the evaluation of 10 test questions processed by the hybrid retrieval engine (`retrieval_engine.py`).

---

## Test Results Log

### Question 1
- **Question Text:** "What is my copay?"
- **Classification:** `structured`
- **Retrieved Context:** Retrieved plan details and copay information from SQLite database `coverage.db`.
- **Manual Score:** `good`

---

### Question 2
- **Question Text:** "Is maternity care covered on the Bronze plan?"
- **Classification:** `unstructured`
- **Retrieved Context:** Retrieved top matching policy chunks from ChromaDB for Bronze plan maternity coverage.
- **Manual Score:** `good`

---

### Question 3
- **Question Text:** "What is the status of claim C-2031?"
- **Classification:** `structured`
- **Retrieved Context:** Query returned matching claim records from `claims` table in SQLite database.
- **Manual Score:** `good`

---

### Question 4
- **Question Text:** "Is physical therapy covered under the Silver plan?"
- **Classification:** `unstructured`
- **Retrieved Context:** Retrieved policy text chunks specifying Silver plan physical therapy coverage limits.
- **Manual Score:** `good`

---

### Question 5
- **Question Text:** "How much deductible have I spent so far?"
- **Classification:** `structured`
- **Retrieved Context:** Retrieved deductible spent accumulator from SQL plan/claims record.
- **Manual Score:** `good`

---

### Question 6
- **Question Text:** "What are the limitations and exclusions for mental health services?"
- **Classification:** `unstructured`
- **Retrieved Context:** Retrieved relevant policy exclusions and mental health benefit limits from vector search.
- **Manual Score:** `good`

---

### Question 7
- **Question Text:** "What is my member ID and plan type?"
- **Classification:** `structured`
- **Retrieved Context:** Fetched member profile info and active plan type from SQLite database.
- **Manual Score:** `good`

---

### Question 8
- **Question Text:** "How much deductible spent is remaining and is physical therapy covered under Silver?"
- **Classification:** `both`
- **Retrieved Context:** Query routed to both SQL (retrieved deductible paid/remaining) and ChromaDB (retrieved Silver physical therapy coverage terms).
- **Manual Score:** `good`

---

### Question 9
- **Question Text:** "What is the out-of-pocket maximum for emergency room visits?"
- **Classification:** `unstructured`
- **Retrieved Context:** Retrieved emergency room coverage limits and out-of-pocket maximums from ChromaDB.
- **Manual Score:** `good`

---

### Question 10
- **Question Text:** "Are prescription drugs covered on the Gold plan?"
- **Classification:** `unstructured`
- **Retrieved Context:** Retrieved policy wording regarding Gold plan prescription drug tiers from ChromaDB.
- **Manual Score:** `good`

---

## Conclusion
The hybrid retrieval engine successfully routed structured, unstructured, and hybrid queries to their respective data stores with high recall and precision.
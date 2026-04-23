# Code Review Report
**Project:** FlowOS AI  
**Date:** April 23, 2026  
**Reviewed By:** Kiro AI  
**Scope:** Full codebase static analysis

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Critical Bugs](#1-critical-bugs)
3. [High Severity — Validation Issues](#2-high-severity--validation-issues)
4. [Code Duplication](#3-code-duplication)
5. [Debug Code in Production](#4-debug-code-in-production)
6. [Unused & Empty Files](#5-unused--empty-files)
7. [Other Issues](#6-other-issues)
8. [Severity Summary Table](#severity-summary-table)

---

## Executive Summary

The codebase has **3 critical bugs** that break core functionality at runtime, **4 high-severity validation issues** that cause silent failures, and significant code duplication across the parsing layer. Several debug `print()` statements are embedded in production paths, and multiple files are entirely unused. Immediate attention is required on the critical bugs before any deployment.

---

## 1. Critical Bugs

> These will cause runtime errors and break core functionality.

---

### BUG-01 — Wrong Variable Name in Execution Loop
**File:** `app/services/execution_service.py`  
**Severity:** 🔴 Critical  

**Problem:**  
Inside the workflow loop, the code accesses `workflows.parsed_rule_json` (the query object) instead of `workflow.parsed_rule_json` (the loop variable). This crashes on every incoming event.

```python
# BROKEN
for workflow in workflows:
    rule = json.loads(workflows.parsed_rule_json)  # ← AttributeError

# FIXED
for workflow in workflows:
    rule = json.loads(workflow.parsed_rule_json)
```

---

### BUG-02 — Duplicate Function with Broken Regex
**File:** `app/services/llm/parser.py`  
**Severity:** 🔴 Critical  

**Problem:**  
`parse_with_regex()` is defined **twice** in the same file. Python silently uses the second definition, which has an incomplete `re.search()` call — the `raw_text` argument is missing. The first definition becomes dead code.

```python
# First definition (correct, but ignored by Python)
def parse_with_regex(raw_text: str):
    match = re.search(r"salary above (\d+) approve loan", raw_text)

# Second definition (used by Python, broken)
def parse_with_regex(raw_text: str):
    match = re.search(r"salary above (\d+)")  # ← missing raw_text argument
```

---

### BUG-03 — Calling an Undefined Function in Route
**File:** `app/api/parser_routes.py`  
**Severity:** 🔴 Critical  

**Problem:**  
The import for `parse_workflow` is commented out, but the function is still called in the route handler. Every request to `POST /parse` will throw a `NameError`.

```python
# Import is commented out
# from app.services.parser.parser import parse_workflow

@router.post("/", response_model=ParseResponse)
def parse_route(payload: ParseRequest):
    return parse_workflow(payload.raw_input)  # ← NameError: parse_workflow is not defined
```

---

## 2. High Severity — Validation Issues

> These cause validation to silently pass or fail incorrectly.

---

### BUG-04 — Typo Makes Condition Check Dead Code
**File:** `app/services/llm/validator.py`  
**Severity:** 🟠 High  

**Problem:**  
The key `"condititons"` (typo) will never match `"conditions"` in the data. The condition type check is permanently skipped for all inputs.

```python
# BROKEN — typo, never matches
if "condititons" in data and not isinstance(data["conditions"], dict):

# FIXED
if "conditions" in data and not isinstance(data["conditions"], dict):
```

---

### BUG-05 — Wrong Key Name in Rule Validator
**File:** `app/services/parser/validator.py`  
**Severity:** 🟠 High  

**Problem:**  
The validator checks for `"condition"` (singular) but the rule object uses `"conditions"` (plural). The check always falls back to the default empty list and never validates actual conditions.

```python
# BROKEN — key never found
if not isinstance(rule.get("condition", []), list):

# FIXED
if not isinstance(rule.get("conditions", []), list):
```

---

### BUG-06 — Allowed Triggers & Actions Defined Twice with Different Values
**Files:** `app/services/llm/schemas.py` vs `app/services/parser/validator.py`  
**Severity:** 🟠 High  

**Problem:**  
Two separate sets of allowed values exist and they do not match. A workflow that passes one validator will fail the other.

| | `llm/schemas.py` | `parser/validator.py` |
|---|---|---|
| **Triggers** | loan_request, ticket_created, payment_due | complaint_created, payment_due, payment_missed |
| **Actions** | approve_loan, reject_loan, send_reminder, escalate_ticket, notify_manager | send_reminder, escalate_case, assign_senior_officer, close_case |

**Fix:** Consolidate into a single constants file and import from it everywhere.

---

### BUG-07 — Inconsistent Action Handler Signatures
**File:** `app/services/actions/handlers.py`  
**Severity:** 🟠 High  

**Problem:**  
Handler functions have inconsistent signatures. If the dispatcher calls all handlers the same way, `send_reminder` and `escalate_ticket` will throw a `TypeError`.

```python
def send_reminder(payload):           # 1 argument
def approve_loan(payload, config):    # 2 arguments
def escalate_ticket(payload):         # 1 argument
```

**Fix:** Standardize all handlers to accept `(payload, config=None)`.

---

## 3. Code Duplication

> Same logic repeated in multiple places — a fix in one location won't apply to the other.

---

### DUP-01 — `parse_workflow()` Exists in Two Files
**Files:** `app/services/llm/parser.py` and `app/services/parser/parser.py`  
**Severity:** 🟡 Medium  

The entire parsing function is copy-pasted between two files. Both contain the same bugs. There is no clear ownership of which one is the "real" parser.

---

### DUP-02 — `get_db()` Duplicated Across Route Files
**Files:** `app/api/event_routes.py` and `app/api/workflow_routes.py`  
**Severity:** 🟡 Medium  

The database session dependency is defined separately in each route file instead of being imported from `app/db/session.py`.

```python
# Duplicated in both files — should be imported once
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### DUP-03 — Regex Extraction Utilities Duplicated
**Files:** `app/services/regex_parser.py` and `app/services/parser/extractors.py`  
**Severity:** 🟡 Medium  

`extract_days()`, `extract_repeat_count()`, and `extract_amount_threshold()` exist in both files. `regex_parser.py` is never imported anywhere — it is dead code.

---

### DUP-04 — `map_intents()` Called Twice Consecutively
**File:** `app/services/parser/orchestrator.py`  
**Severity:** 🟡 Medium  

```python
mapped = map_intents(text)
mapped = map_intents(text)   # ← second call immediately overwrites the first
```

The second call is pointless and wastes a computation cycle.

---

## 4. Debug Code in Production

> These execute automatically and should not be in production code.

---

### DBG-01 — LLM Call Fires on App Startup
**File:** `app/main.py`  
**Severity:** 🟡 Medium  

```python
print(call_llm("if salary above 50000 approve loan"))  # runs every time the server starts
```

This makes a live LLM call and prints to stdout on every application startup.

---

### DBG-02 — `print()` at Module Level in Extractors
**File:** `app/services/parser/extractors.py`  
**Severity:** 🟡 Medium  

A `print(extract_all(...))` statement exists at the module level. It executes every time the module is imported, not just when the function is called.

---

### DBG-03 — `print()` Inside Intent Mapping Loop
**File:** `app/services/parser/intent_mapper.py`  
**Severity:** 🟡 Medium  

A `print(action, phrases)` statement fires inside the mapping logic during normal execution, flooding logs with internal data.

---

## 5. Unused & Empty Files

> These add noise and confusion to the codebase.

| File | Issue |
|---|---|
| `app/services/regex_parser.py` | Never imported or used anywhere |
| `app/services/parser/cache.py` | Empty dictionary, never read or written |
| `app/services/parser/metrics.py` | Metrics dict declared but never updated |
| `app/services/llm/router.py` | Completely empty file |
| `alembic/versions/5a15a7cd98e9_add_status_column.py` | Duplicate migration name, no schema changes |
| `alembic/versions/69ac7ff42317_create_workflows_table.py` | Empty migration — no table is actually created |
| `alembic/versions/3f58052cf840_create_audit_logs_table.py` | Empty migration — no table is actually created |

---

## 6. Other Issues

---

### OTHER-01 — Bare `except` Clauses Swallow All Errors
**Files:** `app/services/execution_service.py`, `app/services/llm/parser.py`  
**Severity:** 🟡 Medium  

```python
try:
    rule = json.loads(workflow.parsed_rule_json)
except:   # ← catches everything including KeyboardInterrupt, SystemExit
    continue
```

Silent failures make debugging extremely difficult. Use `except (json.JSONDecodeError, KeyError) as e` and log the error.

---

### OTHER-02 — Event Matching Logic is Hardcoded
**File:** `app/services/execution_service.py`  
**Severity:** 🟡 Medium  

`is_rule_matched()` contains hardcoded checks for `"vip"` and `"salary_gt"` instead of dynamically evaluating the parsed rule conditions stored in the database. The entire purpose of storing `parsed_rule_json` is bypassed.

---

### OTHER-03 — No Database Transaction Rollback
**Files:** Multiple service files  
**Severity:** 🟡 Medium  

Multiple `db.add()` / `db.commit()` calls have no corresponding `db.rollback()` on failure. A partial write can leave the database in an inconsistent state.

---

### OTHER-04 — Typos in Function and Variable Names
**File:** `app/services/parser/intent_mapper.py`  
**Severity:** 🔵 Low  

| Typo | Should Be |
|---|---|
| `normailze` | `normalize` |
| `pharses` | `phrases` |

These don't cause runtime errors but indicate the code was not reviewed carefully.

---

### OTHER-05 — Domain Validation is Hardcoded
**File:** `app/services/workflow_service.py`  
**Severity:** 🔵 Low  

```python
ALLOWED_DOMAINS = ["support", "loan"]
```

Hardcoded in the service layer with no corresponding configuration or constant file. Adding a new domain requires a code change.

---

## Severity Summary Table

| ID | File | Issue | Severity |
|---|---|---|---|
| BUG-01 | execution_service.py | `workflows` vs `workflow` typo crashes event processing | 🔴 Critical |
| BUG-02 | llm/parser.py | Duplicate function with broken regex | 🔴 Critical |
| BUG-03 | parser_routes.py | Undefined `parse_workflow` called in route | 🔴 Critical |
| BUG-04 | llm/validator.py | Typo `condititons` — condition check never runs | 🟠 High |
| BUG-05 | parser/validator.py | Wrong key `condition` vs `conditions` | 🟠 High |
| BUG-06 | llm/schemas.py + parser/validator.py | Duplicate, mismatched allowed values | 🟠 High |
| BUG-07 | actions/handlers.py | Inconsistent handler signatures | 🟠 High |
| DUP-01 | llm/parser.py + parser/parser.py | `parse_workflow()` duplicated | 🟡 Medium |
| DUP-02 | event_routes.py + workflow_routes.py | `get_db()` duplicated | 🟡 Medium |
| DUP-03 | regex_parser.py + extractors.py | Extraction utilities duplicated | 🟡 Medium |
| DUP-04 | parser/orchestrator.py | `map_intents()` called twice | 🟡 Medium |
| DBG-01 | main.py | LLM call fires on every app startup | 🟡 Medium |
| DBG-02 | parser/extractors.py | `print()` at module level | 🟡 Medium |
| DBG-03 | parser/intent_mapper.py | `print()` inside mapping loop | 🟡 Medium |
| OTHER-01 | execution_service.py + llm/parser.py | Bare `except` swallows all errors | 🟡 Medium |
| OTHER-02 | execution_service.py | Event matching logic is hardcoded | 🟡 Medium |
| OTHER-03 | Multiple services | No DB transaction rollback | 🟡 Medium |
| OTHER-04 | parser/intent_mapper.py | Typos in function/variable names | 🔵 Low |
| OTHER-05 | workflow_service.py | Hardcoded domain list | 🔵 Low |

---

**Total Issues Found: 19**  
🔴 Critical: 3 &nbsp;|&nbsp; 🟠 High: 4 &nbsp;|&nbsp; 🟡 Medium: 10 &nbsp;|&nbsp; 🔵 Low: 2

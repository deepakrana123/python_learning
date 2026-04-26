# Code Review Report — FlowOS AI

**Date:** April 23, 2026  
**Reviewed By:** Kiro AI  
**Scope:** Full codebase (`app/`, `alembic/`)

---

## Summary

| Category | Count |
|---|---|
| Syntax / Runtime Errors | 8 |
| Code Repetition / Duplication | 9 |
| Logic Bugs | 6 |
| Wrong Import Paths | 5 |
| Missing / Broken References | 4 |
| Bad Practices | 7 |

---

## 1. SYNTAX / RUNTIME ERRORS

### 1.1 `app/models/audit_log.py` — Missing comma (SyntaxError, app will not start)
```python
# BROKEN — missing comma before nullable=True
workflow_id = Column(Integer,ForeignKey("workflows.id"),index=True nullable=True)

# FIX
workflow_id = Column(Integer, ForeignKey("workflows.id"), index=True, nullable=True)
```

### 1.2 `app/llm/client.py` — `fake_call` signature mismatch (TypeError at runtime)
`fake_call` is defined with one argument (`prompt`) but called with two (`"Free_Model"`, `prompt`).
```python
# BROKEN
text = fake_call("Free_Model", prompt)   # 2 args
def fake_call(prompt):                   # only 1 param

# FIX — add the missing parameter
def fake_call(provider: str, prompt: str):
    ...
```

### 1.3 `app/llm/client.py` — `fake_call` returns a dict, not a string
`fake_call` returns a `dict`, but the caller does `json.loads(cleaned)` on the result of `clean_json(llm_result["text"])`, expecting a string.
```python
# BROKEN — returns dict, not str
def fake_call(prompt):
    return {"trigger": "loan_request", ...}

# FIX — return a JSON string
def fake_call(provider: str, prompt: str) -> str:
    return json.dumps({"trigger": "loan_request", ...})
```

### 1.4 `app/llm/repair.py` — `fake_repair_call` returns a dict, not a string
Same issue as above. `json.loads(repaired)` will fail because `repaired` is already a dict.
```python
# BROKEN
def fake_repair_call(prompt: str):
    return {"trigger": "loan_request", ...}   # dict, not str

# FIX
def fake_repair_call(prompt: str) -> str:
    return json.dumps({"trigger": "loan_request", ...})
```

### 1.5 `app/schemas/event.py` — Invalid generic type in `List[Dict[str]]`
`Dict` requires two type arguments: key type and value type.
```python
# BROKEN
execution_results: List[Dict[str]]

# FIX
execution_results: List[Dict[str, Any]]
```

### 1.6 `app/parsers/regex_parser.py` — Regex captures `\d+s` instead of `\d+`
The `s` is inside the capture group, so `int(m.group(1))` will raise `ValueError` on any match.
```python
# BROKEN
m = re.search(r"(\d+s)\s*times?", text.lower())

# FIX
m = re.search(r"(\d+)\s*times?", text.lower())
```

### 1.7 `app/parsers/extractors.py` — `print` statement at module level (side effect on import)
```python
# BROKEN — runs on every import
print(extract_all("Send reminder after 10 days"))

# FIX — remove or guard with __main__
if __name__ == "__main__":
    print(extract_all("Send reminder after 10 days"))
```

### 1.8 `app/schemas/parserpy` — File has no `.py` extension
The file `app/schemas/parserpy` is missing the `.py` extension. Python cannot import it, so `app/routes/parsers.py` will crash on startup with `ModuleNotFoundError`.
```
# FIX — rename the file
app/schemas/parserpy  →  app/schemas/parser_schema.py
```

---

## 2. WRONG IMPORT PATHS (ModuleNotFoundError at runtime)

### 2.1 `app/services/workflow_service.py`
```python
# BROKEN — package is app.parsers, not app.parser
from app.parser.orchestrator import parse_workflow_text

# FIX
from app.parsers.orchestrator import parse_workflow_text
```

### 2.2 `app/parsers/orchestrator.py`
```python
# BROKEN — all four imports use app.parser instead of app.parsers
from app.parser.extractors import extract_all
from app.parser.intent_mapper import map_intents
from app.parser.rule_builder import build_final_rule
from app.parser.validator import validate_rule

# FIX
from app.parsers.extractors import extract_all
from app.parsers.intent_mapper import map_intents
from app.parsers.rule_builder import build_final_rule
from app.parsers.validator import validate_rule
```

### 2.3 `app/parsers/main_parser.py`
```python
# BROKEN
from app.parser.metrics import metrics
from app.parser.cache import cache_store

# FIX
from app.parsers.metrics import metrics
from app.parsers.cache import cache_store
```

### 2.4 `app/routes/parsers.py`
```python
# BROKEN — wrong schema module name and missing import for parse_workflow
from app.schemas.parser_schema import ParseRequest, ParseResponse
from app.parser.metrics import metrics
# parse_workflow is commented out but still called in the route body

# FIX
from app.schemas.parser_schema import ParseRequest, ParseResponse
from app.parsers.metrics import metrics
from app.parsers.main_parser import parse_workflow   # uncomment and fix
```

---

## 3. CODE REPETITION / DUPLICATION

### 3.1 `parse_with_regex` defined twice in `app/parsers/main_parser.py`
The function is defined at line ~8 and again at line ~60. The second definition silently overwrites the first. The first version also has a bug (`raw_text.lower()` passed to `re.search` but `raw_text` used for the match group).
```python
# DUPLICATED — remove the first definition, keep only the second (corrected) one
def parse_with_regex(raw_text: str):   # appears TWICE
```

### 3.2 `get_db()` duplicated across three route files
`get_db()` is copy-pasted identically in `app/routes/workflows.py`, `app/routes/events.py`, and already exists in `app/db/session.py`.
```python
# DUPLICATED in workflows.py and events.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FIX — import from the single source of truth
from app.db.session import get_db
```

### 3.3 `extract_days`, `extract_repeat_count`, `extract_amount_threshold` duplicated
These three functions exist in both `app/parsers/regex_parser.py` and `app/parsers/extractors.py` with slightly different implementations. `regex_parser.py` is the inferior copy (has the `\d+s` bug, no `normalize()` helper, narrower regex for amount).
```
FIX — delete app/parsers/regex_parser.py and use app/parsers/extractors.py everywhere.
```

### 3.4 `map_intents` called twice in `app/parsers/orchestrator.py`
```python
# DUPLICATED — second call overwrites the first with identical result
mapped = map_intents(text)
mapped = map_intents(text)   # ← remove this line
```

### 3.5 Trigger/action allow-lists defined in two places
`ALLOWED_TRIGGERS` and `ALLOWED_ACTIONS` are defined in both `app/llm/schemas.py` and `app/parsers/validator.py` with **different values**, causing inconsistent validation between the LLM layer and the parser layer.

| | `app/llm/schemas.py` | `app/parsers/validator.py` |
|---|---|---|
| Triggers | `loan_request`, `ticket_created`, `payment_due` | `complaint_created`, `payment_due`, `payment_missed` |
| Actions | `approve_loan`, `reject_loan`, `send_reminder`, `escalate_ticket`, `notify_manager` | `send_reminder`, `escalate_case`, `assign_senior_officer`, `close_case` |

```
FIX — consolidate into a single app/schemas/constants.py and import from there.
```

### 3.6 `import json` duplicated in `app/services/execution_service.py`
```python
import json   # line 1
...
import json   # line 6 — duplicate, remove it
```

### 3.7 `load_dotenv()` called in both `app/llm/client.py` and `app/main.py`
Calling it twice is harmless but redundant. It should only be called once at application startup in `main.py`.

---

## 4. LOGIC BUGS

### 4.1 `app/parsers/main_parser.py` — Early return missing after regex success
When regex parsing succeeds and the result is valid, the function stores the result in cache but then **falls through** to the LLM call instead of returning.
```python
# BROKEN — missing return
if valid["is_valid"]:
    return {"success": True, "source": "regex", "score": 1.0, "data": parsed}
metrics["regex_hits"] += 1
result = { ... }
cache_store[raw_text] = result
# ← should return here, but doesn't — falls through to LLM call

# FIX
cache_store[raw_text] = result
return result   # add this
```

### 4.2 `app/llm/validator.py` — Validation checks inside `for field in REQUIRED_FIELDS` loop
The trigger, action, conditions, and config checks are indented inside the `for` loop, so they run once per required field (4 times), producing duplicate error messages.
```python
# BROKEN — indented inside for loop
for field in REQUIRED_FIELDS:
    if field not in data:
        errors.append(f"missing field:{field}")
    if data.get("trigger") not in ALLOWED_TRIGGERS:   # runs 4 times
        ...

# FIX — dedent the extra checks out of the loop
for field in REQUIRED_FIELDS:
    if field not in data:
        errors.append(f"missing field:{field}")

if data.get("trigger") not in ALLOWED_TRIGGERS:
    errors.append("Invalid trigger")
...
```

### 4.3 `app/llm/validator.py` — Typo in key name `"condititons"`
```python
# BROKEN — typo will never match the actual key "conditions"
if "condititons" in data and not isinstance(data["conditions"], dict):

# FIX
if "conditions" in data and not isinstance(data["conditions"], dict):
```

### 4.4 `app/services/workflow_service.py` — 404 returned as 400
```python
# WRONG status code — "not found" should be 404
raise HTTPException(status_code=400, detail="Workflow not found")

# FIX
raise HTTPException(status_code=404, detail="Workflow not found")
```

### 4.5 `app/repositories/workflow_repo.py` — `delete` missing `db.commit()`
The `delete` function removes the object from the session but never commits, so the deletion is never persisted.
```python
# BROKEN
def delete(db: Session, workflow: Workflow):
    db.delete(workflow)

# FIX
def delete(db: Session, workflow: Workflow):
    db.delete(workflow)
    db.commit()
```

### 4.6 `app/services/execution_service.py` — `db.commit()` inside loop, one failure rolls back nothing
Committing inside the loop means a crash mid-loop leaves some audit logs committed and others not. Use a single commit after the loop, or wrap each iteration in a try/except with rollback.
```python
# RISKY — commit per iteration
for workflow in workflows:
    ...
    db.add(log)
    db.commit()   # ← move outside the loop

# FIX
    db.add(log)
# after loop:
db.commit()
```

---

## 5. MISSING / BROKEN REFERENCES

### 5.1 `app/routes/parsers.py` — `parse_workflow` is called but never imported
The import is commented out and the function is still used in the route body. The route will raise `NameError` on every request.
```python
# BROKEN
# from app.services.parser.parser import parse_workflow
...
return parse_workflow(payload.raw_input)   # NameError

# FIX — uncomment and correct the import path
from app.parsers.main_parser import parse_workflow
```

### 5.2 `app/actions/handlers.py` — `send_reminder` and `escalate_ticket` missing `config` parameter
`dispatcher.py` calls all handlers as `handler(payload, config)`, but `send_reminder` and `escalate_ticket` only accept one argument.
```python
# BROKEN — called with 2 args but only accepts 1
def send_reminder(payload):
def escalate_ticket(payload):

# FIX
def send_reminder(payload: dict, config: dict):
def escalate_ticket(payload: dict, config: dict):
```

### 5.3 `app/repositories/execution_repo.py` — File is empty
`execution_service.py` does all DB work inline. If an execution repository is intended, it is missing entirely.

### 5.4 `app/llm/client.py` — `try_free_model` is listed twice in the providers list
```python
providers = [try_free_model, try_free_model, try_engineer_model, try_paid_model]
#                            ^^^^^^^^^^^^^^ duplicate — should be try_local_model
```
`try_local_model` is defined but never used. The providers list should be:
```python
providers = [try_free_model, try_local_model, try_engineer_model, try_paid_model]
```

---

## 6. BAD PRACTICES

### 6.1 Bare `except:` in `execution_service.py`
```python
try:
    rule = json.loads(workflow.parsed_rule_json)
except:   # catches everything including KeyboardInterrupt, SystemExit
    continue

# FIX
except (json.JSONDecodeError, TypeError):
    continue
```

### 6.2 Bare `except:` in `llm/repair.py`
```python
except:
    return {"success": False}

# FIX
except json.JSONDecodeError:
    return {"success": False, "error": "invalid json"}
```

### 6.3 `print` statements used for logging throughout
`handlers.py`, `intent_mapper.py`, `client.py`, and `repair.py` all use `print()` for debug output. Use Python's `logging` module instead so output can be controlled by log level.

### 6.4 `app/parsers/metrics.py` and `app/parsers/cache.py` are mutable global state
Both are plain module-level dicts. In a multi-worker deployment (e.g., Gunicorn with multiple processes), each worker has its own copy — metrics will be inaccurate and the cache will not be shared. Use Redis or a proper cache/metrics backend.

### 6.5 `app/llm/client.py` — `try_paid_model` and `try_engineer_model` return the same error
Both stubs return `"provider": "engineer"`, making it impossible to distinguish which provider failed in logs.

### 6.6 `app/parsers/intent_mapper.py` — Typo in function name `normailze`
```python
def normailze(text: str) -> str:   # typo

# FIX
def normalize(text: str) -> str:
```
Both `extractors.py` and `intent_mapper.py` define their own `normalize` helper. Consolidate into a shared utility.

### 6.7 `app/models/workflow.py` — `parsed_rule_json` is `JSONB` but treated as a string elsewhere
The model column is `JSONB` (PostgreSQL native JSON), but `execution_service.py` calls `json.loads(workflow.parsed_rule_json)` and `workflow_service.py` stores `json.dumps(parse_result["rule"])`. SQLAlchemy with JSONB already deserializes the value — calling `json.loads` on it will raise a `TypeError`.
```python
# BROKEN — JSONB is already a dict when read back
rule = json.loads(workflow.parsed_rule_json)

# FIX — use directly
rule = workflow.parsed_rule_json
# and when writing, pass the dict directly (no json.dumps)
parsed_rule_json=parse_result["rule"]
```

---

## Quick-Fix Priority

| Priority | File | Issue |
|---|---|---|
| 🔴 Critical | `app/models/audit_log.py` | SyntaxError — app won't start |
| 🔴 Critical | `app/schemas/parserpy` | Missing `.py` extension — import fails |
| 🔴 Critical | `app/llm/client.py` | `fake_call` wrong signature + wrong return type |
| 🔴 Critical | All `app.parser.*` imports | Wrong package name — `ModuleNotFoundError` |
| 🔴 Critical | `app/routes/parsers.py` | `parse_workflow` never imported — `NameError` |
| 🟠 High | `app/parsers/main_parser.py` | Duplicate `parse_with_regex`, missing `return` after regex hit |
| 🟠 High | `app/llm/validator.py` | Loop indentation bug + typo `condititons` |
| 🟠 High | `app/actions/handlers.py` | Missing `config` param on two handlers |
| 🟠 High | `app/models/workflow.py` | JSONB vs `json.dumps/loads` mismatch |
| 🟡 Medium | `app/parsers/regex_parser.py` | Duplicate of `extractors.py`, has `\d+s` bug |
| 🟡 Medium | `app/parsers/orchestrator.py` | `map_intents` called twice |
| 🟡 Medium | `app/routes/workflows.py` + `events.py` | `get_db` duplicated |
| 🟡 Medium | `app/llm/schemas.py` + `app/parsers/validator.py` | Conflicting allow-lists |
| 🟢 Low | `app/parsers/extractors.py` | `print` at module level |
| 🟢 Low | `app/services/execution_service.py` | Duplicate `import json`, bare `except:` |
| 🟢 Low | `app/parsers/intent_mapper.py` | Typo `normailze`, debug `print` in loop |

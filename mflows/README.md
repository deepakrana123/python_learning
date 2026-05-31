# MFlows — AI Workflow Orchestration Engine

A production-grade workflow automation engine that accepts natural language rules, parses them through a hybrid rule/LLM pipeline, and executes them as DAG-based workflows with full distributed tracing, retry logic, and chaos testing support.

---

## What It Does

You write a workflow in plain DSL:

```
@1: payment_due -> send_reminder
@2 @depends(@1): payment_due -> escalate_case
@3 @depends(@1,@2): sla_breached -> send_sla_breach_alert
```

MFlows parses it, validates the DAG, stores it, and executes it when a matching event arrives — tracking every step, retry, and failure with full distributed tracing.

---

## Architecture

```
POST /api/workflows          POST /api/execute
       │                            │
       ▼                            ▼
  DSL Parser                  WorkflowRun
  (deterministic)             WorkflowExecution
  + LLM fallback              Redis Queue
       │                            │
       ▼                            ▼
  DAG Validation              Worker (BRPOP)
  Cycle detection                   │
  Dependency check                  ▼
       │                     runtime_processor
       ▼                            │
  Workflow stored             mark RUNNING
  (parsed_rule_json)                │
                                    ▼
                             dag_executor
                             (dependency scheduler)
                                    │
                             ┌──────┴──────┐
                             ▼             ▼
                        step_executor  step_executor
                             │
                        execute_action
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
               SUCCESS            FAILURE
                    │                 │
             mark COMPLETED    retry_handler
             trace event       (retry / DLQ)
                    │
             workflow_finalizer
             (derive workflow state
              from step graph)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Database | PostgreSQL (via SQLAlchemy + Alembic) |
| Queue | Redis (BRPOP + sorted set for retry) |
| LLM Providers | Ollama (local) + Gemini REST |
| Tracing IDs | ULID (`python-ulid`) |
| Containerization | Docker Compose |

---

## Project Structure

```
app/
├── main.py                          # FastAPI app entry point
├── routes/
│   ├── workflows.py                 # POST /api/workflows, GET /api/workflows
│   └── execute.py                   # POST /api/execute, pause, resume
├── parsers/
│   ├── dsl_parser.py                # Deterministic DSL grammar parser
│   ├── dag_validator.py             # Cycle detection, dependency validation
│   ├── dag_orchestrator.py          # Parse → validate → LLM repair flow
│   ├── orchestrator.py              # Legacy single-rule text parser (v1)
│   ├── intent_mapper.py             # Trigger/action pattern matching (23 triggers, 37 actions)
│   └── extractors.py                # Entity, amount, flag extraction
├── execution/
│   ├── dispatcher.py                # Routes action_name → handler function
│   ├── actions.py                   # Generic cross-domain actions
│   ├── chaos_actions.py             # Chaos testing — 13 configurable failure modes
│   ├── conditions.py                # Condition string parser (amount>5000, vip=true)
│   ├── retry_handler.py             # Retry vs DLQ decision
│   ├── retry.py                     # Redis zadd/lpush for retry queue
│   ├── retry_policy.py              # Exponential backoff calculation
│   ├── state_manager.py             # ExecutionStep DB status writes
│   ├── dedupe.py                    # Distributed lock (Redis NX)
│   ├── domain_actions/
│   │   ├── support_actions.py       # 10 customer support actions
│   │   └── health_actions.py        # 10 healthcare actions
│   └── runtime/
│       ├── runtime_processor.py     # Orchestration entry point
│       ├── dag_executor.py          # DAG traversal + step scheduling
│       ├── dag_scheduler.py         # get_ready_steps() dependency resolver
│       ├── step_executor.py         # Step lifecycle + trace events
│       ├── step_execution_service.py# ExecutionStep DB operations
│       ├── workflow_execution_service.py # WorkflowExecution DB operations
│       ├── workflow_finalizer.py    # Derive workflow state from step graph
│       ├── retry_executor.py        # Retry path execution
│       ├── execution_state_manager.py # State machine transition validation
│       └── constants.py             # Status constants
├── llm/
│   ├── llmManager.py                # Provider chain with health tracking + timeout
│   ├── service.py                   # LLM parse + DSL repair entry points
│   ├── provider_health.py           # Provider disable/cooldown on fatal errors
│   ├── validator.py                 # LLM output schema validation + scoring
│   ├── repair.py                    # JSON repair utility
│   ├── prompts/
│   │   ├── parser_v1.txt            # LLM prompt (23 triggers, 37 actions)
│   │   └── repair_v1.txt            # DSL repair prompt
│   └── providers/
│       ├── ollama.py                # Ollama local model provider
│       └── gemini_rest.py           # Gemini REST API provider
├── models/
│   ├── workflow.py                  # Workflow definition
│   ├── workflow_run.py              # Business-level run tracking
│   ├── workflow_execution.py        # Runtime execution state + trace_id
│   ├── execution_step.py            # Per-step runtime state + span_id
│   ├── trace_event.py               # Append-only distributed trace log
│   ├── step_retry_history.py        # Immutable retry audit trail
│   ├── audit_log.py                 # Action audit log
│   └── event_processing.py          # Event queue state
├── services/
│   ├── workflow_service.py          # Workflow CRUD + parse orchestration
│   ├── trace_service.py             # All trace event writes (13 event types)
│   └── execution_service.py         # Legacy event-based execution (v1)
├── workers/
│   ├── consumer.py                  # Main worker (ThreadPoolExecutor, BRPOP)
│   ├── retry_worker.py              # Retry queue processor (atomic pipeline)
│   └── reaper_worker.py             # Stuck RUNNING execution recovery
├── repositories/
│   ├── workflow.py                  # Workflow DB queries
│   ├── audit_repo.py                # Audit log writes
│   ├── entity_repo.py               # Entity payload fetching
│   ├── step_retry_history_repo.py   # Retry history writes + queries
│   └── workflows_run_repo.py        # WorkflowRun DB operations
├── core/
│   ├── tracing.py                   # ULID generation, build_log_context, inject_trace
│   ├── logger.py                    # JSON structured logger
│   ├── redis_client.py              # Redis connection
│   └── config.py                    # MAX_RETRIES, BASE_DELAY_SECONDS
└── metrics/
    ├── parser_metrics.py            # Parser hit/miss/LLM usage counters
    └── execution_metrics.py         # Execution counters
```

---

## Supported Domains

| Domain | Triggers | Actions |
|---|---|---|
| **Generic / Finance** | `payment_due`, `payment_missed`, `loan_requested`, `fraud_detected`, `account_locked`, `delivery_failed` | `send_reminder`, `reject_loan`, `lock_account`, `notify_manager`, `flag_for_review`, `generate_report`, + more |
| **Customer Support** | `ticket_created`, `ticket_unresolved`, `sla_breached`, `complaint_created`, `refund_requested`, `customer_churned`, + more | `create_support_ticket`, `assign_support_agent`, `escalate_to_tier2`, `send_sla_breach_alert`, `process_refund`, `send_satisfaction_survey`, + more |
| **Healthcare** | `patient_admitted`, `patient_discharged`, `critical_vitals`, `lab_result_ready`, `medication_overdue`, `followup_due`, + more | `alert_care_team`, `escalate_to_specialist`, `trigger_emergency_protocol`, `send_medication_reminder`, `schedule_appointment`, `send_wellness_check`, + more |

**Total: 23 triggers · 37 actions · 7 domains**

---

## DSL Format

```
# Linear chain
@1: payment_due -> send_reminder
@2 @depends(@1): payment_due -> escalate_case
@3 @depends(@2): sla_breached -> send_sla_breach_alert

# Branching (both @2 and @3 depend on @1)
@1: patient_admitted -> flag_high_risk_patient
@2 @depends(@1): patient_admitted -> request_insurance_approval
@3 @depends(@1): patient_admitted -> alert_care_team

# Multi-dependency
@1: ticket_created -> create_support_ticket
@2: ticket_created -> assign_support_agent
@3 @depends(@1,@2): sla_breached -> escalate_to_tier2
```

**Rules:**
- `@id` — step identifier (required)
- `@depends(@id,...)` — dependency list (optional)
- `trigger -> action` — arrow is required; ambiguous syntax fails immediately
- Lines starting with `#` are comments and ignored

---

## Getting Started

### Prerequisites

- Docker + Docker Compose
- PostgreSQL (or use Supabase)
- Redis (included in Docker Compose)
- Ollama running locally (optional — Gemini is the fallback)

### 1. Clone and configure

```bash
git clone <repo>
cd mflows
cp .env.example .env
# Edit .env with your DATABASE_URL and GEMINI_API_KEY
```

### 2. Run migrations

```bash
alembic upgrade head
```

### 3. Start all services

```bash
docker-compose up --build
```

This starts:
- `api` — FastAPI on port 8000
- `worker` — main execution worker
- `retry_worker` — retry queue processor
- `reaper_worker` — stuck execution recovery
- `redis` — Redis on port 6379

### 4. Verify

```bash
curl http://localhost:8000/
# {"message": "FlowOs running"}
```

---

## API Reference

### Create a Workflow

```http
POST /api/workflows/
Content-Type: application/json

{
  "name": "Payment Escalation",
  "domain": "support",
  "raw_input": "@1: payment_missed -> send_reminder\n@2 @depends(@1): sla_breached -> escalate_to_tier2"
}
```

### Execute a Workflow

```http
POST /api/execute/
Content-Type: application/json

{
  "workflow_id": 1,
  "entity_id": "CU001"
}
```

Response:
```json
{
  "success": true,
  "queued": true,
  "workflow_run_id": 10,
  "workflow_execution_id": 23
}
```

### Pause / Resume

```http
POST /api/execute/{workflow_execution_id}/pause
POST /api/execute/{workflow_execution_id}/resume
```

### Debug Parse

```http
POST /api/workflows/debug-parse
Content-Type: application/json

{
  "raw_input": "@1: ticket_created -> create_support_ticket"
}
```

---

## Distributed Tracing

Every workflow execution gets a `trace_id` (`wf_<ULID>`) at creation. Every step gets a `span_id` (`sp_<ULID>`). All events are written to the `trace_events` table.

```
Workflow Started        trace_id=wf_ABC  source=runtime_processor
├── Step A Started      span_id=sp_111   parent=wf_ABC
├── Action Dispatched   span_id=sp_111   action=send_reminder
├── Action Success      span_id=sp_111
├── Step A Completed    span_id=sp_111
├── Step B Started      span_id=sp_222   parent=wf_ABC
├── Action Failed       span_id=sp_222   error=GatewayError
├── Step B Failed       span_id=sp_222
├── Retry Scheduled     span_id=sp_222   attempt=1
├── Retry Started       span_id=sp_222
├── Retry Completed     span_id=sp_222   success=True
└── Workflow Completed  trace_id=wf_ABC
```

Query a full trace:
```python
from app.services.trace_service import get_trace
events = get_trace(db, trace_id="wf_ABC")
```

---

## Chaos Testing

Set `CHAOS_MODE=true` in your environment to route all actions through the chaos engine.

Configure per-step in the workflow config:

```json
{
  "config": {
    "chaos_mode": "succeed_after_retries",
    "succeed_after": 2
  }
}
```

Available modes:

| Mode | Simulates |
|---|---|
| `success` | Clean response (default) |
| `always_fail` | Permanently down service |
| `timeout` | No response, configurable delay |
| `slow` | Succeeds but slowly |
| `gateway_error` | 502/503 upstream failure |
| `rate_limit` | 429 Too Many Requests |
| `auth_error` | 401/403 invalid API key |
| `bad_payload` | 400 malformed request |
| `payload_overload` | Response too large |
| `partial_success` | 207 partial failure |
| `flaky` | Fails at configurable rate (0.0–1.0) |
| `fail_on_attempt` | Fails only on specific attempt number |
| `succeed_after_retries` | Fails first N attempts then succeeds |

---

## Retry & DLQ

- Steps retry with **exponential backoff**: `delay = BASE_DELAY_SECONDS × 2^(attempt-1)`
- Default: 5 retries, 30s base delay
- After max retries: step moves to **DLQ** (`workflow_dlq` Redis list)
- All retry attempts written to `step_retry_history` table
- **Reaper worker** recovers executions stuck in `RUNNING` for > 60 seconds

Configure in `app/core/config.py`:
```python
MAX_RETRIES = 5
BASE_DELAY_SECONDS = 30
PROCESSING_TIMEOUT_SECONDS = 60
```

---

## LLM Fallback

The parser is deterministic-first. LLM is only called when:
- The DSL is structurally malformed but repairable (broken indentation, corrupted depends syntax)

LLM is **never** called for:
- Missing arrow syntax (hard fail)
- Invalid trigger/action names (semantic validation failure)

Provider chain: **Ollama → Gemini** with 5-second total timeout budget.

Provider health tracking disables providers on fatal errors (401, 403, API key invalid) with a 5-minute cooldown before retry.

---

## Running Tests

```bash
pytest scratch_test.py -v
```

38 tests covering:
- DAG parser (linear, branching, cycle detection)
- Validation (missing action, duplicate IDs, unknown dependencies)
- Chaos modes (all 13 failure scenarios)
- Dispatcher integration
- Provider health tracking

---

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_HOST` | Redis hostname (default: `localhost`) |
| `GEMINI_API_KEY` | Google Gemini API key |
| `GEMINI_MODEL` | Gemini model name (e.g. `gemini-flash-latest`) |
| `CHAOS_MODE` | Set to `true` to enable chaos actions |
| `OLLAMA_TIMEOUT_SECONDS` | Ollama request timeout (default: `5`) |
| `GEMINI_TIMEOUT_SECONDS` | Gemini request timeout (default: `5`) |

"""
app/core/tracing.py

Production-grade distributed tracing foundation.

Provides:
- ULID-based ID generation for trace_id, span_id, provider request IDs
- build_log_context() — standardized structured log context
- build_trace_headers() — outbound HTTP header preparation for downstream propagation
- inject_trace_into_payload() — attaches trace context to action payloads

Design:
- No OpenTelemetry dependency yet — clean foundation for future OTel integration
- All IDs are prefixed for readability: wf_ / sp_ / req_
- Backward compatible — all fields are optional in log context
"""

from ulid import ULID


# ─────────────────────────────────────────────
# ID GENERATION
# ─────────────────────────────────────────────

def generate_trace_id() -> str:
    """
    Generate a root workflow trace ID.
    Format: wf_<ULID>
    Example: wf_01KSSJ2YZAE4AJ44XD9CEQX8WE
    """
    return f"wf_{ULID()}"


def generate_span_id() -> str:
    """
    Generate a step-level span ID.
    Format: sp_<ULID>
    Example: sp_01KSSJ2YZAE4AJ44XD9CEQX8WE
    """
    return f"sp_{ULID()}"


def generate_provider_request_id() -> str:
    """
    Generate a provider request ID for downstream API call tracking.
    Format: req_<ULID>
    Example: req_01KSSJ2YZAE4AJ44XD9CEQX8WE
    """
    return f"req_{ULID()}"


# ─────────────────────────────────────────────
# STRUCTURED LOG CONTEXT
# ─────────────────────────────────────────────

def build_log_context(
    workflow_execution=None,
    execution_step=None,
    trace_id: str = None,
    span_id: str = None,
    extra: dict = None,
) -> dict:
    """
    Build a standardized structured log context dict.

    Usage:
        logger.info("step_started", extra={
            "extra_data": build_log_context(
                workflow_execution=wf_exec,
                execution_step=step,
                extra={"action": "send_reminder"}
            )
        })

    Returns a flat dict suitable for JSON logging:
        {
            "trace_id": "wf_...",
            "span_id": "sp_...",
            "workflow_execution_id": 42,
            "workflow_run_id": 10,
            "step_execution_id": 7,
            "step_name": "send_reminder",
            "attempt": 1,
            ...extra fields
        }
    """
    ctx = {}

    # Resolve trace_id — prefer explicit arg, then from workflow_execution
    resolved_trace_id = trace_id
    if not resolved_trace_id and workflow_execution is not None:
        resolved_trace_id = getattr(workflow_execution, "trace_id", None)
    if resolved_trace_id:
        ctx["trace_id"] = resolved_trace_id

    # Resolve span_id — prefer explicit arg, then from execution_step
    resolved_span_id = span_id
    if not resolved_span_id and execution_step is not None:
        resolved_span_id = getattr(execution_step, "span_id", None)
    if resolved_span_id:
        ctx["span_id"] = resolved_span_id

    # Workflow execution fields
    if workflow_execution is not None:
        ctx["workflow_execution_id"] = getattr(workflow_execution, "id", None)
        ctx["workflow_run_id"] = getattr(workflow_execution, "workflow_run_id", None)
        ctx["workflow_id"] = getattr(workflow_execution, "workflow_id", None)
        ctx["workflow_status"] = getattr(workflow_execution, "status", None)

    # Step execution fields
    if execution_step is not None:
        ctx["step_execution_id"] = getattr(execution_step, "id", None)
        ctx["step_name"] = getattr(execution_step, "step_name", None)
        ctx["step_id"] = getattr(execution_step, "step_id", None)
        ctx["attempt"] = getattr(execution_step, "attempts", None)
        ctx["parent_span_id"] = getattr(execution_step, "parent_span_id", None)
        ctx["provider_request_id"] = getattr(execution_step, "provider_request_id", None)

    # Merge extra fields — extra takes lowest priority (ctx wins on conflict)
    if extra:
        for k, v in extra.items():
            if k not in ctx:
                ctx[k] = v

    # Remove None values for clean logs
    return {k: v for k, v in ctx.items() if v is not None}


# ─────────────────────────────────────────────
# DOWNSTREAM PROPAGATION
# ─────────────────────────────────────────────

def build_trace_headers(
    trace_id: str,
    span_id: str,
    parent_span_id: str = None,
    provider_request_id: str = None,
) -> dict:
    """
    Build standardized HTTP headers for downstream API call propagation.

    These headers follow the W3C traceparent convention naming pattern.
    Ready to be passed to requests.post(headers=...) when real HTTP clients are added.

    Usage:
        headers = build_trace_headers(
            trace_id=workflow_execution.trace_id,
            span_id=step_execution.span_id,
            parent_span_id=step_execution.parent_span_id,
        )
        # Future: requests.post(url, headers=headers, json=payload)

    Returns:
        {
            "X-Trace-Id": "wf_...",
            "X-Span-Id": "sp_...",
            "X-Parent-Span-Id": "wf_...",   # optional
            "X-Request-Id": "req_...",       # optional
        }
    """
    headers = {
        "X-Trace-Id": trace_id,
        "X-Span-Id": span_id,
    }

    if parent_span_id:
        headers["X-Parent-Span-Id"] = parent_span_id

    if provider_request_id:
        headers["X-Request-Id"] = provider_request_id

    return headers


def inject_trace_into_payload(
    payload: dict,
    workflow_execution,
    execution_step=None,
) -> dict:
    """
    Inject trace context into the action payload dict.

    Every downstream action receives _trace automatically.
    Chaos actions and real actions can read trace_id for logging/correlation.

    Usage:
        enriched_payload = inject_trace_into_payload(
            payload=payload,
            workflow_execution=workflow_execution,
            execution_step=step_execution,
        )
        execute_action(action_name=action, payload=enriched_payload, config=config)

    Injects:
        payload["_trace"] = {
            "trace_id": "wf_...",
            "span_id": "sp_...",
            "parent_span_id": "wf_...",
            "workflow_execution_id": 42,
            "step_execution_id": 7,
        }
    """
    trace_context = {
        "trace_id": getattr(workflow_execution, "trace_id", None),
        "workflow_execution_id": getattr(workflow_execution, "id", None),
    }

    if execution_step is not None:
        trace_context["span_id"] = getattr(execution_step, "span_id", None)
        trace_context["parent_span_id"] = getattr(execution_step, "parent_span_id", None)
        trace_context["step_execution_id"] = getattr(execution_step, "id", None)

    # Remove None values
    trace_context = {k: v for k, v in trace_context.items() if v is not None}

    enriched = dict(payload)
    enriched["_trace"] = trace_context
    return enriched

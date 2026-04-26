from app.models.audit_log import AuditLog


def create(
    db, workflow_id, action, status, event_type, request_payload, response_payload
):
    log = AuditLog(
        workflow_id=workflow_id,
        action=action,
        status=status,
        event_type=event_type,
        request_payload=request_payload,
        response_payload=response_payload,
    )
    db.add(log)

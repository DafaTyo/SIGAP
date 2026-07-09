from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    *,
    entity_type: str,
    entity_id: str,
    action: str,
    actor_id: str | None = None,
    old_values: dict | None = None,
    new_values: dict | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    log = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor_id=actor_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

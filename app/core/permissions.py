from app.models.case import Case, CaseStatus
from app.models.user import Role, User

# Roles that may create/edit cases and upload images.
CASE_WRITER_ROLES = (Role.ADMIN, Role.RADIOLOGIST, Role.CLINICIAN, Role.DOCTOR)


def can_view_case(user: User, case: Case) -> bool:
    if case.status == CaseStatus.ARCHIVED:
        return user.role == Role.ADMIN
    if user.role == Role.PATIENT:
        return case.patient_id == user.id
    return True  # admin, radiologist, clinician, doctor, data scientist
import json

from .extensions import db
from .models import ExamQuestion, ExamRecord


def migrate_details_options():
    records = ExamRecord.query.all()
    changed = 0
    for record in records:
        details = record.details or []
        need_patch = any(isinstance(item, dict) and "options" not in item for item in details)
        if not need_patch:
            continue
        question_ids = [item.get("questionId") for item in details if isinstance(item, dict)]
        questions = ExamQuestion.query.filter(ExamQuestion.id.in_(question_ids)).all()
        question_map = {q.id: q for q in questions}
        for item in details:
            if not isinstance(item, dict) or "options" in item:
                continue
            q = question_map.get(item.get("questionId"))
            if q:
                item["options"] = q.options
            else:
                item["options"] = ["(题目已从题库移除)"]
        record.details = details
        changed += 1
    if changed:
        db.session.commit()
    return changed

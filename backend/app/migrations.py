from .extensions import db
from .models import ExamQuestion, ExamRecord

_REMOVED_PLACEHOLDER = "(题目已从题库移除)"


def _options_need_standardize(options):
    if not isinstance(options, list):
        return True
    if len(options) != 4:
        return True
    if len(options) == 1 and options[0] == _REMOVED_PLACEHOLDER:
        return True
    return False


def migrate_details_options():
    records = ExamRecord.query.all()
    changed = 0
    for record in records:
        details = record.details or []
        need_patch = False
        for item in details:
            if not isinstance(item, dict):
                continue
            if "options" not in item or _options_need_standardize(item.get("options")):
                need_patch = True
                break
        if not need_patch:
            continue
        question_ids = [item.get("questionId") for item in details if isinstance(item, dict)]
        questions = ExamQuestion.query.filter(ExamQuestion.id.in_(question_ids)).all()
        question_map = {q.id: q for q in questions}
        for item in details:
            if not isinstance(item, dict):
                continue
            q = question_map.get(item.get("questionId"))
            if q and (not isinstance(item.get("options"), list) or len(item.get("options")) < 4):
                item["options"] = list(q.options)
            elif "options" not in item or _options_need_standardize(item.get("options")):
                removed_text = f"{_REMOVED_PLACEHOLDER}（原题目ID: {item.get('questionId', '未知')}）"
                item["options"] = [removed_text, removed_text, removed_text, removed_text]
        record.details = details
        changed += 1
    if changed:
        db.session.commit()
    return changed

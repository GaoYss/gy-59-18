from flask import Blueprint, jsonify, request

from ..models import ExamQuestion, ExamRecord

scores_bp = Blueprint("scores", __name__, url_prefix="/api/scores")


def _enrich_details(record_dict):
    details = record_dict.get("details") or []
    need_patch = any("options" not in item for item in details)
    if not need_patch:
        return record_dict
    question_ids = [item["questionId"] for item in details]
    questions = ExamQuestion.query.filter(ExamQuestion.id.in_(question_ids)).all()
    question_map = {q.id: q for q in questions}
    for item in details:
        q = question_map.get(item["questionId"])
        if q and "options" not in item:
            item["options"] = q.options
    return record_dict


@scores_bp.get("")
def list_scores():
    student_name = request.args.get("studentName")
    subject = request.args.get("subject")
    query = ExamRecord.query.order_by(ExamRecord.submitted_at.desc())
    if student_name:
        query = query.filter(ExamRecord.student_name.contains(student_name))
    if subject:
        query = query.filter_by(subject=subject)
    records = [_enrich_details(record.to_dict()) for record in query.all()]
    return jsonify(records)

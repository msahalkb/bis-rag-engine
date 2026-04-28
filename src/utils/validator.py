def validate_standards(recommended_ids, allowed_ids):
    return [rid for rid in recommended_ids if rid in allowed_ids]
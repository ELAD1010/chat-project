def model_to_dict(model):
    """Helper to convert SQLAlchemy models to dicts"""
    if not model:
        return None
    return {col.name: getattr(model, col.name) for col in model.__table__.columns}
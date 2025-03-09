from models import db, ActionHub

def get_user_by_id(user_id):
    return db.session.query(ActionHub).filter_by(ah_user_id=user_id).first()

def get_report_by_id(report_id):
    return db.session.query(ActionHub).filter_by(ah_report_id=report_id).first()


def get_section_by_id(section_id):
    return db.session.query(ActionHub).filter_by(ah_section_id=section_id).first()
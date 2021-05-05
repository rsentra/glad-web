from app import db

class Contracts(db.Model):
    """
    Create a Contracts table
    """

    __tablename__ = 'contracts'
    __table_args__ = {'extend_existing': True} 

    지점 = db.Column(db.String(30))
    직할지점 = db.Column(db.String(30))
    팀 = db.Column(db.String(30))
    수금사원번호 = db.Column(db.String(20))
    수금사원명 = db.Column(db.String(30))
    증권번호 = db.Column(db.String(30),primary_key=True)
    계약일자 = db.Column(db.String(10))
    보험사 = db.Column(db.String(30))
    계약종류 = db.Column(db.String(20))
    상품종류 = db.Column(db.String(20))
    초회보험료 = db.Column(db.Integer)
    계약상태 = db.Column(db.String(10))
    납입회차 = db.Column(db.Integer)
    납입방법 = db.Column(db.String(10))
    최종상태변경일 = db.Column(db.String(10))
    원수사성적 = db.Column(db.Integer)
    신글로벌성적 = db.Column(db.Integer)
    계약자 = db.Column(db.String(50))
    피보험자 = db.Column(db.String(50))
    최종납입년월 = db.Column(db.String(10))
    최종수금일 = db.Column(db.String(10))
    상품명 = db.Column(db.String(100))

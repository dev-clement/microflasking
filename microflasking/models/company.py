from microflasking import db

class CompanyModel(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    ceo_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ceo = db.relationship('companies', back_populates='users')
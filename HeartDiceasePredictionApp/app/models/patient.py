from app import db

class Patient(db.Model):
    '''
    Klasa tworząca tabele pacjent
    w bazie danych SQLite
    '''

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(3))
    sex = db.Column(db.String(10))
    cp = db.Column(db.String(30))
    trestbps = db.Column(db.String(30))
    chol = db.Column(db.String(30))
    fbs = db.Column(db.String(30))
    restecg = db.Column(db.String(30))
    thalach = db.Column(db.String(30))
    exang = db.Column(db.String(30))
    oldpeak = db.Column(db.String(30))
    slope = db.Column(db.String(30))
    ca = db.Column(db.String(30))
    thal = db.Column(db.String(30))
    
    decisiontree = db.Column(db.Boolean)
    knn = db.Column(db.Boolean)
    logisticregression = db.Column(db.Boolean)
    mlp = db.Column(db.Boolean)
    randomforest = db.Column(db.Boolean)
    scv = db.Column(db.Boolean)



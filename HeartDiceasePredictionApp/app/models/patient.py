from app import db


class Algoritm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model=db.Column(db.String(30))
    test_score=db.Column(db.Float) 
    precision=db.Column(db.Float) 
    recall=db.Column(db.Float) 
    f1=db.Column(db.Float) 
    auc=db.Column(db.Float) 
    cost_of_loss=db.Column(db.Integer) 
    type = db.Column(db.String(30))
    access = db.Column(db.Boolean)
    version = db.Column(db.Integer)

    algoritmHeard_patient_id = db.relationship('Algoritm_Patient', backref='algoritmHeard', lazy=True)
    algoritmBreastCancer_patient_id = db.relationship('Algoritm_PatientBreastCancer', backref='algoritmBreastCancer', lazy=True)
    algoritmThyroid_patient_id = db.relationship('Algoritm_PatientThyroid', backref='algoritmThyroid', lazy=True)


class Patient(db.Model):
    '''
    Klasa tworząca tabele pacjent
    w bazie danych SQLite
    '''

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    cp = db.Column(db.String(30))
    trestbps = db.Column(db.Integer)
    chol = db.Column(db.Integer)
    fbs = db.Column(db.String(30))
    restecg = db.Column(db.String(30))
    thalach = db.Column(db.Integer)
    exang = db.Column(db.String(5))
    oldpeak = db.Column(db.Float)
    slope = db.Column(db.String(30))
    ca = db.Column(db.Integer)
    thal = db.Column(db.String(30))

    access = db.Column(db.Boolean)
    
    correct_prediction = db.Column(db.Boolean)

    patient_algoritmML_id = db.relationship('Algoritm_Patient', backref='patient', lazy=True)

class Algoritm_Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    algorytmML_id = db.Column(db.Integer, db.ForeignKey('algoritm.id'))
    prediction = db.Column(db.Boolean)

class Patientbreastcancer(db.Model):
    '''
    Klasa tworząca tabele pacjent
    w bazie danych SQLite
    '''

    id = db.Column(db.Integer, primary_key=True)
    cThickness = db.Column(db.Integer) #clumpThickness
    uofCSize = db.Column(db.Integer) # uniformity of Cell Size
    uofShape = db.Column(db.Integer) # uniformity of Cell Shape
    mAdhesion = db.Column(db.Integer) # marginal Adhesion
    sECSize = db.Column(db.Integer) # single Epithelial Cell Size
    bNuclei = db.Column(db.Integer) # bare Nuclei
    bChromatin = db.Column(db.Integer) #bland Chromatin
    nNucleoli = db.Column(db.Integer) #normal Nucleoli
    mitoses = db.Column(db.Integer) #mitoses
    access = db.Column(db.Boolean)
    
    correct_prediction = db.Column(db.Boolean)

    patient_algoritmML_id = db.relationship('Algoritm_PatientBreastCancer', backref='patient', lazy=True)

class Algoritm_PatientBreastCancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patientbreastcancer.id'))
    algorytmML_id = db.Column(db.Integer, db.ForeignKey('algoritm.id'))
    prediction = db.Column(db.Boolean)

class Patientthyroid(db.Model):
    '''
    Klasa tworząca tabele pacjent
    w bazie danych SQLite
    '''

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer) 
    sex = db.Column(db.Integer) 
    on_thyroxine = db.Column(db.Boolean) 
    maybe_on_thyroxine = db.Column(db.Boolean) 
    on_antithyroid_medication = db.Column(db.Boolean) 
    sick_patient_reports_malaise = db.Column(db.Boolean) 
    pregnant = db.Column(db.Boolean) 
    thyroid_surgery = db.Column(db.Boolean) 
    treatment = db.Column(db.Boolean) 
    test_hypothyroid = db.Column(db.Boolean) 
    test_hyperthyroid = db.Column(db.Boolean) 
    on_lithium = db.Column(db.Boolean) 
    has_goitre = db.Column(db.Boolean) 
    has_tumor = db.Column(db.Boolean) 
    hypopituitary = db.Column(db.Boolean) 
    psychological_symptoms = db.Column(db.Boolean) 
    tsh = db.Column(db.Float) 
    t_three = db.Column(db.Float) 
    tt_four = db.Column(db.Float) 
    t_four_u = db.Column(db.Float) 
    fti = db.Column(db.Float)
    access = db.Column(db.Boolean) 
    
    correct_prediction = db.Column(db.Boolean)

    patient_algoritmML_id = db.relationship('Algoritm_PatientThyroid', backref='patient', lazy=True)

class Algoritm_PatientThyroid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patientthyroid.id'))
    algorytmML_id = db.Column(db.Integer, db.ForeignKey('algoritm.id'))
    prediction = db.Column(db.Boolean)






from flask_wtf import FlaskForm
from flask_wtf.recaptcha import widgets
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField, RadioField
from wtforms.validators import DataRequired, InputRequired,Required, NumberRange,Optional
from wtforms.widgets.html5 import NumberInput


class FormHeardDicease(FlaskForm):
    age =  IntegerField('Clump Thickness', widget=NumberInput(step=1,min=1,max=110), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=110,message='Zła wartość')])
    sex = SelectField('sex',choices=[('female','kobieta'),('male','meżczyna')])
    cp = SelectField('cp',choices=[('typical angina','typical angina'),('atypical angina','atypical angina'),('non-anginal pain','non-anginal pain'),('asymptomatic','asymptomatic')],validators=[DataRequired()])
    trestbps = IntegerField('trestbps', widget=NumberInput(step=1,min=80,max=250), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=80,max=250,message='Zła wartość')])
    chol = IntegerField('chol', widget=NumberInput(step=1,min=100,max=750), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=100,max=750,message='Zła wartość')]) 
    fbs = RadioField('fbs', choices=[('lower than 120mg/ml','lower than 120mg/ml'),('greater than 120mg/ml','greater than 120mg/ml')],validators=[DataRequired(message='Wypełnij pole')],default='lower than 120mg/ml')
    restecg = SelectField('restecg',choices=[('normal','normal'),('ST-T wave abnormality','ST-T wave abnormality'),('left ventricular hypertrophy','left ventricular hypertrophy')],validators=[DataRequired()])
    thalach =  IntegerField('thalach', widget=NumberInput(step=1,min=50,max=250), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=50,max=250,message='Zła wartość')]) 
    exang = RadioField('exang', choices=[('no','Nie'),('yes','Tak')],validators=[DataRequired(message='Wypełnij pole')],default='no')
    oldpeak = FloatField('oldpeak', widget=NumberInput(step=0.01,min=0,max=10), validators=[InputRequired(message='Wypełnij pole'), NumberRange(min=0,max=10,message='Zła wartość')])
    slope = SelectField('slope',choices=[('upsloping','upsloping'),('flat','flat'),('downsloping','downsloping')],validators=[DataRequired()]) 
    ca = IntegerField('ca', widget=NumberInput(step=1,min=0,max=3), validators=[InputRequired(message='Wypełnij pole'), NumberRange(min=0,max=3,message='Zła wartość')]) 
    thal = SelectField('thal',choices=[('normal','normal'),('fixed defect','fixed defect'),('reversable defect','reversable defect')],validators=[DataRequired()]) 
    submit = SubmitField('Potwierdz')

class Formbreastcancer(FlaskForm):
    clump_thickness = IntegerField('Clump Thickness', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    uniformity_of_cell_size = IntegerField('Uniformity of Cell Size', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    uniformity_of_cell_shape = IntegerField('Uniformity of Cell Shape', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    marginal_adhesion = IntegerField('Marginal Adhesion', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    single_epithelial_cell_size = IntegerField('Single Epithelial Cell Size', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    bare_nuclei = IntegerField('Bare Nuclei', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    bland_chromatin = IntegerField('Bland Chromatin', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    normal_nucleoli = IntegerField('Normal Nucleoli', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    mitoses = IntegerField('Mitoses', widget=NumberInput(step=1,min=1,max=10), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=10,message='Zła wartość')])
    submit = SubmitField('Potwierdz')

class FormThyroid(FlaskForm):
    age = IntegerField('Clump Thickness', widget=NumberInput(step=1,min=1,max=120), validators=[DataRequired(message='Wypełnij pole'), NumberRange(min=1,max=120,message='Zła wartość')])
    sex = SelectField('sex',choices=[(0,'kobieta'),(1,'meżczyna')])

    on_thyroxine = SelectField('on_thyroxine',choices=[(0,'Fałsz'),(1,'Prawda')],validators=[DataRequired(message='Wypełnij pole')])
    maybe_on_thyroxine = SelectField('on_thyroxine',choices=[(0,'Fałsz'),(1,'Prawda')],validators=[DataRequired(message='Wypełnij pole')])
    on_antithyroid_medication = SelectField('on_thyroxine',choices=[(0,'Fałsz'),(1,'Prawda')],validators=[DataRequired(message='Wypełnij pole')])

    sick_patient_reports_malaise = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)
    pregnant = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)
    thyroid_surgery = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)
    treatment = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)

    test_hypothyroid = SelectField('on_thyroxine',choices=[(0,'Fałsz'),(1,'Prawda')],validators=[DataRequired(message='Wypełnij pole')])
    test_hyperthyroid = SelectField('on_thyroxine',choices=[(0,'Fałsz'),(1,'Prawda')],validators=[DataRequired(message='Wypełnij pole')])
    on_lithium = SelectField('on_thyroxine',choices=[(0,'Fałsz'),(1,'Prawda')],validators=[DataRequired(message='Wypełnij pole')])

    has_goitre = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)
    has_tumor = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)
    hypopituitary = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)
    psychological_symptoms = RadioField('on thyroxine', choices=[(0,'Nie'),(1,'Tak')],validators=[DataRequired(message='Wypełnij pole')],default=0)

    tsh = FloatField('Clump Thickness', widget=NumberInput(step=0.001,min=0,max=1), validators=[InputRequired(message='Wypełnij pole'), NumberRange(min=0,max=1,message='Zła wartość')])
    t_three = FloatField('Clump Thickness', widget=NumberInput(step=0.0001,min=0,max=0.3), validators=[InputRequired(message='Wypełnij pole'), NumberRange(min=0,max=0.3,message='Zła wartość')])
    tt_four = FloatField('Clump Thickness', widget=NumberInput(step=0.001,min=0,max=0.75), validators=[InputRequired(message='Wypełnij pole'), NumberRange(min=0,max=0.75,message='Zła wartość')])
    t_four_u = FloatField('Clump Thickness', widget=NumberInput(step=0.001,min=0,max=0.3), validators=[InputRequired(message='Wypełnij pole'), NumberRange(min=0,max=0.3,message='Zła wartość')])
    fti = FloatField('Clump Thickness', widget=NumberInput(step=0.001,min=0,max=0.75), validators=[InputRequired(message='Wypełnij pole'), NumberRange(min=0,max=0.75,message='Zła wartość')])
    submit = SubmitField('Potwierdz')
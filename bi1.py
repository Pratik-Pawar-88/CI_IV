
# Download data from (heart.csv) -> https://rb.gy/kteskv

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HeartData(db.Model):
    __tablename__ = 'heart_data'  # Ensures the table name is explicitly set
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    Age = db.Column(db.Float)
    Sex = db.Column(db.Float)
    ChestPainType = db.Column(db.Float)
    RestingBP = db.Column(db.Float)
    Cholesterol = db.Column(db.Float)
    FastingBS = db.Column(db.Float)
    RestingECG = db.Column(db.Float)
    MaxHR = db.Column(db.Float)
    ExerciseAngina = db.Column(db.Float)
    Oldpeak = db.Column(db.Float)
    ST_Slope = db.Column(db.Float)
    HeartDisease = db.Column(db.Float)

    def __repr__(self):
        return f'<HeartData {self.id}>'

def load_data_from_csv(csv_file):
    with app.app_context():
        data = pd.read_csv(csv_file)
        data.reset_index(inplace=True)  # Reset index to create an automatic 'index' column
        data.rename(columns={'index': 'id'}, inplace=True)  # Rename 'index' column to 'id'
        data.to_sql('heart_data', db.engine, index=False, if_exists='replace')  # 'index=False' avoids creating an extra unnamed column

@app.route('/')
def index():
    return 'Flask App with SQLAlchemy'

@app.route('/data')
def view_data():
    heart_data = HeartData.query.all()
    data = [{
        'Age': entry.Age,
        'Sex': entry.Sex,
        'ChestPainType': entry.ChestPainType,
        'RestingBP': entry.RestingBP,
        'Cholesterol': entry.Cholesterol,
        'FastingBS': entry.FastingBS,
        'RestingECG': entry.RestingECG,
        'MaxHR': entry.MaxHR,
        'ExerciseAngina': entry.ExerciseAngina,
        'Oldpeak': entry.Oldpeak,
        'ST_Slope': entry.ST_Slope,
        'HeartDisease': entry.HeartDisease
    } for entry in heart_data]

    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Create tables based on model definitions
        load_data_from_csv('heart.csv')
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignments.db'
db = SQLAlchemy(app)


# Database model
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(50), nullable=False)


def initialize_database():
    with app.app_context():
        db.create_all()


# Initialize the database
initialize_database()


@app.route('/')
def index():
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00",
             "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00",
             "18:00-19:00", "19:00-20:00"]
    options = ["none", "TV", "PC/PHONE", "PLAY", "STUDY", "READ HEBREW", "READ ENGLISH"]

    days_with_index = list(enumerate(days))
    hours_with_index = list(enumerate(hours))

    # Retrieve assignments from the database
    assignments = {}
    for assignment in Assignment.query.all():
        assignments[(assignment.day, assignment.hour)] = assignment.value

    return render_template('index.html', days_with_index=days_with_index, hours_with_index=hours_with_index,
                           options=options, assignments=assignments)


@app.route('/update_assignment', methods=['POST'])
def update_assignment():
    day = int(request.json['day'])
    hour = int(request.json['hour'])
    value = request.json['value']

    assignment = Assignment.query.filter_by(day=day, hour=hour).first()
    if assignment:
        assignment.value = value
    else:
        assignment = Assignment(day=day, hour=hour, value=value)
        db.session.add(assignment)

    db.session.commit()
    return jsonify(success=True)


@app.route('/reset_assignments', methods=['POST'])
def reset_assignments():
    Assignment.query.delete()
    db.session.commit()
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

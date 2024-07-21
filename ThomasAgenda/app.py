from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Persistent storage for assignments
assignments = {}

@app.route('/')
def index():
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00",
             "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00",
             "18:00-19:00", "19:00-20:00"]
    options = ["none", "TV", "PC/PHONE", "PLAY", "STUDY", "READ HEBREW", "READ ENGLISH"]

    days_with_index = list(enumerate(days))
    hours_with_index = list(enumerate(hours))

    # Initialize assignments if not already done
    if not assignments:
        for day_index, _ in days_with_index:
            for hour_index, _ in hours_with_index:
                assignments[(day_index, hour_index)] = "none"

    return render_template('index.html', days_with_index=days_with_index,
                           hours_with_index=hours_with_index, options=options, assignments=assignments)

@app.route('/update_assignment', methods=['POST'])
def update_assignment():
    day = int(request.json['day'])
    hour = int(request.json['hour'])
    value = request.json['value']
    assignments[(day, hour)] = value
    return jsonify(success=True)

@app.route('/reset_assignments', methods=['POST'])
def reset_assignments():
    for key in assignments.keys():
        assignments[key] = "none"
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

from flask import Flask, render_template, request, jsonify
import hashlib
import datetime

app = Flask(__name__)

# Simulating a simple blockchain
blockchain = []

class Certificate:
    def __init__(self, student_name, roll_number, institution, date, subjects):
        self.student_name = student_name
        self.roll_number = roll_number
        self.institution = institution
        self.date = date
        self.subjects = subjects
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.student_name}{self.roll_number}{self.institution}{self.date}{str(self.subjects)}"
        return hashlib.sha256(data.encode()).hexdigest()

def add_certificate_to_blockchain(certificate):
    blockchain.append(certificate)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/issue_certificate', methods=['POST'])
def issue_certificate():
    data = request.json
    subjects = {subject: int(mark) for subject, mark in data['subjects'].items() if mark}
    certificate = Certificate(
        data['student_name'],
        data['roll_number'],
        data['institution'],
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        subjects
    )
    add_certificate_to_blockchain(certificate)
    return jsonify({"message": "Certificate issued successfully", "hash": certificate.hash})

@app.route('/verify_certificate', methods=['POST'])
def verify_certificate():
    data = request.json
    for cert in blockchain:
        if cert.hash == data['hash']:
            return jsonify({
                "verified": True,
                "student_name": cert.student_name,
                "roll_number": cert.roll_number,
                "institution": cert.institution,
                "date": cert.date,
                "subjects": cert.subjects
            })
    return jsonify({"verified": False})

@app.route('/get_certificates', methods=['GET'])
def get_certificates():
    return jsonify([{
        "hash": cert.hash,
        "student_name": cert.student_name,
        "roll_number": cert.roll_number,
        "institution": cert.institution,
        "date": cert.date,
        "subjects": cert.subjects
    } for cert in blockchain])

if __name__ == '__main__':
    app.run(debug=True)
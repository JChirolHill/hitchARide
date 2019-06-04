from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from models import create_car, get_cars, deleteCar, joinCar, getCar, editCar
app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        destination = request.form.get('destination')
        name = request.form.get('name')
        phone = request.form.get('phone')
        location = request.form.get('location')
        passengerNum = request.form.get('passengerNum')
        secretCode = request.form.get('secretCode')
        create_car(date, time, destination, name, phone, location, passengerNum, secretCode)

    cars = get_cars()

    return render_template('index.html', cars=cars)

@app.route('/delete/<carID>', methods=['POST'])
def delete_entry(carID):
    deleteCar(carID)
    cars = get_cars()
    return redirect('/')

@app.route('/join/<carID>', methods=['POST'])
def join_car(carID):
    car = getCar(carID)
    return render_template('join.html', car=car)

@app.route('/join/<carID>/submit', methods=['POST'])
def join_car_Submit(carID):
    name = request.form.get('name')
    phone = request.form.get('phone')
    joinCar(carID, name, phone)
    
    cars = get_cars()
    return redirect('/')

@app.route('/edit/<carID>', methods=['POST'])
def edit_car(carID):
    secretCode = request.form.get('sc')
    car = getCar(carID)
    if secretCode == car[0][20]:
        return render_template('edit.html', car=car)
    else: 
        cars = get_cars()
        return redirect('/')

@app.route('/edit/<carID>/submit', methods=['POST'])
def edit_car_Submit(carID):
    date = request.form.get('date')
    time = request.form.get('time')
    destination = request.form.get('destination')
    phone = request.form.get('phone')
    location = request.form.get('location')
    editCar(carID, date, time, destination, phone, location)

    cars = get_cars()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True) 
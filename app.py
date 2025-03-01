from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from passlib.hash import sha256_crypt
from models import createRide, getRides, deleteRide, joinRide, getRide, editRide, createPerson, getPeople, getPerson, getPassengers, getRequests, driveRide, getDriver
app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        newId = createPerson(name, phone)

        date = request.form.get('date')
        time = request.form.get('time')
        destination = request.form.get('destination')
        pickUpSpot = request.form.get('pickUpSpot')
        passengerNum = request.form.get('passengerNum')
        sc = request.form.get('secretCode')
        secretCode = sha256_crypt.encrypt(sc)
        print(secretCode)
        createRide(date, time, destination, pickUpSpot, newId, passengerNum, passengerNum, secretCode)

    rides = getRides()
    ridesWithDrivers = []
    for ride in rides:
        ridesWithDrivers.append((ride, getDriver(ride[5])))
    requests = getRequests()
 
    return render_template('index.html', rides=ridesWithDrivers, requests=requests)

@app.route('/createRequest', methods=['POST'])
def create_request():
    date = request.form.get('date')
    time = request.form.get('time')
    destination = request.form.get('destination')
    pickUpSpot = request.form.get('pickUpSpot')
    rideId = createRide(date, time, destination, pickUpSpot, -1, 0, 0, None)

    rides = getRides()
    drivers = getPeople()
    reqests = getRequests()
    return redirect('/')

@app.route('/driveRide/<rideId>', methods=['POST'])
def drive_ride(rideId):
    ride = getRide(rideId)
    return render_template('driveRide.html', ride=ride)

@app.route('/driveRide/<rideId>/submit', methods=['POST'])
def drive_ride_submit(rideId):
    name = request.form.get('name')
    phone = request.form.get('phone')
    passengerNum = request.form.get('passengerNum')
    sc = request.form.get('secretCode')
    secretCode = sha256_crypt.encrypt(sc)

    driverId = createPerson(name, phone)
    driveRide(rideId, driverId, passengerNum, secretCode)
    
    rides = getRides()
    return redirect('/')


@app.route('/join/<rideId>', methods=['POST'])
def join_ride(rideId):
    ride = getRide(rideId)
    return render_template('join.html', ride=ride)

@app.route('/join/<rideId>/submit', methods=['POST'])
def join_ride_submit(rideId):
    name = request.form.get('name')
    phone = request.form.get('phone')
    passengerId = createPerson(name, phone)
    joinRide(rideId, passengerId)
    
    rides = getRides()
    return redirect('/')

@app.route('/details/<rideId>', methods=['POST'])
def ride_details(rideId):
    ride = getRide(rideId)
    passengerLimit = ride[0][6]
    driver = getPerson(ride[0][5])
    passengers = getPassengers(rideId, passengerLimit)

    return render_template('details.html', ride=ride, driver=driver, passengers=passengers)

@app.route('/edit/<rideId>', methods=['POST'])
def edit_ride(rideId):
    secretCode = request.form.get('sc')
    ride = getRide(rideId)
    if sha256_crypt.verify(secretCode, ride[0][8]):
        passengerLimit = ride[0][6]
        passengers = getPassengers(rideId, passengerLimit)
        return render_template('edit.html', ride=ride, passengers=passengers)
    else: 
        rides = getRides()
        return redirect('/')

@app.route('/edit/<rideId>/submit', methods=['POST'])
def edit_ride_submit(rideId):
    date = request.form.get('date')
    time = request.form.get('time')
    destination = request.form.get('destination')
    pickUpSpot = request.form.get('pickUpSpot')
    removedPassengers = request.form.getlist('removedPassenger')
    removedPassengerIds = (passenger[0] for passenger in removedPassengers)
    removedPeopleIds = (passenger[1] for passenger in removedPassengers)
    editRide(rideId, date, time, destination, pickUpSpot, removedPassengerIds, removedPeopleIds)

    rides = getRides()
    return redirect('/')

@app.route('/delete/<rideId>', methods=['POST'])
def delete_ride(rideId):
    deleteRide(rideId)
    rides = getRides()
    return redirect('/')

@app.route('/privacy', methods=['POST'])
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True) 
import sqlite3 as sql
from datetime import datetime, time, timedelta
from os import path

ROOT = path.dirname(path.relpath((__file__)))

def createRide(date, time, destination, pickUpSpot, driverId, passengerNum, spotsOpen, secretCode):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('insert into rides (date, time, destination, pickUpSpot, driverId, numberOfPassengers, spotsOpen, secretCode) values(?,?,?,?,?,?,?,?)', (date, time, destination, pickUpSpot, driverId, passengerNum, passengerNum, secretCode))
    newID = cur.lastrowid
    con.commit()
    con.close()
    return newID;

def getRides():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from rides where not driverId = -1 ORDER BY date, destination;')
    rides = cur.fetchall()
    con.close()
    #Delete the first car if it is out of date
    if len(rides) > 0:
        firstTripDate = datetime.strptime(rides[0][1], "%Y-%m-%d")
        if firstTripDate < datetime.now() - timedelta(days=1):
            deleteRide(rides[0][0])
    return rides

def getRequests():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor() 
    cur.execute('select * from rides where driverId = -1 ORDER BY date, destination;')
    requests = cur.fetchall()
    con.close()
    #Delete the first request if it is out of date
    if len(requests) > 0:
        firstTripDate = datetime.strptime(requests[0][1], "%Y-%m-%d")
        if firstTripDate < datetime.now() - timedelta(days=1):
            deleteRide(requests[0][0])
    return requests

def driveRide(rideId, driverId, passengerNum, secretCode):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('update rides set driverId = ? where id = ?', [driverId, rideId])
    cur.execute('update rides set secretCode = ? where id = ?', [secretCode, rideId])
    cur.execute('update rides set spotsOpen = spotsOpen + ? where id = ?', [passengerNum, rideId])
    cur.execute('update rides set numberOfPassengers = ? where id = ?', [passengerNum, rideId])
    con.commit()
    con.close()

def joinRide(rideId, passengerId):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('insert into passengers (rideId, passengerId) values(?,?)', (rideId, passengerId))
    cur.execute('update rides set spotsOpen = spotsOpen - 1 where id = ?', [rideId])
    con.commit()
    con.close()

def getRide(rideId):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from rides where id = ?', [rideId])
    car = cur.fetchall()
    con.close()
    return car

def deleteRide(rideId):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('delete from rides WHERE id = ?', [rideId])
    con.commit()
    con.close()
    passengers = getPassengers(rideId, 10000)
    passIds=(passenger[3] for passenger in passengers)
    peopleIds=(passenger[0] for passenger in passengers)
    deletePassengers(passIds)
    deletePeople(peopleIds)


def editRide(rideId, date, time, destination, pickUpSpot, removedPassengerIds, removedPeopleIds):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('update rides set date = ? where id = ?', [date, rideId])
    cur.execute('update rides set time = ? where id = ?', [time, rideId])
    cur.execute('update rides set destination = ? where id = ?', [destination, rideId])
    cur.execute('update rides set pickUpSpot = ? where id = ?', [pickUpSpot, rideId])
    con.commit()
    con.close()
    deletePassengers(removedPassengerIds)
    deletePeople(removedPeopleIds)


def createPerson(name, phone):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('insert into people (name, phone) values(?,?)', (name, phone))
    newID = cur.lastrowid
    con.commit()
    con.close()
    return newID

def getPeople():
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from people;')
    people = cur.fetchall()
    con.close()
    return people

def getPerson(personId):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from people where id = ?', [personId])
    person = cur.fetchall()
    con.close()
    return person

#Get rid of this if we move to a log in method 
def deletePeople(peopleIds):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    for id in peopleIds:
        cur.execute('delete from people where id = ?', [id])
    con.commit()
    con.close()

def getDriver(driverId):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from people where id = ?', [driverId])
    drivers = cur.fetchall()
    con.close()
    return drivers

def getPassengers(rideId, passengerLimit):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    cur.execute('select * from people join passengers on people.id = passengers.passengerId where passengers.rideId = ? limit ?', [rideId, passengerLimit])
    passengers = cur.fetchall()
    con.close()
    return passengers

def deletePassengers(removedPassengers):
    con = sql.connect(path.join(ROOT, 'database.db'))
    cur = con.cursor()
    for id in removedPassengers:
        cur.execute('delete from passengers where id = ?', [id])
        cur.execute('update rides set spotsOpen = spotsOpen + 1 where id = ?', [id])
    con.commit()
    con.close()

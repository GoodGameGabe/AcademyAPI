import os, copy
import sqlalchemy
from models import db, Course, Student
from flask_migrate import Migrate
from flask import Flask, jsonify, request

app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/hey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)



def getAll(table):
    entries = table.query.all()
    response = []
    for e in entries:
        entry = e.to_dict()
        response.append(entry)
    return response

def getID(anID, table):
    if anID > 0:
        check = table.query.get(anID)
        entry = check.to_dict()
        return jsonify({"data": entry})
        
    response = jsonify({"error": 400, "message":"no member found"})  
    return jsonify({"data": response})

def getRelatives(member, types):
  tempList= []
  for types_id in member[types]:
    tempList.append(getMainID(types_id))
  member[types] = tempList
  return member
    
def getStudent(studentID):    
    #this gives me the writable student
    student = Student.query.get(studentID);
    #gives me student course id
    students_course = student.course
    #gets the course
    the_course = Course.query.get(students_course)
    #gets the course
    course_name = the_course.name
    student.course = course_name
    the_student = student.to_dict()
    return jsonify({"data": the_student})
    
def deleteAll(table):
    every = table.query.all()
    arr = []
    for i in every:
        arr.append(i)
        db.session.delete(i)
        db.session.commit()
    return jsonify({"deleted": "%s" % arr})

def deleteOne(anID, table):
    entries = table.query.get(anID)
    arr = []
    arr.append(i)
    db.session.delete(i)
    db.session.commit()
    return jsonify({"deleted": "%s" % arr})
    
    response = jsonify({"error": 400, "message":"no member found"})  
    return jsonify({"data": response})
        
@app.route('/', methods=['GET'])
def test(): 
    bele = Student.query.get(1)
    bele = getCourse(bele, "name")
    return bele

@app.route('/courses', methods=['GET'])
def courses():
    return jsonify({"data": getAll(Course)})
    
@app.route('/course/add', methods=['POST'])
def addCourse():
    info = request.get_json() or {}
    course = Course(name=info["name"])
    db.session.add(course)
    db.session.commit()
    return jsonify({"response":"ok"})

@app.route('/course/<int:id>', methods=['GET','DELETE'])
def courseID(id):
    if id > 0:
        if request.method == 'GET':
            return getID(id, Course)
        elif request.method == 'DELETE':
            return deleteOne(id, Course)
        else:
            return("NOPE")
    
@app.route('/coursesOut', methods=['DELETE'])
def destroyCourses():
    return deleteAll(Course)

@app.route('/students', methods=['GET'])
def students():
    return jsonify({"data": getAll(Student)})
    
@app.route('/student/add', methods=['POST'])
def addStudent():
    info = request.get_json() or {}
    student = Student(
        first_name=info["first_Name"],
        last_name=info["last_Name"],
        course=info["course"],
        age=info["age"]
        )
    db.session.add(student)
    db.session.commit()
    return jsonify({"response":"ok"})

@app.route('/student/<int:id>', methods=['GET','PUT','DELETE'])
def studentMethod(id):
    if id > 0:
        if request.method == 'GET':
            return(getStudent(id))
        
        elif request.method == 'PUT':
            info = request.get_json() or {}
            student = Student.query.get(id)
            student.course = info["course"]
            db.session.commit()
            return jsonify({"status_code":"200","data":student.to_dict()})
        
        elif request.method == 'DELETE':
            return deleteOne(id, Student)
        else:
            return("NOPE")

@app.route('/studentsOut', methods=['DELETE'])
def destroyStudents():
    return deleteAll(Student)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
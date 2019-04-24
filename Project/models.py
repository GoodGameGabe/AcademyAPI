from flask_sqlalchemy import SQLAlchemy
  
db = SQLAlchemy()
  
#Example model Item 
#It represents an Item in a list
#you can use any name, first letter in CAPS
  
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    students = db.relationship("Student") #List of students
  
    def __repr__(self):
        return 'Course: %s' % self.name
  
    def to_dict(self):
        students = []
        for s in self.students:
            students.append(s.to_dict())
        return { 
          "id": self.id, 
          "name": self.name, 
          "students": students 
        }
  
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    
    def __repr__(self):
        return 'Student: %s' % self.first_name
  
    def to_dict(self):
        return { 
          "id": self.id, 
          "first_name": self.first_name, 
          "last_name": self.last_name, 
          "course": self.course,
          "age": self.age 
        }
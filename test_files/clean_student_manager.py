"""
Clean Student Management System
A safe student record management application.
This file contains no malware signatures.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class Student:
    """Represents a student record."""
    student_id: str
    name: str
    age: int
    grade: str
    gpa: float
    courses: List[str]
    enrollment_date: datetime


class StudentManager:
    """Manage student records safely."""
    
    def __init__(self):
        self.students: Dict[str, Student] = {}
    
    def add_student(self, student: Student) -> bool:
        """Add a new student to the system."""
        if student.student_id in self.students:
            print(f"Student {student.student_id} already exists")
            return False
        
        self.students[student.student_id] = student
        print(f"Added student: {student.name} ({student.student_id})")
        return True
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve a student by ID."""
        return self.students.get(student_id)
    
    def update_gpa(self, student_id: str, new_gpa: float) -> bool:
        """Update a student's GPA."""
        student = self.get_student(student_id)
        if not student:
            print(f"Student {student_id} not found")
            return False
        
        old_gpa = student.gpa
        student.gpa = new_gpa
        print(f"Updated GPA for {student.name}: {old_gpa:.2f} -> {new_gpa:.2f}")
        return True
    
    def enroll_course(self, student_id: str, course: str) -> bool:
        """Enroll a student in a course."""
        student = self.get_student(student_id)
        if not student:
            print(f"Student {student_id} not found")
            return False
        
        if course in student.courses:
            print(f"{student.name} is already enrolled in {course}")
            return False
        
        student.courses.append(course)
        print(f"Enrolled {student.name} in {course}")
        return True
    
    def get_students_by_grade(self, grade: str) -> List[Student]:
        """Get all students in a specific grade."""
        return [s for s in self.students.values() if s.grade == grade]
    
    def get_honor_students(self, min_gpa: float = 3.5) -> List[Student]:
        """Get students with GPA above threshold."""
        honor_students = [s for s in self.students.values() if s.gpa >= min_gpa]
        honor_students.sort(key=lambda x: x.gpa, reverse=True)
        return honor_students
    
    def get_statistics(self) -> Dict[str, any]:
        """Get statistics about all students."""
        if not self.students:
            return {}
        
        total = len(self.students)
        avg_gpa = sum(s.gpa for s in self.students.values()) / total
        
        grade_distribution = {}
        for student in self.students.values():
            grade_distribution[student.grade] = grade_distribution.get(student.grade, 0) + 1
        
        return {
            'total_students': total,
            'average_gpa': avg_gpa,
            'grade_distribution': grade_distribution,
            'honor_students': len(self.get_honor_students())
        }
    
    def display_student(self, student_id: str):
        """Display detailed information about a student."""
        student = self.get_student(student_id)
        if not student:
            print(f"Student {student_id} not found")
            return
        
        print(f"\nStudent Information:")
        print(f"  ID: {student.student_id}")
        print(f"  Name: {student.name}")
        print(f"  Age: {student.age}")
        print(f"  Grade: {student.grade}")
        print(f"  GPA: {student.gpa:.2f}")
        print(f"  Enrolled: {student.enrollment_date.strftime('%Y-%m-%d')}")
        print(f"  Courses: {', '.join(student.courses)}")


def demo():
    """Demonstrate student management system."""
    print("Student Management System Demo")
    print("=" * 60)
    
    # Create manager
    manager = StudentManager()
    
    # Add students
    students_data = [
        Student("S001", "Alice Johnson", 20, "Sophomore", 3.8, 
                ["Math", "Physics", "Computer Science"], datetime(2023, 9, 1)),
        Student("S002", "Bob Smith", 19, "Freshman", 3.2, 
                ["English", "History", "Biology"], datetime(2024, 9, 1)),
        Student("S003", "Charlie Brown", 21, "Junior", 3.9, 
                ["Chemistry", "Math", "Statistics"], datetime(2022, 9, 1)),
        Student("S004", "Diana Prince", 20, "Sophomore", 4.0, 
                ["Physics", "Math", "Engineering"], datetime(2023, 9, 1)),
        Student("S005", "Eve Davis", 22, "Senior", 3.6, 
                ["Computer Science", "AI", "Data Science"], datetime(2021, 9, 1)),
    ]
    
    for student in students_data:
        manager.add_student(student)
    
    # Display statistics
    stats = manager.get_statistics()
    print(f"\nSystem Statistics:")
    print(f"  Total Students: {stats['total_students']}")
    print(f"  Average GPA: {stats['average_gpa']:.2f}")
    print(f"  Honor Students: {stats['honor_students']}")
    
    print("\nGrade Distribution:")
    for grade, count in stats['grade_distribution'].items():
        print(f"  {grade}: {count}")
    
    # Show honor students
    print("\nHonor Roll (GPA >= 3.5):")
    for student in manager.get_honor_students():
        print(f"  {student.name}: {student.gpa:.2f}")
    
    # Display a specific student
    manager.display_student("S001")
    
    # Enroll in new course
    print()
    manager.enroll_course("S001", "Algorithms")


if __name__ == "__main__":
    demo()

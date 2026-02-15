"""
Verification Agent
Handles student authentication and verification
"""

from typing import Dict
from sqlalchemy.orm import Session
from models import Student


class VerificationAgent:
    """Verifies student credentials"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_student(self, faculty_number: str, enrollment_number: str) -> Dict:
        """Verify student credentials"""
        student = self.db.query(Student).filter(
            Student.faculty_number == faculty_number,
            Student.enrollment_number == enrollment_number
        ).first()
        
        if not student:
            return {
                "verified": False,
                "message": "Invalid credentials",
                "student": None
            }
        
        return {
            "verified": True,
            "message": f"Welcome, {student.name}!",
            "student": {
                "id": student.id,
                "name": student.name,
                "faculty_number": student.faculty_number,
                "branch": student.branch,
                "current_semester": student.current_semester,
                "cgpa": student.cgpa,
                "total_earned_credits": student.total_earned_credits
            }
        }
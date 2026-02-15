"""
Course Selector Agent
Recommends courses based on eligibility and curriculum
"""

from typing import Dict, List
from sqlalchemy.orm import Session
from models import Course, AcademicRecord

class CourseSelectorAgent:
    """Selects appropriate courses for registration"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def recommend_courses(self, student_id: int, eligibility: Dict) -> Dict:
        """
        Recommend courses based on eligibility status
        Returns: {
            "student_id": int,
            "semester": int,
            "courses": {
                "current": [],
                "backlogs": [],
                "advance": []
            },
            "total_credits": int,
            "summary": Dict
        }
        """
        
        # Unpack eligibility
        current_sem = eligibility["current_semester"]
        has_backlogs = eligibility["has_backlogs"]
        can_advance = eligibility["can_advance"]
        risk_level = eligibility["risk_level"]
        backlog_list = eligibility.get("backlog_courses", [])
        
        # 1. Get Current Semester Courses
        current_courses = self._get_courses_by_semester(current_sem)
        
        # 2. Get Backlog Courses (Already identified by eligibility agent)
        # We need to map them to Course objects or consistent structure
        backlog_courses = []
        for bl in backlog_list:
            # bl is already a dict from eligibility agent
            backlog_courses.append(bl)
            
        # 3. Get Advance Courses (Next Semester)
        advance_courses = []
        if can_advance:
             advance_courses = self._get_courses_by_semester(current_sem + 1)
             
        # Filter based on Risk
        if risk_level == "CRITICAL":
            # Only backlogs allowed usually, or minimal load
            current_courses = [] # Block current? Or warn?
            # Typically critical risk means focus on backlogs
            pass
            
        return {
            "student_id": student_id,
            "semester": current_sem,
            "courses": {
                "current": [self._course_to_dict(c) for c in current_courses],
                "backlogs": backlog_courses,
                "advance": [self._course_to_dict(c) for c in advance_courses]
            },
            "total_credits": sum(c.credits for c in current_courses), # Estimate
            "summary": {
                "risk_level": risk_level,
                "can_advance": can_advance,
                "message": self._generate_message(risk_level, len(backlog_courses))
            }
        }
        
    def _get_courses_by_semester(self, semester: int) -> List[Course]:
        """Fetch courses for a given semester"""
        return self.db.query(Course).filter(Course.semester == semester).all()
        
    def _course_to_dict(self, course: Course) -> Dict:
        """Convert Course model to dict"""
        return {
            "course_id": course.id,
            "course_code": course.course_code,
            "course_name": course.course_name,
            "credits": course.credits,
            "semester": course.semester,
            "is_theory": course.is_theory,
            "is_lab": course.is_lab,
            "is_elective": course.is_elective
        }
        
    def _generate_message(self, risk: str, backlog_count: int) -> str:
        if risk == "CRITICAL":
            return "CRITICAL ACADEMIC STANDING. Contact Advisor."
        elif backlog_count > 0:
            return f"You have {backlog_count} backlog courses to clear."
        else:
            return "You are on track. Proceed with registration."

def create_course_selector_agent(db: Session) -> CourseSelectorAgent:
    return CourseSelectorAgent(db)

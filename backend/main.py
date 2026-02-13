"""
FastAPI Main Application
AMU Course Registration System Backend
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime

from database import get_db, init_db
from models import Student, Course, Registration, ChatHistory, AcademicRecord
from schemas import *
from business_rules import *

# Initialize FastAPI
app = FastAPI(
    title="AMU Course Registration System",
    description="AI-Powered Registration for ZHCET",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
Path("../data/uploads").mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
async def startup():
    init_db()
    print("✅ Backend started")


@app.get("/")
async def root():
    return {"status": "healthy", "timestamp": datetime.utcnow()}


@app.post("/api/auth/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.faculty_number == request.faculty_number,
        Student.enrollment_number == request.enrollment_number
    ).first()
    
    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "verified": True,
        "message": f"Welcome, {student.name}!",
        "student": {
            "id": student.id,
            "name": student.name,
            "faculty_number": student.faculty_number,
            "enrollment_number": student.enrollment_number,
            "branch": student.branch,
            "current_semester": student.current_semester,
            "cgpa": student.cgpa,
            "total_earned_credits": student.total_earned_credits
        }
    }


@app.get("/api/eligibility/{student_id}")
async def check_eligibility(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    records = db.query(AcademicRecord).filter(AcademicRecord.student_id == student_id).all()
    
    # Calculate semester credits
    sem_credits = {}
    for r in records:
        if r.status == "PASSED":
            course = db.query(Course).filter(Course.id == r.course_id).first()
            if course:
                sem_credits[r.semester] = sem_credits.get(r.semester, 0) + course.credits
    
    # Check promotion
    can_promote, promo_reason = check_promotion_eligibility(
        student.current_semester, student.total_earned_credits, sem_credits
    )
    
    # Check risk
    risk_level, action, risk_msg = check_name_removal_risk(student.not_promoted_count)
    
    # Get backlogs
    backlogs = []
    for r in records:
        if r.grade in ["E", "F"]:
            course = db.query(Course).filter(Course.id == r.course_id).first()
            if course:
                backlogs.append({
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "credits": course.credits
                })
    
    has_backlogs = len(backlogs) > 0
    can_advance, adv_reason = check_advance_eligibility(
        student.current_semester, student.cgpa, has_backlogs
    )
    
    allowed_types = []
    if risk_level != "CRITICAL":
        allowed_types.append("CURRENT")
    if has_backlogs:
        allowed_types.append("BACKLOG")
    if can_advance:
        allowed_types.append("ADVANCE")
    
    return {
        "student_id": student.id,
        "current_semester": student.current_semester,
        "cgpa": student.cgpa,
        "total_earned_credits": student.total_earned_credits,
        "status": "BLOCKED" if risk_level == "CRITICAL" else "ELIGIBLE",
        "can_register": risk_level != "CRITICAL",
        "can_advance": can_advance,
        "has_backlogs": has_backlogs,
        "backlog_count": len(backlogs),
        "allowed_registration_types": allowed_types,
        "risk_level": risk_level,
        "backlog_courses": backlogs
    }


@app.get("/api/courses/recommend/{student_id}")
async def recommend_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get current courses
    courses = db.query(Course).filter(
        Course.branch == student.branch,
        Course.semester == student.current_semester
    ).all()
    
    current = [
        {
            "course_id": c.id,
            "course_code": c.course_code,
            "course_name": c.course_name,
            "credits": c.credits
        }
        for c in courses
    ]
    
    return {
        "student_id": student.id,
        "semester": student.current_semester,
        "courses": {"current": current, "backlogs": [], "advance": []},
        "total_credits": sum(c["credits"] for c in current)
    }


@app.post("/api/registration/submit")
async def submit_registration(request: RegistrationCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    courses = db.query(Course).filter(Course.id.in_(request.course_ids)).all()
    total_credits = sum(c.credits for c in courses)
    
    if total_credits > 40:
        raise HTTPException(status_code=400, detail="Credit limit exceeded")
    
    reg_ids = []
    for cid in request.course_ids:
        reg = Registration(
            student_id=request.student_id,
            course_id=cid,
            semester=student.current_semester,
            registration_type=RegistrationTypeEnum.CURRENT,
            registration_mode=request.registration_mode,
            status=RegistrationStatusEnum.CONFIRMED,
            confirmed_at=datetime.utcnow()
        )
        db.add(reg)
        db.flush()
        reg_ids.append(reg.id)
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Registered for {len(request.course_ids)} courses",
        "registration_ids": reg_ids,
        "total_credits": total_credits
    }


@app.post("/api/chat")
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    # Placeholder - will connect to LangChain agents
    user_chat = ChatHistory(
        student_id=message.student_id,
        message=message.message,
        sender="USER"
    )
    db.add(user_chat)
    db.commit()
    
    response = "Chat agent coming soon with RAG integration."
    
    agent_chat = ChatHistory(
        student_id=message.student_id,
        message=response,
        sender="AGENT"
    )
    db.add(agent_chat)
    db.commit()
    
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
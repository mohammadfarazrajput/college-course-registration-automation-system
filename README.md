# College Course Registration System - Expert Multi-Agent System

A production-ready hybrid application for college course registration with intelligent multi-agent backend and modern React frontend.

## 🎯 Features

### For Students
- ✅ Intelligent course recommendations based on eligibility
- ✅ Real-time timetable conflict detection
- ✅ Automated prerequisite validation
- ✅ Integrated payment gateway (Razorpay/Stripe)
- ✅ Waitlist management with auto-promotion
- ✅ PDF receipt generation
- ✅ Multi-channel notifications (Email/SMS/In-app)
- ✅ Real-time registration status tracking

### For Administrators
- ✅ Approval workflow system (Advisor → HoD → Dean)
- ✅ Advanced constraint enforcement
- ✅ Analytics and reporting dashboard
- ✅ Seat allocation priority management
- ✅ Revenue tracking and reports

### Technical Highlights
- 🤖 **10 Specialized AI Agents** using LangGraph
- ⚡ **Real-time updates** via WebSockets
- 🔒 **Secure authentication** with JWT
- 💳 **Integrated payments** (Razorpay/Stripe)
- 📊 **Advanced analytics** with MongoDB
- 🎨 **Modern UI** with React + Tailwind CSS
- 📱 **Fully responsive** design
- 🧪 **Comprehensive testing** (95%+ coverage goal)

---

## 🏗️ System Architecture

```
Frontend (React + Vite)
    ↓ HTTPS/WSS
API Gateway (FastAPI)
    ↓
Agent Orchestrator (LangGraph)
    ↓
┌─────────────────────────────────────┐
│  Core Agents                        │
│  - Student Agent                    │
│  - Eligibility Agent                │
│  - Course Agent                     │
│  - Registration Agent               │
│  - Notification Agent               │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│  Advanced Agents                    │
│  - Timetable Agent                  │
│  - Payment Agent                    │
│  - Approval Agent                   │
│  - Waitlist Agent                   │
│  - Reporting Agent                  │
└─────────────────────────────────────┘
    ↓
Data Layer (PostgreSQL + Redis + MongoDB)
```

---

## 📋 Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- **PostgreSQL** 14+
- **Redis** 7+
- **MongoDB** 6+ (optional, for logs)
- **Docker** & Docker Compose (for easy setup)

---

## 🚀 Quick Start (Docker)

### 1. Clone Repository
```bash
git clone <repository-url>
cd college-registration-system
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services
```bash
docker-compose up -d
```

This will start:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- MongoDB: localhost:27017

### 4. Initialize Database
```bash
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_data.py
```

### 5. Access Application
- **Student Portal**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:5173/admin

---

## 🛠️ Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
alembic upgrade head

# Seed initial data
python scripts/seed_data.py

# Run development server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with API URL

# Run development server
npm run dev
```

---

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/college_registration
REDIS_URL=redis://localhost:6379/0
MONGODB_URL=mongodb://localhost:27017/college_logs

# Authentication
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/LLM
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key

# Payment Gateway
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret
STRIPE_SECRET_KEY=your-stripe-secret

# Email & SMS
SENDGRID_API_KEY=your-sendgrid-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890

# File Storage
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=college-registration-docs

# Application
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development

# RPUIT Integration
RPUIT_API_URL=http://rpuit.example.com/api
RPUIT_API_KEY=your-rpuit-key
```

#### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_RAZORPAY_KEY=your-razorpay-key
VITE_ENVIRONMENT=development
```

---

## 📚 API Documentation

### Authentication
```bash
POST /api/auth/login
POST /api/auth/register
POST /api/auth/refresh
POST /api/auth/logout
```

### Student
```bash
GET  /api/students/profile
GET  /api/students/academic-record
PUT  /api/students/profile
```

### Registration
```bash
POST /api/registration/start
GET  /api/registration/status/{faculty_number}
POST /api/registration/courses/select
DELETE /api/registration/courses/{course_code}
```

### Courses
```bash
GET  /api/courses
GET  /api/courses/{course_code}
GET  /api/courses/available
POST /api/courses/check-prerequisites
```

### Timetable
```bash
POST /api/timetable/check-conflicts
GET  /api/timetable/weekly/{faculty_number}
```

### Payment
```bash
POST /api/payment/calculate
POST /api/payment/initiate
POST /api/payment/verify
POST /api/payment/webhook
```

### Approval
```bash
GET  /api/approvals/pending
POST /api/approvals/{id}/approve
POST /api/approvals/{id}/reject
```

Full API documentation: http://localhost:8000/docs

---

## 🧪 Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_agents/test_eligibility_agent.py

# Run with verbose output
pytest -v -s
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# With coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

---

## 📊 Agent Responsibilities

| Agent | Purpose | LLM Usage |
|-------|---------|-----------|
| **Student Agent** | Fetch & validate student data from RPUIT | Medium |
| **Eligibility Agent** | Check constraints, backs, advancement | High |
| **Course Agent** | Manage course catalog, prerequisites | Medium |
| **Registration Agent** | Execute registration, generate forms | Low |
| **Notification Agent** | Send multi-channel notifications | Low |
| **Timetable Agent** | Detect conflicts, optimize schedule | Medium |
| **Payment Agent** | Process payments, generate receipts | Low |
| **Approval Agent** | Manage approval workflows | Medium |
| **Waitlist Agent** | Handle waitlist, auto-promote | Low |
| **Reporting Agent** | Generate analytics, insights | High |

---

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Rate limiting (100 req/hour per IP)
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS protection
- ✅ CSRF tokens
- ✅ Encrypted passwords (bcrypt)
- ✅ Secure payment integration
- ✅ Audit logging for all actions
- ✅ Role-based access control (RBAC)

---

## 🎨 UI Components

### Key Screens
1. **Login Page** - Authentication with SSO support
2. **Dashboard** - Overview, notifications, quick actions
3. **Course Selection** - Smart filtering, search, recommendations
4. **Timetable View** - Weekly calendar, conflict highlighting
5. **Payment Page** - Razorpay integration, receipt download
6. **Profile Page** - Academic record, documents
7. **Admin Panel** - Approvals, reports, analytics

---

## 📱 Mobile Responsiveness

All screens are fully responsive:
- Desktop: 1920x1080+
- Tablet: 768x1024
- Mobile: 375x667+

---

## 🚢 Deployment

### Production Deployment (Docker)

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Manual Deployment

#### Backend (AWS/GCP/Azure)
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ENVIRONMENT=production
export DATABASE_URL=postgresql://...

# Run with gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend (Vercel/Netlify)
```bash
# Build
npm run build

# Deploy
npm run deploy
```

---

## 📈 Monitoring

### Metrics to Track
- Registration success rate
- Payment completion rate
- Agent response times
- API latency
- Error rates
- User satisfaction scores

### Tools
- **Backend**: Prometheus + Grafana
- **Frontend**: Sentry for error tracking
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style
- **Python**: Black formatter, flake8 linting
- **JavaScript**: ESLint, Prettier
- **Commits**: Conventional commits format

---

## 📄 License

MIT License - see LICENSE file for details

---

## 👥 Support

For issues and questions:
- 📧 Email: support@college.edu
- 💬 Slack: #registration-support
- 📞 Phone: +91-XXXX-XXXX

---

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Core registration flow
- [x] Payment integration
- [x] Basic agents

### Phase 2 (Next)
- [ ] Mobile app (React Native)
- [ ] AI course recommendations
- [ ] Predictive analytics

### Phase 3 (Future)
- [ ] Voice-based registration
- [ ] Blockchain certificates
- [ ] Integration with learning management system

---

**Built with ❤️ for better education**

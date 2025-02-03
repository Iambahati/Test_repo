# AI-Powered Mental Health Platform

## Overview
A comprehensive mental health support platform leveraging AI for personalized care, crisis detection, and therapeutic assistance. Built with Django Ninja, React, and state-of-the-art ML models, ensuring HIPAA compliance and robust security.

## 🌟 Key Features

### User Interface
- Real-time AI chatbot support
- Personalized assessment tools
- Progress tracking dashboard
- Emergency response system
- Therapist matching interface

### AI & ML Capabilities
- **Crisis Detection:** Real-time monitoring using custom ML models
- **Sentiment Analysis:** Emotion detection using HuggingFace transformers
- **Risk Assessment:** ML-powered risk evaluation and triage
- **NLP Engine:** Rasa-powered intent and entity extraction

### Security & Compliance
- HIPAA-compliant data handling
- End-to-end encryption
- Secure authentication system
- Audit logging
- Data anonymization

## 🏗 Architecture

### Backend Services
```
backend/
├── api/                  # Django Ninja API endpoints
├── ml_models/           # ML model implementations
│   ├── crisis_detection/
│   ├── risk_assessment/
│   ├── sentiment_analysis/
│   └── rasa_bot/
├── core/                # Django core settings
├── utils/               # Utility functions
└── tests/               # Test suites
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Main application pages
│   ├── services/       # API integration
│   └── utils/          # Helper functions
├── public/
└── tests/
```

### MVP Development
```
mvp-colab/
├── models/             # Jupyter notebooks for model development
├── notebooks/         # Analysis and evaluation notebooks
└── data/             # Training and test datasets
```

## 🚀 Getting Started

### Prerequisites
```bash
# Python 3.8+
python --version

# Node.js 16+
node --version

# Docker & Docker Compose
docker --version
docker-compose --version
```

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/hakkenlab/mental-health-platform.git
cd mental-health-platform
```

2. **Backend Setup**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configurations

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

4. **Docker Deployment**
```bash
# Build and run all services
docker-compose up --build

# Run specific services
docker-compose up backend frontend
```

### Environment Variables
```env
# Backend
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# ML Services
RASA_MODEL_PATH=/app/models
HUGGINGFACE_API_KEY=your-key

# External Services
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### ML Model Testing
```bash
cd backend/ml_models
pytest tests/
```

## 📚 API Documentation

### Chat Endpoints
```python
POST /api/chat
{
    "text": "string",
    "user_id": "string",
    "session_id": "string"
}
```

### Assessment Endpoints
```python
POST /api/assess
{
    "user_id": "string",
    "responses": "dict",
    "current_mood": "string"
}
```

## 🛠 Development Guidelines

### Code Style
- Backend: PEP 8
- Frontend: ESLint + Prettier
- Documentation: Google Style Python Docstrings

### Branch Strategy
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `hotfix/*`: Emergency fixes

### Commit Messages
```
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Code style changes
refactor: Code refactoring
test: Test updates
```

## 📈 Monitoring & Maintenance

### Health Checks
- Backend service status
- ML model performance metrics
- API response times
- Error rates

### Backup Procedures
```bash
# Database backup
./scripts/backup_db.sh

# Model artifacts backup
./scripts/backup_models.sh
```

## 🔐 Security Considerations

### Data Protection
- All PHI (Protected Health Information) is encrypted at rest and in transit
- Regular security audits
- Access control and authentication
- Data retention policies

### Crisis Protocol
1. Automatic detection of crisis situations
2. Immediate notification to crisis team
3. Integration with emergency services
4. Audit trail of all crisis-related actions

## 📦 Dependencies

### Backend
- Django==4.2.0
- django-ninja==0.22.0
- rasa==3.5.0
- transformers==4.28.0
- torch==2.0.0
- scikit-learn==1.2.2
- twilio==8.1.0

### Frontend
- react==18.2.0
- @material-ui/core==4.12.4
- axios==1.3.4
- socket.io-client==4.6.1

## 🤝 Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## 🙏 Acknowledgments
- HuggingFace team for transformer models
- Rasa for the conversational AI framework
- Twilio for communication services

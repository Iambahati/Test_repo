# AI-Powered Mental Health Platform

A secure, HIPAA-compliant mental health support platform leveraging AI for personalized care, crisis detection, and therapeutic assistance. Built with Django, React, and advanced ML models.

## 🌟 Key Features

- **AI-Powered Chat Support**: Real-time therapeutic conversations with crisis detection
- **Personalized Care**: Customized assessment tools and progress tracking
- **Professional Integration**: Seamless therapist matching and oversight
- **Security First**: HIPAA-compliant with end-to-end encryption
- **Emergency Response**: Automated crisis detection with immediate professional intervention

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker-compose
- PostgreSQL 13+

### Development Setup

1. **Clone and Configure**
```bash
git clone https://github.com/hakkenlab/mental-health-platform.git
cd mental-health-platform
```

2. **Using Make Commands**
```bash
# Local development

make env-setup          # Setup .env file with secret key
make init               # Init db
make install            # Install project dependencies
make migrations         # Run database migrations
make migrate            # Run database migrations
make run                # Start development server

# Production deployment
make ENV=prod install
make ENV=prod docker-build
make ENV=prod docker-up
```

3. **Access the Application**
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Admin Interface: http://localhost:8000/admin

## 🏗 Project Structure

```
mental-health-platform/
├── src/                    # Django backend
│   ├── core/               # Project configuration
│   ├── apps/               # Django applications
│   │   ├── chat/           # AI chat functionality
│   │   ├── users/          # User management
│   │   ├── db/             # User management
│   │   └── others/         # Additional modules
│   └── templates/          # HTML templates
├── data/                   # Jupyter notebooks and ML development
├── docker/                 # Deployment infra
├── manage.py               # Django management script
├── requirements.txt        # Project packages
└── README.md  
```

### Running Tests

```bash
make test               # Run all tests
make test-coverage     # Run tests with coverage report
```

### Code Quality

```bash
make lint              # Run linters
make format           # Format code
```

## 🚀 Deployment

### Using Docker (Recommended)

```bash
# Production deployment
make ENV=prod docker-build
make ENV=prod docker-up

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Manual Deployment

1. Configure production settings
2. Install production dependencies
3. Collect static files
4. Run migrations
5. Configure web server (Nginx/Apache/Gunicorn)

```bash
make ENV=prod install
make ENV=prod collectstatic
make ENV=prod migrate
```

## 🔒 Security Features

- End-to-end encryption for all communications
- Comprehensive access logging
- Automated threat detection

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

## 📫 Support

For support and queries:
- Create a GitHub issue

## 🙏 Acknowledgments

- HuggingFace for transformer models
- Django community for the robust framework

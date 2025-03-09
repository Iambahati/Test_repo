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
git clone https://github.com/Iambahati/Test_repo.git
cd Test_repo
```

2. **Using Django Management Commands**
```bash
# Set up environment, initialize project and install dependencies
python src/manage.py setup

python src/manage.py migrate                  # Apply database migrations

# Start the development server
python src/manage.py runserver 0.0.0.0:8000   # Start development server

# Create a new app
python src/manage.py create_app myapp         # Create a new Django app in src/apps/

# Docker commands
python src/manage.py docker_build             # Build Docker images
python src/manage.py docker_up                # Start Docker containers
python src/manage.py docker_down              # Stop Docker containers

# Production mode
python src/manage.py env_setup --env=prod     # Setup production environment
python src/manage.py docker_build --env=prod  # Build production Docker images
python src/manage.py docker_up --env=prod     # Start production Docker containers
```

3. **Access the Application**
- Backend API: http://localhost:8000
- Admin Interface: http://localhost:8000/admin

## 🏗 Project Structure

```
mental-health-platform/
├── src/                    # Django backend
│   ├── core/               # Project configuration
│   │   ├── settings/       # Settings modules (base, local, prod)
│   │   ├── management/     # Custom management commands
│   ├── apps/               # Django applications
│   │   ├── chat/           # AI chat functionality
│   │   ├── users/          # User management
│   │   └── others/         # Additional modules
│   ├── db/                 # Database files for development
│   ├── templates/          # HTML templates
│   │   ├── base/
│   │   │   ├── base.html   # Base template
│   │   │   ├── navbar.html # Navbar template
│   │   │   ├── footer.html # Footer template
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── signup.html # Signup page
│   │   │   │   ├── signin.html # Signin page
│   │   │   ├── index.html    # Home page
│   ├── static/             # CSS, JS, images
│   ├── media/              # User-uploaded content
│   ├── manage.py           # Django management script
├── data/                   # Jupyter notebooks and ML development
├── docker/                 # Deployment infrastructure
├── docker-compose.yml      # Development Docker configuration
├── docker-compose.prod.yml # Production Docker configuration
├── Dockerfile              # Docker image definition
├── requirements.txt        # Project packages
├── .env.example            # Example environment variables
└── README.md  
```

### Running Tests

```bash
python src/manage.py test       # Run all tests
```

### Project Maintenance

```bash
python src/manage.py clean      # Clean up Python compiled files
```

### Database Tasks

```bash
python src/manage.py createsuperuser    # Create an admin user
python src/manage.py dbshell            # Open database shell
python src/manage.py shell              # Open Django shell
```

## 🚀 Deployment

### Using Docker (Recommended)

```bash
# Production deployment
python src/manage.py docker_build --env=prod
python src/manage.py docker_up --env=prod

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
# Install dependencies
pip install -r requirements.txt

# Prepare static files
python src/manage.py collectstatic --noinput

# Apply migrations
python src/manage.py migrate
```

## 🔒 Security Features

- End-to-end encryption for all communications
- Comprehensive access logging

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
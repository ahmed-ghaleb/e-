Self-Service Portal - e& Egypt
A Django-based web application that provides e& Egypt employees with a self-service portal to manage AWS RDS database instances.
Project Overview
We're building an internal tool that streamlines database management for our development teams. Instead of going through lengthy approval processes, employees can now provision and manage RDS instances directly through this web interface.
The portal features a clean, corporate-branded interface that matches e& Egypt's design standards and provides essential database management capabilities in a user-friendly format.
Features
Authentication

Secure login system for e& Egypt employees only
Role-based access control

RDS Management

View Database Instances: Complete list of existing RDS instances with connection details
Create New Databases: Simple form-based database provisioning
Instance Information: Display database names, endpoints, credentials, and service accounts

User Interface

Responsive design with header, footer, and sidebar navigation
e& Egypt branded theme and styling
Intuitive user experience optimized for internal workflows

Tech Stack
Backend:

Python 3.x
Django Framework
AWS SDK (boto3) for RDS integration

Frontend:

HTML5/CSS3
Django Templates
Bootstrap (for responsive design)
JavaScript for interactive elements

Database:

SQLite (development)
AWS RDS integration for database provisioning

DevOps:

GitHub Actions for CI/CD
AWS deployment pipeline

Project Structure
selfServicePortalEtisalat/
├── accounts/          # User authentication and management
├── core/             # Main project settings and configuration  
├── rds/              # RDS management functionality
├── static/           # CSS, JavaScript, images, and other static assets
├── templates/        # HTML templates
├── requirements.txt  # Python dependencies
└── manage.py        # Django management commands

Getting Started
Prerequisites

Python 3.8+
AWS Account with RDS permissions
Git

Installation

Clone the repository:
git clone https://github.com/alyyousef/selfServicePortalEtisalat.git
cd selfServicePortalEtisalat

Create and activate virtual environment:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Configure AWS credentials
# Set up your AWS credentials for RDS access
aws configure

Run migrations
python manage.py migrate

Start development server
python manage.py runserver

Visit http://127.0.0.1:8000 to access the portal.

Development Workflow
We use GitHub Actions for our CI/CD pipeline. When code is pushed to the main branch:

Automated tests run
Code quality checks are performed
Application is deployed to staging environment
After manual approval, deployed to production

Contributing
Create a feature branch from main
Make your changes following our coding standards
Submit a pull request with a clear description
Code review and testing will be conducted
Merge after approval

AWS Integration
The application integrates with AWS RDS to:
List existing database instances
Create new RDS instances programmatically
Retrieve connection information and credentials
Monitor database status and health

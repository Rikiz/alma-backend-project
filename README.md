# FastAPI Leads Service

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern leads (prospects) management system built with FastAPI, supporting resume file uploads, email notifications, and status tracking. Designed with asynchronous architecture for high performance and high concurrency scenarios.

## ✨ Features

- 🚀 **High-performance Async API** - Built with FastAPI and asyncio, supporting high-concurrent requests
- 📁 **File Upload Support** - Secure handling of PDF resume file uploads and storage
- 📧 **Smart Email Notifications** - Automatic confirmation emails and internal notifications
- 🗄️ **Flexible Data Storage** - Support for SQLite and PostgreSQL databases
- 🔒 **Secure Design** - Built-in input validation and error handling
- 📊 **Status Management** - Complete lead status tracking system
- 🏗️ **Modular Architecture** - Clean layered design for easy maintenance and extension
- 🛠️ **Developer Friendly** - Auto-generated API documentation and hot reload support

## 🏗️ Tech Stack

- **Framework**: FastAPI - Modern asynchronous web framework
- **Database ORM**: SQLAlchemy 2.0 - Powerful database abstraction layer
- **Data Validation**: Pydantic - Data models and validation
- **Async File Handling**: aiofiles - Asynchronous file operations
- **Email Service**: aiosmtplib - Asynchronous SMTP client
- **Server**: Uvicorn - ASGI server
- **Configuration Management**: Pydantic Settings - Environment variable management

## 📋 System Requirements

- Python 3.11+
- SQLite 3.0+ (default) or PostgreSQL (optional)

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Rikiz/alma-backend-project.git
cd fastapi-leads
```

### 2. Create conda environment

```bash
conda create -n fastapi-leads python=3.11
conda activate fastapi-leads
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (optional)

Create `.env` file:

```env
# Database configuration
DATABASE_URL=sqlite:///leads.db

# File upload configuration
UPLOAD_DIR=./uploads

# SMTP email configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourdomain.com
ATTORNEY_EMAIL=attorney@yourdomain.com

# Logging configuration
LOG_LEVEL=INFO
```

### 5. Start the service

```bash
# Development mode (with hot reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the convenience script
./run.sh
```

Visit http://localhost:8000/docs to view the auto-generated API documentation.

## 📚 API Documentation

### Health Check

- **GET** `/health` - Service health check

### Public APIs

#### Create Lead
- **POST** `/public/create_leads`
- **Description**: Submit new prospect information
- **Request Body**: `multipart/form-data`
  - `first_name` (string, required): First name
  - `last_name` (string, required): Last name
  - `email` (string, required): Email address
  - `resume` (file, optional): Resume file (PDF)

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/public/create_leads" \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "email=john.doe@example.com" \
  -F "resume=@resume.pdf"
```

**Response**:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "resume_path": "/uploads/abc123.pdf",
  "state": "PENDING",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

#### Update Lead
- **PUT** `/public/update_leads/{lead_id}`
- **Description**: Update existing lead information
- **Parameter**: `lead_id` (integer, path)
- **Request Body**: `multipart/form-data`
  - `first_name` (string, optional): First name
  - `last_name` (string, optional): Last name
  - `resume` (file, optional): New resume file

### Internal APIs

#### Get All Leads
- **GET** `/internal/leads`
- **Parameters**:
  - `skip` (integer, query, default=0): Number of records to skip
  - `limit` (integer, query, default=100): Maximum records to return

#### Get Single Lead
- **GET** `/internal/leads/{lead_id}`
- **Parameter**: `lead_id` (integer, path)

#### Update Lead Status
- **PATCH** `/internal/leads/{lead_id}/state`
- **Description**: Update lead follow-up status
- **Request Body**:
```json
{
  "state": "REACHED_OUT"
}
```

**Available States**: `PENDING`, `REACHED_OUT`

#### Delete Lead
- **DELETE** `/internal/leads/{lead_id}`
- **Description**: Delete specified lead record

## 🗂️ Project Structure

```
fastapi-leads/
├── app/
│   ├── api/           # API route definitions
│   │   ├── public.py  # Public interfaces
│   │   └── internal.py # Internal interfaces
│   ├── core/          # Core configuration
│   │   └── config.py  # Application configuration
│   ├── models/        # Data models
│   │   ├── models.py  # SQLAlchemy models
│   │   ├── schemas.py # Pydantic schemas
│   │   └── enums.py   # Enum definitions
│   ├── services/      # Business services layer
│   │   ├── email_service.py    # Email service
│   │   └── storage_service.py  # File storage service
│   ├── server/        # Data access layer
│   │   └── lead_dao.py # Lead data access object
│   └── database/      # Database configuration
│       └── db.py
├── uploads/           # File upload directory
├── alembic/           # Database migrations (optional)
├── .env              # Environment variables configuration
├── .gitignore        # Git ignore file
├── main.py           # Application entry point
├── requirements.txt  # Python dependencies
├── run.sh           # Startup script
└── README.md        # Project documentation
```

## ⚙️ Configuration Options

### Required Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///leads.db` | Database connection URL |
| `UPLOAD_DIR` | `./uploads` | File upload directory |

### Optional Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SMTP_HOST` | - | SMTP server host |
| `SMTP_PORT` | - | SMTP server port |
| `SMTP_USER` | - | SMTP username |
| `SMTP_PASSWORD` | - | SMTP password |
| `FROM_EMAIL` | - | Sender email address |
| `ATTORNEY_EMAIL` | - | Attorney email (receives internal notifications) |
| `LOG_LEVEL` | `INFO` | Logging level |

## 📧 Email Notification System

When creating a new lead, the system automatically sends two emails:

1. **Customer Confirmation Email**: Sent to the lead confirming receipt of their application
2. **Internal Notification Email**: Sent to the configured attorney email with lead details

Email functionality requires complete SMTP configuration to be enabled.

## 🔧 Development Guide

### Run Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest
```

### Database Migration (using Alembic)

```bash
# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Code Formatting

```bash
# Install development dependencies
pip install black isort flake8

# Format code
black .
isort .

# Check code quality
flake8 .
```

## 🚀 Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Environment Configuration

```bash
# Use production WSGI server
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check `DATABASE_URL` configuration
   - Ensure database file exists and has write permissions

2. **File Upload Failure**
   - Check `UPLOAD_DIR` directory exists and has write permissions
   - Verify file size limits

3. **Email Sending Failure**
   - Check SMTP configuration completeness
   - Verify email credentials and server settings

4. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Or use different port
   uvicorn app.main:app --port 8001
   ```

## 🤝 Contributing Guidelines

1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

### Code Standards

- Use `black` for code formatting
- Use `isort` to organize imports
- Follow PEP 8 standards
- Add appropriate tests for new features

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or suggestions, please:

- Submit [GitHub Issue](https://github.com/Rikiz/alma-backend-project/issues)
- View [API Documentation](http://localhost:8000/docs) (after running the service)
- View [Interactive API Documentation](http://localhost:8000/redoc) (after running the service)

---

**Happy coding! 🚀**

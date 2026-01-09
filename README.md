# Rent2Rent Pro Backend

Django REST API backend for the Rent2Rent Pro application - a property rental management platform with user authentication and administrative features. Built with Celery task processing and Docker support.

## Features

- **User Authentication** - JWT-based authentication with email verification, password reset, and social login (Google)
- **Account Management** - User registration, profile management, and account administration
- **Admin Dashboard** - Administrative interface for user and system management
- **Background Tasks** - Celery-powered async task processing for scalable operations
- **Docker Ready** - Full containerization with Docker Compose for easy deployment
- **RESTful API** - Well-structured API endpoints for frontend integration

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Method 1: Using Docker (Recommended)](#method-1-using-docker-recommended)
  - [Method 2: Local Setup](#method-2-local-setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Database Management](#database-management)
- [Common Commands](#common-commands)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)

## Tech Stack

- **Framework:** Django 4.x + Django REST Framework
- **Authentication:** JWT (SimpleJWT), django-allauth, dj-rest-auth
- **Social Auth:** Google OAuth
- **Task Queue:** Celery + Redis
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Server:** Gunicorn
- **Containerization:** Docker + Docker Compose

## Prerequisites

### For Docker Setup

- [Docker](https://www.docker.com/get-started) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)

### For Local Setup

- Python 3.8 or higher
- pip (Python package manager)
- Redis (for Celery task queue)
- Virtual environment (recommended)

## Installation

### Method 1: Using Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/Sawjal-sikder/rent2rentpro.git
   cd rent2rentpro/rent2rent_backend
   ```

2. **Create environment file**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your configuration values.

3. **Build and start containers**

   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Run migrations**

   ```bash
   docker compose exec web python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   docker compose exec web python manage.py collectstatic --noinput
   ```

### Method 2: Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Sawjal-sikder/rent2rentpro.git
   cd rent2rentpro/rent2rent_backend
   ```

2. **Create and activate virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your configuration values.

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if not using SQLite)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Social Auth (if applicable)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Running the Project

### Using Docker

1. **Start all services**

   ```bash
   docker compose up -d
   ```

2. **View logs**

   ```bash
   docker compose logs -f
   ```

3. **Stop services**

   ```bash
   docker compose down
   ```

4. **Restart services**
   ```bash
   docker compose restart
   ```

### Local Development

1. **Start Redis server** (in a separate terminal)

   ```bash
   redis-server --port 6379
   ```

2. **Start Django development server**

   ```bash
   python manage.py runserver
   ```

   The API will be available at http://localhost:14050 (Docker) or http://localhost:8000 (local)

3. **Start Celery worker** (in a separate terminal)

   ```bash
   celery -A project worker --loglevel=info
   ```

4. **Start Celery beat** (optional, for scheduled tasks)
   ```bash
   celery -A project beat --loglevel=info
   ```

## Database Management

### Migrations

**Create new migrations after model changes:**

```bash
# Docker
docker compose exec web python manage.py makemigrations

# Local
python manage.py makemigrations
```

**Apply migrations:**

```bash
# Docker
docker compose exec web python manage.py migrate

# Local
python manage.py migrate
```

**Show migration status:**

```bash
# Docker
docker compose exec web python manage.py showmigrations

# Local
python manage.py showmigrations
```

**Rollback migrations:**

```bash
# Docker
docker compose exec web python manage.py migrate <app_name> <migration_name>

# Local
python manage.py migrate <app_name> <migration_name>
```

### Database Shell

**Access Django shell:**

```bash
# Docker
docker compose exec web python manage.py shell

# Local
python manage.py shell
```

**Access database directly:**

```bash
# Docker
docker compose exec web python manage.py dbshell

# Local
python manage.py dbshell
```

## Common Commands

### User Management

**Create superuser:**

```bash
# Docker
docker compose exec web python manage.py createsuperuser

# Local
python manage.py createsuperuser
```

**Change user password:**

```bash
# Docker
docker compose exec web python manage.py changepassword <username>

# Local
python manage.py changepassword <username>
```

### Static Files

**Collect static files:**

```bash
# Docker
docker compose exec web python manage.py collectstatic --noinput

# Local
python manage.py collectstatic --noinput
```

**Clear static files:**

```bash
# Docker
docker compose exec web python manage.py collectstatic --clear --noinput

# Local
python manage.py collectstatic --clear --noinput
```

### Testing

**Run all tests:**

```bash
# Docker
docker compose exec web python manage.py test

# Local
python manage.py test
```

**Run specific app tests:**

```bash
# Docker
docker compose exec web python manage.py test accounts

# Local
python manage.py test accounts
```

**Run with coverage:**

```bash
# Docker
docker compose exec web coverage run --source='.' manage.py test
docker compose exec web coverage report

# Local
coverage run --source='.' manage.py test
coverage report
```

### Custom Management Commands

**Delete expired reset codes:**

```bash
# Docker
docker compose exec web python manage.py delete_expired_reset_codes

# Local
python manage.py delete_expired_reset_codes
```

### Container Management (Docker)

**View running containers:**

```bash
docker compose ps
```

**Access container shell:**

```bash
docker compose exec web bash
```

**View container logs:**

```bash
docker compose logs -f web
docker compose logs -f worker
docker compose logs -f redis
```

**Rebuild containers:**

```bash
docker compose build --no-cache
docker compose up -d
```

**Remove containers and volumes:**

```bash
docker compose down -v
```

## Project Structure

```
rent2rent_backend/
├── accounts/              # User authentication and account management
│   ├── models.py         # Custom user model, password reset codes
│   ├── views/            # Authentication views (register, login, social auth)
│   │   ├── user_login.py
│   │   └── user_registration.py
│   ├── serializers/      # API serializers
│   │   ├── user_login.py
│   │   └── user_registration.py
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin interface configuration
│   └── migrations/       # Database migrations
├── dashboard/            # Admin dashboard functionality
│   ├── models.py         # Dashboard-related models
│   ├── views.py          # Dashboard views
│   └── admin.py          # Admin configurations
├── service/              # Additional services and utilities
│   ├── models.py         # Service-related models
│   └── views.py          # Service endpoints
├── project/              # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   ├── celery.py         # Celery configuration
│   └── wsgi.py           # WSGI configuration
├── media/                # User uploaded files
│   ├── documents/        # Uploaded documents
│   ├── dxf/              # DXF files
│   ├── profile_images/   # User profile images
│   └── prompt_icons/     # Template icons
├── staticfiles/          # Collected static files
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker build instructions
├── requirements.txt      # Python dependencies
├── manage.py             # Django management script
└── db.sqlite3            # SQLite database (development)
```

## API Endpoints

### Authentication (`/api/accounts/`)

| Method | Endpoint                  | Description                     |
| ------ | ------------------------- | ------------------------------- |
| POST   | `/auth/register/`         | User registration               |
| POST   | `/auth/active/user/`      | Verify activation code          |
| POST   | `/auth/resend/code/`      | Resend activation code          |
| POST   | `/auth/login/`            | User login (JWT access token)   |
| POST   | `/auth/refresh/`          | Refresh JWT token               |
| POST   | `/auth/forgot-password/`  | Request password reset          |
| POST   | `/auth/set_new_password/` | Set new password                |
| POST   | `/auth/change-password/`  | Change password (authenticated) |
| POST   | `/auth/logout/`           | User logout                     |
| DELETE | `/auth/account-delete/`   | Delete account                  |
| GET    | `/auth/user/details/`     | Get current user details        |
| PUT    | `/auth/users/update/`     | Update user profile             |
| POST   | `/auth/google/`           | Google OAuth login              |

### Admin User Management (`/api/accounts/`)

| Method | Endpoint                     | Description                  |
| ------ | ---------------------------- | ---------------------------- |
| GET    | `/auth/users/`               | List all users (admin)       |
| DELETE | `/auth/users/delete/`        | Delete users (admin)         |
| PUT    | `/auth/users/<id>/`          | Update user details (admin)  |
| POST   | `/auth/users/activate/<id>/` | Activate user (admin)        |
| POST   | `/auth/users/premium/<id>/`  | Set premium status (admin)   |
| GET    | `/auth/dashboard/`           | Dashboard statistics (admin) |
| GET    | `/auth/admin/`               | List admins                  |
| POST   | `/auth/admin/create/`        | Create superuser             |

### Dashboard (`/api/dashboard/`)

| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| GET    | `/dashboard/`       | Get dashboard overview  |
| GET    | `/dashboard/stats/` | Get platform statistics |

### Services (`/api/service/`)

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| GET    | `/service/`        | Get service status |
| POST   | `/service/health/` | Health check       |

## Troubleshooting

### Common Issues

**Port already in use:**

```bash
# Check what's using the port
# Windows
netstat -ano | findstr :14050

# Linux/macOS
lsof -i :14050

# Change port in docker-compose.yml or stop the conflicting service
```

**Database locked error:**

```bash
# Stop all services and restart
docker compose down
docker compose up -d
```

**Permission denied errors:**

```bash
# On Linux/macOS, you may need to adjust file permissions
sudo chown -R $USER:$USER .
```

**Migrations not applying:**

```bash
# Reset migrations (WARNING: This will delete data)
docker compose exec web python manage.py migrate --fake <app_name> zero
docker compose exec web python manage.py migrate <app_name>
```

**Celery tasks not running:**

```bash
# Check Redis connection
docker compose logs redis

# Restart Celery worker
docker compose restart worker
```

**Static files not loading:**

```bash
# Recollect static files
docker compose exec web python manage.py collectstatic --clear --noinput
```

### Reset Development Environment

```bash
# Stop and remove all containers
docker compose down -v

# Remove SQLite database
rm db.sqlite3

# Rebuild and start
docker compose build --no-cache
docker compose up -d

# Run migrations and create superuser
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

## Development Workflow

1. **Create a new feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and test**

   ```bash
   python manage.py test
   ```

3. **Create migrations if models changed**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Use a production-grade database (PostgreSQL recommended)
3. Configure proper `ALLOWED_HOSTS`
4. Use environment variables for all secrets
5. Set up proper logging
6. Use HTTPS/SSL certificates
7. Configure proper CORS settings
8. Set up monitoring and error tracking

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For support, open an issue in the [GitHub repository](https://github.com/Sawjal-sikder/rent2rentpro/issues).

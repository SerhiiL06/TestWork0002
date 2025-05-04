# 🤖 TestWork Tasks API

This is a test project that provides an API interface for managing tasks.

---

## 📌 Features

- User Registration  
- JWT Authentication  
- Task Creation  
- Task Updating  
- Viewing Own Tasks  
- Docker Support for Easy Deployment  

---

## 🚀 Minimum Deployment Requirements

### 💾 Software Requirements

- **Python**: version 3.10 or higher  
- **PostgreSQL**: as the primary database  
- **FastAPI**  
- **Dishka** (Dependency Injection library)  
- **Docker**  

---

## ⚙️ Environment Configuration

Before starting the project, create and configure the environment variables.

Use the provided example file:

### `./.env.example`

```env
POSTGRES_DB=tasks_db
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

SECRET_KEY=your-secret-key
```

Copy and rename the file if necessary:

```cp .env.example .env```

---

## 🐳 Docker Launch (Recommended)

To run the application using Docker, simply execute:

```
docker compose up -d
```
---

## 🧪 Local Launch Instructions

Make sure that PostgreSQL is installed and running locally.

Then run the following command:

```
python -m backend.presentation.web.main:app --reload
```

## 📚 API Documentation (Swagger UI)

Once the application is running, the interactive API documentation is available at:

👉 http://localhost:8000/docs

For the alternative ReDoc view: http://localhost:8000/redoc



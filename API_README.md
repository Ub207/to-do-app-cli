# Todo API Documentation

A comprehensive REST API for task management built with FastAPI and SQLAlchemy.

## 🚀 Features

- ✅ Full CRUD operations for tasks
- ✅ Task prioritization (HIGH/MEDIUM/LOW)
- ✅ Tag management
- ✅ Due dates and recurring tasks
- ✅ Advanced search and filtering
- ✅ Sorting capabilities
- ✅ SQLite (local) and PostgreSQL (production) support
- ✅ Auto-generated API documentation (Swagger/ReDoc)

## 📦 Installation

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Ub207/to-do-app-cli.git
cd to-do-app-cli
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the server**
```bash
uvicorn api.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🌐 Deployment

### Deploy on Render (Free)

1. **Create account** on [Render.com](https://render.com)

2. **Create New Web Service**
   - Connect your GitHub repository
   - Select: `to-do-app-cli`

3. **Configure settings**:
   - **Name**: `todo-api` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variable**:
   - Key: `DATABASE_URL`
   - Value: `postgresql://...` (Render provides free PostgreSQL)

5. **Deploy!**

### Deploy on Railway

1. **Create account** on [Railway.app](https://railway.app)

2. **New Project** → **Deploy from GitHub**

3. **Add PostgreSQL** database to your project

4. **Configure**:
   - Railway auto-detects Python and uses Procfile
   - DATABASE_URL is automatically set

5. **Deploy!**

### Deploy on Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch

# Deploy
flyctl deploy
```

## 📚 API Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "healthy"
}
```

---

### Tasks - CRUD Operations

#### Create Task
```http
POST /api/v1/tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response: 201 Created**
```json
{
  "id": "f3ea8fd9-b2a7-460f-8762-cd49d362c0d4",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": null,
  "tags": [],
  "due_date": null,
  "recurring": null,
  "created_at": "2025-12-28T10:30:00",
  "updated_at": "2025-12-28T10:30:00"
}
```

#### Get All Tasks
```http
GET /api/v1/tasks
```

**Query Parameters:**
- `completed` (bool): Filter by completion status
- `priority` (string): Filter by priority (HIGH/MEDIUM/LOW)
- `tag` (string): Filter by tag
- `search` (string): Search in title/description
- `sort_by` (string): Sort by field (created, title, priority, due_date)
- `order` (string): Sort order (asc, desc)

**Response: 200 OK**
```json
{
  "total": 5,
  "completed": 2,
  "tasks": [...]
}
```

#### Get Single Task
```http
GET /api/v1/tasks/{task_id}
```

**Response: 200 OK**

#### Update Task
```http
PUT /api/v1/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response: 200 OK**

#### Delete Task
```http
DELETE /api/v1/tasks/{task_id}
```

**Response: 204 No Content**

#### Toggle Task Completion
```http
PATCH /api/v1/tasks/{task_id}/toggle
```

**Response: 200 OK**

---

### Priority Management

#### Set Priority
```http
PATCH /api/v1/tasks/{task_id}/priority
Content-Type: application/json

{
  "priority": "HIGH"
}
```

**Values**: `HIGH`, `MEDIUM`, `LOW`, or `null`

**Response: 200 OK**

---

### Tag Management

#### Add Tag
```http
POST /api/v1/tasks/{task_id}/tags
Content-Type: application/json

{
  "tag": "work"
}
```

**Response: 200 OK**

#### Remove Tag
```http
DELETE /api/v1/tasks/{task_id}/tags/{tag}
```

**Response: 200 OK**

#### Get All Tags
```http
GET /api/v1/tags
```

**Response: 200 OK**
```json
["personal", "work", "urgent"]
```

---

### Due Date Management

#### Set Due Date
```http
PATCH /api/v1/tasks/{task_id}/due-date
Content-Type: application/json

{
  "due_date": "2025-12-31"
}
```

**Format**: `YYYY-MM-DD`

**Response: 200 OK**

#### Clear Due Date
```http
DELETE /api/v1/tasks/{task_id}/due-date
```

**Response: 200 OK**

#### Get Overdue Tasks
```http
GET /api/v1/tasks/due/overdue
```

#### Get Tasks Due Today
```http
GET /api/v1/tasks/due/today
```

#### Get Tasks Due This Week
```http
GET /api/v1/tasks/due/week
```

---

### Recurring Tasks

#### Set Recurring Pattern
```http
PATCH /api/v1/tasks/{task_id}/recurring
Content-Type: application/json

{
  "recurring": "daily"
}
```

**Values**: `daily`, `weekly`, `monthly`, or `null`

**Note**: Task must have a due date before setting recurrence.

**Response: 200 OK**

---

## 🔍 Example Use Cases

### Example 1: Create and Manage Task
```bash
# Create task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Morning workout", "description": "30 min cardio"}'

# Set priority
curl -X PATCH http://localhost:8000/api/v1/tasks/abc123/priority \
  -H "Content-Type: application/json" \
  -d '{"priority": "HIGH"}'

# Add tags
curl -X POST http://localhost:8000/api/v1/tasks/abc123/tags \
  -H "Content-Type: application/json" \
  -d '{"tag": "health"}'

# Set due date
curl -X PATCH http://localhost:8000/api/v1/tasks/abc123/due-date \
  -H "Content-Type: application/json" \
  -d '{"due_date": "2025-12-30"}'
```

### Example 2: Search and Filter
```bash
# Search for tasks containing "workout"
curl "http://localhost:8000/api/v1/tasks?search=workout"

# Get high priority tasks
curl "http://localhost:8000/api/v1/tasks?priority=HIGH"

# Get incomplete tasks sorted by due date
curl "http://localhost:8000/api/v1/tasks?completed=false&sort_by=due_date&order=asc"
```

### Example 3: Create Recurring Task
```bash
# Create task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Team standup", "description": "Daily team meeting"}'

# Set due date
curl -X PATCH http://localhost:8000/api/v1/tasks/xyz789/due-date \
  -H "Content-Type: application/json" \
  -d '{"due_date": "2025-12-29"}'

# Set as daily recurring
curl -X PATCH http://localhost:8000/api/v1/tasks/xyz789/recurring \
  -H "Content-Type: application/json" \
  -d '{"recurring": "daily"}'

# When completed, a new task will be automatically created for next day
curl -X PATCH http://localhost:8000/api/v1/tasks/xyz789/toggle
```

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Server**: Uvicorn
- **Validation**: Pydantic
- **CORS**: Enabled for all origins (configure for production)

---

## 📊 Database Schema

### Tasks Table

| Column | Type | Description |
|--------|------|-------------|
| id | String (UUID) | Primary key |
| title | String(200) | Task title |
| description | String(2000) | Task description |
| completed | Boolean | Completion status |
| priority | String(10) | HIGH/MEDIUM/LOW |
| tags | JSON Array | List of tags |
| due_date | String(10) | YYYY-MM-DD format |
| recurring | String(10) | daily/weekly/monthly |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

---

## 🔐 Security Notes

For production deployment:

1. **Configure CORS properly** in `api/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Use HTTPS** (handled automatically by Render/Railway/Fly.io)

3. **Set strong DATABASE_URL** with proper credentials

4. **Add rate limiting** if needed

---

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Test with httpx:
```python
import httpx

response = httpx.get("http://localhost:8000/health")
print(response.json())
```

---

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | sqlite:///./data/todo.db |
| PORT | Server port | 8000 |

---

## 🐛 Troubleshooting

### Database connection errors
- Check DATABASE_URL format
- For PostgreSQL: `postgresql://user:pass@host:port/db`
- For SQLite: `sqlite:///./data/todo.db`

### Module not found errors
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (3.11+ recommended)

### Port already in use
- Change port: `uvicorn api.main:app --port 8001`
- Or kill process using port 8000

---

## 📄 License

MIT License

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📧 Contact

GitHub: [@Ub207](https://github.com/Ub207)
Repository: [to-do-app-cli](https://github.com/Ub207/to-do-app-cli)

---

Built with ❤️ using FastAPI

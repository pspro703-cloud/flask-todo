# Flask Todo App

Full-stack todo application with Flask, SQLAlchemy, SQLite, and Tailwind CSS.

## Features

- ✅ User auth (register/login/logout)
- 📝 Create, edit, delete todos
- 🏷️ Custom categories with colors
- ⚡ Priority levels (Low/Medium/High)
- 📅 Due dates with overdue detection
- 📊 Progress stats & dashboard
- 🔍 Filter by status, priority, category
- 🔄 Sort by date, priority, created
- 📱 Responsive design

## Setup

```bash
# 1. Create virtual env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install deps
pip install -r requirements.txt

# 3. Config
cp .env.example .env

# 4. Run (tables auto-create)
python run.py

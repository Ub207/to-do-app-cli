"""Task management endpoints."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from api.database import get_db
from api.models import TaskDB
from api.schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    PriorityUpdate, TagAdd, TagRemove, DueDateUpdate, RecurringUpdate
)

router = APIRouter()


# ==================== CRUD Operations ====================

@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    Args:
        task: Task data
        db: Database session

    Returns:
        Created task
    """
    db_task = TaskDB(
        id=str(uuid.uuid4()),
        title=task.title.strip(),
        description=task.description.strip() if task.description else "",
        tags=[]
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority (HIGH/MEDIUM/LOW)"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    search: Optional[str] = Query(None, description="Search in title/description"),
    sort_by: Optional[str] = Query("created", description="Sort by: created, title, priority, due_date"),
    order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filtering and sorting.

    Args:
        completed: Filter by completion status
        priority: Filter by priority
        tag: Filter by tag
        search: Search query
        sort_by: Sort field
        order: Sort order
        db: Database session

    Returns:
        List of tasks with metadata
    """
    query = db.query(TaskDB)

    # Apply filters
    if completed is not None:
        query = query.filter(TaskDB.completed == completed)

    if priority:
        query = query.filter(TaskDB.priority == priority.upper())

    if tag:
        # SQLite JSON search - this works for SQLite
        query = query.filter(TaskDB.tags.contains(tag.lower()))

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                TaskDB.title.ilike(search_term),
                TaskDB.description.ilike(search_term)
            )
        )

    # Apply sorting
    if sort_by == "title":
        query = query.order_by(TaskDB.title.asc() if order == "asc" else TaskDB.title.desc())
    elif sort_by == "priority":
        query = query.order_by(TaskDB.priority.asc() if order == "asc" else TaskDB.priority.desc())
    elif sort_by == "due_date":
        query = query.order_by(TaskDB.due_date.asc() if order == "asc" else TaskDB.due_date.desc())
    else:  # created
        query = query.order_by(TaskDB.created_at.asc() if order == "asc" else TaskDB.created_at.desc())

    tasks = query.all()

    # Calculate counts
    total = len(tasks)
    completed_count = sum(1 for t in tasks if t.completed)

    return {
        "total": total,
        "completed": completed_count,
        "tasks": tasks
    }


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.

    Args:
        task_id: Task ID (full or partial)
        db: Database session

    Returns:
        Task details
    """
    # Try exact match first
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    # If not found, try partial match
    if not task and len(task_id) >= 4:
        tasks = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).all()
        if len(tasks) == 1:
            task = tasks[0]
        elif len(tasks) > 1:
            raise HTTPException(status_code=400, detail="Multiple tasks match this ID. Please be more specific.")

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task's title and/or description.

    Args:
        task_id: Task ID
        task_update: Updated fields
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.title is not None:
        task.title = task_update.title.strip()
    if task_update.description is not None:
        task.description = task_update.description.strip()

    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete a task.

    Args:
        task_id: Task ID
        db: Database session
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()


@router.patch("/tasks/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(task_id: str, db: Session = Depends(get_db)):
    """
    Toggle a task's completion status.

    Args:
        task_id: Task ID
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed

    # Handle recurring tasks
    if task.completed and task.recurring and task.due_date:
        # Create new instance
        from datetime import datetime, timedelta
        due = datetime.strptime(task.due_date, "%Y-%m-%d")

        if task.recurring == "daily":
            new_due = due + timedelta(days=1)
        elif task.recurring == "weekly":
            new_due = due + timedelta(weeks=1)
        elif task.recurring == "monthly":
            # Simple month increment
            month = due.month + 1
            year = due.year
            if month > 12:
                month = 1
                year += 1
            new_due = due.replace(year=year, month=month)

        new_task = TaskDB(
            id=str(uuid.uuid4()),
            title=task.title,
            description=task.description,
            completed=False,
            priority=task.priority,
            tags=task.tags.copy() if task.tags else [],
            due_date=new_due.strftime("%Y-%m-%d"),
            recurring=task.recurring
        )
        db.add(new_task)

    db.commit()
    db.refresh(task)
    return task


# ==================== Priority Operations ====================

@router.patch("/tasks/{task_id}/priority", response_model=TaskResponse)
async def set_priority(task_id: str, priority_update: PriorityUpdate, db: Session = Depends(get_db)):
    """
    Set a task's priority.

    Args:
        task_id: Task ID
        priority_update: Priority data
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.priority = priority_update.priority
    db.commit()
    db.refresh(task)
    return task


# ==================== Tag Operations ====================

@router.post("/tasks/{task_id}/tags", response_model=TaskResponse)
async def add_tag(task_id: str, tag_data: TagAdd, db: Session = Depends(get_db)):
    """
    Add a tag to a task.

    Args:
        task_id: Task ID
        tag_data: Tag to add
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tags = task.tags or []
    tag = tag_data.tag.lower()

    if tag in tags:
        raise HTTPException(status_code=400, detail="Tag already exists")

    tags.append(tag)
    task.tags = tags
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}/tags/{tag}", response_model=TaskResponse)
async def remove_tag(task_id: str, tag: str, db: Session = Depends(get_db)):
    """
    Remove a tag from a task.

    Args:
        task_id: Task ID
        tag: Tag to remove
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tags = task.tags or []
    tag = tag.lower()

    if tag not in tags:
        raise HTTPException(status_code=404, detail="Tag not found")

    tags.remove(tag)
    task.tags = tags
    db.commit()
    db.refresh(task)
    return task


@router.get("/tags", response_model=List[str])
async def get_all_tags(db: Session = Depends(get_db)):
    """
    Get all unique tags across all tasks.

    Args:
        db: Database session

    Returns:
        List of unique tags
    """
    tasks = db.query(TaskDB).all()
    tags = set()
    for task in tasks:
        if task.tags:
            tags.update(task.tags)
    return sorted(tags)


# ==================== Due Date Operations ====================

@router.patch("/tasks/{task_id}/due-date", response_model=TaskResponse)
async def set_due_date(task_id: str, due_date_data: DueDateUpdate, db: Session = Depends(get_db)):
    """
    Set a task's due date.

    Args:
        task_id: Task ID
        due_date_data: Due date in YYYY-MM-DD format
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.due_date = due_date_data.due_date
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}/due-date", response_model=TaskResponse)
async def clear_due_date(task_id: str, db: Session = Depends(get_db)):
    """
    Clear a task's due date.

    Args:
        task_id: Task ID
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.due_date = None
    task.recurring = None
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/due/overdue", response_model=List[TaskResponse])
async def get_overdue_tasks(db: Session = Depends(get_db)):
    """
    Get all overdue tasks.

    Args:
        db: Database session

    Returns:
        List of overdue tasks
    """
    from datetime import date
    today = date.today().isoformat()

    tasks = db.query(TaskDB).filter(
        TaskDB.due_date < today,
        TaskDB.completed == False
    ).all()

    return tasks


@router.get("/tasks/due/today", response_model=List[TaskResponse])
async def get_due_today(db: Session = Depends(get_db)):
    """
    Get all tasks due today.

    Args:
        db: Database session

    Returns:
        List of tasks due today
    """
    from datetime import date
    today = date.today().isoformat()

    tasks = db.query(TaskDB).filter(
        TaskDB.due_date == today,
        TaskDB.completed == False
    ).all()

    return tasks


@router.get("/tasks/due/week", response_model=List[TaskResponse])
async def get_due_this_week(db: Session = Depends(get_db)):
    """
    Get all tasks due in the next 7 days.

    Args:
        db: Database session

    Returns:
        List of tasks due this week
    """
    from datetime import date, timedelta
    today = date.today()
    week_end = (today + timedelta(days=7)).isoformat()

    tasks = db.query(TaskDB).filter(
        TaskDB.due_date >= today.isoformat(),
        TaskDB.due_date <= week_end,
        TaskDB.completed == False
    ).order_by(TaskDB.due_date).all()

    return tasks


# ==================== Recurring Operations ====================

@router.patch("/tasks/{task_id}/recurring", response_model=TaskResponse)
async def set_recurring(task_id: str, recurring_data: RecurringUpdate, db: Session = Depends(get_db)):
    """
    Set a task's recurring pattern.

    Args:
        task_id: Task ID
        recurring_data: Recurring pattern (daily/weekly/monthly)
        db: Database session

    Returns:
        Updated task
    """
    task = db.query(TaskDB).filter(TaskDB.id.startswith(task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if recurring_data.recurring and not task.due_date:
        raise HTTPException(status_code=400, detail="Task must have a due date before setting recurrence")

    task.recurring = recurring_data.recurring
    db.commit()
    db.refresh(task)
    return task

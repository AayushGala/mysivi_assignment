# Secure Multi-Tenant Task Management System

A secure, role-based task management API built with Django and Django REST Framework.

## Features

- **Role-Based Access Control (RBAC)**: Distinct permissions for Managers and Reportees.
- **Tenant Isolation**: Tasks and Reportees are scoped to the Manager who created them.
- **API Rate Limiting**: Strict throttling policies to prevent abuse.
- **Secure Authentication**: Token-based authentication.

## Data Model

- **User**: Custom model with roles (`MANAGER`, `REPORTEE`).
- **Task**: 
    - Linked to `created_by` (Manager) and `assigned_to` (Reportee).
    - Status workflow: DEV -> TEST -> STUCK -> COMPLETED.
    - Categories supported.

## Setup Instructions

1. **Create and Activate Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-filter markdown
   ```

3. **Run Migrations**:
   ```bash
   python3 manage.py migrate
   ```

3. **Run Server**:
   ```bash
   python3 manage.py runserver
   ```

## API Usage

- **Manager Signup**: `POST /api/auth/signup/manager/`
- **Login**: `POST /api/auth/login/`
- **Create Reportee**: `POST /api/auth/create-reportee/` (Manager only)
- **Tasks**: `GET/POST /api/tasks/`
    - Manager: Full CRUD on own tasks.
    - Reportee: List assigned tasks. Update status only.

## Rate Limiting

Configured via DRF Throttling:
- **Auth**: 5 requests/min (Login/Signup/Reportee Creation).
- **Task Creation**: 100 requests/hour.
- **Task List**: 1000 requests/hour.
- **General**: 1000 requests/day for authenticated users.

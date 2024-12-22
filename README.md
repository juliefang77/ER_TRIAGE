# ER Triage System

A Django-based Emergency Room Triage System API that manages patient information, triage records, vital signs, and medical staff data.

## Features

- Patient Management
- Triage Records
- Vital Signs Monitoring
- Medical Staff Management
- RESTful API

## Prerequisites

- Python 3.x
- Django
- Django REST Framework
- MySQL

## Setup Instructions
    ```

### Mac
1. Clone the repository
    ```
    git clone https://github.com/juliefang77/ER_TRIAGE.git
    cd ER_TRIAGE
    ```

2. Create and activate virtual environment
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies
    ```
    pip3 install -r requirements.txt
    ```

4. Run migrations
    ```
    python3 manage.py migrate
    ```

5. Create superuser
    ```
    python3 manage.py createsuperuser
    ```

6. Run server
    ```
    python3 manage.py runserver
    ```

## API Endpoints

### Patients
- List/Create: `http://localhost:8000/apisaas/patients/`
- Detail/Update/Delete: `http://localhost:8000/apisaas/patients/{id}/`

### Triage
- List/Create: `http://localhost:8000/apisaas/triage/`
- Detail/Update/Delete: `http://localhost:8000/apisaas/triage/{id}/`

### Vital Signs
- List/Create: `http://localhost:8000/apisaas/vitals/`
- Detail/Update/Delete: `http://localhost:8000/apisaas/vitals/{id}/`

### Medical Staff
- List/Create: `http://localhost:8000/apisaas/staff/`
- Detail/Update/Delete: `http://localhost:8000/apisaas/staff/{id}/`

## API Documentation

### Patient Model Fields
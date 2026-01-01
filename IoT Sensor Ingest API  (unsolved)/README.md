Got it. Here’s a **clear instruction guide for someone who will be solving this DRF practice project**, i.e., fixing bugs, completing features, and running tests:

---

# **IoT Sensor Ingest API — Instructions for Solvers**

This is a **practice project** where the goal is to **find and fix bugs**, make the API fully functional, and ensure all tests pass.

---

### **1. Understand the Project**

* The project is a Django REST Framework API for **IoT sensor data ingestion**.

* Features included:

  1. User registration & JWT authentication.
  2. User profile management (with optional profile picture).
  3. IoT devices management (create & list devices per user).
  4. Sensor readings ingestion (temperature, humidity, motion).
  5. Listing sensor readings (with optional filtering by device).

* **Intended bug:** The `ReadingCreateView` returns `200 OK` instead of `201 CREATED`. There may be other small issues; use the failing tests to identify them.

---

### **2. Setup**

1. Ensure you have **Python 3.12** installed.
2. Create and activate virtual environment:

   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```
5. (Optional) Create superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```
6. Run the server:

   ```bash
   python manage.py runserver
   ```

---

### **3. How to Solve the Problem**

1. **Run the tests first** to see which tests fail:

   ```bash
   python manage.py test sensors
   ```
2. **Analyze the failing test** and trace it to the code causing failure (view, serializer, or model).
3. **Fix the bug(s)**:

   * Make the API behave as expected by the test.
   * Ensure proper HTTP status codes (201 for creation, 400 for validation errors, etc.).
   * Ensure user isolation (one user cannot access another’s devices/readings).
4. **Re-run tests** until all tests pass.

---

### **4. Testing the API Manually**

* **Register a user:**

  ```http
  POST /api/auth/register/
  {
    "username": "tester",
    "password": "testpass",
    "email": "test@example.com"
  }
  ```
* **Obtain JWT token:**

  ```http
  POST /api/auth/token/
  {
    "username": "tester",
    "password": "testpass"
  }
  ```
* **Create a device (auth required):**

  ```http
  POST /api/sensors/devices/
  Authorization: Bearer <access_token>
  {
    "name": "Device 1",
    "location": "Lab"
  }
  ```
* **Submit a sensor reading (auth required):**

  ```http
  POST /api/sensors/readings/
  Authorization: Bearer <access_token>
  {
    "device": 1,
    "temperature": 23.5,
    "humidity": 45.0,
    "motion": true
  }
  ```
* **List readings for a device:**

  ```http
  GET /api/sensors/readings/list/?device=1
  Authorization: Bearer <access_token>
  ```

---

### **5. Goal**

* Make all API endpoints functional.
* Fix failing tests.
* Ensure proper **user isolation** and **correct status codes**.
* Keep project compatible with **Python 3.12**.

---

If you want, I can also write a **step-by-step “solver checklist”** so someone can follow it like a guide and fix all issues systematically.

Do you want me to create that checklist?

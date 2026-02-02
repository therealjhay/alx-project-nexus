# Job Board Backend API 🚀

A production-ready, secure, and scalable REST API for a job board platform. This project demonstrates advanced backend engineering practices, including **Role-Based Access Control (RBAC)**, **PostgreSQL Full-Text Search Optimization**, and **Automated API Documentation**.

---

## 🏗️ Architecture & Features

This system was built with a "Security First" and "Performance First" mindset, moving beyond basic CRUD operations to handle real-world scale and threats.

### 1. 🔐 Advanced Security (RBAC)
* **Custom User Model:** Implemented a scalable `CustomUser` model extending `AbstractUser` to support distinct roles (`Admin`, `Employer`, `Job Seeker`) without bloat.
* **Row-Level Access Control:**
    * **Employers:** Can only edit/delete their *own* job postings.
    * **Applicants:** Can only view their *own* applications.
    * **Employers:** Can only view applications for *their* specific jobs.
* **JWT Authentication:** Secure stateless authentication using `simplejwt` with short-lived access tokens.

### 2. ⚡ High-Performance Search
* **The Problem:** Standard SQL `LIKE` queries are slow (O(n)) and fail on complex text.
* **The Solution:** Implemented **PostgreSQL GIN (Generalized Inverted Index)**.
* **Implementation:** Used Django's `SearchVector` to combine `title` and `description` fields into a lexeme vector, enabling instant O(1) text search capabilities.

### 3. 📄 Automated Documentation
* Integrated **Drf-Spectacular** to generate OpenApi 3.0 schema.
* **Swagger UI:** Fully interactive frontend for testing endpoints directly from the browser.
* **Custom Schema Extensions:** Manually extended the auto-schema to document complex query parameters like `?search=`.

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | Django 5.0 + DRF | Rapid, secure API development |
| **Database** | PostgreSQL | Relational data + Full-Text Search Engine |
| **Auth** | JWT (SimpleJWT) | Stateless, secure token-based auth |
| **Docs** | Drf-Spectacular | Swagger/OpenAPI generation |
| **Indexing** | GIN Index | High-performance text querying |

---
🧪 Testing the API
Once the server is running, access the interactive documentation:

Swagger UI: http://127.0.0.1:8000/api/docs/

Redoc: http://127.0.0.1:8000/api/schema/redoc/

Key Endpoints
Method,Endpoint,Description,Access
POST,/api/auth/token/,Get Access/Refresh Tokens,Public
GET,/api/jobs/postings/,List all jobs,Public
GET,/api/jobs/postings/?search=python,Search using GIN Index,Public
POST,/api/jobs/postings/,Create a job,Employer Only
POST,/api/jobs/applications/,Apply for a job,Authenticated

Challenge: The "Invisible Parameter"
Issue: The Swagger UI was not showing the search parameter because we handled the logic manually in get_queryset.

Solution: Used @extend_schema from drf_spectacular to explicitly inject the search parameter definition into the OpenAPI schema, making it visible and testable for frontend developers.

Challenge: Security vs. Usability
Issue: We needed Employers to post jobs easily, but we couldn't trust them to manually input their user ID (security risk).

Solution: Overrode perform_create in the ViewSet to automatically inject self.request.user as the employer, ensuring data integrity while keeping the API simple.

📜 License
This project is part of the ProDev Backend Engineering Program.
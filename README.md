<div align="center">

# 🕌 Zad Al-Seghar API

### زاد الصغار

**An Islamic Educational REST API for Children**

Built with Django REST Framework · JWT Authentication · Role-Based Access Control

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.x-ff1709?logo=django&logoColor=white)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io)

---

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Authentication](#-authentication)
- [Authorization & Roles](#-authorization--roles)
- [API Reference](#-api-reference)
  - [Accounts](#accounts)
  - [Prophets (الأنبياء)](#prophets-الأنبياء)
  - [Prayer (الصلاة)](#prayer-الصلاة)
  - [Hadith (الحديث)](#hadith-الحديث)
  - [Azkar (الأذكار)](#azkar-الأذكار)
  - [Doaa (الدعاء)](#doaa-الدعاء)
  - [Fiqh (الفقه)](#fiqh-الفقه)
  - [Tawhid (التوحيد)](#tawhid-التوحيد)
- [Pagination](#-pagination)
- [Filtering](#-filtering)
- [Error Handling](#-error-handling)

---

## 🌟 Overview

**Zad Al-Seghar** (زاد الصغار — "Provision for the Young") is a RESTful API designed to serve Islamic educational content for children. It provides structured access to multimedia resources across seven core Islamic knowledge domains: **Prophets' Stories**, **Prayer**, **Hadith**, **Azkar**, **Doaa**, **Fiqh**, and **Tawhid**.

### Key Features

- 🔐 **JWT Authentication** with token refresh and blacklisting
- 👥 **Role-Based Access Control** (User / Staff / Superuser)
- 📹 **Video & PDF Management** with upload and URL support
- 📂 **Category-Based Organization** for structured content
- 🔍 **Advanced Filtering** on all content endpoints
- 📄 **Pagination** across all list endpoints (20 items/page)
- 📬 **Contact System** with admin reply and email notifications
- 📊 **Admin Dashboard** with view statistics

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| **Framework** | Django 5.2 |
| **API Layer** | Django REST Framework |
| **Authentication** | Simple JWT (access + refresh tokens) |
| **Database** | SQLite (default) |
| **Filtering** | django-filter |
| **Environment** | python-decouple |
| **Email** | Django Console Email Backend |

---

## 📁 Project Structure

```
zadProject/
├── zadProject/          # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/            # Auth, users, contact, dashboard
├── prophets/            # Stories of the Prophets
├── Prayer/              # Prayer education (Pillars & Advices)
├── hadith/              # Hadith videos & PDFs
├── azkar/               # Azkar (remembrance) content
├── doaa/                # Doaa (supplications) content
├── Fiqh/                # Islamic jurisprudence
├── tawhid/              # Tawhid (monotheism)
├── media/               # Uploaded files (thumbnails, videos, PDFs)
├── manage.py
├── .env                 # Environment variables (not in repo)
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd zadProject

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-filter python-decouple Pillow

# 4. Create .env file (see Environment Variables section)

# 5. Apply migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## 🔧 Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
```

---

## 🔐 Authentication

The API uses **JWT (JSON Web Token)** authentication via `djangorestframework-simplejwt`.

| Setting | Value |
|---|---|
| Access Token Lifetime | 60 minutes |
| Refresh Token Lifetime | 1 day |
| Token Blacklisting | Enabled (on logout) |

### Register

```
POST /api/accounts/register/
```

**Permission:** Public

**Request Body:**
```json
{
  "username": "ali",
  "email": "ali@example.com",
  "password": "securePassword123"
}
```

**Response `201 Created`:**
```json
{
  "user": {
    "id": "uuid-here",
    "username": "ali",
    "email": "ali@example.com",
    "is_staff": false,
    "is_superuser": false
  },
  "refresh": "eyJ...",
  "access": "eyJ..."
}
```

### Login (Obtain Token)

```
POST /api/accounts/login/
```

**Permission:** Public

**Request Body:**
```json
{
  "username": "ali",
  "password": "securePassword123"
}
```

**Response `200 OK`:**
```json
{
  "refresh": "eyJ...",
  "access": "eyJ..."
}
```

### Refresh Token

```
POST /api/accounts/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ..."
}
```

**Response `200 OK`:**
```json
{
  "access": "eyJ..."
}
```

### Logout (Blacklist Token)

```
POST /api/accounts/logout/
```

**Permission:** Authenticated

**Request Body:**
```json
{
  "refresh": "eyJ..."
}
```

**Response:** `205 Reset Content`

### Using Tokens

Include the access token in the `Authorization` header for all protected endpoints:

```
Authorization: Bearer <access_token>
```

---

## 👥 Authorization & Roles

The API implements three permission levels:

| Role | Read Content | Create/Edit/Delete Content | View Dashboard | Manage Users |
|---|:---:|:---:|:---:|:---:|
| **User** | ✅ | ❌ | ❌ | ❌ |
| **Staff** | ✅ | ✅ | ✅ (partial) | ❌ |
| **Superuser** | ✅ | ✅ | ✅ (full) | ✅ |

### Permission Classes

| Class | Description |
|---|---|
| `IsStaffOrReadOnly` | Read for everyone; write for staff/superuser only |
| `IsStaffOrSuperUser` | Only staff or superuser can access |
| `IsSuperUser` | Only superuser can access |

---

## 📚 API Reference

**Base URL:** `http://127.0.0.1:8000/`

All content endpoints (except registration/login) require authentication.

---

### Accounts

**Base path:** `/api/accounts/`

#### Contact Messages

Full CRUD via ViewSet. Users see only their own messages; staff/superuser see all.

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/accounts/contact/` | List contact messages | Authenticated |
| `POST` | `/api/accounts/contact/` | Create a message | Authenticated |
| `GET` | `/api/accounts/contact/{id}/` | Retrieve a message | Authenticated |
| `PUT` | `/api/accounts/contact/{id}/` | Update a message | Authenticated |
| `PATCH` | `/api/accounts/contact/{id}/` | Partial update (admin reply) | Authenticated |
| `DELETE` | `/api/accounts/contact/{id}/` | Delete a message | Authenticated |

**Contact Message Fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | integer | Read-only |
| `user` | UUID | Read-only, auto-set |
| `subject` | string | Max 255 chars |
| `message` | text | Required |
| `admin_reply` | text | Read-only for users |
| `created_at` | datetime | Read-only |
| `replied_at` | datetime | Read-only |

**Filters:** `subject` (icontains), `created_at` (date range), `replied_at`

#### Record View

```
POST /api/accounts/record-view/
```

Tracks which content a user has viewed (one record per user per item).

**Request Body:**
```json
{
  "model_name": "video",
  "object_id": 1
}
```

#### Dashboard Statistics

```
GET /api/accounts/dashboard/stats/
```

**Permission:** Staff or Superuser

**Response (Superuser):**
```json
{
  "content_views": [
    { "content_type__model": "video", "total_views": 42 },
    { "content_type__model": "pdf", "total_views": 18 }
  ],
  "total_users": 150,
  "users": [
    { "id": "uuid", "username": "ali", "email": "ali@example.com", "date_joined": "..." }
  ]
}
```

> Staff users receive only `content_views`. Superusers also receive `total_users` and `users` list.

---

### Prophets (الأنبياء)

**Base path:** `/api/prophets/`

Stories of the Prophets with associated videos and PDFs.

#### Prophets

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/prophets/` | List all prophets | Authenticated |
| `POST` | `/api/prophets/` | Create a prophet | Staff |
| `GET` | `/api/prophets/{id}/` | Retrieve a prophet | Authenticated |
| `PUT` | `/api/prophets/{id}/` | Update a prophet | Staff |
| `PATCH` | `/api/prophets/{id}/` | Partial update | Staff |
| `DELETE` | `/api/prophets/{id}/` | Delete a prophet | Staff |

**Prophet Fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | integer | Read-only |
| `name` | string | Max 100 chars |
| `age` | integer | Optional |
| `info` | text | Biography/story |
| `videos` | array | Nested videos (read-only) |
| `pdfs` | array | Nested PDFs (read-only) |

**Query Params:** `name` (icontains), `age` (exact), `info` (icontains)

#### Prophet Videos

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `POST` | `/api/prophets/material/videos/` | Create video | Staff |
| `GET` | `/api/prophets/material/videos/{id}/` | Retrieve video | Authenticated |
| `PUT` | `/api/prophets/material/videos/{id}/` | Update video | Staff |
| `PATCH` | `/api/prophets/material/videos/{id}/` | Partial update | Staff |
| `DELETE` | `/api/prophets/material/videos/{id}/` | Delete video | Staff |

**Video Fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | integer | Read-only |
| `title` | string | Max 200 chars |
| `thumbnail` | image | Optional |
| `description` | text | Optional |
| `url` | URL | Provide either `url` or `video`, not both |
| `video` | file | Provide either `url` or `video`, not both |
| `prophet_id` | integer | Write-only, FK to Prophet |
| `created_at` | datetime | Read-only |
| `updated_at` | datetime | Read-only |

#### Prophet PDFs

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `POST` | `/api/prophets/material/pdfs/` | Create PDF | Staff |
| `GET` | `/api/prophets/material/pdfs/{id}/` | Retrieve PDF | Authenticated |
| `PUT` | `/api/prophets/material/pdfs/{id}/` | Update PDF | Staff |
| `PATCH` | `/api/prophets/material/pdfs/{id}/` | Partial update | Staff |
| `DELETE` | `/api/prophets/material/pdfs/{id}/` | Delete PDF | Staff |

**PDF Fields:** `id`, `title`, `file`, `prophet_id` (write-only), `created_at`, `updated_at`

---

### Prayer (الصلاة)

**Base path:** `/api/prayer/`

Prayer education content organized by category (Pillars, Advices).

#### Categories

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/prayer/categories/` | List categories | Authenticated |
| `GET` | `/api/prayer/categories/{id}/` | Retrieve category | Authenticated |

**Category Choices:** `PILLARS`, `ADVICES`

#### Videos

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/prayer/videos/` | List videos | Authenticated |
| `POST` | `/api/prayer/videos/` | Create video | Staff |
| `GET` | `/api/prayer/videos/{id}/` | Retrieve video | Authenticated |
| `PUT` | `/api/prayer/videos/{id}/` | Update video | Staff |
| `PATCH` | `/api/prayer/videos/{id}/` | Partial update | Staff |
| `DELETE` | `/api/prayer/videos/{id}/` | Delete video | Staff |

**Video Fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | integer | Read-only |
| `title` | string | Max 200 chars |
| `thumbnail` | image | Required |
| `description` | text | Required |
| `url` | URL | Provide either `url` or `video`, not both |
| `video` | file | Provide either `url` or `video`, not both |
| `category` | object | Read-only, nested category |
| `category_id` | integer | Write-only |
| `order` | integer | Display order (default: 0) |
| `created_at` | datetime | Read-only |
| `updated_at` | datetime | Read-only |

**Filters:** `title` (icontains), `description` (icontains), `category` (icontains on category content), `created_at` (date range)

#### PDFs

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/prayer/pdfs/` | List PDFs | Authenticated |
| `POST` | `/api/prayer/pdfs/` | Create PDF | Staff |
| `GET` | `/api/prayer/pdfs/{id}/` | Retrieve PDF | Authenticated |
| `PUT` | `/api/prayer/pdfs/{id}/` | Update PDF | Staff |
| `PATCH` | `/api/prayer/pdfs/{id}/` | Partial update | Staff |
| `DELETE` | `/api/prayer/pdfs/{id}/` | Delete PDF | Staff |

**PDF Fields:** `id`, `title`, `file`, `category` (read-only), `category_id` (write-only), `order`, `created_at`, `updated_at`

**Filters:** `title` (icontains), `category` (icontains), `created_at` (date range)

---

### Hadith (الحديث)

**Base path:** `/api/hadith/`

Hadith educational videos and PDF resources (no categories).

#### Videos

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/hadith/videos/` | List videos | Authenticated |
| `POST` | `/api/hadith/videos/` | Create video | Staff |
| `GET` | `/api/hadith/videos/{id}/` | Retrieve video | Authenticated |
| `PUT` | `/api/hadith/videos/{id}/` | Update video | Staff |
| `PATCH` | `/api/hadith/videos/{id}/` | Partial update | Staff |
| `DELETE` | `/api/hadith/videos/{id}/` | Delete video | Staff |

**Video Fields:** `id`, `title`, `thumbnail`, `description`, `url`, `video`, `order`, `created_at`, `updated_at`

**Filters:** `title` (icontains), `description` (icontains), `created_at` (date range)

#### PDFs

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/hadith/pdfs/` | List PDFs | Authenticated |
| `POST` | `/api/hadith/pdfs/` | Create PDF | Staff |
| `GET` | `/api/hadith/pdfs/{id}/` | Retrieve PDF | Authenticated |
| `PUT` | `/api/hadith/pdfs/{id}/` | Update PDF | Staff |
| `PATCH` | `/api/hadith/pdfs/{id}/` | Partial update | Staff |
| `DELETE` | `/api/hadith/pdfs/{id}/` | Delete PDF | Staff |

**PDF Fields:** `id`, `title`, `file`, `order`, `created_at`, `updated_at`

**Filters:** `title` (icontains), `created_at` (date range)

---

### Azkar (الأذكار)

**Base path:** `/api/azkar/`

Daily remembrance (Azkar) organized by category.

#### Categories

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/azkar/categories/` | List categories | Authenticated |
| `POST` | `/api/azkar/categories/` | Create category | Staff |
| `GET` | `/api/azkar/categories/{id}/` | Retrieve category | Authenticated |
| `PUT` | `/api/azkar/categories/{id}/` | Update category | Staff |
| `DELETE` | `/api/azkar/categories/{id}/` | Delete category | Staff |

**Category Fields:** `id`, `category` (string, unique, max 100)

#### Azkar Content

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/azkar/contents/` | List all azkar | Authenticated |
| `POST` | `/api/azkar/contents/` | Create azkar | Staff |
| `GET` | `/api/azkar/contents/{id}/` | Retrieve azkar | Authenticated |
| `PUT` | `/api/azkar/contents/{id}/` | Update azkar | Staff |
| `DELETE` | `/api/azkar/contents/{id}/` | Delete azkar | Staff |
| `GET` | `/api/azkar/contents/category/{category_name}/` | Get by category | Authenticated |

**Azkar Fields:** `id`, `azkar` (string), `category` (FK), `order`, `created_at`, `updated_at`

---

### Doaa (الدعاء)

**Base path:** `/api/doaa/`

Supplications (Doaa) organized by category.

#### Categories

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/doaa/categories/` | List categories | Authenticated |
| `POST` | `/api/doaa/categories/` | Create category | Staff |
| `GET` | `/api/doaa/categories/{id}/` | Retrieve category | Authenticated |
| `PUT` | `/api/doaa/categories/{id}/` | Update category | Staff |
| `DELETE` | `/api/doaa/categories/{id}/` | Delete category | Staff |

#### Doaa Content

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/doaa/content/` | List all doaa | Authenticated |
| `POST` | `/api/doaa/content/` | Create doaa | Staff |
| `GET` | `/api/doaa/content/{id}/` | Retrieve doaa | Authenticated |
| `PUT` | `/api/doaa/content/{id}/` | Update doaa | Staff |
| `DELETE` | `/api/doaa/content/{id}/` | Delete doaa | Staff |
| `GET` | `/api/doaa/content/category/{category_name}/` | Get by category | Authenticated |

**Doaa Fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | integer | Read-only |
| `title` | string | Max 200 chars |
| `content` | text | The supplication text |
| `category` | object | Read-only, nested |
| `category_id` | integer | Write-only |
| `order` | integer | Display order |
| `created_at` | datetime | Read-only |
| `updated_at` | datetime | Read-only |

**Filters:** `category` (icontains on name), `title` (icontains), `content` (icontains), `created_at` (date range), `updated_at` (date range)

---

### Fiqh (الفقه)

**Base path:** `/api/fiqh/`

Islamic jurisprudence content with categories, videos, and PDFs.

#### Categories

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/api/fiqh/categories/` | List categories | Authenticated |
| `POST` | `/api/fiqh/categories/` | Create category | Staff |
| `GET` | `/api/fiqh/categories/{id}/` | Retrieve category | Authenticated |
| `PUT` | `/api/fiqh/categories/{id}/` | Update category | Staff |
| `DELETE` | `/api/fiqh/categories/{id}/` | Delete category | Staff |

#### Videos & PDFs

Same structure as [Prayer](#prayer-الصلاة) videos and PDFs — replace `/api/prayer/` with `/api/fiqh/`.

**Video Filters:** `title`, `description`, `category` (by name), `created_at`
**PDF Filters:** `title`, `category` (by name), `created_at`

---

### Tawhid (التوحيد)

**Base path:** `/api/tawhid/`

Tawhid (Islamic monotheism) content with categories, videos, and PDFs.

#### Categories, Videos & PDFs

Identical structure to [Fiqh](#fiqh-الفقه) — replace `/api/fiqh/` with `/api/tawhid/`.

---

## 📄 Pagination

All list endpoints use **PageNumberPagination** with a default page size of **20**.

**Response format:**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/prayer/videos/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

**Query parameter:** `?page=2`

---

## 🔍 Filtering

Filtering is powered by `django-filter`. Use query parameters to filter results.

### Date Range Filtering

For `DateFromToRangeFilter` fields, use:

```
?created_at_after=2025-01-01&created_at_before=2025-12-31
```

### Text Search

For `CharFilter` with `icontains`, pass a partial match:

```
?title=prayer
?category=pillars
```

### Examples

```bash
# Videos with "salah" in the title
GET /api/prayer/videos/?title=salah

# PDFs in the "PILLARS" category
GET /api/prayer/pdfs/?category=pillars

# Hadith videos created after a date
GET /api/hadith/videos/?created_at_after=2025-06-01

# Contact messages by subject
GET /api/accounts/contact/?subject=question
```

---

## ⚠️ Error Handling

### Standard Error Responses

| Status Code | Description |
|---|---|
| `400 Bad Request` | Validation errors (invalid data) |
| `401 Unauthorized` | Missing or invalid token |
| `403 Forbidden` | Insufficient permissions |
| `404 Not Found` | Resource not found |
| `405 Method Not Allowed` | HTTP method not supported |

### Validation Error Example

```json
{
  "title": ["This field is required."],
  "url": ["Enter a valid URL."]
}
```

### Video Validation Rules

When creating or updating videos (Prophets, Prayer, Hadith, Fiqh, Tawhid):
- On **create**: must provide either `url` or `video` file — not both, not neither
- On **update**: cannot add `video` if `url` exists, and vice versa

---

## 📜 License

This project is for educational purposes.

---

<div align="center">


Made with ❤️ for Islamic education

</div>
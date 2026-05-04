# Django Authentication API

A Django REST Framework-based authentication API with JWT tokens, multi-channel OTP (Email, WhatsApp, SMS), content management (Challenges, Blog, Products), and Razorpay payment integration.

---

## Architecture

```
                              ┌─────────────────────────┐
                              │       Client Layer       │
                              │  Web / Mobile / Postman  │
                              └────────────┬────────────┘
                                           │  HTTPS (JSON)
                                           ▼
                              ┌─────────────────────────┐
                              │     Middleware Layer     │
                              │  ┌───────────────────┐  │
                              │  │  CORS Middleware   │  │
                              │  │  (corsheaders)     │  │
                              │  ├───────────────────┤  │
                              │  │  Session Middleware│  │
                              │  ├───────────────────┤  │
                              │  │  CSRF Middleware   │  │
                              │  ├───────────────────┤  │
                              │  │  Auth Middleware    │  │
                              │  └───────────────────┘  │
                              └────────────┬────────────┘
                                           │
                                           ▼
                       ┌──────────────────────────────────────┐
                       │          URL Router Layer            │
                       │         (auth/urls.py)               │
                       │            /api/                     │
                       └──────────────┬───────────────────────┘
                                      │
                                      ▼
              ┌───────────────────────────────────────────────────────┐
              │                   API View Layer                      │
              │                 (users/views.py)                      │
              │                                                       │
              │  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
              │  │  Register   │  │    Login      │  │   User      │ │
              │  │  View       │  │    View       │  │   View      │ │
              │  │  (APIView)  │  │   (APIView)   │  │  (APIView)  │ │
              │  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘ │
              │         │                │                  │        │
              │  ┌──────┴──────┐  ┌──────┴───────┐  ┌──────┴──────┐ │
              │  │ ForgotPass  │  │  OTP_Sent     │  │ OTP_Verify  │ │
              │  │ (APIView)   │  │  (APIView)    │  │ (APIView)   │ │
              │  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘ │
              │         │                │                  │        │
              │  ┌──────┴──────┐  ┌──────┴───────┐                  │
              │  │  WhatsApp   │  │     SMS      │                  │
              │  │  (APIView)  │  │  (APIView)   │                  │
              │  └─────────────┘  └──────────────┘                  │
              │                                                       │
              │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
              │  │  Challenges  │  │   BlogPost   │  │  Products  │ │
              │  │  (Create/    │  │   APIView    │  │ Register   │ │
              │  │   Filter)    │  │              │  │ (APIView)  │ │
              │  └──────────────┘  └──────────────┘  └────────────┘ │
              │                                                       │
              │  ┌──────────────────────────────────────┐           │
              │  │  initiate_payment (Razorpay)         │           │
              │  └──────────────────────────────────────┘           │
              └───────────────────────┬─────────────────────────────┘
                                      │
                    ┌─────────────────┴──────────────────┐
                    ▼                                     ▼
         ┌──────────────────┐               ┌─────────────────────┐
         │  Serializer Layer│               │  Helper Layer       │
         │ (users/          │               │ (users/helpers.py)  │
         │  serializers.py) │               │                     │
         │                  │               │  send_forgot_email() │
         │  UserSerializer  │               │  send_otp_email()    │
         │  ChallengesSer.  │               └─────────────────────┘
         │  BlogSerializer  │
         │  ProductsSer.    │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────────────────────────────────────┐
         │              Model Layer (ORM)                    │
         │           (users/models.py)                       │
         │                                                   │
         │  ┌─────────┐  ┌────────────┐  ┌───────────────┐ │
         │  │  User   │  │ Challenges │  │   BlogPost    │ │
         │  │(Custom  │  │            │  │               │ │
         │  │Abstract │  │ stack      │  │ title         │ │
         │  │ User)   │  │ level      │  │ content       │ │
         │  │         │  │ language   │  │ writer        │ │
         │  │ email   │  │ rating     │  │ created_at    │ │
         │  │ name    │  │ problemstm │  └───────────────┘ │
         │  │ password│  │ image      │                    │
         │  │ mobile  │  └────────────┘                    │
         │  │ otp     │                                    │
         │  └─────────┘  ┌────────────┐                    │
         │               │  Products  │                    │
         │               │            │                    │
         │               │ UUID id    │                    │
         │               │ productnm  │                    │
         │               │ productid  │                    │
         │               └────────────┘                    │
         └──────────────────────┬──────────────────────────┘
                                │
                                ▼
                  ┌──────────────────────────┐
                  │       Database Layer     │
                  │        MySQL             │
                  └──────────────────────────┘


  ─── External Service Integrations ───

  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐
  │     Brevo      │  │    Twilio      │  │   Razorpay     │  │   PyJWT      │
  │  (SMTP Email)  │  │ (WhatsApp/SMS) │  │  (Payments)    │  │  (JWT Auth)  │
  └────────────────┘  └────────────────┘  └────────────────┘  └──────────────┘
```

---

## Request Flow

### Register Flow

```
Client  ──POST /api/register/──►  RegisterView
                                      │
                                      ├─→ UserSerializer.create()
                                      │     ├─→ validate email
                                      │     ├─→ hash password
                                      │     └─→ save to MySQL
                                      │
                                      └─→ 201 Created
```

### Login Flow

```
Client  ──POST /api/login/──►  LoginView
                                  │
                                  ├─→ Check email/password
                                  ├─→ Generate JWT (PyJWT, HS256)
                                  │     payload: {id, exp, iat}
                                  │
                                  ├─→ Set JWT in HttpOnly Cookie
                                  └─→ 200 OK + User Data
```

### Protected Access Flow

```
Client  ──GET /api/user/──►  UserView
  (Cookie: jwt=xxx)              │
                                 ├─→ Decode JWT from cookie
                                 ├─→ Validate expiry
                                 ├─→ Fetch user from DB
                                 └─→ 200 OK + User Data
```

### Forgot Password Flow

```
Client  ──POST /api/forgotpass/──►  ForgotPass
                                      │
                                      ├─→ Generate UUID token
                                      ├─→ send_forgot_email()
                                      │     (via Brevo SMTP)
                                      └─→ 200 OK
```

### OTP Verification Flow

```
GET  /api/sentotp/        ──►  Otp_sent   ──►  send_otp_email()  ──►  Brevo
POST /api/verify/         ──►  Otp_varify ──►  pyotp verify
POST /api/whatsappotp/    ──►  whatsapp   ──►  Twilio
POST /api/sms/            ──►  sms        ──►  Twilio
```

---

## API Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/api/register/` | Register new user | No |
| POST | `/api/login/` | Login, returns JWT | No |
| GET | `/api/user/` | Get authenticated user | JWT Cookie |
| POST | `/api/forgotpass/` | Trigger password reset email | No |
| GET | `/api/sentotp/` | Send OTP via Email | No |
| POST | `/api/verify/` | Verify OTP | No |
| POST | `/api/whatsappotp/` | Send OTP via WhatsApp | No |
| POST | `/api/sms/` | Send OTP via SMS | No |
| POST/GET | `/api/challengespost/` | Create / List challenges | No |
| GET | `/api/challengespost/<stack>/<level>/` | Filter challenges by stack & level | No |
| POST/GET | `/api/blog/` | Create / List blog posts | No |
| GET | `/api/blog/<title>/` | Filter blog by title | No |
| POST | `/api/Productregister/` | Register product | No |
| GET | `/api/Productregister/<productname>/` | Filter products by name | No |
| POST | `/api/payment/` | Initiate Razorpay payment | No |

---

## API Examples

### Register [POST]

**Endpoint:** `/api/register/`

**Input:**
```json
{
    "name": "NEW",
    "email": "newq@gmail.com",
    "password": "qwerty",
    "mobile": "1234567890"
}
```

**Output:** All user data

### Login [POST]

**Endpoint:** `/api/login/`

**Input:**
```json
{
    "email": "newq@gmail.com",
    "password": "qwerty"
}
```

**Output:**
```json
{
    "token": "jwt_token_here"
}
```

### Get Logged-in User [GET]

**Endpoint:** `/api/user/`

**Output:** User data in JSON

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 3.2 + DRF |
| Database | MySQL |
| Auth | PyJWT (HS256), HttpOnly Cookies |
| OTP | pyotp |
| Email | Brevo SMTP (port 587) |
| SMS/WhatsApp | Twilio |
| Payments | Razorpay |
| CORS | django-cors-headers |

---

## Project Structure

```
Django-Authentication/
├── auth/                          # Main Django project
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Root URL routing (/api/)
│   └── wsgi.py                   # WSGI configuration
├── users/                        # Users Django app
│   ├── __init__.py
│   ├── admin.py                  # Admin panel registration
│   ├── apps.py                   # App configuration
│   ├── helpers.py                # Email utility functions
│   ├── manage.py                 # Custom UserManager
│   ├── models.py                 # User, Challenges, BlogPost, Products
│   ├── serializers.py            # DRF serializers
│   ├── urls.py                   # App URL patterns
│   ├── views.py                  # All API views
│   └── migrations/
│       ├── 0001_initial.py
│       └── __init__.py
├── manage.py                     # Django management script
└── README.md
```

---

## Key Files

| File | Purpose |
|------|---------|
| `auth/settings.py` | Project config, DB, CORS, email, INSTALLED_APPS |
| `auth/urls.py` | Root URL routing (`/api/` -> users app) |
| `users/models.py` | User, Challenges, BlogPost, Products models |
| `users/views.py` | All API views (auth, OTP, content, payment) |
| `users/serializers.py` | DRF serializers for all models |
| `users/urls.py` | App-level URL patterns |
| `users/manage.py` | Custom UserManager (createsuperuser, create_user) |
| `users/helpers.py` | Email utility functions (send_forgot_email, send_otp_email) |
| `users/admin.py` | Admin panel registration |



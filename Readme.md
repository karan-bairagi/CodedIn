# 🚀 CodeIn — Developer Portfolio & Project Showcase Platform

<div align="center">

[![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Deployment](https://img.shields.io/badge/Deployment-Render-black?style=for-the-badge&logo=render)](https://codedin.onrender.com)

<h3>Build. Showcase. Grow as a Developer.</h3>

[![Live Demo](https://img.shields.io/badge/🌐_Live_Application-Click_Here_To_Visit-6366f1?style=for-the-badge&logo=google-chrome&logoColor=white)](https://codedin.onrender.com)

<br>

CodeIn is a production-grade developer portfolio platform engineered with Django and cloud-hosted PostgreSQL. It empowers software engineers to deploy public portfolios, manage active repositories, track profile metrics, and securely govern their cloud identity in one integrated ecosystem.

</div>

---

# 👨‍💻 The Engineer Behind the Code

Hi, I am **Karan Bairagi**, a 17-year-old Backend Engineer. 

In March 2025, right after passing my 10th-grade exams, I chose an unconventional path—I moved to Hyderabad and joined **Naresh i Technologies** to master core software architecture. Skipping traditional 11th-grade schooling to dedicate 100% of my focus to code, I mastered C and Python Full Stack. 

> 💡 **Engineering Philosophy:** I don't specialize in complex UI/CSS layouts. The frontend interface of CodeIn was generated using AI tools, allowing me to focus entirely on what matters most: **Robust Backend Logic, Complex Database Relational Integrity, and Production-Grade Security Operations.** I engineered CodeIn's entire backend in just **1 week** as a practical challenge.

---

# ✨ Core Features

## 👤 Advanced Authentication & Identity Security Engine
- **Custom Multi-Step Auth Flow:** Session-based login validation and registration pipelines.
- **Crypto-Hashing Layer:** Multi-tier password hashing using Django's built-in secure crypto hashers (`PBKDF2`).
- **Protected Route Gates:** Account routes and user views strictly governed by customized `@login_required` metadata.
- **Zero-Gateway Secure Password Recovery:** Multi-step wizard layout for forgotten passwords that bypasses third-party networks (relying entirely on internal cryptographic assertions).
- **Two-Factor Secret Challenge:** Intercepts recovery attempts with a secure dropdown list of predefined security questions matched against a small-case stripped verification matrix.
- **Ephemeral Alpha-Numeric Tokens:** Generates cryptographically secure 12-character alpha-numeric authorization passes using Python's `secrets` module, embedded with an automatic 10-minute expiry checkpoint on the server side.
- **Manual Account Rescue System:** Implemented a fail-safe manual override tunnel (`SupportTicket`). If a user forgets both their password and security answer, they can request manual recovery via a **Three-Point Identity Cross-Verification** model (Matching Full Name, Email, and Mobile Signatures) routed straight to the Django Administration dashboard.

## 🧑‍💻 Developer Profile Ecosystem
- Dynamic profile fields rendering full name, profile image assets, taglines, and markdown bios.
- Cloud routing links to connect active GitHub and LinkedIn handles.
- **Privacy Control Toggle:** Instant shift between Global Public Visibility vs Secure Private Modes (replaces standard 404 sheets with modern Instagram-style lock views).

## 📦 Project Showcase System
- Individual repository cards to push project titles, tech-stack tags, source code databases, and live URLs.
- Built-in safe asset filters (`accept="image/*"`) on file input nodes.
- Full CRUD execution controls directly tied to session owner constraints.

## 🔍 Smart Search Architecture
- Real-time directory lookups matching username handles, names, and taglines.
- Implemented using complex Django ORM `Q` expressions to evaluate loose keyword sequences safely.

## 👀 Analytical Visitor Tracking
- Profile metrics engine storing isolated timestamps for incoming requests.
- Unique counter tracking public repository views directly on the user's control board.

---

# 🔐 Strict Form Validation Matrix

Advanced custom validation routines written into `forms.py` to protect database health:

### 🔹 Username Validation
- Absolute restriction on whitespace, special characters, and repeated periods.
- Enforced minimum and maximum boundary scales.
- Real-time duplicate registration blocking.

### 🔹 Cryptographic Password Guard
- Enforced alphanumeric strength (at least one Uppercase, Lowercase, Number, and Special character).
- Hardcoded dictionary blocks against common weak passwords.

### 🔹 Telephony & Email Validation
- Enforced structure matching the Indian national formatting guidelines (10-digit strict regex).
- Suppression of repeated sequences and invalid mobile patterns.
- Whitelisted validation checks targeting authoritative mail service providers only.

---

# 🛠 Tech Stack & Architecture



| Layer | Technology | Operational Focus |
|---|---|---|
| **Backend** | Python | Core logic, structural validations, and session handlers |
| **Framework** | Django | MVT Engine, routing, middleware orchestration |
| **Database** | Supabase (PostgreSQL) | Enterprise cloud relational data mapping & query execution |
| **Storage** | Django Media | User file assets, avatars, project cards |
| **Security** | Crypto Tokens | Environment protection, `secrets` alpha-numeric token generation, string mapping |
| **Identity Verification** | Internal Challenge | Double-layer verification using encrypted question-answer sets |
| **Account Overrides** | Support Matrix | Multi-point manual rescue ticket parsing for locked profiles |

---

# 📂 Database Schema Design

### 🔷 `UserProfile`
Tracks core user attributes: Full name, uploaded avatar paths, descriptive taglines, linked external platforms, security boolean flags (public/private), audience view integers, along with standard columns for `security_question` text hashes and `security_answer` data nodes.

### 🔷 `ProjectCard`
Maps external assets: Multi-string tech tags, repository links, direct application pointers, and unique title strings bound to a User instance via a `ForeignKey`.

### 🔷 `ProfileVisitor`
Audit model: Captures relation parameters linking profile owners to distinct viewer keys coupled with automatic `auto_now_add` timestamps.

### 🔷 `SupportTicket`
Manual override logger: Captures account rescue details containing `user_email`, a status flag defaulted to `'Pending'`, and system validation notes paired with chronological tracking elements.

---

# ⚙️ Local Installation & Development Staging

### 1️⃣ Clone the Ecosystem
```bash
git clone https://github.com
cd CodedIn
```

### 2️⃣ Staging the Environment
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On Linux/Mac:
source env/bin/activate
```

### 3️⃣ Resolve Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Database Architecture Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Run Local Staging Server
```bash
python manage.py runserver
```

---

# 🚀 Production Deployment Staging (Render + Supabase)

This architecture is configured to securely separate secrets from code using environment variables. When deploying to **Render**, inject the following keys into the **Environment Variables** control board:



| Variable Key | Operational Value |
|---|---|
| `DJANGO_SECRET_KEY` | Your unique production cryptographic key |
| `DEBUG` | Set to `False` |
| `DB_NAME` | Your Supabase database name |
| `DB_USER` | Your Supabase database user (postgres) |
| `DB_PASSWORD` | Your secure Supabase database password |
| `DB_HOST` | Your Supabase database connection host URL |
| `DB_PORT` | `5432` |

---

# 📜 Contact & Connect
- **LinkedIn:** [Karan Bairagi](https://www.linkedin.com/in/karan-bairagi/)
- **GitHub Profile:** [@karanbairagivaidik57-web](https://github.com)

---

<div align="center">

### ⭐ If this project inspired your backend architecture journey, feel free to drop a Star!

</div>

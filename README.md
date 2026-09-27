# XAI & GenAI Based MRI Brain Tumor Detection Using CNN

A research/educational **medical imaging decision-support system** — not an autonomous diagnostic tool. A doctor/researcher always reviews the AI output before it is finalized.

**Workflow:**
MRI Upload → Validation → Preprocessing → CNN Prediction → Confidence Score → Grad-CAM Explanation → GenAI Draft Report → Doctor Review → Save Case History

---

## 1. Research Gap / Motivation

Most published brain-tumor CNN classifiers optimize for accuracy in isolation and behave as black boxes; explainability (e.g. Grad-CAM) is usually added as a separate visualization rather than integrated into a reviewable clinical artifact.

Very few systems connect:

**Prediction → Explanation → Structured Human-Reviewed Report → Case History**

in one auditable workflow.

### Project Contribution

This project integrates:

* CNN-based brain tumor classification
* Confidence scoring
* Grad-CAM visual explanation
* AI-assisted structured report generation
* Human/doctor review and approval
* Case history management
* Role-based authentication
* Audit logging
* Security and image validation

The system keeps a **doctor/researcher in the loop** rather than treating classification accuracy as the entire problem.

---

## 2. Tech Stack

| Layer             | Technology                                                               |
| ----------------- | ------------------------------------------------------------------------ |
| Frontend          | React 18 + Vite                                                          |
| Backend           | Python FastAPI                                                           |
| AI/ML             | PyTorch — ResNet18 Transfer Learning / Custom CNN                        |
| XAI               | Grad-CAM                                                                 |
| GenAI             | Template-based Draft Report Generator, optional Claude API               |
| Database          | SQLAlchemy ORM — SQLite for local development, SQL Server for production |
| Authentication    | JWT + bcrypt                                                             |
| Deployment        | Docker + Docker Compose                                                  |
| API Documentation | Swagger/OpenAPI                                                          |
| Image Processing  | Pillow (PIL)                                                             |
| Data Science      | NumPy, Pandas, Matplotlib                                                |
| Version Control   | Git + GitHub                                                             |

---

## 3. Folder Structure

```text
brain-tumor-detection/
│
├── ml/
│   ├── train.py                  # CNN training pipeline
│   ├── gradcam.py                # Grad-CAM implementation
│   ├── explore_dataset.py        # Dataset sanity check
│   ├── requirements.txt
│   ├── dataset/                  # Gitignored - Kaggle dataset
│   └── models/                   # Gitignored - trained model + metrics
│
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI entrypoint
│   │   ├── core/                 # Config, DB, security, auth, audit logging
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── routers/              # API routes
│   │   ├── ml/                   # ML inference wrapper
│   │   └── genai/                # Report generator
│   │
│   ├── seed_db.py                # Creates roles + demo doctor
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login
│   │   │   ├── Dashboard
│   │   │   ├── CaseList
│   │   │   ├── NewCase
│   │   │   ├── CaseDetail
│   │   │   ├── PredictionResult
│   │   │   └── ModelAdmin
│   │   │
│   │   ├── api/
│   │   │   └── client.js          # Axios + JWT interceptor
│   │   └── AuthContext.jsx
│   │
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
│
└── docs/
```

---

## 4. System Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         │ Doctor / Researcher │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │    React + Vite      │
                         └──────────┬──────────┘
                                    │ REST API
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         │ Authentication/API  │
                         └──────────┬──────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │ MRI Upload   │    │ CNN Model    │    │  Database    │
        │ Validation   │    │ Prediction   │    │ SQLAlchemy   │
        └──────┬───────┘    └──────┬───────┘    └──────────────┘
               │                   │
               │                   ▼
               │            ┌──────────────┐
               │            │  Grad-CAM    │
               │            │ Explanation  │
               │            └──────┬───────┘
               │                   │
               └──────────┬────────┘
                          ▼
                 ┌──────────────────┐
                 │ GenAI Report      │
                 │ Draft Generator   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Doctor / Research│
                 │ Review & Approval│
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Case History   │
                 │  + Audit Log     │
                 └──────────────────┘
```

---

## 5. End-to-End Workflow

```text
1. User Login
       ↓
2. Create New Case
       ↓
3. Upload MRI Image
       ↓
4. Validate Image
       ↓
5. Preprocess Image
       ↓
6. CNN Prediction
       ↓
7. Confidence Score
       ↓
8. Grad-CAM Explanation
       ↓
9. Generate AI-Assisted Draft Report
       ↓
10. Doctor/Researcher Reviews Report
       ↓
11. Approve / Edit Report
       ↓
12. Save Case History
       ↓
13. Audit Log Updated
```

---

## 6. Research Gap and Innovation

### Existing Problem

Many CNN-based medical image classification systems focus primarily on classification accuracy.

This creates several limitations:

* Predictions may be difficult to interpret.
* Explanations may not be integrated with the prediction workflow.
* Generated reports may not have human-review controls.
* Case history and auditability are often handled separately.
* Security and privacy considerations may not be included in educational prototypes.

### Proposed Solution

This project combines:

```text
CNN Prediction
       +
Confidence Score
       +
Grad-CAM Explanation
       +
Structured AI-Assisted Report
       +
Human Review
       +
Case History
       +
Audit Logging
```

This creates a more transparent and reviewable research/educational workflow.

---

# 7. Database Schema

The database follows this relationship:

```text
Role
  │
  ▼
User
  │
  ▼
Case
  │
  ├──────────────► MRIImage
  │
  └──────────────► Prediction
                         │
                         ▼
                   ModelVersion
                         │
                         ▼
                       Report

User ───────────────► AuditLog
```

### Main Entities

#### Role

Defines the type of system user.

Examples:

* Doctor
* Researcher
* Admin

#### User

Stores authentication and authorization information.

#### Case

Stores an opaque patient reference ID without storing personally identifying information.

#### MRIImage

Stores metadata related to uploaded MRI images.

#### Prediction

Stores:

* Predicted class
* Confidence score
* Model version
* Prediction timestamp

#### ModelVersion

Stores information about the CNN model and its evaluation metrics.

#### Report

Stores the AI-generated draft and its review status.

#### AuditLog

Records significant system actions.

Examples:

* Login
* Image upload
* Prediction
* Report generation
* Report review
* Report approval

---

# 8. API Endpoints

| Method | Endpoint                            | Purpose                  |
| ------ | ----------------------------------- | ------------------------ |
| POST   | `/api/auth/register`                | Create user              |
| POST   | `/api/auth/login`                   | Login and return JWT     |
| GET    | `/api/auth/me`                      | Get current user         |
| POST   | `/api/cases`                        | Create a case            |
| GET    | `/api/cases`                        | List cases               |
| POST   | `/api/cases/{id}/upload`            | Upload and validate MRI  |
| POST   | `/api/predictions`                  | Run CNN + Grad-CAM       |
| GET    | `/api/predictions/{id}`             | Get prediction           |
| GET    | `/api/predictions/{id}/explanation` | Get Grad-CAM explanation |
| POST   | `/api/reports/generate`             | Generate draft report    |
| PUT    | `/api/reports/{id}/review`          | Review/approve report    |
| GET    | `/api/models`                       | List model versions      |
| GET    | `/api/models/current`               | Get current model status |
| GET    | `/api/models/audit-logs`            | Admin audit trail        |
| GET    | `/api/dashboard`                    | Dashboard statistics     |
| GET    | `/api/health`                       | Backend health check     |

---

# 9. API Documentation

Once the backend is running, FastAPI automatically provides interactive Swagger/OpenAPI documentation.

Open:

```text
http://localhost:8000/docs
```

You can use Swagger to:

* View API endpoints
* Test API requests
* Check request parameters
* Check response formats
* Test authentication
* Debug backend functionality

---

# 10. Local Setup — Without Docker

## 10.1 Train the CNN

Training should be performed before expecting meaningful model predictions.

Open CMD/PowerShell:

```bash
cd ml
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

For Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 10.2 Dataset

The project can use the Brain Tumor MRI Dataset available on Kaggle:

**Brain Tumor MRI Dataset — Nickparvar**

Dataset:

```text
https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset
```

After downloading, extract it into:

```text
ml/dataset/
```

Expected structure:

```text
ml/
└── dataset/
    ├── Training/
    │   ├── glioma/
    │   ├── meningioma/
    │   ├── notumor/
    │   └── pituitary/
    │
    └── Testing/
        ├── glioma/
        ├── meningioma/
        ├── notumor/
        └── pituitary/
```

The dataset directory is intentionally **gitignored** because datasets can be large.

---

## 10.3 Explore the Dataset

Run:

```bash
python explore_dataset.py
```

This performs basic dataset sanity checks.

---

## 10.4 Train the Model

For ResNet18 transfer learning:

```bash
python train.py --epochs 15 --arch resnet18
```

After training, the model generates:

```text
ml/models/best_model.pth
ml/models/metrics.json
```

The trained model is intentionally gitignored because model files can be large.

---

# 11. Backend Setup

Open a new CMD/PowerShell window.

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from the example file:

### Windows

```bash
copy .env.example .env
```

### Mac/Linux

```bash
cp .env.example .env
```

Initialize the database:

```bash
python seed_db.py
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 12. Frontend Setup

Open another terminal.

```bash
cd frontend
```

Install Node dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

The frontend proxies `/api` requests to the FastAPI backend.

---

# 13. Demo Login

The development database can create a demo doctor account:

```text
Email: doctor@example.com
Password: Doctor@123
```

**Important:** This account is intended only for local development/demo purposes. Production credentials must be changed and securely managed.

---

# 14. Docker Setup

The project also supports Docker Compose.

From the project root:

```bash
docker compose up --build
```

Services:

```text
Frontend → http://localhost:5173
Backend  → http://localhost:8000
Swagger  → http://localhost:8000/docs
```

The `ml/` directory can be mounted into the backend container so the backend can load an already-trained model.

Training should normally be performed on the host machine before starting the production-like container workflow.

---

# 15. SQL Server Support

SQLite is used for local development because it is lightweight and easy to configure.

For production deployment, SQL Server can be used.

The application uses SQLAlchemy ORM, making the database layer portable.

The database can be switched through the environment configuration.

Example:

```text
DATABASE_URL=<SQL_SERVER_CONNECTION_STRING>
```

The core ORM model definitions do not need to be redesigned simply because the database backend changes.

---

# 16. CNN Model

The project supports a CNN-based image classification workflow.

A ResNet18 transfer-learning architecture can be used.

### Classification Classes

```text
1. Glioma
2. Meningioma
3. No Tumor
4. Pituitary
```

The model receives a preprocessed MRI image and produces class probabilities.

Example conceptual output:

```text
Glioma       → 0.72
Meningioma   → 0.08
No Tumor     → 0.05
Pituitary    → 0.15
```

The predicted class is the class with the highest model probability.

The system also displays the confidence score.

---

# 17. Grad-CAM Explainability

Grad-CAM stands for:

**Gradient-weighted Class Activation Mapping**

It is used to identify image regions that contributed to the CNN's prediction.

Conceptually:

```text
MRI Image
    ↓
CNN
    ↓
Prediction
    ↓
Gradients from target class
    ↓
Activation Maps
    ↓
Heatmap
    ↓
Overlay on MRI
```

### Why Grad-CAM?

A segmentation model requires pixel-level tumor annotations.

The classification dataset used by this educational project does not provide the required segmentation masks.

Grad-CAM can therefore provide an explanation for an existing classifier without requiring pixel-level tumor annotations.

### Important Limitation

The Grad-CAM heatmap:

* Shows regions that influenced the model prediction.
* Does not represent a confirmed tumor boundary.
* Should not be interpreted as medical segmentation.

---

# 18. GenAI Draft Report

The project contains a report-generation component.

The report generator receives structured and verified information such as:

* Case reference
* Model prediction
* Confidence score
* Explanation information
* Disclaimer information

The generator is designed to produce a structured draft rather than an autonomous medical diagnosis.

### Guardrails

The GenAI component should:

* Use only verified structured fields.
* Avoid inventing medical facts.
* Avoid adding patient history.
* Avoid presenting generated text as a confirmed diagnosis.
* Clearly label the output as a draft.
* Require professional review before approval.

---

# 19. Human-in-the-Loop Review

The system intentionally includes a human review stage.

```text
AI Prediction
      ↓
Grad-CAM Explanation
      ↓
AI Draft Report
      ↓
Doctor/Researcher Review
      ↓
Edit if required
      ↓
Approve
      ↓
Save to Case History
```

The AI-generated report does not become a finalized report automatically.

This makes the workflow suitable for a research/educational decision-support prototype rather than an autonomous diagnostic system.

---

# 20. Model Performance

The training pipeline calculates real evaluation metrics from the held-out testing dataset.

Metrics include:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix
* Per-class sensitivity
* Per-class specificity

The metrics are saved to:

```text
ml/models/metrics.json
```

The project does **not** hard-code or fabricate model performance numbers.

If the model has not been trained yet, the application displays:

```text
Untrained / Demo Placeholder
```

rather than presenting fake accuracy values.

---

# 21. Important Dataset Limitation

The public Kaggle dataset does not provide patient IDs suitable for a strict patient-level split.

Therefore, it is not possible to guarantee that scans from the same patient are never represented across different dataset splits.

This is an important limitation because image-level splitting can potentially introduce data leakage.

The limitation is explicitly disclosed rather than hidden.

This should also be mentioned during project presentation/viva.

---

# 22. Testing Plan

## 22.1 Unit Testing

Examples:

* Validate Grad-CAM output dimensions.
* Validate preprocessing functions.
* Validate model loading.
* Validate image processing.
* Validate authentication utilities.

---

## 22.2 Upload Validation Testing

The upload endpoint should reject:

* Non-image files
* Oversized files
* Invalid image files
* Spoofed content types

Pillow's:

```python
Image.verify()
```

can be used to verify actual image integrity.

---

## 22.3 Integration Testing

The complete workflow should be tested:

```text
Create Case
    ↓
Upload MRI
    ↓
Run Prediction
    ↓
Generate Grad-CAM
    ↓
Generate Report
    ↓
Review Report
    ↓
Approve Report
    ↓
Check Case History
```

---

## 22.4 UI Testing

Test:

* Login
* Logout
* Dashboard
* Empty case list
* Loading states
* Error messages
* Invalid image upload
* Expired session
* Unauthorized access
* Prediction results
* Grad-CAM visualization
* Report review

---

## 22.5 Model Evaluation Testing

After every significant dataset or architecture modification:

```bash
python train.py --epochs 15 --arch resnet18
```

The resulting metrics should be reviewed again.

---

# 23. Authentication and Authorization

The application uses JWT-based authentication.

Passwords are hashed using bcrypt.

Role-based access control can restrict specific operations.

Example roles:

```text
Admin
Doctor
Researcher
```

Example:

```text
Admin
 ├── Manage models
 ├── View audit logs
 └── Manage users

Doctor
 ├── Create cases
 ├── Upload MRI
 ├── Run predictions
 └── Review reports

Researcher
 ├── Create cases
 ├── Run experiments
 └── Review predictions
```

---

# 24. Security and Privacy

The project includes several security controls.

### Password Security

Passwords are not stored in plain text.

They are hashed using bcrypt.

### JWT Authentication

Authenticated requests use JWT tokens.

### Role-Based Authorization

Protected routes check user roles.

### Upload Validation

Uploaded files are checked using:

* Allowed content types
* File size limits
* Actual image verification

### Patient Privacy

The application uses an opaque:

```text
patient_ref_id
```

rather than storing:

* Patient name
* Date of birth
* Address
* Other direct identifying information

### Audit Logging

Significant actions are recorded with:

```text
User
+
Action
+
Timestamp
```

---

# 25. Audit Logging

The system records important actions such as:

```text
LOGIN
UPLOAD_MRI
CREATE_CASE
RUN_PREDICTION
GENERATE_REPORT
REVIEW_REPORT
APPROVE_REPORT
```

This helps create an auditable workflow.

Administrators can use the audit trail to review system activity.

---

# 26. Why SQLite for Development?

SQLite is used for local development because:

* It requires no separate database server.
* It is easy to configure.
* It is suitable for demonstrations and grading.
* It reduces setup complexity.

SQL Server can be used for production deployment.

The application uses SQLAlchemy so the database layer remains portable.

---

# 27. Why FastAPI?

FastAPI was selected because it provides:

* High-performance Python APIs
* Automatic Swagger/OpenAPI documentation
* Pydantic validation
* Easy integration with Python ML libraries
* Async support
* Simple route organization

It is particularly suitable for connecting a Python ML model to a modern web frontend.

---

# 28. Why React + Vite?

React provides a component-based frontend architecture.

Vite provides:

* Fast development server
* Fast build process
* Simple React configuration
* Modern frontend development workflow

The frontend communicates with FastAPI using REST APIs.

---

# 29. Why PyTorch?

PyTorch is used for the CNN model because it provides:

* Flexible deep learning architecture
* Transfer learning support
* GPU acceleration
* Easy model experimentation
* Compatibility with Grad-CAM implementations

---

# 30. Why ResNet18?

ResNet18 is a relatively lightweight convolutional neural network architecture.

It uses residual connections that help training deeper networks.

Transfer learning allows a pretrained model to be adapted to the MRI classification task instead of training an entire CNN from scratch.

---

# 31. Why Grad-CAM Instead of Segmentation?

This is an important viva question.

A segmentation model requires pixel-level annotations showing exactly where the tumor exists.

The classification dataset used in this project does not provide those annotations.

Grad-CAM can instead explain which regions contributed to the classification decision.

Therefore:

```text
Classification Dataset
        ↓
CNN Classifier
        ↓
Grad-CAM Explanation
```

is more appropriate for this educational project than requiring a complete segmentation dataset.

---

# 32. Why GenAI?

The purpose of GenAI is not to independently diagnose a patient.

Instead, it helps transform verified structured model information into a readable draft report.

Example:

```text
Model Output
     +
Confidence
     +
Explanation
     ↓
Structured Draft Report
     ↓
Human Review
```

The report remains a draft until reviewed and approved by a qualified professional.

---

# 33. Advantages

The proposed system provides:

* CNN-based MRI classification
* Confidence score
* Explainable AI using Grad-CAM
* AI-assisted structured reporting
* Human-in-the-loop review
* Case history
* Audit logging
* JWT authentication
* Role-based access
* MRI upload validation
* Docker support
* Swagger API documentation
* Portable database architecture

---

# 34. Limitations

The project has several limitations:

1. It is a research/educational prototype.
2. It is not a clinically validated diagnostic system.
3. The public dataset does not provide reliable patient-level identifiers.
4. Grad-CAM is an explanation method, not tumor segmentation.
5. Model performance depends heavily on dataset quality and distribution.
6. External clinical validation has not been performed.
7. The GenAI report is a draft and requires professional review.
8. Production deployment would require additional security, compliance, monitoring, validation, and clinical testing.

---

# 35. Future Scope

Possible future improvements include:

* Larger multi-center MRI datasets
* Patient-level dataset splitting
* External validation datasets
* MRI segmentation using U-Net or similar architectures
* 3D MRI analysis
* Improved explainability techniques
* Model uncertainty estimation
* Model monitoring
* Federated learning
* Advanced clinical workflow integration
* Secure cloud deployment
* FHIR/healthcare interoperability
* More robust model versioning
* Human feedback collection
* Improved GenAI report generation with stronger validation

---

# 36. Viva / Defense Questions

## Q1. What is the main objective of the project?

The main objective is to develop a research/educational MRI brain tumor decision-support system that combines CNN-based classification, Grad-CAM explainability, AI-assisted reporting, and human review in one workflow.

---

## Q2. What are the tumor classes?

The system supports:

```text
Glioma
Meningioma
No Tumor
Pituitary
```

---

## Q3. What is Grad-CAM?

Grad-CAM is an explainability technique that produces a heatmap showing image regions that contributed to a CNN's prediction.

---

## Q4. Why did you use Grad-CAM?

Because the project uses a classification dataset without pixel-level tumor segmentation annotations. Grad-CAM can explain a classifier without requiring segmentation masks.

---

## Q5. Is the system a medical diagnostic tool?

No.

It is a research/educational decision-support prototype and does not provide an autonomous medical diagnosis.

---

## Q6. Why is human review required?

AI predictions can contain errors. A qualified professional must review the model output and AI-generated report before any clinical use.

---

## Q7. Why use FastAPI?

FastAPI provides a lightweight, high-performance Python API framework with automatic Swagger/OpenAPI documentation and easy integration with ML models.

---

## Q8. Why React?

React provides a modern component-based frontend and allows the dashboard to communicate with FastAPI through REST APIs.

---

## Q9. Why PyTorch?

PyTorch provides flexible deep-learning development, transfer learning, GPU support, and easy integration with explainability methods such as Grad-CAM.

---

## Q10. What is the purpose of GenAI?

GenAI converts verified structured prediction information into a readable draft report. It does not independently diagnose the patient.

---

## Q11. How do you prevent GenAI from inventing medical information?

The report generator receives restricted structured inputs and uses guardrails instructing it not to introduce unsupported medical facts. The output is also clearly labeled as a draft and requires professional review.

---

## Q12. How do you protect patient privacy?

The prototype uses an opaque patient reference ID instead of storing direct patient-identifying information such as name or date of birth.

---

## Q13. How do you secure passwords?

Passwords are hashed using bcrypt rather than stored in plain text.

---

## Q14. What is JWT?

JWT stands for JSON Web Token. It is used to securely represent authenticated user sessions between the frontend and backend.

---

## Q15. What is an audit log?

An audit log records important system actions along with the acting user and timestamp.

---

## Q16. What happens if the model is not trained?

The application explicitly shows:

```text
Untrained / Demo Placeholder
```

instead of presenting fabricated accuracy or prediction performance.

---

## Q17. How do you evaluate the model?

The training pipeline calculates:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix
* Sensitivity
* Specificity

on the held-out testing data.

---

## Q18. What is the major dataset limitation?

The dataset does not provide patient-level identifiers that allow a strict patient-level train/test split.

Therefore, potential data leakage between scans from the same patient cannot be completely ruled out.

---

# 37. Disclaimer

> **This system is a research/educational decision-support tool. It does not provide a medical diagnosis. The Grad-CAM heatmap indicates regions that influenced the model's prediction; it is not a confirmed tumor boundary. All AI-generated content requires review and approval by a qualified professional before any clinical use.**

---

# 38. Project Status

Current project status:

```text
Frontend        → React + Vite
Backend         → FastAPI
ML              → CNN / ResNet18
Explainability  → Grad-CAM
GenAI           → Draft Report Generator
Database        → SQLAlchemy + SQLite
Authentication  → JWT + bcrypt
Security        → Upload validation + RBAC
Deployment      → Docker Compose
API Docs        → Swagger/OpenAPI
```

The model should be trained using the provided dataset before using the system for meaningful model predictions.

---

# 39. Repository

GitHub:

```text
https://github.com/pratikshap2810-star/Brain-tumor-detection
```

---

## 40. Final Project Workflow

```text
                  ┌─────────────────┐
                  │   MRI Upload    │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Image Validation│
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │  Preprocessing  │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │   CNN Model     │
                  │   Prediction    │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Confidence Score│
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │    Grad-CAM     │
                  │   Explanation   │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ GenAI Draft     │
                  │     Report      │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Doctor/Research │
                  │     Review      │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │  Save History   │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │   Audit Log     │
                  └─────────────────┘
```

**This project demonstrates the integration of Deep Learning, Explainable AI, Generative AI, Full-Stack Development, Database Management, Authentication, Security, and Human-in-the-Loop decision support in a single research/educational application.**

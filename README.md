# 📚 The Reader E-Book API – Django + Supabase

Welcome to **The Reader E-Book API**, a modern RESTful backend built with Django REST Framework and Supabase Storage. This API powers the [**"The Reader" Android App**](https://github.com/sumonkumarbd/Pdf-Books-Reader-App), allowing users to access PDF books with rich metadata and secure cloud storage.

---

## 🚀 Features

- **Upload PDF books** with full metadata and cover images (stored in Supabase)
- **List, search, and filter** all uploaded books
- **Detailed book view** with all metadata, including category, language, publisher, and more
- **Update book** information and files
- **Delete books** (with automatic file cleanup in Supabase)
- **Download endpoints** for PDFs and cover images
- **Foreign key support** for Category and Language
- **Production-ready**: scalable, secure, and cloud-native API

---

## 👨‍💻 Developer

**Name**: Sumon Kumar  
[🔗 LinkedIn](https://www.linkedin.com/in/sumonkmr/)

---

## 🛠️ Technologies Used

- Python 3.11+
- Django 4+
- Django REST Framework
- Supabase Storage (cloud file storage)
- PostgreSQL (or SQLite for development)
- HTML (for root/landing page)
- RESTful API Design

---

## 📂 Project Structure

The project is organized for clarity and scalability.  
Below is the top-level file and folder structure:

```
THE-READER-EBOOK-API-DJANGO/
│
├── .idea/               # IDE settings (optional)
├── .venv/               # Python virtual environment (not tracked)
├── books/               # Main Django app: models, views, serializers, signals
├── config/              # Configuration files (e.g., settings, wsgi, asgi)
├── static/              # Static assets
├── staticfiles/         # Collected static files for deployment
├── storage/             # Supabase integration and storage utilities
├── templates/           # HTML templates (landing page, etc.)
│
├── .env                 # Environment variables (not committed)
├── .gitignore
├── build_files.sh       # Build/deployment script
├── manage.py            # Django management script
├── Procfile             # For deployment (e.g., Heroku)
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment config
```

**Key Points:**
- **books/**: Contains everything related to the Book model and API logic.
- **storage/**: Handles communication with Supabase Storage for file upload, download, and deletion.
- **config/**: Django settings and configurations.
- **templates/**: Contains the HTML for the root landing page and any other template-based views.

---

## ⚙️ Installation & Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/sumonkumarbd/The-Reader-eBook-API-Django.git
    cd The-Reader-eBook-API-Django
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root with your Supabase and Django secrets:

    ```
    DJANGO_SECRET_KEY=your_secret
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    SUPABASE_BUCKET=the-reader-ebook
    DEBUG=True
    ```

5. **Migrate the Database**
    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser (Optional, for admin access)**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Server**
    ```bash
    python manage.py runserver
    ```
    The API will be available at:  
    `http://127.0.0.1:8000/`

---

## 🌐 Deployed URL

**Production Root Endpoint:**  
[https://the-reader-ebook.vercel.app/](https://the-reader-ebook.vercel.app/)

---

## 📬 API Endpoints Reference

All endpoints are under `/api/`.  
Return data as JSON unless otherwise stated.

| Method   | Endpoint                           | Description                            | Auth Required |
|----------|------------------------------------|----------------------------------------|--------------|
| GET      | `/api/books/`                      | List all books                         | No           |
| GET      | `/api/books/{pk}/`                 | Retrieve book details by ID            | No           |
| POST     | `/api/books/`                      | Upload a new book                      | Yes          |
| PUT      | `/api/books/{pk}/`                 | Update book info/files                 | Yes          |
| DELETE   | `/api/books/{pk}/`                 | Delete a book by ID                    | Yes          |
| GET      | `/api/books/search/?q=term`        | Search books by title or author        | No           |
| GET      | `/api/download/pdf/{pk}/`          | Download PDF file                      | No           |
| GET      | `/api/download/cover/{pk}/`        | Download cover image                   | No           |

---

## 🛠️ API Data Structure

All book data follows this schema:

| Field            | Type      | Description                                            |
|------------------|-----------|--------------------------------------------------------|
| id               | Integer   | Unique identifier                                      |
| title            | String    | Book title                                             |
| author           | String    | Author name                                            |
| slug             | String    | URL-friendly unique slug                               |
| category         | String    | Category name (or object, if using FK in serializer)   |
| language         | String    | Language name (or object, if using FK in serializer)   |
| publisher        | String    | Publisher name                                         |
| publication_date | String    | Publication date (DD-MM-YYYY)                          |
| description      | String    | Book summary/description                               |
| pdf_url          | String    | Public URL to the PDF file in Supabase                 |
| cover_url        | String    | Public URL to the cover image in Supabase              |
| upload_date      | String    | Upload date (DD-MM-YYYY)                               |
| featured         | Boolean   | Whether the book is featured                           |

#### Example

```json
{
  "id": 76,
  "title": "Python Crash Course",
  "author": "Eric Matthes",
  "slug": "python-crash-course-eric-matthes",
  "category": "Education",
  "language": "English",
  "publisher": "Book Publications",
  "publication_date": "30-09-2022",
  "description": "If you've been thinking about learning how to code or picking up Python, ...",
  "pdf_url": "https://zkrmzrvzkhmqtiacdvzo.supabase.co/storage/v1/object/public/the-reader-ebook/eBooks/Python_Crash_Course.pdf",
  "cover_url": "https://zkrmzrvzkhmqtiacdvzo.supabase.co/storage/v1/object/public/the-reader-ebook/images/Python_Crash_Course.jpg",
  "upload_date": "16-05-2025",
  "featured": true
}
```

---

## 📱 Android App

An official Android app is available for users to experience this API in action:

- **Download the latest APK:**  
  [the_reader.apk](https://github.com/sumonkumarbd/Pdf-Books-Reader-App/raw/refs/heads/master/the_reader.apk)

- **Source code:**  
  [Pdf-Books-Reader-App GitHub Repository](https://github.com/sumonkumarbd/Pdf-Books-Reader-App)

---

## 📌 Book Upload Metadata

- `title`: string (required)
- `author`: string (required)
- `category`: string (required)
- `language`: string (required)
- `publisher`: string (optional)
- `publication_date`: string (optional, format: DD-MM-YYYY)
- `description`: string (required)
- `featured`: boolean (required)
- `pdf_file`: file (required)
- `cover_image`: file (required)

---

## ☁️ Supabase Storage Integration

- All files (PDFs, covers) are stored in a Supabase bucket.
- On book deletion, files are automatically removed from storage.
- File fields store only the relative path, public URLs are generated for access.

---

## 🛡️ Authentication

- Default: Django token authentication (can be extended with JWT/OAuth).
- Obtain your token via the DRF `/api-token-auth/` endpoint (details in code/docs).

---

## 📝 Logging & Production

- Production-ready logging via Django's logging system.
- Automatic file cleanup and error logging.
- Never log sensitive user data.

---

## ❤️ Acknowledgments

Developed for **The Reader Android App** community.  
Feedback and contributions are welcome!

---

> **Security Notice:**  
> Never commit `.env` files with real secrets. Use `.env.example` to share required environment variables.

---

> **Best Practice:**  
> Never commit your local `.venv` (virtual environment) folder. All dependencies are tracked in `requirements.txt`. Re-create your environment using:
> 
> ```
> python -m venv venv
> source venv/bin/activate  # or venv\Scripts\activate on Windows
> pip install -r requirements.txt
> ```

---

## 💼 Commercial Use, Customization, and Licensing

This project is released under the permissive [MIT License](https://github.com/sumonkumarbd/The-Reader-eBook-API-Django/blob/master/MIT%20License), allowing anyone to use, modify, and even integrate this code into commercial products.

If you are interested in:
- Purchasing exclusive rights,
- Custom versions or private deployments,
- Or commissioning similar Django/Android eBook solutions,

please contact [Sumon Kumar](https://www.linkedin.com/in/sumonkmr/) for business inquiries and custom offers.

---

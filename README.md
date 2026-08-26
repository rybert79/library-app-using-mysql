# Library App using MySQL

A simple library management API built with **FastAPI** and **MySQL**. The application provides CRUD operations for books and also serves a simple frontend from the `static` directory.

## Features

- Add a new book
- Get all books
- Get a book by ID
- Update a book
- Delete a book
- MySQL database integration
- Environment variable support for the database password
- Custom 404 page

## Requirements

- Python 3.9+
- MySQL Server
- `pip`

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

## Database Setup

Create the database and `books` table in MySQL:

```sql
CREATE DATABASE perpustakaan;

CREATE USER 'fastapi'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON perpustakaan.* TO 'fastapi'@'localhost';
FLUSH PRIVILEGES;

USE perpustakaan;

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    jumlah_halaman INT NOT NULL
);
```

The application expects the MySQL configuration used in `app.py`:

- Host: `localhost`
- User: `fastapi`
- Database: `perpustakaan`
- Password: stored in the `password_sql` environment variable

## Environment Variable

Create a `.env` file in the project root:

```env
password_sql=your_password
```

Replace `your_password` with the password of the MySQL `fastapi` user.

> Do not commit your `.env` file to GitHub. Add `.env` to `.gitignore` if it is not already ignored.

## Running the Application

Start the FastAPI application with Uvicorn:

```bash
uvicorn app:app
```

By default, the application will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Open the frontend (`static/index.html`) |
| POST | `/book` | Add a new book |
| GET | `/books` | Get all books |
| GET | `/books/{id}` | Get a book by ID |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |

### Add a Book

Send a `POST` request to `/book` with JSON:

```json
{
  "judul": "Contoh Buku",
  "jumlah_halaman": 200
}
```

### Update a Book

Send a `PUT` request to `/books/{id}` with JSON:

```json
{
  "judul": "Judul Baru",
  "jumlah_halaman": 250
}
```

### Get a Book by ID

```text
GET /books/1
```

### Delete a Book

```text
DELETE /books/1
```

## Project Structure

```text
library-app-using-mysql/
├── app.py
├── requirements.txt
├── README.md
├── .env
└── static/
    ├── index.html
    └── 404.html
```

The `.env` file contains local secrets and should not be committed to the repository.

## Notes

The application uses a single MySQL connection and cursor created when `app.py` starts. For a production application, consider using a connection pool, handling database connection failures, and separating database logic from the API routes.

## License

This project is licensed under the terms of the included [LICENSE](LICENSE) file.

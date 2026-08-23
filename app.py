from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Request
from pydantic import BaseModel
from dotenv import load_dotenv
import mysql.connector
import os

app = FastAPI()

load_dotenv()
password = os.getenv("password_sql")

db = mysql.connector.connect(
    host="localhost",
    user="fastapi",
    password=password,
    database="perpustakaan"
)
cursor = db.cursor()

class Book(BaseModel):
    judul: str
    jumlah_halaman: int

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def halaman_utama():
    return FileResponse("static/index.html")

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return FileResponse(
        "static/404.html",
        status_code=404
    )

@app.post("/book")
def tambah_buku(book: Book):

    sql = """
    INSERT INTO books (judul, jumlah_halaman)
    VALUES (%s, %s)
    """

    values = (book.judul, book.jumlah_halaman)

    cursor.execute(sql, values)
    db.commit()

    return {
        "message": "Buku berhasil ditambahkan",
        "id": cursor.lastrowid,
        "judul": book.judul,
        "jumlah_halaman": book.jumlah_halaman
    }

@app.get("/books")
def liatbuku():
	dbjson = []

	cursor.execute("SELECT * FROM books")
	items = cursor.fetchall()
	for item in items:
		dbjson.append({"id": item[0], "judul": item[1], "jumlah_halaman": item[2]})

	return dbjson

@app.get("/books/{id}")
def liat_buku_berdasarkan_id(id: int):
    cursor.execute(
        "SELECT * FROM books WHERE id = %s",
        (id,)
    )

    hasil = cursor.fetchone()

    if hasil is None:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    return {
        "id": hasil[0],
        "judul": hasil[1],
        "jumlah_halaman": hasil[2]
    }
@app.delete("/books/{id}")
def delete_buku(id: int):
    cursor.execute("DELETE FROM books WHERE id = %s", (id,))

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Buku tidak ditemukan"
        )

    db.commit()

    return {"message": "Buku berhasil dihapus"}

@app.put("/books/{id}")
def update_buku_berdasarkan_id(id: int, book: Book):
	cursor.execute("UPDATE books SET judul = %s, jumlah_halaman = %s WHERE id = %s", (book.judul, book.jumlah_halaman, id))

	if cursor.rowcount == 0:
		raise HTTPException(
			status_code=404, 
			detail="Buku tidak ditemukan")

	db.commit()

	return {"message": "Buku berhasil diupdate"}

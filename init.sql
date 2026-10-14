CREATE DATABASE IF NOT EXISTS praktikum_db;
USE praktikum_db;

CREATE TABLE IF NOT EXISTS mahasiswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO mahasiswa (nama) VALUES ('Sulthoni'), ('Mahasiswa Contoh');

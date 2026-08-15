CREATE DATABASE IF NOT EXISTS urlshortener;

USE urlshortener;

CREATE TABLE IF NOT EXISTS urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(20) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL,
    click_count INT DEFAULT 0
);

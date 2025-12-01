DROP DATABASE IF EXISTS qlhocsinh;
CREATE DATABASE qlhocsinh CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE qlhocsinh;

CREATE TABLE hocsinh (
    mahs INT PRIMARY KEY,
    hoten VARCHAR(150),
    phai VARCHAR(10),
    ngaysinh DATE,
    lop VARCHAR(10)
);
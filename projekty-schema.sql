CREATE TABLE `rodzaj` (
 `id_rodzaj` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 `nazwa_rodzaj` VARCHAR(50) NOT NULL
);

CREATE TABLE `status` (
 `id_status` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 `nazwa_status` VARCHAR(50) NOT NULL
);

CREATE TABLE `projekt` (
 `id_projekt` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 `id_rodzaj` INTEGER NOT NULL,
 `id_status` INTEGER NOT NULL,
 `nr_projekt` VARCHAR(15) NOT NULL,
 `temat_projekt` VARCHAR(150) NOT NULL,
 `data_rozpoczecia` DATE NOT NULL,
 `data_zakonczenia` DATE,
 `kwota` DECIMAL(10,2) NOT NULL,
 `uwagi` VARCHAR(500)
);

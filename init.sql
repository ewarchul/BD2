-- roznice wzg diagramu
-- 1) tabela pracownik, kolumna pesel jest tekstem
-- 2) tabela katalog_informacji nie ma kolumny id_pracownika (bo po co jej??)
-- 3) tabela osoba_uprawniona, kolumna rodzaj_uprawnienia_lp_uprawnienia i lp_uprawnienia duplikują rodzaj_uprawnienia, wiec ich nie ma
-- 4) tabela rodzaj_uprawnienia, lp_uprawnienia duplikuje rodzaj_uprawnienia
-- 5) czy w tabeli osoba_uprawniona kolumna id_umowy_upowazniajacej nie powinno byc FK?
-- 6) tabela umowa, kolumna lp powinna sie nazywac 'rodzaj umowy'?


PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS dzial;
CREATE TABLE dzial(
	id_dzialu INTEGER PRIMARY KEY,
	nazwa_dzialu CLOB
);

DROP TABLE IF EXISTS pracownik;
CREATE TABLE pracownik(
	id_pracownika INTEGER PRIMARY KEY,
	imie CLOB,
	nazwisko CLOB,
	pesel CHARACTER(11) CHECK(length(pesel) == 11),
	stanowisko CLOB,
	poziom_dostepu INTEGER,
	id_dzialu INTEGER NOT NULL,
	CONSTRAINT pracownik_dzial_fk
		FOREIGN KEY (id_dzialu)
		REFERENCES dzial(id_dzialu)
);

DROP TABLE IF EXISTS katalog_informacji;
CREATE TABLE katalog_informacji(
	id_katalogu INTEGER PRIMARY KEY,
	nazwa_katalogu CLOB,
	data_utworzenia TEXT
);

DROP TABLE IF EXISTS uprawnienie;
CREATE TABLE uprawnienie(
	id_uprawnienia INTEGER PRIMARY KEY,
	poziom_dostepu INTEGER,
	id_pracownika INTEGER NOT NULL,
	id_katalogu INTEGER NOT NULL,
	CONSTRAINT uprawnienie_pracownik_fk
		FOREIGN KEY (id_pracownika)
		REFERENCES pracownik(id_pracownika)
	CONSTRAINT uprawnienie_katalog_informacji_fk
		FOREIGN KEY (id_katalogu)
		REFERENCES katalog_informacji(id_katalogu)
);

DROP TABLE IF EXISTS katalog_osob;
CREATE TABLE katalog_osob(
	id_katalogu_osob INTEGER PRIMARY KEY,
	data_utworzenia TEXT,
	wymagany_poziom_dostepu INTEGER,
	id_katalogu INTEGER NOT NULL,
	CONSTRAINT katalog_osob_katalog_informacji_fk
		FOREIGN KEY (id_katalogu)
		REFERENCES katalog_informacji(id_katalogu)
);

DROP TABLE IF EXISTS rodzaj_uprawnienia;
CREATE TABLE rodzaj_uprawnienia(
	rodzaj_uprawnienia INTEGER PRIMARY KEY,
	opis CLOB
);

DROP TABLE IF EXISTS osoba_uprawniona;
CREATE TABLE osoba_uprawniona(
	numer_osoby INTEGER PRIMARY KEY,
	imie CLOB,
	nazwisko CLOB,
	id_katalogu_osob INTEGER NOT NULL,
	rodzaj_uprawnienia INTEGER NOT NULL,
	nasz_pracownik CHAR(1),

	CONSTRAINT osoba_uprawniona_katalog_osob_fk
		FOREIGN KEY (id_katalogu_osob)
		REFERENCES katalog_osob(id_katalogu_osob)
	CONSTRAINT osoba_uprawniona_rodzaj_uprawnienia_fk
		FOREIGN KEY (rodzaj_uprawnienia)
		REFERENCES rodzaj_uprawnienia(rodzaj_uprawnienia)
);

DROP TABLE IF EXISTS katalog_umow;
CREATE TABLE katalog_umow(
	id_katalogu_umow INTEGER PRIMARY KEY,
	data_utworzenia TEXT,
	wymagany_poziom_dostepu INTEGER,
	id_katalogu INTEGER,
	CONSTRAINT katalog_umow_katalog_informacji_fk
		FOREIGN KEY (id_katalogu_umow)
		REFERENCES katalog_informacji(id_katalogu)
);

DROP TABLE IF EXISTS rodzaj_umowy;
CREATE TABLE rodzaj_umowy(
	id INTEGER PRIMARY KEY,
	typ_umowy CLOB
);

DROP TABLE IF EXISTS podmiot_zewnetrzny;
CREATE TABLE podmiot_zewnetrzny(
	id_podmiotu INTEGER PRIMARY KEY,
	status_prawny CLOB,
	typ CLOB
);

DROP TABLE IF EXISTS umowa;
CREATE TABLE umowa(
	id_umowy INTEGER PRIMARY KEY,
	nazwa_umowy CLOB,
	id_katalogu_umow INTEGER NOT NULL,
	podmiot_zewnetrzny_id_podmiotu INTEGER NOT NULL,
	rodzaj_umowy INTEGER NOT NULL,
	CONSTRAINT umowa_katalog_umow_fk
		FOREIGN KEY (id_katalogu_umow)
		REFERENCES katalog_umow(id_katalogu_umow),
	CONSTRAINT umowa_rodzaj_umowy_fk
		FOREIGN KEY (rodzaj_umowy)
		REFERENCES rodzaj_umowy(id)
	CONSTRAINT umowa_podmiot_zewnetrzny_fk
		FOREIGN KEY (podmiot_zewnetrzny_id_podmiotu)
		REFERENCES podmiot_zewnetrzny(id_podmiotu)
);
CREATE INDEX umowa_podmiot_zewnetrzny_idx ON umowa(podmiot_zewnetrzny_id_podmiotu);

DROP TABLE IF EXISTS pozycja;
CREATE TABLE pozycja(
	id_pozycji INTEGER PRIMARY KEY,
	nazwa_pozycji CLOB,
	tresc_pozycji CLOB,
	id_umowy INTEGER NOT NULL,
	CONSTRAINT pozycja_umowa_fk
		FOREIGN KEY (id_umowy)
		REFERENCES umowa(id_umowy)
);
CREATE INDEX pozycja_id_umowy_idx ON pozycja(id_umowy);


DROP TABLE IF EXISTS organizacja;
CREATE TABLE organizacja(
	id_podmiotu INTEGER PRIMARY KEY,
	nip CHAR(10) CHECK(length(nip) == 10),
	nazwa CLOB,
	regon CHAR(14) CHECK(length(regon) == 9 or length(regon) == 14),
	CONSTRAINT osoba_prawna_podmiot_zewnetrzny_fk
		FOREIGN KEY (id_podmiotu)
		REFERENCES podmiot_zewnetrzny(id_podmiotu)
);

DROP TABLE IF EXISTS osoba_fizyczna;
CREATE TABLE osoba_fizyczna(
	id_podmiotu INTEGER PRIMARY KEY,
	imie CLOB,
	nazwisko CLOB,
	pesel CHAR(11) CHECK(length(pesel) == 11),
	CONSTRAINT osoba_fizyczna_podmiot_zewnetrzny_fk
		FOREIGN KEY (id_podmiotu)
		REFERENCES podmiot_zewnetrzny(id_podmiotu)
);

INSERT INTO dzial(id_dzialu, nazwa_dzialu) VALUES(1, "dummy dzial");
INSERT INTO pracownik(id_pracownika, imie, id_dzialu) VALUES(1, "dummy pracownik", 1);

CREATE TRIGGER after_pracownik_delete2 AFTER DELETE on pracownik
BEGIN
	UPDATE uprawnienie SET id_pracownika=1 wHERE id_pracownika = OLD.id_pracownika;
END;
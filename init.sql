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
	pesel CHARACTER(11) CHECK(length(pesel) == 11) UNIQUE,
	stanowisko CLOB,
	poziom_dostepu INTEGER,
	aktywny CHAR(1)
	id_dzialu INTEGER NOT NULL,
	CONSTRAINT pracownik_dzial_fk
		FOREIGN KEY (id_dzialu)
		REFERENCES dzial(id_dzialu)
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
	id_umowy INTEGER NOT NULL,
	rodzaj_uprawnienia INTEGER NOT NULL,
	data_dodania TEXT,
	wymagany_poziom_dostepu INTEGER DEFAULT 1,
	CONSTRAINT osoba_uprawniona_id_umowy_fk
		FOREIGN KEY (id_umowy)
		REFERENCES umowa(id_umowy)
	CONSTRAINT osoba_uprawniona_rodzaj_uprawnienia_fk
		FOREIGN KEY (rodzaj_uprawnienia)
		REFERENCES rodzaj_uprawnienia(rodzaj_uprawnienia)
);

DROP TABLE IF EXISTS rodzaj_umowy;
CREATE TABLE rodzaj_umowy(
	id INTEGER PRIMARY KEY,
	typ_umowy CLOB
);

DROP TABLE IF EXISTS podmiot_zewnetrzny;
CREATE TABLE podmiot_zewnetrzny(
	id_podmiotu INTEGER PRIMARY KEY
);

DROP TABLE IF EXISTS umowa;
CREATE TABLE umowa(
	id_umowy INTEGER PRIMARY KEY,
	nazwa_umowy CLOB,
	podmiot_zewnetrzny_id_podmiotu INTEGER NOT NULL,
	rodzaj_umowy INTEGER NOT NULL,
	data_utworzenia TEXT,
	wymagany_poziom_dostepu INTEGER DEFAULT 1,
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

CREATE TRIGGER after_osoba_fizyczna_insert AFTER INSERT on osoba_fizyczna
BEGIN
	INSERT INTO podmiot_zewnetrzny(id_podmiotu) VALUES(NEW.id_podmiotu);
END;

CREATE TRIGGER after_organizacja_insert AFTER INSERT on organizacja
BEGIN
	INSERT INTO podmiot_zewnetrzny(id_podmiotu) VALUES(NEW.id_podmiotu);
END;
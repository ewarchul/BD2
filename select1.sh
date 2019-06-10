#!/bin/bash

# Do testerów:
# gdyby nie te 'where' w drugim selectcie, to zapytanie zwracałoby 4 gości, ale zwraca jednego, bo jeden ma zbyt slaby poziom dostępu, drugi zbyt wcześnie dostał dostęp, a trzeci jest kobietą

# te dane powinny brac sie z GUI - teraz je zahardkodowałem w celach developerskich
ID_UMOWY=23
CZY_KOBIETA=false
DATA_DODANIA='1994-01-01'

sqlite3 mydb "
SELECT 
	imie, nazwisko 
FROM 
	osoba_fizyczna 
WHERE 
	id_podmiotu=(SELECT podmiot_zewnetrzny_id_podmiotu FROM umowa WHERE id_umowy=$ID_UMOWY)
	AND (
		($CZY_KOBIETA AND substr(imie, -1) == 'a')
		OR (NOT $CZY_KOBIETA AND substr(imie, -1) <> 'a')
	)


UNION ALL


SELECT 
	imie, nazwisko 
FROM 
	osoba_uprawniona 
WHERE 
	id_umowy=$ID_UMOWY 
	AND wymagany_poziom_dostepu <= (SELECT wymagany_poziom_dostepu FROM umowa WHERE id_umowy=$ID_UMOWY)
	AND data_dodania >= $DATA_DODANIA
	AND (
			($CZY_KOBIETA AND substr(imie, -1) == 'a') 
			OR (NOT $CZY_KOBIETA AND substr(imie, -1) <> 'a')
		)
"
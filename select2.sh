#!/bin/bash

# umowy zawarte z daną firmą w danym czasie z minimalną ilością pozycji + ilość pozycji w każdej umowie

# te dane powinny brac sie z GUI - teraz je zahardkodowałem w celach developerskich
ID_PODMIOTU=48
MINIMALNA_ILOSC_POZYCJI_UMOWY=11
DATA_OD='1800-01-01'
DATA_DO='2030-01-01'


sqlite3 mydb "
SELECT 
	count(*) as liczba_pozycji_umowy, u.id_umowy, u.nazwa_umowy, u.data_utworzenia
FROM 
	pozycja p
JOIN
	umowa u ON p.id_umowy = u.id_umowy
WHERE 
	u.podmiot_zewnetrzny_id_podmiotu = $ID_PODMIOTU
	AND u.data_utworzenia >= $DATA_OD
	AND u.data_utworzenia <= $DATA_DO
GROUP BY 
	u.id_umowy
HAVING 
	liczba_pozycji_umowy >= $MINIMALNA_ILOSC_POZYCJI_UMOWY
ORDER BY
	nazwa_umowy
"

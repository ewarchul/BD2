#!/bin/bash

# organizacje, które podpisały z nami umowę w danym roku i do ich wszystkich umów jest łącznie tyle, a tyle osób upoważnionych

# te dane powinny brac sie z GUI - teraz je zahardkodowałem w celach developerskich
ROK='2001'

sqlite3 mydb "
SELECT 
	count(*), o.* 
FROM 
	osoba_uprawniona up
JOIN
	umowa u ON u.id_umowy = up.id_umowy
JOIN
	organizacja o ON o.id_podmiotu = u.podmiot_zewnetrzny_id_podmiotu
WHERE 
	u.data_utworzenia >= $ROK || '-01-01'
	AND u.data_utworzenia <= $ROK || '-12-31'
GROUP BY 
	o.id_podmiotu
"
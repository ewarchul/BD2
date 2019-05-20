#!/bin/bash
BAZA=mydb
sqlite3 $BAZA < init.sql 
(echo .separator ,; echo .import data/dzialy.csv dzial) | sqlite3 $BAZA
(echo .separator ,; echo .import data/pracownicy.csv pracownik) | sqlite3 $BAZA
(echo .separator ,; echo .import data/umowa.csv umowa) | sqlite3 $BAZA
(echo .separator ,; echo .import data/organizacje.csv organizacja) | sqlite3 $BAZA
(echo .separator ,; echo .import data/osoba-fizyczna.csv osoba_fizyczna) | sqlite3 $BAZA
(echo .separator ,; echo .import data/pozycja.csv pozycja) | sqlite3 $BAZA
library(tidyverse)
library(stringi)
library(magrittr)
library(randomNames)
set.seed(666)
code_gen <- function(num, len){
	pesele <- list()
	for(i in 1:num){
		pesele[[i]] <- sample(9, len, replace=1) %>% as.character %>%
			paste(collapse="")
	}
	return(pesele %>% unlist)
}
workers_generator <- function(worker.num){
	persons <- randomNames::randomNames(worker.num, return.complete.data=1)
	workplace <- c('CIO', 'Webmaster', 'Data Base Administrator', 
		'Network Administrator',
		'Health and Safety Inspector',
		'HR specialist',
		'System Administrator',
		'Law Advisor',
		'Chief Accountant',
		'Tax Specialist',
		'Key Account Manager',
		'Customer Relationships Manager',
		'Supply Chain Manager')
	return(tibble(id_pracownika=1:worker.num,
		imie=persons$first_name,
		  nazwisko=persons$last_name,
		  pesel=code_gen(worker.num, 11),
		  stanowisko=sample(workplace, worker.num, replace=1),
		  poziom_dostepu=sample(1:10, worker.num, replace=1),
		  aktywny=sample(c('tak', 'nie'), worker.num, replace=1, prob=c(0.9, 0.1)),
		  id_dzialu=sample(1:6, worker.num, replace=1)
		  ) %>% dplyr::distinct(pesel, .keep_all=1)) 
}
contractor_generator <- function(contractor.num){
	persons <- randomNames::randomNames(contractor.num, return.complete.data=1)
	return(tibble(id_podmiotu=1:contractor.num,
		imie=persons$first_name,
		  nazwisko=persons$last_name,
		  pesel=code_gen(contractor.num, 11)) %>% dplyr::distinct(pesel, .keep_all=1))
}
company_generator <- function(company.num, forbes_filepath){
	if(company.num > 2000)
		stop("Forbes dataset contains only 2000 unique company names.")
	forbes_companies <- readr::read_csv(forbes_filepath)$name	
	return(tibble(id_podmiotu=1000+1:company.num,
		      nip=code_gen(company.num, 10),
		      nazwa=sample(forbes_companies,company.num, replace=1),
		      regon=code_gen(company.num, 9)) %>%
		dplyr::distinct(nip, regon, nazwa, .keep_all=1))
}
date_generator <- function(num){
	return(sample(seq(as.Date('1980/01/01'), as.Date('2019/01/01'), by="day"), num))
}

catalog_generator <- function(companies_filepath, contractors_filepath){
	companies <- readr::read_csv(companies_filepath)
	contractors <- readr::read_csv(contractors_filepath)
	all_cc <- dim(companies)[[1]] + dim(contractors)[[1]]
	return(tibble(id_katalogu=1:all_cc,
		      nazwa_katalogu=sample(c(companies$regon, contractors$pesel)),
		      data_utworzenia=date_generator(all_cc)) %>%
		dplyr::distinct(nazwa_katalogu, data_utworzenia, .keep_all=1))
}
random_string <- function(num, len){
	string.list <- list()
	for(i in 1:num)
		string.list[[i]] <- stringi::stri_rand_strings(len, 1, '[a-z]') %>% paste0(collapse='')
	return(string.list %>% unlist)
}
agreement_generator <- function(companies_filepath, contractors_filepath, agreement_type){
	companies <- readr::read_csv(companies_filepath)
	contractors <- readr::read_csv(contractors_filepath)
	agr.num <- dim(companies)[[1]] + dim(contractors)[[1]] + 20
	return(tibble(id_umowy=1:agr.num,
		      nazwa_umowy=random_string(agr.num, 8),
		      podmiot_zewnetrzny_id_podmiotu=sample(c(companies$id_podmiotu, contractors$id_podmiotu), agr.num, replace=1),
		      rodzaj_umowy=sample(agreement_type$typ_umowy, agr.num, replace=1),
		      data_utworzenia=date_generator(agr.num),
		      wymagany_poziom_dostepu=sample(1:10, agr.num, replace=1)) %>% dplyr::distinct(data_utworzenia, .keep_all=1))
}
agrpos_generator <- function(agreement_id, posnames){
	return(tibble(id_pozycji=1:length(posnames),
		      nazwa_pozycji=posnames,
		      tresc_pozycji=random_string(length(posnames), 300),
		      id_umowy=agreement_id))
}
position_generator <- function(agreement_filepath, posnames){
	agreements <- readr::read_csv(agreement_filepath)$id_umowy
	temp <- agrpos_generator(-1, posnames)
	positions <- temp[FALSE,]
	for(i in agreements)
		positions <- bind_rows(positions, agrpos_generator(i, posnames))
	return(positions)
}
authorized_generator <- function(companies_filepath, agreement_filepath, permission_filepath){
	companies <- readr::read_csv(companies_filepath)
	agreements <- readr::read_csv(agreement_filepath)
	permissions <- readr::read_csv(permission_filepath)
	valid_agreements <- agreements %>% dplyr::filter(podmiot_zewnetrzny_id_podmiotu %in% companies$id_podmiotu) 
	print(valid_agreements)
	print("XD")
	print(agreements)
	stop()
	persons <- randomNames::randomNames(dim(valid_agreements)[[1]], return.complete.data=1)
	return(tibble(numer_osoby=1:dim(valid_agreements)[[1]],
		      imie=persons$first_name,
		      nazwisko=persons$last_name,
		      id_umowy=valid_agreements$podmiot_zewnetrzny_id_podmiotu,
		      rodzaj_uprawnienia=sample(permissions$rodzaj_uprawnienia,dim(valid_agreements)[[1]], replace=1),
		      data_dodania=valid_agreements$data_utworzenia,
		      wymagany_poziom_dostepu=sample(1:10, dim(valid_agreements)[[1]], replace=1)))
}
sectors <- tibble(id_dzialu=1:6, nazwa_dzialu=c('Marketing',
						'IT',
						'HR',
						'Management',
						'Front office',
						'Compliance'))
agreement_type <- tibble(id = 1:11,
			 typ_umowy=c('umowa adhezyjna',
			 'umowa administracyjna',
			 'umowa losowa',
			 'umowa realna',
			 'umowa odpłatna',
			 'umowa o dzieło',
			 'umowa leasingu',
			 'umowa agencyjna',
			 'umowa poręczenia',
			 'umowa zobowiązująca',
			 'umowa wzajemna'))
permission_type <- tibble(rodzaj_uprawnienia=1:10, opis = c('może wszystko', letters[1:8], 'nic nie moze'))

posnames <- c("Data zawarcia umowy", "Nazwisko kontrahenta", "Imiona", "Data urodzenia", "Miejsce urodzenia", "Miejscowoúś", "Ulica", "Kod pocztowy", "Numer domu", "Numer mieszkania", "Reprezentant zleceniodawcy")

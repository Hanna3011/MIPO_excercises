# -*- coding: utf-8 -*-
from __future__ import annotations


class Przelew():

	def __init__(self, nr_rachunku_nadawcy, nr_rachunku_odbiorcy, kwota):
		self.nr_rachunku_nadawcy = str(nr_rachunku_nadawcy)
		self.nr_rachunku_odbiorcy = str(nr_rachunku_odbiorcy)
		self.kwota_przelewu = kwota

class Iodsetki():

	def odsetki(self, saldo):
		return

	def nazwa(self):
		return ""

#liniowy mechanizm naliczania odsetek

class Odsetki_liniowe(Iodsetki):
	def __init__(self):
		self.nazwa = "Odsetki liniowe - 1"

	def odsetki(self, saldo):
		return saldo * 0.1

	def nazwa(self):
		return self.nazwa

#progowy mechanizm naliczania odsetek - progi ver 1.

class Odsetki_progowe1(Iodsetki):

	def __init__(self):
		self.nazwa = "Odsetki progowe - 1"

	def odsetki(self, saldo):
		if saldo < 10000:
			odsetki = 0.03 * saldo
		elif saldo < 2000:
			odsetki = 0.04 * saldo
		else:
			odsetki = 0.05 * saldo
		return odsetki

	def nazwa(self):
		return self.nazwa

#progowy mechanizm naliczania odsetek - progi ver 2.

class Odsetki_progowe2(Iodsetki):

	def __init__(self):
		self.nazwa = "Odsetki progowe - 2"

	def odsetki(self, saldo):
		if saldo < 10000:
			odsetki = (0.01 * saldo)
		elif saldo < 50000:
			odsetki = 100 + (0.02 * (saldo - 10000))
		else:
			odsetki = 100 + 800 + (0.03 * (saldo - 50000))
		return odsetki

	def nazwa(self):
		return self.nazwa

class IRachunek(object):

	def numer(self):
		pass

	def wlasciciel(self):
		pass

	def saldo(self):
		pass

	def piszHistorie(self):
		pass

	def wplata(self, kwota):
		pass

	def wyplata(self, kwota):
		pass

	def przelew_wychodzacy(self, kwota):
		pass

	def przelew_przychodzacy(self, kwota):
		pass

	def ustaw_typ_odsetek(self, typ_odsetek):
		pass

	def nalicz_odsetki(self):
		pass


class Rachunek(IRachunek):

	def __init__(self, numer, imie, nazwisko):
		self._historia = list()
		self._numer = numer
		self._imie = imie
		self._nazwisko = nazwisko
		self._saldo = 0
		self._typ_odsetek = Odsetki_liniowe()

	def numer(self):
		return self._numer

	def wlasciciel(self):
		return self._imie + " " + self._nazwisko

	def saldo(self):
		return self._saldo

	def piszHistorie(self):
		print("##########################")
		for zapis in self._historia:
			print(zapis)

	def wplata(self, kwota):
		self._saldo += kwota
		self._historia.append("Wpłata: " + str(kwota) + ", saldo: " + str(self._saldo))
		return 0

	def wyplata(self, kwota):
		if self._saldo >= kwota:
			self._saldo -= kwota
			self._historia.append("Wypłata: " + str(kwota) + ", saldo: " + str(self._saldo))
			return 0
		self._historia.append("Nieudana wypłata: " + str(kwota) + ", saldo: " + str(self._saldo))
		return -1

	def przelew_wychodzacy(self, kwota):
		if self._saldo >= kwota:
			self._saldo -= kwota
			self._historia.append("Przelew wychodzący: " + str(kwota) + ", saldo: " + str(self._saldo))
			return 0
		self._historia.append("Nieudana transakcja wychodzaca: " + str(kwota) + ", saldo: " + str(self._saldo))
		return -1

	def przelew_przychodzacy(self, kwota):
		self._saldo += kwota
		self._historia.append("Przelew przychodzacy: " + str(kwota) + ", saldo: " + str(self._saldo))
		return 0

	def ustaw_typ_odsetek(self, typ_odsetek):
		self._typ_odsetek = typ_odsetek
		self._historia.append("Zmieniono typ naliczania odsetek na: " + self._typ_odsetek.nazwa)

	def nalicz_odsetki(self):
		odsetki = self._typ_odsetek.odsetki(self._saldo)
		self._saldo += odsetki
		saldo = self._saldo
		self._historia.append("Naliczono odsetki w kwocie: " + str(odsetki) + ", saldo: " + str(saldo))


class RachunekDebetowy(IRachunek):
	def __init__(self, rachunek: Rachunek, dopuszczalny_debet):
		self.rachunek = rachunek
		self.dopuszczalnyDebet = dopuszczalny_debet

	def numer(self):
		return self.rachunek.numer()

	def wlasciciel(self):
		return self.rachunek.wlasciciel()

	def saldo(self):
		return self.rachunek.saldo()

	def ustawDebet(self, debet):
		self.dopuszczalnyDebet = debet
		return self.dopuszczalnyDebet

	def debet(self):
		return self._dopuszczalnyDebet

	def piszHistorie(self):
		return self.rachunek.piszHistorie()

	def wplata(self, kwota):
		return self.rachunek.wplata()

	def wyplata(self, kwota):
		mozliwosc_wyplaty = self.rachunek._saldo + self.dopuszczalnyDebet
		print((mozliwosc_wyplaty))
		if self.rachunek._saldo + self.dopuszczalnyDebet >= kwota:
			self.rachunek._saldo -= kwota
			self.rachunek._historia.append("Wypłata: " + str(kwota) + ", saldo: " + str(self.rachunek._saldo))
			return 0
		self.rachunek._historia.append("Nieudana wypłata: " + str(kwota) + ", saldo: " + str(self.rachunek._saldo))
		return -1

	def przelew_wychodzacy(self, kwota):
		if self.rachunek._saldo + self.dopuszczalnyDebet >= kwota:
			self.rachunek._saldo -= kwota
			self.rachunek._historia.append("Przelew wychodzący: " + str(kwota) + ", saldo: " + str(self.rachunek._saldo))
			return 0
		self.rachunek._historia.append("Nieudana transakcja wychodzaca: " + str(kwota) + ", saldo: " + str(self.rachunek._saldo))
		return -1

	def przelew_przychodzacy(self, kwota):
		return self.rachunek.przelew_przychodzacy()

	def ustaw_typ_odsetek(self, typ_odsetek):
		return self.rachunek.ustaw_typ_odsetek()

	def nalicz_odsetki(self):
		return self.rachunek.nalicz_odsetki()


class KIRInterface():
	def dodaj_bank(self, bank: Bank):
		pass

	def znajdz_bank_rachunku(self, nr_rachunku):
		pass

	def notify(self, sender: object, event: str, przelew: Przelew) -> None:
		pass

class KIR(KIRInterface):

	def __init__(self):
		self.banki = {}

	def dodaj_bank(self, bank: Bank):
		self.banki[bank.nazwa] = bank

	def znajdz_bank_rachunku(self, nr_rachunku):
		for bank in self.banki.keys():
			for numer in self.banki[bank]._rachunki.keys():
				if numer == str(nr_rachunku):
					return self.banki[bank]
		return None

	def notify(self, nazwa_banku_nadawcy: str, przelew: Przelew) -> None:
		bank_nadawcy = self.banki[nazwa_banku_nadawcy]
		if bank_nadawcy == None:
			print("Nie udało się znaleźć banku nadawcy")
			return -1
		bank_odbiorcy = self.znajdz_bank_rachunku(przelew.nr_rachunku_odbiorcy)
		if bank_odbiorcy == None:
			print("Nie udało się znaleźć banku odbiorcy")
			return -1
		rachunek_odbiorcy = bank_odbiorcy._rachunki[str(przelew.nr_rachunku_odbiorcy)]
		rachunek_nadawcy = bank_nadawcy._rachunki[str(przelew.nr_rachunku_nadawcy)]
		if rachunek_nadawcy.przelew_wychodzacy(przelew.kwota_przelewu) != -1:
			rachunek_odbiorcy.przelew_przychodzacy(przelew.kwota_przelewu)
		return 0


class Bank(object):
	def __init__(self, nazwa: str, kir: KIRInterface):
		self._rachunki = dict()
		self.nazwa = nazwa
		self.kir = kir

	def zalozRachunek(self, numer, imie, nazwisko):
		rach = Rachunek(str(numer), imie, nazwisko)
		self._rachunki[numer] = rach
		return rach

	def zalozRachunekDebetowy(self, numer, imie, nazwisko, dopuszczalny_debet):
		rach_niedebetowy = Rachunek(str(numer), imie, nazwisko)
		rach = RachunekDebetowy(rach_niedebetowy, dopuszczalny_debet)
		self._rachunki[str(numer)] = rach
		return rach

	def przeksztalcRachnekNaDebetowy(self, numer_rachunku_niedebetowego, dopuszczalny_debet):
		rach_niedebetowy = self.szukaj(numer_rachunku_niedebetowego)
		rach = RachunekDebetowy(rach_niedebetowy, dopuszczalny_debet)
		self._rachunki[rach.rachunek._numer] = rach
		rach.rachunek._historia.append("Zmieniono rachunek na debetowy. Dopuszczalna wielkość debetu to: " + str(rach.dopuszczalnyDebet))
		return rach

	def szukaj(self, numer):
		return self._rachunki[str(numer)]

	def zlec_przelew(self, nr_rachunku_nadawcy, nr_rachunku_odbiorcy, kwota):
		przelew = Przelew(nr_rachunku_nadawcy, nr_rachunku_odbiorcy, kwota)
		self.kir.notify(self.nazwa, przelew)

def main():
	#tworzenie kir i bankow
	krajowa_IR = KIR()
	bank_PKO = Bank("PKO", krajowa_IR)
	bank_Santander = Bank("Santander", krajowa_IR)
	#dodawanie bankow do KIR
	krajowa_IR.dodaj_bank(bank_PKO)
	krajowa_IR.dodaj_bank(bank_Santander)
	# stworzenie rachunków w bankach
	bank_Santander.zalozRachunek("1", "Jan", "Kowalski")
	bank_PKO.zalozRachunek("2", "Jacek", "Nowak")
	# operacje na rachunkach obsługiwane przez banki

	# wpłata,naliczanie odsetek, przelew
	bank_Santander.szukaj(1).wplata(1500)
	bank_Santander.szukaj(1).nalicz_odsetki()
	bank_Santander.zlec_przelew(1, 2, 100)

	# wyświetlanie historii stworzonych rachunków po operacjach

	bank_Santander.szukaj(1).piszHistorie()
	bank_PKO.szukaj(2).piszHistorie()

	# zmiana sposobu naliczanie odsetek na rachunku o numerze "1" i naliczanie odsetek nowym mechanizmem

	bank_Santander.szukaj(1).ustaw_typ_odsetek(Odsetki_progowe1())
	bank_Santander.szukaj(1).nalicz_odsetki()
	bank_Santander.szukaj(1).piszHistorie()

	# zmiana sposobu naliczanie odsetek na rachunku o numerze "2" i naliczanie odsetek nowym mechanizmem, wpłata i kolejne naliczenie odsetek

	bank_PKO.szukaj(2).ustaw_typ_odsetek(Odsetki_progowe2())
	bank_PKO.szukaj(2).nalicz_odsetki()
	bank_PKO.szukaj(2).wplata(40000)
	bank_PKO.szukaj(2).nalicz_odsetki()

	# operacje na rachunku debetowym obsługiwane przez bank

	bank_Santander.przeksztalcRachnekNaDebetowy(1, 100)
	bank_Santander.szukaj(1).wyplata(1600)
	bank_Santander.zlec_przelew(1,2,100)
	bank_Santander.zlec_przelew(1, 2, 50)

	# wyświtelanie historii obu kont

	bank_PKO.szukaj(2).piszHistorie()
	bank_Santander.szukaj(1).piszHistorie()

main()

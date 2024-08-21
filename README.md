# Nezavisna analiza podataka kvaliteta vazduha suspendovanih cestica PM2.5µg/m3 i PM10µg/m3 na teritoriji Strelista

Nezavisna analiza podataka koja je uradjena uz pomoc python-a i pratecih datoteki izvedana je za naselje Streliste. Streliste je jedno od 7 mernih mesta za pracenje kvaliteta vazduha u lokalnoj mrezi na teritoriji grada Panceva. Stanica se nalazi na lokaciji 7474301,89 4971176,43, **mobilna** je  i prema **Eol klasifikaciji** 

tip stanice je: **bazan**->B,<br> 
tip oblasti je: **urban**->U,<br>
karakteristika oblasti je: **stambena** -> R<br> 

Stanica na Strelistu se svakodnevno analizira i podatke evidentira **manuelno** ovlascena laboratorija [Zavod za javno zdravlje Pancevo](https://www.zjzpa.org.rs/vazduh/).<br>

Iako je u **"Planu kvaliteta vazduha i aglomeraciji  Panceva"** za period 2022 do 2027 navedeno da stanica prati samo **PM10µg/m3**, rezultati 24  casovnih merenja kvaliteta vazduha na sajtu Zavoda za javno zdravlje Pancevo pokazuju i druge 
suspendovane cestice **PM2.5µg/m3** kao sto su:<br>

Rezultati analize suspendovanih cestica u naselju Streliste 2017-2024 god.
<p align="center">
  <img src="https://github.com/6c756e6172/zjzpa-analiza/blob/main/median.png?raw=true" />
</p>

<p align="center">
  <img src="https://github.com/6c756e6172/zjzpa-analiza/blob/main/min-max.png?raw=true" />
</p>

|Suspendovane cestice | Princip uzorkovanja i merenja | Granicna gornja vrednost koja ne bi trebala biti predjena za kal. godinu           
|----------------|----------------|----------------| 
|SO2                |Uzorkovanje u toku 24h. analiza uzorka u laboratoriji metoda sa tetrahlormerkuratom i pararosanilinom. | 50µg/m3
ČAĐ				|	Uzorkovanje u toku 24h. analiza uzorka u laboratoriji, reflektometrija.| 50µg/m3
NO2				| Uzorkovanje u toku 24h. analiza uzorka u laboratoriji, Griess-Saltzmann-ov metod(spektrofotometrija)| 40µg/m3
NH3				| Uzorkovanje u toku 24h. analiza uzorka u laboratoriji, spektrofotometrija, "indofenol plavo"| Nedefinisano
Benzen			| Nedefinisano | 5µg/m3
PM10          | Jedno uzorkovanje u toku 24h u laboratoriji, druga cetiri se vrse automatski| 40µg/m3

# Postojece stanice

Cara Dusana -> T/U/RC -> koordinate 7472621.54 4969543.54 -> **automatska merenja**<br>
Vatrogasni dom -> B/U/RCI -> koordinate 7472732.02 4968331.34 -> **automatska merenja**<br>
Vojlovica -> I/U/IR ->  koordinate 7474301.42 4966661.42 -> **automatska merenja**<br>
Starcevo -> B/S/IR -> koordinate 7477111.06 4962655.41 -> **automatska merenja**<br>
Narodna basta -> B/U/N -> koordinate 7473079.90 4969292.89 -> **automatsko merenje**<br>
Streliste -> B/U/R -> koordinate 7474301,89 4971176,43 -> **manuelno merenje**<br>
Nova Misa -> B/U/R -> koordinate 7474020,43 4968831,86 -> **manuelno merenje**<br>

Klasifikacija<br> 
tip stanice: T -> saobracaj, I -> industrija, B -> bazna<br>
tip oblasti: U -> urbana, S -> prigradska, R-> ruralna<br>
karakteristike oblasti: <br>
R -> stambena, C -> poslovna, I -> industrijska<br>
A -> poljoprivredna, N -> prirodna, RC -> stambeno/poslovna<br>
RC -> poslovno/industrijska, CI -> industrijsko/stambena, IR -> stambeno/poslovna<br>
RCI -> stambeno/poslovno/industrijska, AN -> poljoprivredno/prirodna<br>

## Vrsta i stepen zagadjenja

Glavni izvori zagadjivaca vazduha u Pancevu cine produkti sagorevanja goriva u domacinstvima, industrija, toplana, individualne kotlarnice i lozista, saobracaj, gradjevinska delatnost i neodgovarajuce skladistenje sirovina, neadekvatne deponije smeca i nedovoljan nivo higijene javnih prostora u gradu.<br>

Dominantan izvor u Pancevu predstavlja industrija, **na rasprostiranje zagadjujucih materija u vazduhu na teritoriji grada Panceva najvise uticu dominantni jugoistocni i severni vetrovi tako da se emisija iz Juzne industrijske zone rasprostiru do centra grada duz reke Tamis i duz sela Starcevo** zatim slede lozista, saobracaj je na trecem mestu.<br>

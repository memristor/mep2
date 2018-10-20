# mep2
Eurobot 2017 code

Nisam stigao da komentarišem kod, malo sam ga pregledao, ali još nije sve dovršeno,
neke stvari koje još nismo koristili (jer nije bilo potrebe), a može biti korisno posle, taj deo
treba da završim, moram napisati testove u vidu strategija. Testovi će se izvršavati u
simulaciji. Moram pregledati i taj program, srediti ga, i onda napisati dokumentaciju i tutorijal.
Zbog tih budućih izmena, možda će se imena nekih funkcija menjati, biće dodate dodatne funkcionalnosti i materijala
za korišćenje, zbog toga još nisam hteo da gubim vreme pišući tutorijal (imam i master rad da završim).

Pathfinding radi, ali ga nisam koristio jer je bilo malo vremena za testiranje.
U jednom tasku nije bio ubačen pathfinding, pa kad sam testirao u simulatoru, mislio sam
da nešto pathfinding ne valja, jer sam bio pod velikim pritiskom.

Od korisnih stvari fali:
- mehanizam bezbednog pauziranja taska
- mehanizam podrske simulacije za napredan efikasniji scheduler (API za podršku simulacije)
- moram jos malo testirati mehanizam za pisanje handlera za razne situacije, npr. try catch na svakoj liniji nece biti potrebno kao kod lukicevog koda, ali ce biti obezbedjen kao moguce sredstvo za hendlovanje specificnih situacija za pojedini task. Hendlovanje ce biti odradjeno tako da vazi za sve taskove, kao sto je funkcionisalo hendlovanje detekcije senzora i stajanje. Taj deo je bio definisan u konfiguraciji, sto znaci da ne postoji predefinisano ponasanje robota u samoj platformi, ovo je dobra stvar jer je laksa izmena ponasanja, i lakse je pronalazenje gresaka, manja je zapletenost i medjuzavisnost koda.
- treba još raditi na sistemu introspekcije


Moja platforma je bila prototip, i u principu, ja mislim da je dobar smer za dalje. 
Konfiguracija je pojednostavljena, pisanje strategije je pojednostavljeno, a pritom nije uvedeno ni jedno veliko ograničenje,
osim što se handlovanje grešaka rešava na drugačiji način koji samo na prvi pogled izgleda kao izkomplikovan jer je novi koncept, ali kad vam objasnim biće vam jasnije,
beskonačne petlje nisu dozvoljene u tasku i slična ograničenja, ova ograničenja imaju adekvatnu zamenu ako kojim slučajem bude bilo potrebe da se koristi, mada dobra strategija
ne bi trebala da koristi ovakvu praksu, ovo je namerno uvedeno zbog buduće implementacije naprednog schedulera koji podržava mehanizam simulacije, merenja vremena koje bi trebalo
da se izvrši task iz trenutnog položaja robota i trenutnog stanja na terenu. Ovo je napredan koncept koji još nije testiran, ali sve ću objasniti kad dođem u Novi Sad.

Platforma je pravljena uz pogled u budućnost i budući razvoj, što znači da sam istovremeno razmišljao o
olakšanju rešavanja budućih problema.

Ciljevi ove platforme su:
	* Jednostavnost - lakše se uči, manje koda, sve što je nepotrebno je izbegnuto
	* Fleksibilnost - za svako ograničenje koje sam uveo, smislio sam adekvatnu zamenu koja nije komplikovana kao i zadovoljava cilj jednostavnosti. Ograničenja su svedena na minimum (tj. ja ih ne vidim trenutno).
	* Efikasnost pri korišćenju (sa manje kucanja uraditi više što znači da se više treba fokusirati na problem)
	* Ne zavisnost od 3rd party biblioteka, može se pokrenuti bilo gde sa default python 3 instalacijom
	* Lakši jezik: PYTHON - Čitljiviji je kod u python-u i python se lako uči, a pritom podržava korisne sintaksne olakšice
	* Mogućnost lakog debagovanja - sistem introspekcije, zapisa izvršenja (ne samo kao log, nego i kao ceo trace, kao demo u counter strike npr.)
	* Generalnost rešenja - ova platforma je pravljena u vidu da se koristi ne samo za eurobot takmičenje, 
		nego i za programiranje drugih botova, kao npr. botova u igrici (koju sam isto planirao, tj. koju pravim na osnovu simulatora, biće interestantna multiplayer igrica)
	* Kompatibilnost sa jednostavnijim mehanizmom - ovo je deo koji moram da odradim, zbog nekih
	* Mogućnost implementacije naprednih algoritama - omogućavanjem introspekcije, globalnog i fleksibilnog event sistema koji takođe omogućava implementaciju servisa (tj. moguće je implementirati uslovni događaj), i omogućavanjem uticaja na taskove izvan schedulera, ovo omogućava implementaciju veštačke inteligencije na više nivoa (čime ću se ja baviti u februaru).
	
Šta nije cilj:
	* Formalna ispravnost koda mi nije cilj, moguća je sprega sa ROS-om, što ću i odraditi u vidu modula.
	* Bezbednost okruženja takođe nije cilj, što znači, tehnički moguće je promeniti task iz modula i slične neobične stvari (sve ovo se može lako rešiti omogućenim lakim debagovanjem), python takođe ne podržava privatna polja u klasi, i omogućava da se rade čudne stvari, ali se programi prave mnogo brže kao rezultat ovoga.


Pre nego što završim planirane stvari i izbacim kod na git, pre toga ćemo se naći jedan dan, da vam pokažem kako se pišu moduli i strategije, pa će svako od vas biti osposobljen
da napiše modul i strategiju i pokrene na robotu.

Ne preporučujem ti da gubiš vreme sam da proučavaš ceo kod, moraš razumeti zašto sam baš tako radio da bi lakše razumeo kod (jer sam dosta toga pravio kao prototip).

Pišem ti sve ovo jer si rekao da ćeš pisati svoju platformu, ili si planirao da pišeš svoju. Pa ako si još za to, moraš smisliti pre toga ceo koncept u detalje i razmisliti o mogućim problemima koji bi se mogli pojaviti tokom korišćenja platforme. Ako ovde pogrešiš to posle će biti teže to ispraviti.

Ja sam pisao svoju platformu jer je moj koncept mnogo divergirao u odnosu na Lukićev (razmišljao sam i da izmenim njegovu platformu, ali skontao sam da bi većinu toga trebao da menjam da implementiram moje ideje).
Poenta ove priče je da ukoliko imaš neku ideju za platformu, prvo sve isplaniraš, pa kad dođem, nemoj samostalno da je praviš bez konsultacije da ne bi ponavljao iste greške i da ne bi napravio sličnu stvar i time bacio vreme. Takođe možeš svoju ideju implementirati u moju platformu kad budem postavio na git.

Po mom mišljenju platforma je ok, sve što bi vi trebali da radite, je da programirate module u pythonu, c++-u ili kao zasebnu aplikaciju (po principu ROS-a): moguće je lako ostvariti komunikaciju sa platformom

Problemi koji ostaju da se reše su:
	- pozicioniranje robota (potrebno je dosta testiranja i koda koji garantuje veliku pouzdanost)
	- možeš pisati svoje krivolinijsko kretanje ukoliko želiš, kretačka ploča je upotpunosti portovana tako da se može pokrenuti na linuksu na virtuelnom CAN-u, ponašanje je skoro identično kao na robotu. Za ovo ako želiš da se baviš moram ti pokazati kako da pokreneš simulator
	- Aktuatorska ploča: treba rešiti problem čitanja povratne informacije sa servoa (nije bilo pouzdano: npr. nakon pokušaja čitanja sa RX24 servoa, aktuatorska prestane da radi, pa nije korišćeno, ali bi moglo biti korisno)
	- vizija: pored lidara, vizija bi mogla da bude korisna za detekciju sitnih stvari na terenu itd.
	- za platformu: status RAM memorije, zauzeće procesora, zauzeće mreže itd. (moduli moraju imati laki pristup tim informacijama radi optimizacije iskorišćenja resursa na RPI)
	- ... ako imaš još neke ideje šta bi još moglo da se radi ...

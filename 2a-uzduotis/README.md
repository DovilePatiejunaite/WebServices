Adresas: http://193.219.91.103:8067
Darbą atliko Dovilė Patiejūnaitė ir Paulius Matijošaitis
Web servisas tv programa, pasiekiamas 80 portu.
Paleisti web servisą, reikia įsirašyti docker ir docker-compose.
Paleidimo komandos:
docker-compose build
docker-compose up -d

Paleisti terminale galima šias užklausas, naudojant curl:

1.GET metodas. Parodyti visą TV programą:
#curl -i http://localhost:80/tv_programs

2.GET metodas. Parodyti programą pagal pasirinktą id:
#curl -i http://localhost:80/tv_programs/<id>

3.POST metodas. Patalpinti dar vieną įrašą, rodomą per tv:
#curl -i -H "Content-Type: application/json" - X POST -d '{"title":"<>", "television":"<>","start_time":"<>", etc <optional>}' https://localhost:80/tv_programs

4.PUT metodas. Atnaujinti įrašą, rodomą per tv, pagal įrašo id:
#curl -i -H "Content-Type: application/json" - X PUT -d '{"<>":"<>"}' https://localhost:80/tv_programs/<element_id>

5.DELETE metodas. Ištrinti įrašą, rodomą per tv, pagal id:
#curl -i -H "Content-Type: application/json" -X DELETE http://localhost:80/tv_programs/<element_id>

2 užduotis

Pasileisti reikia:

docker-compose build 

docker-compose up

Servisams naudojami 80 ir 81 portai. 80 - mūsų serviso, 81 - serviso, kurį įtraukiame į savajį.

Galimos užklausos 2-ąjai užduočiai:

1. GET metodas. Parodyti naudojamo serviso visas futbolo komandas:

#curl -i http://localhost:80/football_teams

2. GET metodas. Parodyti konkrečioje tv_programoje, esančias futbolo komandas:

#curl -i http://localhost:80/tv_programs/<tv_:id>/football_teams

3. POST metodas. Sukuria naują televizijos programos dalį, kurioje įdeda tam tikrų futbolo komandų identifikatorius. 

#curl -i -H "Content-Type: application/json" - X POST -d '{"title":"<>", "television":"<>","start_time":"<>","football_teams":"<"id":<>>" etc <optional>}' https://localhost:80/tv_programs

4. DELETE metodas. Ištrina egzistuojančių futbolo komandų numerius iš tv programos.

#curl -i -H "Content-Type: application/json" -X DELETE http://localhost:80/tv_programs/<tv_:id>

5. PUT metodas. Atnaujina tv programos įrašą, pagal jos identifikatorių:id. Galima atnaujinti pasirinktinai: tv_programs įrašus, taip pat ir kito serviso, kurį naudojame įrašus.

#curl -i -H "Content-Type: application/json" - X PUT -d '{"<>":"<>"}' https://localhost:80/tv_programs/<element_id> 

6. GET metodas. Įgyvendintas "embedded" reikalavimas. Vietoje id, tv_programoje bus rodomas pilnas football_team objektas. (1)
Taip pat galima prafiltruoti pasirinktą tv programos įrašą pagal televiziją. (2)

#curl -i http://localhost:80/tv_programs?embedded=football_teams (1)

#curl -i http://localhost:80/tv_programs?television=LNK (2) (Pavyzdys)



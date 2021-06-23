# Amstelhaege

Na jarenlang getouwtrek is de knoop eindelijk doorgehakt: er komt een nieuwe woonwijk in de Duivendrechtse polder, net ten noorden van Ouderkerk aan de Amstel. De huisjes zijn bedoeld voor het midden- en bovensegment van de markt, met name expats en hoogopgeleide werknemers actief op de Amsterdamse Zuidas.

Omdat de Duivenderechtse polder ooit beschermd natuurgebied was, is de compromis dat er alleen lage vrijstaande woningen komen, om zo toch het landelijk karakter te behouden. Dit, gecombineerd met een aantal strenge restricties ten aanzien van woningaanbod en het oppervlaktewater, maakt het een planologisch uitdagende klus. De gemeente overweegt drie varianten: de 20-huizenvariant, de 40-huizenvariant en de 60-huizenvariant. Er wordt aangenomen dat een huis meer waard wordt naarmate de vrijstand toeneemt, de rekenpercentages zijn per huistype vastgesteld.

### Restricties en voorwaarden

- De plattegrond heeft een oppervlakte van 180x160
- De huizen hebben niet dezelfde afmetingen en opbrengst functies. 
- Het aantal woningen in de wijk bestaat voor 60% uit eengezinswoningen, 25% uit bungalows en 15% uit maisons.
- Huizen mogen elkaar en het water niet overlappen.
- We hebben drie verschillende kaarten (water ligt verschillend).
- Huizen hebben vaste minimale vrijstaande meters.
- De verplichte vrijstand voor iedere woning moet binnen de kaart vallen. Overige vrijstand mag buiten de kaart worden meegerekend.


## Aan de slag

### Installatie

Deze codebase is volledig geschreven in Python 3.6. In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

Of via conda:

```
conda install --file requirements.txt
```

### Gebruik

Het programma kan gerund worden middels de volgende code:

```
python main.py 
```

Het programma genereert de volgende output: 

- **Random Solution**: De opbrengst value van de plattegrond, gerund door het random algoritme (baseline algoritme)
- **Iteration**: Het programma iterateert tot de waarde van de constante ITERATIONS_AMOUNT. Deze waarde print de iteraties met interval van 1000. 
- **Current value**:  Deze waarde print bij elke 1000 iterates de opbrengst van de totale plattegrond.
- **i**:  Het programma iterateert 2000 keer een swap_house functie. Deze waarde print de iteraties met interval van 1000.
- **Algoritm solution**: Print de uiteindelijke waarde na de laatste iteratie. 
- **Time**: Weergeeft de tijd in milliseconden hoe lang het programma gedraaid heeft tot de solution.

Verder genereert het programma de volgende files in de results folder:

- **output file**: Het programma genereert een output.csv file waarin de coördinaten van het water en de huizen uiteengezet worden. Tevens wordt de totale waarde van de plattegrond vermeld. 
- **visualization map**: Het programma genereert een visualization.png file die de plattegrond visualiseert.

De aantal huizen variant kan gewijzigd worden middels de variabele amount_of_houses, bovenin de main.py file. Je geeft hierbij 20, 40 of 60 huizen op. 


### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor algoritmes
  - **/code/classes**: bevat de zes benodigde classes voor deze case
  - **/code/visualisation**: bevat de code voor de visualisatie
- **/docs**: bevat de verschillende databestanden die nodig zijn om de plattegrond te vullen en te visualiseren
- **/results**: bevat de output.csv file en de gevisualiseerde plattegrond file

## Random algoritme

Dit algoritme onderneemt de volgende stappen: 

- **1**: Het plaatsen van het water op de map aan de hand van de coördinaten. Deze leest hij uit de docs/docs folder.
- **2**: Het algoritme genereert een random x,y coördinaat van de linker onder hoek (bottom_left) van een huis. 
- **3**: Aan de hand van de bottom_left coördinaat berekent het algoritme de overige coördinaten van de hoekpunten middels het optellen van de lengte en breedte van het betreffende huis.
- **4**: Het controleert of het gegenereerde huis overlapt met een bestaand huis of water.
- **5**: Mits dit niet gebeurt wordt het huis geplaatst, anders genereert het algoritme een nieuwe coördinaat om vervolgens terug te keren naar stap 4. 
- **6**: Dit proces wordt herhaald tot alle 20, 40 of 60 huizen geplaatst zijn.

Als je alleen het random algoritme wil runnen, dien je de volgende code te commenten in main.py
<details>
    <summary> Klik hier om de code te zien </summary>
  
    hillclimb = HillClimber(map)
    map = hillclimb.run(ITERATIONS_AMOUNT, mutate_houses_number=1)
    solution = hillclimb.value
    print('Algoritm solution: ', solution)

    sim_al = SimulatedAnnealing(map)
    map = sim_al.run(ITERATIONS_AMOUNT, mutate_houses_number=1)
    solution = sim_al.value
    print('Algoritm solution: ', solution)
</details>

### Resultaten Random algoritme

Hieronder worden de visualizaties uiteengezet in respectievelijk de wijk 1, 2 en 3 volgorde. Deze resultaten kunnen gerund worden middels het weghalen van de hillclimber en simulated annealing functie in main.py.

<img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/random_image_wijk_1.PNG" width="200" height="150"><img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/random_image_wijk_2.PNG" width="200" height="150"><img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/random_image_wijk_3.PNG" width="200" height="150">

Deze resultaten zijn gegenereerd aan de hand van random.seed(1243546) bovenin models.py.

## Hill Climber  algoritme

Dit algoritme onderneemt de volgende stappen: 

- **1**: Het selecteert een van de bestaande huizen
- **2**: Het zoekt een nieuwe random locatie voor dit huis
- **3**: Het controleert of dit een geldige locatie is
- **4**: Het berekent de nieuwe totale opbrengsten van de plattegrond
- **5**: Mits deze opbrengst hoger is wordt de oude plattegrond vervangen, zo niet wordt de oude plattegrond behouden. 
- **6**: Dit proces wordt 50.000 keer herhaald. Na 50.000 iteraties stagneert de verhoging van de totale opbrengst. 
- **7**: Hierna swapt het programma 2 huizen. Mits deze opbrengst hoger is wordt de oude plattegrond vervangen, zo niet wordt de oude plattegrond behouden. 
- **8**: Dit proces wordt 2.000 keer herhaald
- **9**: Het programma loopt over alle huizen en controleert of het rotaten van de huizen een hogere value op levert.

Als je alleen het Hill Climber algoritme wil runnen, dien je de volgende code te **de**commenten in main.py
<details>
    <summary> Klik hier om de code te zien </summary>

    hillclimb = HillClimber(map)
    map = hillclimb.run(ITERATIONS_AMOUNT, mutate_houses_number=1)
    solution = hillclimb.value
    print('Algoritm solution: ', solution)
  
</details>

### Resultaten Hill Climber

<img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/Hillclimbing_40_wijk1.png" width="200" height="150"><img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/Hillclimbing_40_wijk2.png" width="200" height="150"><img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/Hillclimbing_40_wijk3.png" width="200" height="150">

Deze resultaten zijn gegenereerd aan de hand van random.seed(1243546)  bovenin models.py.

## Simulated Annealing algoritme

Dit algoritme onderneemt de volgende stappen: 

- **1**: Het selecteert een van de bestaande huizen
- **2**: Het zoekt een nieuwe random locatie voor dit huis
- **3**: Het controleert of dit een geldige locatie is
- **4**: Het berekent de nieuwe totale opbrengsten van de plattegrond
- **5**: Het berekent het verschil tussen de oude en de nieuwe opbrengst 
- **5a**: Mits dit verschil groter is dan 0 wordt de oude plattegrond vervangen
- **5b**: Mits dit verschil kleiner is dan 0, wordt het verschil gedeeld door de temperatuur (deze wordt vooraf ingesteld). 
- **5b.1**: Deze uitkomst wordt gebruikt als exponent voor de formule probability = math.exp(uitkomst). Deze genereert een kans tussen de 0 en 1.  
- **5b.2**: Het algoritme genereert een random kansberekening tussen 0 en 1. Als deze random kansberekening groter is dan je kansberekening bij 5b.1, wordt er geen aanpassing gedaan. Als deze kleiner is, wordt het huisje op de nieuwe locatie geplaatst. In dit geval is deze locatie slechter voor de totale uitkomst. Des te langer het algoritme draait, des te kleiner de kans is dat verslechteringen worden geaccepteerd.
- **6**: De temperatuur variable wordt bijgewerkt aan de hand van de formule temperatuur - (temperature / iteraties).  
- **7**: Dit proces wordt 50.000 keer herhaald. Na 50.000 iteraties stagneert de verhoging van de totale opbrengst. 
- **8**: Het programma loopt over alle huizen en controleert of het rotaten van de huizen een hogere value op levert. 

Als je alleen het Simulated Annealing algoritme wil runnen, dien je de volgende code te **de**commenten in main.py
<details>
    <summary> Klik hier om de code te zien </summary>
  
    sim_al = SimulatedAnnealing(map)
    map = sim_al.run(ITERATIONS_AMOUNT, mutate_houses_number=1)
    solution = sim_al.value
    print('Algoritm solution: ', solution)
  
</details>


### Resultaten Simulated Annealing

<img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/Simulated_annealing_40_wijk1.png" width="200" height="150"><img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/Simulated_annealing_40_wijk2.png" width="200" height="150"><img src="https://github.com/Paulmolenaar/MaMaPa/blob/main/results/images/Simulated_annealing_40_wijk3.png" width="200" height="150">

Deze resultaten zijn gegenereerd aan de hand van random.seed(1243546) bovenin models.py.

## Future work

- Alle parameters zijn gebruikt voor de 40 huizen variant in combinatie met de wijk_2 variant. Future work zou kunnen zijn dit in alle variaties (20, 60 huizen, wijk_1, wijk_3) te doen. 
- De Hill Climber en Simulated Annealing nemen als startpunt de oplossing vanuit de random algoritme. Deze oplossing is echter nog niet optimaal. Future work zou kunnen zijn deze beginoplossing optimaliseren zodat het programma minder tijd nodig heeft een betere oplossing te vinden. 
- Het implementeren van een (sub)algoritme die de huisjes 1 meter in elke richting probeert te verplaatsen en toetst of de value hoger wordt. 

## Auteurs
- Max Santosa 
- Marco Veenboer
- Paul Molenaar

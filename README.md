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
- **Algoritm solution**: Print de uiteindelijke waarde na de laatste iteratie. 
- **Time**: Weergeeft de tijd in milliseconden hoe lang het programma gedraaid heeft tot de solution.

Verder genereert het programma de volgende files in de results folder:

- **output file**: Het programma genereert een output.csv file waarin de coördinaten van het water en de huizen uiteengezet worden. Tevens wordt de totale waarde van de plattegrond vermeld. 
- **visualization map**: Het programma genereert een visualization.png file die de plattegrond visualiseert.


### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor algoritmes
  - **/code/classes**: bevat de zes benodigde classes voor deze case
  - **/code/visualisation**: bevat de bokeh code voor de visualisatie
- **/docs**: bevat de verschillende databestanden die nodig zijn om de plattegrond te vullen en te visualiseren
- **/results**: bevat de output.csv file en de gevisualiseerde plattegrond file

### Resultaten


## Auteurs
- Max Santosa 
- Marco Veenboer
- Paul Molenaar

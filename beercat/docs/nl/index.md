# BeerCat - Catalogus van bier, brouwers en brouwerijen

BeerCat is een database over brouwerijen gericht op historisch
onderzoek. Van een brouwerij wordt zoveel mogelijk data vastgelegd, op
een zo gestructureerd mogelijke manier, zodat zoekopdrachten inzicht
kunnen geven in de historie van een brouwerij of brouwer. Een
zoekopdracht heeft bijvoorbeelde de volgende vorm:

    Zoek een brouwer die kennis van zaken heeft over Princessebier
    en die werkzaam was in Haarlem in 1860.

De kernzaken van het systeem zijn **brouwerijen**, **brouwers** en
**bierstijlen**.


## Brouwerij

Om de historie van brouwerijen vast te kunnen leggen is het van belang
te bepalen wat precies een *brouwerij* is. Een brouwerij kan
veranderen van rechtsvorm, eigenaar, lokatie, etc. In deze database is
ervoor gekozen dat een brouwerij wordt gedefinieerd door de
werknaam. Brouwerij *De Hooiberg* kent bijvoorbeeld een lange
geschiedenis, alvorens over te worden genomen door Heineken. Deze
opereert ook nog een tijdje onder dezelfde naam, en verandert dan de
naam in *Heineken*. Vanaf dat moment is het binnen deze database dus
ook een andere brouwerij. De overgang van de ene in de andere kan
worden aangegeven. Wijzigingen in de naam door andere rechtsvormen, of
eventuele toevoegingen (denk: *Koninklijke* of *Stoom*) tellen niet
als veranderde werknaam.


## Brouwer

Onder brouwer wordt verstaan een persoon die zich bezig houdt met de
brouwerij. Dit kan dus ook een directeur zijn, of een eigenaar. Van de
mogelijke functies worden er een aantal gerekend als daadwerkelijk als
*brouwer* betrokken: eigenaar, directeur, brouwer, brouwknecht en
onbekend. In veel gevallen zijn met name in de 19e eeuw eigenaars nog
wel brouwers, maar later niet meer. Dit wordt buiten beschouwing
gelaten.


## Bier

Onder een bierstijl wordt verstaan een algemeen gebruikte
soortnaam. Tot het eind van de 19e eeuw was het nog gebruikelijk van
een biersoort meerdere versies te brouwen, van goedkoper tot
duurder. Deze verschillen worden niet als aparte stijl beschouwd. Een
moderne *Dubbel* is wel een eigen stijl, maar een *Dubbele Princesse*
valt onder de algemene stijl *Princesse*.

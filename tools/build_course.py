# -*- coding: utf-8 -*-
"""Schrijft de inhoud van de Deconstructie-e-learning weg als Adapt-JSON."""
import io, json, os

ROOT = r'C:\Users\seube\Desktop\Other\deconstructie-elearning\src\course\nl'

def w(name, data):
    p = os.path.join(ROOT, name)
    io.open(p, 'w', encoding='utf-8').write(json.dumps(data, indent=2, ensure_ascii=False))
    print('  %-22s %5d regels' % (name, json.dumps(data, indent=2).count('\n')))

# ================================================================== course
course = {
    "_id": "course",
    "_type": "course",
    "_courseId": "deconstructie",
    "title": "Deconstructie",
    "displayTitle": "Deconstructie",
    "subtitle": "Vanaf je einddoel terugredeneren naar je concrete stappen voor nu",
    "description": "Green Office",
    "body": "Je begint niet bij de eerste stap, maar bij het eind. In deze module leer je een project deconstrueren: van je einddoel onderaan terug naar wat je vandaag concreet gaat doen.",
    "instruction": "",
    "_buttons": {
        "_submit": {"buttonText": "Nakijken", "ariaLabel": "Kijk mijn antwoord na"},
        "_reset": {"buttonText": "Opnieuw", "ariaLabel": "Probeer deze vraag opnieuw"},
        "_showCorrectAnswer": {"buttonText": "Toon antwoord", "ariaLabel": "Toon het juiste antwoord"},
        "_hideCorrectAnswer": {"buttonText": "Mijn antwoord", "ariaLabel": "Toon mijn eigen antwoord"},
        "_showFeedback": {"buttonText": "Toelichting", "ariaLabel": "Toon de toelichting"}
    },
    "_globals": {
        "_menu": {"_boxMenu": {"durationLabel": "Tijd:"}},
        "_extensions": {
            "_trickle": {
                "incompleteContent": "Hierboven staat nog iets wat je moet afronden voordat je verder kunt."
            }
        },
        "_accessibility": {
            "_ariaLabels": {
                "skipNavigation": "Ga direct naar de inhoud",
                "navigation": "Hoofdnavigatie",
                "previous": "Vorige", "next": "Volgende", "close": "Sluiten",
                "closeDrawer": "Sluit het zijpaneel", "drawer": "Extra informatie",
                "complete": "Afgerond", "incomplete": "Nog niet afgerond",
                "correct": "Goed", "incorrect": "Fout",
                "selectedAnswer": "gekozen", "unselectedAnswer": "niet gekozen",
                "answeredIncorrectly": "Je antwoord was fout",
                "answeredCorrectly": "Je antwoord was goed",
                "selectAnswer": "Kies een antwoord", "done": "Klaar"
            }
        }
    }
}

# ======================================================= pagina's
PAGES = [
    ("co-10", "Waarom deconstructie?",
     "Wat het probleem is dat deze methode oplost, en waarom je bij het eind begint.", "6 min"),
    ("co-20", "De vier lagen",
     "De opbouw van onder naar boven, met de vraag die bij elke laag hoort.", "8 min"),
    ("co-30", "Het idee in beeld",
     "Een uitgewerkt voorbeeld, laag voor laag gelezen.", "8 min"),
    ("co-40", "Zo werkt het, stap voor stap",
     "De vijf stappen, met per stap hoe je weet dat je klaar bent.", "9 min"),
    ("co-50", "Valkuilen en tips",
     "Wat er in de praktijk misgaat, en hoe je dat voorkomt.", "6 min"),
    ("co-60", "Mini-voorbeeld",
     "Een tweede deconstructie, helemaal uitgeschreven.", "7 min"),
    ("co-65", "Oefening · 30 seconds",
     "Deconstrueer zelf een kaartspel. Laat hem daarna checken door je coach.", "20 min"),
    ("co-70", "Kennischeck",
     "Vijf vragen over situaties uit de praktijk. Je hebt 75% nodig.", "6 min"),
    ("co-80", "Jouw deconstructie",
     "Het canvas. Vul je eigen project in.", "15 min"),
]

contentObjects = [{
    "_id": _id, "_parentId": "course", "_type": "page", "_classes": "",
    "title": t, "displayTitle": t, "body": b, "pageBody": "",
    "linkText": "Bekijken", "duration": d,
    "_graphic": {"alt": "", "src": ""},
    "_pageLevelProgress": {"_isEnabled": True, "_isCompletionIndicatorEnabled": True}
} for _id, t, b, d in PAGES]

# de doorgaan-knop: één blok tegelijk, met vergrendeling zodat je niet vooruit springt
articles = []
for _id, t, b, d in PAGES:
    n = _id.split('-')[1]
    articles.append({"_id": "a-" + n, "_parentId": _id, "_type": "article", "_classes": "",
                     "title": t, "displayTitle": "", "body": "", "instruction": ""})

articles.append({"_id": "a-71", "_parentId": "co-70", "_type": "article", "_classes": "",
                 "title": "Uitslag", "displayTitle": "", "body": "", "instruction": ""})

for a in articles:
    if a["_id"] == "a-70":
        a["_assessment"] = {
            "_isEnabled": True, "_id": "kennischeck",
            "_questions": {"_resetType": "soft", "_canShowFeedback": True},
            "_scoreToPass": 75, "_isPercentageBased": True,
            "_includeInTotalScore": True, "_assessmentWeight": 1,
            "_attempts": "infinite", "_allowResetIfPassed": True,
            "_banks": {"_isEnabled": False},
            "_randomisation": {"_isEnabled": False}
        }

blocks, components = [], []

def block(bid, parent, naam, classes="", verplicht=False):
    """Blokken krijgen bewust geen displayTitle: anders staat de kop dubbel,
    één keer op het blok en één keer op de component eronder.

    verplicht=True zet de doorgaan-knop op slot tot het blok is afgerond.
    Gebruik dat alleen bij vragen: die ronden af als je op Nakijken klikt.
    Bij tekstblokken hangt afronden aan 'is in beeld geweest', en dan kun
    je vastlopen zonder te zien waarom."""
    b = {"_id": bid, "_parentId": parent, "_type": "block", "_classes": classes,
         "title": naam, "displayTitle": "", "body": "", "instruction": ""}
    if verplicht:
        b["_trickle"] = {"_isEnabled": True, "_stepLocking": {"_isEnabled": True, "_isCompletionRequired": True}}
    blocks.append(b)

def text(cid, parent, title, body, classes=""):
    components.append({"_id": cid, "_parentId": parent, "_type": "component", "_component": "text",
                       "_classes": classes, "_layout": "full",
                       "title": title or "Tekst", "displayTitle": title, "body": body, "instruction": ""})

def graphic(cid, parent, src, alt, onderschrift="", title=""):
    components.append({"_id": cid, "_parentId": parent, "_type": "component", "_component": "graphic",
                       "_classes": "", "_layout": "full",
                       "title": title or "Afbeelding", "displayTitle": title, "body": "", "instruction": "",
                       "_graphic": {"large": src, "small": src, "alt": alt,
                                    "attribution": onderschrift, "_url": "", "_target": ""}})

def accordion(cid, parent, title, body, items):
    components.append({"_id": cid, "_parentId": parent, "_type": "component", "_component": "accordion",
                       "_classes": "", "_layout": "full",
                       "title": title, "displayTitle": title, "body": body,
                       "instruction": "Klik op een kop om die open te klappen.",
                       "_shouldCollapseItems": False, "_items": items})

def mcq(cid, parent, title, body, items, feedback, multi=False):
    components.append({"_id": cid, "_parentId": parent, "_type": "component", "_component": "mcq",
                       "_classes": "", "_layout": "full",
                       "title": title, "displayTitle": title, "body": body,
                       "instruction": ("Kies twee antwoorden en klik op Nakijken." if multi
                                       else "Kies één antwoord en klik op Nakijken."),
                       "ariaQuestion": body,
                       "_attempts": 1, "_shouldDisplayAttempts": False,
                       "_isRandom": True, "_hasItemScoring": False, "_questionWeight": 1,
                       "_selectable": 2 if multi else 1,
                       "_canShowModelAnswer": True, "_canShowFeedback": True,
                       "_canShowMarking": True, "_recordInteraction": True,
                       "_items": items, "_feedback": feedback})

def matching(cid, parent, title, body, items, feedback):
    components.append({"_id": cid, "_parentId": parent, "_type": "component", "_component": "matching",
                       "_classes": "", "_layout": "full",
                       "title": title, "displayTitle": title, "body": body,
                       "instruction": "Kies bij elke uitspraak de laag waar hij thuishoort, en klik op Nakijken.",
                       "_attempts": 1, "_shouldDisplayAttempts": False,
                       "_isRandom": True, "_hasItemScoring": False, "_questionWeight": 1,
                       "_canShowModelAnswer": True, "_canShowFeedback": True,
                       "_canShowMarking": True, "_recordInteraction": True,
                       "_items": items, "_feedback": feedback})

def canvas(cid, parent, title, body, velden):
    rijen = ''.join(
        '<div class="canvas-rij">'
        '<label class="canvas-label" for="%s">%s</label>'
        '<textarea class="canvas-invoer js-canvas-veld" id="%s" name="%s" rows="2" placeholder="%s"></textarea>'
        '</div>' % (vid, label, vid, vid, hint) for vid, label, hint in velden)
    components.append({"_id": cid, "_parentId": parent, "_type": "component", "_component": "text",
                       "_classes": "canvas-veld", "_layout": "full",
                       "title": title, "displayTitle": title,
                       "body": body + '<div class="canvas-groep" data-laag="%s">' % title + rijen + '</div>',
                       "instruction": ""})

# de vier lagen als antwoordopties, hergebruikt in beide matchingvragen
LAGEN = ["Laag 1 · Einddoel", "Laag 2 · Richtingen",
         "Laag 3 · Weten of kunnen", "Laag 4 · Concrete stappen"]

def laagopties(juist):
    return [{"text": l, "_isCorrect": (l == juist)} for l in LAGEN]

# ==================================================== 1 · WAAROM
block("b-100", "a-10", "Het probleem")
text("c-100", "b-100", "Het probleem dat deze methode oplost",
     "<p>Een projectgroep krijgt een opdracht en wil aan de slag. Wat er dan bijna altijd gebeurt: iemand opent een document en begint een lijst met taken te typen. Interviews plannen. Literatuur zoeken. Een enquête maken. Het voelt productief, want er staat iets op papier en er kan meteen iemand beginnen.</p>"
     "<p>Drie weken later blijkt er iets vervelends. Die taken waren nergens op gebaseerd. Niemand had scherp wat er aan het eind moest liggen, dus niemand kon controleren of ze daar naartoe leidden. Soms mist er een heel onderdeel dat pas laat opvalt. Soms is er weken gewerkt aan iets wat de opdrachtgever helemaal niet nodig had.</p>"
     "<p>Deconstructie is de tegenbeweging. Je begint niet bij de eerste stap, maar bij het <b>eind</b>, en je redeneert terug. Daardoor kan elke taak die je opschrijft één vraag beantwoorden: draagt dit bij aan wat er straks moet liggen?</p>")

block("b-101", "a-10", "Wat het is", classes="separator")
text("c-101", "b-101", "Een omgekeerde mindmap",
     "<p>De makkelijkste manier om deconstructie te begrijpen is door hem naast een mindmap te leggen.</p>"
     "<p>Bij een <b>mindmap</b> zet je een onderwerp in het midden en waaier je naar buiten. Elk idee mag erbij. Dat is prettig om te verkennen, maar er komt geen richting uit: als je klaar bent heb je twintig bolletjes en nog steeds geen antwoord op de vraag waar je morgen begint.</p>"
     "<p>Bij een <b>deconstructie</b> staat het eindpunt onderaan vast, en werk je omhoog. Elke laag beantwoordt de vraag die de laag eronder oproept. Daardoor is er maar één leesrichting, en eindig je automatisch bij wat je nu moet doen.</p>")

block("b-102", "a-10", "Het verschil in beeld", classes="separator")
graphic("c-102", "b-102", "course/nl/images/omgekeerde-mindmap.svg",
        "Links een gewone mindmap: een onderwerp in het midden met takken die alle kanten op waaieren, met daaronder de tekst: waar begin je, onduidelijk. Rechts een deconstructie: een verticale stapel van vier genummerde lagen met een pijl omhoog, beginnend bij het einddoel onderaan, met daaronder de tekst: je begint onderaan, altijd.",
        "Links waaiert het uit, rechts kiest het richting.",
        "Mindmap tegenover deconstructie")

block("b-103", "a-10", "Uitleg bij het beeld")
text("c-103", "b-103", "Wat je in het beeld hierboven ziet",
     "<p>Kijk naar de linkerkant. De bolletjes hebben geen onderlinge volgorde: je kunt bij elk van de zes beginnen en geen enkele is duidelijk eerst. Dat is precies waarom een mindmap je niet helpt plannen.</p>"
     "<p>Kijk nu naar de rechterkant. De pijl loopt maar één kant op. Laag 1 onderaan bepaalt wat er in laag 2 hoort, laag 2 bepaalt laag 3, en zo verder. Wil je iets veranderen aan je stappen bovenaan, dan moet je terug naar beneden — en dat is een kenmerk, geen last. Het dwingt je te controleren of je verandering nog wel bij je einddoel past.</p>")

block("b-104", "a-10", "Wanneer", classes="separator")
graphic("c-104", "b-104", "course/nl/images/wanneer-in-je-project.svg",
        "Een keten van vier stappen naast elkaar: de discover-fase, dan deconstructie, dan de product backlog, dan sprint 1. Onder de keten loopt een gestippelde pijl terug van sprint 1 naar deconstructie met het label: bij elke grote nieuwe stap opnieuw.",
        "Deconstructie zit tussen verkennen en plannen — en je komt er telkens op terug.",
        "Waar deconstructie in je project zit")

block("b-105", "a-10", "Uitleg wanneer")
text("c-105", "b-105", "Twee momenten om te deconstrueren",
     "<p><b>Aan het begin, in de discover-fase.</b> Je weet dan nog het minst, en dat is juist het punt: de methode maakt zichtbaar wát je niet weet, zodat je dat gericht kunt uitzoeken in plaats van erachter te komen als het te laat is.</p>"
     "<p><b>Bij elke grote nieuwe stap.</b> Merk je halverwege dat je niet meer weet wat de volgende taak is, dan is dat het signaal. Deconstrueer opnieuw, vanaf je nieuwe einddoel.</p>"
     "<p>Deconstructie hoort bij de vaste manier van werken: <i>eerst denken, dan schetsen, dan prompten</i>. Het is het denkwerk dat aan al het maken voorafgaat. Wat er bovenaan uit komt rollen, gaat rechtstreeks door naar je scrum-backlog.</p>")

block("b-106", "a-10", "Tussenvraag", classes="separator")
mcq("c-106", "b-106", "Even checken",
    "Een projectgroep begint maandag met een lijst taken: interviews plannen, literatuur zoeken, een enquête opstellen. Wat is hier het grootste risico?",
    [{"text": "Ze kunnen niet controleren of deze taken naar het juiste eindresultaat leiden", "_shouldBeSelected": True},
     {"text": "Ze hebben te weinig taken opgeschreven om een sprint te vullen", "_shouldBeSelected": False},
     {"text": "Interviews en literatuur horen niet thuis in een projectplanning", "_shouldBeSelected": False},
     {"text": "Ze hadden eerst een mindmap moeten maken van het onderwerp", "_shouldBeSelected": False}],
    {"title": "Even checken",
     "correct": "<p>Precies. Zonder einddoel is er geen maatstaf. Elke taak lijkt dan redelijk, en pas weken later blijkt of het de juiste was.</p>",
     "_incorrect": {"final": "<p>Niet helemaal. Het probleem is niet het aantal taken of het soort werk — interviews en literatuur kunnen prima nodig zijn. Het probleem is dat er geen einddoel is waaraan je ze kunt toetsen.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Het draait om de ontbrekende maatstaf: zonder einddoel kun je geen enkele taak beoordelen.</p>"}})

# ==================================================== 2 · VIER LAGEN
block("b-200", "a-20", "Inleiding")
text("c-200", "b-200", "Vier lagen, vier vragen",
     "<p>Een deconstructie heeft vier lagen. Je bouwt van onder naar boven, en elke laag beantwoordt precies <b>één vraag</b>. Die beperking is belangrijk: zodra je in één laag twee dingen tegelijk probeert te beantwoorden, loopt het vast.</p>"
     "<p>Hieronder staat het schema. Daaronder kun je per laag openklappen wat de vraag is, wat eruit komt, en waar het meestal misgaat.</p>")

block("b-201", "a-20", "Het schema", classes="separator")
graphic("c-201", "b-201", "course/nl/images/vier-lagen.svg",
        "Vier lagen boven elkaar met een pijl omhoog aan de linkerkant. Onderaan laag 1, het einddoel, in magenta: wat wil ik uiteindelijk opleveren, schets het. Daarboven laag 2, richtingen: wat heb ik daarvoor nodig, met als opbrengst de grote bouwstenen. Daarboven laag 3, weten of kunnen: wat moet ik daarvoor weten of kunnen, met als opbrengst wat je al weet en wat nog een leerstap is. Bovenaan laag 4, concrete stappen: wat ga ik nu doen, met als opbrengst je acties voor nu. Daarboven een gestippelde balk: volgende stap, zet de concrete stappen om in scrum-taken.",
        "De vier lagen. Let op de pijl links: je bouwt van onder naar boven.",
        "De vier lagen van onder naar boven")

block("b-202", "a-20", "Leeswijzer")
text("c-202", "b-202", "Hoe je dit schema leest",
     "<p>Drie dingen vallen op in het schema hierboven, en alle drie zijn ze bedoeld.</p>"
     "<p><b>Laag 1 staat onderaan en is als enige gevuld.</b> Dat is geen opmaak maar een geheugensteun: hier begin je, en dit is het enige blok dat je zelf verzint. De rest volgt eruit.</p>"
     "<p><b>De pijl wijst omhoog.</b> Je leest een deconstructie dus tegen de leesrichting van gewone documenten in. Dat went sneller dan je denkt, en het voorkomt dat je alsnog bovenaan begint.</p>"
     "<p><b>Bovenaan staat een gestippelde balk die buiten de vier lagen valt.</b> Dat is geen vijfde laag, maar wat er ná je deconstructie gebeurt: laag 4 verhuist naar je scrum-backlog. De deconstructie zelf stopt bij laag 4.</p>")

block("b-2021", "a-20", "Elementen", classes="separator")
text("c-2021", "b-2021", "Je schrijft elementen op, geen zinnen",
     "<p>Dit is het meest gemaakte misverstand, dus even heel expliciet: in de lagen zet je <b>losse elementen</b> — onderdelen van je product. Geen volzinnen, geen meningen, geen notulen van je overleg.</p>"
     "<p><i>Deconstrueren</i> betekent letterlijk uit elkaar halen. Je haalt je eindproduct uit elkaar in de onderdelen waar het uit bestaat. Elk blokje is zo'n onderdeel.</p>"
     "<p><b>Wel:</b> 'kloppende inhoud', 'visueel ontwerp', 'tool om te bouwen', 'toegankelijkheid', 'stem van de opdrachtgever'.</p>"
     "<p><b>Niet:</b> 'we moeten nog even kijken hoe we de inhoud gaan aanpakken want daar is nog geen duidelijkheid over'.</p>"
     "<p>Een blokje is meestal twee tot vier woorden. Past het niet op een post-it, dan is het geen element maar een verhaal — en dan heb je waarschijnlijk twee dingen tegelijk te pakken die je moet splitsen.</p>")

block("b-2022", "a-20", "De vaste vraag", classes="separator")
text("c-2022", "b-2022", "De vraag die je bij elk element opnieuw stelt",
     "<p>Er is één vraag die je door de hele deconstructie heen blijft herhalen, bij elk element apart:</p>"
     "<p><b>Hoe maken we dit echt goed, en wat moeten we daarvoor kunnen en weten?</b></p>"
     "<p>Let op dat er <i>goed</i> staat en niet <i>af</i>. Dat is geen woordspel maar het verschil tussen twee heel verschillende projecten. Vraag je hoe je iets af krijgt, dan kom je uit bij wat je toevallig al kunt, en lever je iets in dat precies zo goed is als je op dag één al was. Vraag je hoe je het echt goed maakt, dan stuit je op wat je nog niet weet — en dat is precies de opbrengst waar je voor komt.</p>"
     "<p>Werk dus <b>niveau-verhogend</b>. Leg de lat per element op goed, en accepteer dat daar leerstappen uit komen. Die leerstappen zijn geen vertraging; ze zijn het bewijs dat je de lat hoog genoeg hebt gelegd.</p>",
     classes="attention")

block("b-203", "a-20", "Per laag", classes="separator")
accordion("c-203", "b-203", "Wat elke laag precies inhoudt",
          "<p>Klap een laag open. Je vindt per laag de vraag, wat eruit komt, een voorbeeld, en de fout die daar het vaakst wordt gemaakt.</p>",
          [
              {"title": "Laag 1 · Einddoel — onderaan, hier begin je",
               "body": "<p><b>De vraag:</b> wat lever ik uiteindelijk op, en wat weet ik daar nu al van?</p>"
                       "<p><b>Maak het fysiek.</b> Schets betekent hier niet dat je moet kunnen tekenen. Het betekent: zet het op een bord of op tafel, in geschreven vorm, zodat je er met z'n allen naar kunt wijzen. Iets wat op een scherm in een document staat, blijft van één persoon. Iets wat op een bord staat, is van de groep.</p>"
                       "<p><b>Schets breed.</b> Zet alles neer wat je al voor je ziet: hoe het eruitziet, wat erin zit, voor wie het is, hoe iemand het gebruikt, waar het moet werken, hoe goed het moet zijn. Het hele beeld, niet alleen een lijstje eisen. Hoe voller deze schets, hoe meer je er in laag 2 uit kunt halen.</p>""<p><b>En wacht niet tot alles duidelijk is.</b> Ook als het onderwerp, de doelgroep en de inhoud nog open staan, zie je meestal al een hoop voor je — en eisen tellen daar volwaardig in mee.</p>"
                       "<p><b>Voorbeeld:</b> je moet een e-learning maken, meer is er niet gezegd. Onbekend: waarover, voor wie, welke inhoud. Maar je weet al: minimaal hbo-niveau, ongeveer dertig minuten, moet in Brightspace draaien, moet toegankelijk zijn. Vier eisen — en daar rollen meteen drie richtingen uit: didactische opbouw, een tool om te bouwen, en toegankelijkheid.</p>"
                       "<p><b>Waar het misgaat:</b> wachten tot alles duidelijk is. Er is bijna altijd meer bekend dan het voelt. Schrijf elke eis, grens en randvoorwaarde op die je nu al kunt noemen.</p>"},
              {"title": "Laag 2 · Richtingen",
               "body": "<p><b>De vraag:</b> wat heb ik daarvoor nodig? Welke grote onderdelen of richtingen?</p>"
                       "<p><b>Wat eruit komt:</b> de bouwstenen van je project. Dit is <b>verbreden</b>: je noemt de grote onderdelen, nog niet de details.</p>"
                       "<p><b>Voorbeeld:</b> voor die infographic zijn dat er drie — kloppende inhoud, een visueel ontwerp, en een tool om hem mee te maken. Meer niet. Drie tot vijf richtingen is normaal.</p>"
                       "<p><b>Waar het misgaat:</b> meteen te diep gaan. Schrijf je hier al \"interviews afnemen met twee supermarktmanagers\", dan zit je in laag 4 en sla je twee lagen over. Blijf op het niveau van bouwstenen.</p>"},
              {"title": "Laag 3 · Weten of kunnen",
               "body": "<p><b>De vraag:</b> hoe maken we dit <i>echt goed</i>, en wat moeten we daarvoor kunnen en weten?</p>"
                       "<p>Let op die formulering. De vraag is niet hoe je het <i>af</i> krijgt, maar hoe je het <i>goed</i> krijgt. Dat verschil bepaalt alles wat er daarna gebeurt. Vraag je hoe je het af krijgt, dan komt er een lijstje met wat je toevallig al kunt. Vraag je hoe je het echt goed maakt, dan kom je vanzelf uit bij wat je nog niet weet — en dat is precies wat je zoekt.</p>"
                       "<p>Deze vraag stel je bij <b>elk element</b> uit laag 2, niet bij het geheel. Werk niveau-verhogend: bij elk onderdeel apart de lat leggen op goed, niet op klaar.</p>"
                       "<p><b>Wat eruit komt:</b> je ontleedt per element concreet wát er nodig is om het goed te maken. Dit is nog niet je takenlijst — het is de laag waarin je scherp krijgt waar het werk zit, opgedeeld in stukken.</p>""<p>Die stukken vallen in twee soorten. <b>Dingen waarvan je weet dat ze moeten gebeuren:</b> bij een vergelijking zijn dat bijvoorbeeld de criteria, de databronnen en de controle op betrouwbaarheid. Drie losse stukken, geen één vaag blok. En <b>dingen die je eerst moet uitzoeken:</b> dat zijn je <b>leerstappen</b>, en die markeer je apart.</p>""<p>Hoe fijner je hier opdeelt, hoe makkelijker laag 4 wordt. Uit één groot stuk komt één vage taak; uit drie scherpe stukken komen drie taken die je kunt inplannen.</p>""<p>Let op de verhouding: staan er alleen maar leerstappen, dan ben je nog niet concreet genoeg geworden. De vraag \"hoe maken we dit echt goed\" levert bij elk element ook stukken op waarvan je précies weet wat er moet gebeuren.</p>"
                       "<p><b>Voorbeeld:</b> bij het element 'visueel ontwerp' is de vraag niet \"kunnen we iets in elkaar zetten?\" maar \"wat maakt een infographic echt goed, en weten we dat?\". Het antwoord is nee — dus dat is een leerstap.</p>"
                       "<p><b>Waar het misgaat:</b> te snel zeggen dat je iets weet. Twijfel je? Dan is het een leerstap. Op de volgende pagina staat een schema dat die keuze voor je maakt.</p>"},
              {"title": "Laag 4 · Concrete stappen — bovenaan",
               "body": "<p><b>De vraag:</b> wat ga ik nu concreet doen?</p>"
                       "<p><b>Wat eruit komt:</b> acties die je maandag kunt oppakken. Zo concreet dat iemand anders ze zou kunnen uitvoeren.</p>""<p><b>Dit is de stap waar het taken worden.</b> Laag 3 gaf je de stukken; hier maak je er werk van dat een naam en een dag kan krijgen. Elk stuk uit laag 3 levert hier minstens één taak op — de stukken die je al kende worden gewone taken, de leerstappen worden taken die beginnen met uitzoeken.</p>"
                       "<p><b>Voorbeeld:</b> een leerstap uit laag 3 wordt hier een gewone taak. \"We weten niet hoe je een leesbare infographic opbouwt\" wordt: \"drie goede infographics zoeken en ontleden, donderdag klaar\".</p>"
                       "<p><b>Waar het misgaat:</b> doorgaan met vertakken. Zodra je bij uitvoerbare stappen bent, ben je klaar. Deze laag verhuist naar je product backlog en daar krijgt elke stap een prioriteit en een eigenaar.</p>"}
          ])

block("b-2031", "a-20", "Laag 1 zonder onderwerp", classes="separator")
graphic("c-2031", "b-2031", "course/nl/images/laag1-wat-je-al-weet.svg",
        "Voorbeeld van een einddoel voor een e-learning waarvan het onderwerp en de doelgroep nog onbekend zijn. Links een grijs vak met wat nog open staat: waar gaat het over, voor wie is het, welke inhoud komt erin. Rechts een roze omlijnd vak met wat je al wel weet en dus opschrijft: minimaal hbo-niveau, ongeveer dertig minuten, moet in Brightspace werken, moet toegankelijk zijn. Daaronder een magenta balk met het einddoel, en daaronder drie richtingen die eruit volgen: didactische opbouw, tool om te bouwen, en toegankelijkheid.",
        "Vier eisen zijn genoeg om laag 2 mee op te bouwen.",
        "Laag 1 invullen terwijl je het onderwerp nog niet weet")

block("b-2032", "a-20", "Uitleg laag 1 zonder onderwerp")
text("c-2032", "b-2032", "Wachten is niet nodig",
     "<p>Het schema hierboven laat zien waarom je nooit hoeft te wachten met laag 1. Links staat wat nog open is, en dat is veel. Rechts staat wat je al wél weet, en dat is genoeg.</p>"
     "<p>Die vier eisen rechts zijn geen bijzaken. Uit 'moet in Brightspace draaien' volgt direct de richting 'tool om te bouwen'. Uit 'moet toegankelijk zijn' volgt de richting 'toegankelijkheid', en daar hangt bijna zeker een leerstap aan — want wie weet uit z'n hoofd wat WCAG 2.1 AA precies eist?</p>"
     "<p>Zo kom je met een half ingevuld einddoel toch bij concrete stappen voor deze week. En als het onderwerp later duidelijk wordt, vul je laag 1 aan en loop je de lagen erboven nog eens na.</p>")

block("b-204", "a-20", "Tussenvraag", classes="separator")
matching("c-204", "b-204", "In welke laag hoort dit thuis?",
         "Een groep werkt aan een campagne over textielafval. Hieronder staan vier uitspraken uit hun overleg. Zet elke uitspraak in de laag waar hij thuishoort.<br><br><i>Let op: in je eigen deconstructie schrijf je losse elementen op, geen zinnen. Deze citaten staan er alleen om te oefenen met het herkennen van de lagen.</i>",
         [
             {"text": "\"We willen een poster die studenten laat zien wat er met hun afgedankte kleding gebeurt.\"",
              "_options": laagopties("Laag 1 · Einddoel")},
             {"text": "\"Dan hebben we betrouwbare cijfers nodig, een goed beeldconcept en iemand die kan opmaken.\"",
              "_options": laagopties("Laag 2 · Richtingen")},
             {"text": "\"Niemand van ons weet hoe je een poster maakt die van vijf meter afstand leesbaar is.\"",
              "_options": laagopties("Laag 3 · Weten of kunnen")},
             {"text": "\"Sanne zoekt deze week drie posters op en we ontleden ze donderdag samen.\"",
              "_options": laagopties("Laag 4 · Concrete stappen")}
         ],
         {"title": "In welke laag hoort dit thuis?",
          "correct": "<p>Goed gezien. Let op het verschil tussen de derde en de vierde uitspraak: de derde constateert wat je niet weet, de vierde maakt daar een afspraak van met een naam en een dag erbij.</p>",
          "_incorrect": {"final": "<p>Nog niet. Loop ze na op signaalwoorden: een <i>willen</i> hoort bij het einddoel, <i>nodig hebben</i> bij richtingen, <i>niet weten</i> bij leerstappen, en een naam met een dag erbij is altijd laag 4.</p>"},
          "_partlyCorrect": {"final": "<p>Deels goed. Kijk vooral naar de laatste twee: \"niemand weet hoe\" is een constatering (laag 3), \"Sanne zoekt deze week\" is een afspraak (laag 4).</p>"}})

# ==================================================== 3 · IN BEELD
block("b-300", "a-30", "Inleiding")
text("c-300", "b-300", "Een echte deconstructie, laag voor laag",
     "<p>Tot nu toe ging het over de methode. Nu een uitgewerkt geval: een duo wil een infographic maken over voedselverspilling.</p>"
     "<p>Bekijk het schema hieronder eerst een halve minuut zonder uitleg, en probeer het van onder naar boven te lezen. Daarna leggen we het blok voor blok uit.</p>")

block("b-301", "a-30", "Het voorbeeld", classes="separator")
graphic("c-301", "b-301", "course/nl/images/deconstructie-voorbeeld.jpg",
        "Uitgewerkte deconstructie in vier lagen. Onderaan het einddoel in magenta: een infographic over hoe voedselverspilling in de keten ontstaat. Daarboven drie richtingen: kloppende inhoud, visueel ontwerp en een tool om te maken. Daarboven wat je moet weten of kunnen, met twee witte vakken die bekend zijn en twee gestippelde roze vakken gemarkeerd als nog uitzoeken. Bovenaan vier concrete stappen met het label nu, en daarboven een gestippelde balk: volgende stap, zet de concrete stappen om in scrum-taken.",
        "De gestippelde vakken zijn leerstappen: dat weet het duo nog niet. Versimpeld voorbeeld — een echte deconstructie is een stuk voller.",
        "Deconstructie van een infographic over voedselverspilling")

block("b-302", "a-30", "Laag 1 en 2")
text("c-302", "b-302", "Onderaan beginnen: het einddoel en de richtingen",
     "<p><b>Laag 1, de roze balk onderaan.</b> Het einddoel is niet \"iets met voedselverspilling\", maar een infographic die één specifieke vraag beantwoordt: hoe ontstaat voedselverspilling in de keten? Die scherpte is wat de rest bruikbaar maakt.</p>"
     "<p><b>Laag 2, de drie witte blokken erboven.</b> Wat heb je nodig om die infographic te maken? Drie dingen: de inhoud moet kloppen, er moet een visueel ontwerp zijn, en je hebt een tool nodig om hem mee te bouwen.</p>"
     "<p>Merk op dat dit een nogal saai rijtje is. Dat is goed. Richtingen horen voor de hand liggend te zijn — als je hier iets origineels bedenkt, zit je waarschijnlijk al te diep.</p>")

block("b-303", "a-30", "Laag 3", classes="separator")
text("c-303", "b-303", "De laag waar het interessant wordt",
     "<p><b>Laag 3</b> is waar deze deconstructie zijn waarde bewijst. Per richting is de vraag gesteld: wat moeten we hiervoor weten of kunnen? En daar lopen de antwoorden uiteen.</p>"
     "<p>Voor <b>kloppende inhoud</b> staan er twee witte vakken: de oorzaken per ketenfase kennen, en betrouwbare cijfers hebben. Wit betekent hier: dit kunnen we al, of we weten in elk geval hoe we eraan komen.</p>"
     "<p>Voor <b>visueel ontwerp</b> en <b>tool</b> staan gestippelde roze vakken, met het label 'nog uitzoeken'. Het duo weet niet hoe je een leesbare infographic opbouwt, en niet welke tool daarbij past. Dat zijn <b>leerstappen</b>.</p>"
     "<p>Dit is het moment waarop de meeste groepen zichzelf voor de gek houden. \"Dat ontwerpen zien we wel.\" Door het hier hardop op te schrijven, wordt het een taak in plaats van een verrassing.</p>")

block("b-304", "a-30", "Hoe je dat besluit")
graphic("c-304", "b-304", "course/nl/images/leerstap-herkennen.svg",
        "Een beslisschema. Bovenaan een richting uit laag 2, als voorbeeld visueel ontwerp. Daaronder een ruit met de vraag: weten we echt hoe dit moet? De linkertak, ja, leidt naar een vak: gewone stap, je kunt hem meteen inplannen. De rechtertak, nee, leidt naar een gestippeld vak met het label leerstap: markeer hem apart, hij gaat op je onderzoekslijst. Vanuit dat vak loopt een pijl terug naar het midden: in laag 4 wordt hij, eerst uitzoeken hoe. Onderaan staat: twijfel je, dan is het een leerstap.",
        "De hele beslissing zit in één eerlijke vraag.",
        "Hoe je een leerstap herkent")

block("b-305", "a-30", "Laag 4")
text("c-305", "b-305", "Bovenaan: wat er maandag gebeurt",
     "<p><b>Laag 4</b> bevat vier blokken met het label 'nu'. Elk daarvan is een taak die je meteen kunt oppakken.</p>"
     "<p>Let op wat er met de leerstappen is gebeurd. \"Hoe bouw je een leesbare infographic?\" — een vraag zonder antwoord — is bovenaan geworden: \"verdiepen: hoe bouw je een goede infographic?\". Van een gat in je kennis naar een taak met een tijdvak.</p>"
     "<p>Dat is de kern van de hele methode. Je zet niet alleen om wat je weet in taken, maar ook wat je níet weet.</p>"
     "<p>De gestippelde balk daarboven valt buiten de deconstructie: die vier taken gaan naar je product backlog en krijgen daar een prioriteit en een eigenaar.</p>")

block("b-306", "a-30", "Waarschuwing", classes="separator")
text("c-306", "b-306", "Let op: dit is een versimpelde versie",
     "<p>Dit voorbeeld is <b>bewust uitgekleed</b>. Het gaat over een kleine opdracht waarbij al veel bekend is, en de blokjes zijn kort gehouden zodat het schema op één beeld past. Puur als voorbeeld dus, om het patroon te laten zien.</p>"
     "<p><b>Een echte deconstructie ziet er heel anders uit.</b> Die heeft meer richtingen, veel meer leerstappen, en regelmatig een extra laag omdat één vraag nog niet genoeg was. De taken zijn er ook langer en preciezer dan de paar woorden die je hier ziet.</p>"
     "<p>Gebruik dit dus als patroon, niet als maatstaf. Ziet jouw deconstructie er na een uur werken een stuk voller uit dan deze, dan doe je het waarschijnlijk goed.</p>",
     classes="attention")

block("b-3065", "a-30", "Schema erbij", classes="separator")
graphic("c-3065", "b-3065", "course/nl/images/deconstructie-voorbeeld.jpg",
        "Dezelfde uitgewerkte deconstructie als bovenaan deze pagina. Vier lagen, met onderaan het einddoel over voedselverspilling, daarboven drie richtingen, daarboven wat je moet weten of kunnen met twee witte en twee gestippelde roze vakken, en bovenaan vier concrete stappen.",
        "Het versimpelde schema van bovenaan deze pagina, nog even bij de hand voor de vraag hieronder.",
        "Nog even terugkijken")

block("b-307", "a-30", "Tussenvraag", classes="separator")
mcq("c-307", "b-307", "Even checken",
    "Kijk naar het schema hierboven, de deconstructie van de infographic. In laag 3 staan twee vakken gestippeld en twee niet. Wat betekent dat verschil?",
    [{"text": "De gestippelde vakken zijn dingen die het duo nog niet weet en dus moet uitzoeken", "_shouldBeSelected": True},
     {"text": "De gestippelde vakken zijn optioneel en mogen weggelaten worden", "_shouldBeSelected": False},
     {"text": "De gestippelde vakken zijn minder belangrijk dan de witte", "_shouldBeSelected": False},
     {"text": "De gestippelde vakken zijn al af, de witte moeten nog gebeuren", "_shouldBeSelected": False}],
    {"title": "Even checken",
     "correct": "<p>Klopt. En juist die worden bovenaan een concrete stap: 'eerst uitzoeken hoe'. Wat je niet weet is de waardevolste opbrengst van een deconstructie.</p>",
     "_incorrect": {"final": "<p>Nee. Gestippeld betekent leerstap: dit weten we nog niet. Ze zijn niet optioneel en niet minder belangrijk — ze zijn vaak juist het risicovolste deel van je project, omdat je er nog geen grip op hebt.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Gestippeld staat voor een leerstap: iets wat nog uitgezocht moet worden.</p>"}})

# ==================================================== 4 · STAPPEN
block("b-400", "a-40", "Inleiding")
text("c-400", "b-400", "Vijf stappen, in deze volgorde",
     "<p>Hieronder staan de vijf stappen. Per stap lees je wat je doet, waaraan je merkt dat je klaar bent, en wat er meestal misgaat.</p>"
     "<p>Werk met losse post-its of kaartjes in plaats van in een document. Je gaat namelijk schuiven — een richting blijkt een leerstap, of twee blokken blijken hetzelfde. Op papier vastgeschreven ga je minder snel herzien, en dat is precies wat je hier wél moet doen.</p>")

block("b-4001", "a-40", "Overzicht", classes="separator")
graphic("c-4001", "b-4001", "course/nl/images/vijf-stappen.svg",
        "Vijf stappen onder elkaar, verbonden door een verticale lijn, met links een roze balk met het label de deconstructie die de eerste vier stappen omvat. Stap 1: schets onderaan je einddoel, klaar als iemand buiten je groep begrijpt wat er straks ligt. Stap 2: wat heb ik daarvoor nodig, klaar als je drie tot vijf elementen hebt die je niet kunt missen. Stap 3: hoe maken we dit echt goed, klaar als er minstens een leerstap staat. Stap 4: werk uit in concrete stappen, klaar als iemand anders ze zou kunnen uitvoeren zonder jou. Stap 5: zet om in scrum-taken, klaar als alles op de backlog staat met een eigenaar.",
        "Let op de roze balk links: stap 5 valt buiten de deconstructie zelf.",
        "De vijf stappen en hun stopsignaal")

STAPPEN = [
    ("Stap 1 · Schets onderaan je einddoel",
     "<p><b>Wat je doet:</b> begin met beeldvorming. Zet je einddoel onderaan en beschrijf het <b>zo uitgebreid mogelijk</b>. Niet in één zin, maar als compleet beeld: hoe het eruitziet, waar het uit bestaat, hoe iemand het gebruikt, voor wie het is, waar het moet werken, en wanneer het echt goed is.</p>""<p>Doe dit fysiek, op een bord of op tafel, in geschreven vorm. Hoe voller dit beeld, hoe meer je er in laag 2 uit kunt halen — en hoe minder je later moet gokken.</p>"
     "<p><b>Klaar als:</b> je het aan iemand buiten je groep kunt laten zien en die begrijpt wat er straks ligt, zonder dat jij erbij hoeft te praten.</p>"
     "<p><b>Gaat vaak mis:</b> blijven hangen in een onderwerp in plaats van een product. \"Circulaire mode\" is een onderwerp. \"Een keuzehulp van één pagina voor studenten die tweedehands willen kopen\" is een einddoel.</p>"),
    ("Stap 2 · Vraag: wat heb ik daarvoor nodig?",
     "<p><b>Wat je doet:</b> zet de grote richtingen of bouwstenen een laag hoger. Dit is verbreden: noem de onderdelen, nog niet de details.</p>"
     "<p><b>Klaar als:</b> je drie tot vijf blokken hebt en je bij elk kunt zeggen: zonder dit bestaat mijn einddoel niet. Kun je een blok weglaten zonder dat het einddoel sneuvelt, dan hoort het hier niet.</p>"
     "<p><b>Gaat vaak mis:</b> te diep gaan. Zodra er een werkwoord met een datum in staat, zit je in laag 4. Richtingen zijn zelfstandige naamwoorden: inhoud, ontwerp, tool.</p>"),
    ("Stap 3 · Vraag per richting: wat moet ik weten of kunnen?",
     "<p><b>Wat je doet:</b> loop je elementen één voor één langs en stel bij elk dezelfde vraag: hoe maken we dit echt goed, en wat moeten we daarvoor kunnen en weten? Schrijf het antwoord concreet op, niet als één woord.</p>""<p>Deel je antwoord op in stukken in plaats van er één zin van te maken. Per stuk: weet je hoe het moet, of niet? Dat laatste is een <b>leerstap</b>. Markeer die apart — met een andere kleur, een stippellijn of gewoon een sterretje.</p>"
     "<p><b>Klaar als:</b> je per element in stukken hebt opgedeeld wát er nodig is, en per stuk weet of je het al weet of nog moet uitzoeken. Staat er geen enkele leerstap, dan heb je niet eerlijk genoeg gekeken. Staan er álleen leerstappen, dan heb je nog niet fijn genoeg opgedeeld.</p>"
     "<p><b>Gaat vaak mis:</b> te snel \"dat weten we wel\". Gebruik het beslisschema van de vorige pagina: twijfel je, dan is het een leerstap.</p>"),
    ("Stap 4 · Werk de bovenste laag uit in concrete stappen",
     "<p><b>Wat je doet:</b> vertaal alles uit laag 3 naar acties. Een leerstap wordt hier een gewone taak die begint met uitzoeken: \"eerst uitzoeken hoe je een goede infographic maakt\".</p>"
     "<p><b>Klaar als:</b> elke stap zo concreet is dat iemand anders hem zou kunnen uitvoeren zonder jou erbij. \"Verdiepen in ontwerp\" is niet concreet. \"Drie infographics zoeken en ontleden op opbouw\" wel.</p>"
     "<p><b>Gaat vaak mis:</b> blijven vertakken. Zodra je bij uitvoerbare stappen bent, stop je. Een deconstructie is een werkkaart, geen kunstwerk.</p>"),
    ("Stap 5 · Zet de concrete stappen om in scrum-taken",
     "<p><b>Wat je doet:</b> je bovenste laag verhuist naar je product backlog. Geef elke stap een prioriteit en een eigenaar.</p>"
     "<p><b>Klaar als:</b> elke taak op de backlog staat met een naam erachter, en de eerste paar in je sprint zijn ingepland.</p>"
     "<p><b>Gaat vaak mis:</b> de leerstappen achterin laten liggen omdat ze vaag voelen. Plan juist die vroeg in: zolang ze open staan, blokkeren ze alles wat erachter komt.</p>"),
]
for i, (t, b) in enumerate(STAPPEN, start=1):
    bid = "b-4%02d" % i
    block(bid, "a-40", t, classes="separator" if i > 1 else "")
    text("c-4%02d" % i, bid, t, b)

block("b-406", "a-40", "Uitkomst", classes="separator")
text("c-406", "b-406", "Wat je aan het eind in handen hebt",
     "<p>Na deze vijf stappen liggen er twee lijsten, en die hebben elk een eigen bestemming.</p>"
     "<p><b>Je scrum-taken.</b> Dat is de bovenste laag: alle concrete stappen waarmee je nu kunt beginnen. Elk stuk uit laag 3 is hier een taak geworden — de stukken die je al kende zijn gewone taken, de leerstappen zijn uitzoektaken. Ze gaan samen op je product backlog.</p>"
     "<p><b>Je onderzoekslijst.</b> Dat zijn de leerstappen: alles wat je nog moet uitzoeken of leren voordat je verder kunt. Dit is je gerichte onderzoek — geen algemeen literatuuronderzoek, maar precies de vragen die jouw project blokkeren.</p>"
     "<p>Die tweede lijst is meestal de nuttigste opbrengst. Zonder deconstructie ontdek je die vragen ook wel, maar dan pas op het moment dat je erover struikelt.</p>")

block("b-407", "a-40", "Tussenvraag", classes="separator")
mcq("c-407", "b-407", "Even checken",
    "Je bent bij stap 3. Bij de richting 'een werkende webshop' constateert je groep dat niemand weet hoe je een betaalkoppeling regelt. Wat gebeurt daarmee in stap 4?",
    [{"text": "Het wordt een concrete stap die begint met uitzoeken, bijvoorbeeld: uitzoeken welke betaalkoppelingen er zijn en wat ze kosten", "_shouldBeSelected": True},
     {"text": "Het blijft een leerstap en komt niet in laag 4 terecht", "_shouldBeSelected": False},
     {"text": "Het verhuist naar laag 2, want het is eigenlijk een richting", "_shouldBeSelected": False},
     {"text": "Het wordt geschrapt, want je kunt niet plannen wat je niet weet", "_shouldBeSelected": False}],
    {"title": "Even checken",
     "correct": "<p>Precies. Een leerstap verdwijnt niet, hij verandert van vorm: van een gat in je kennis naar een taak met een tijdvak.</p>",
     "_incorrect": {"final": "<p>Nee. Juist leerstappen moeten in laag 4 terechtkomen — anders blijven ze onzichtbaar en kom je er pas achter als ze je blokkeren. Ze worden een taak die begint met uitzoeken.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Elke leerstap wordt in laag 4 een concrete uitzoektaak.</p>"}})

# ==================================================== 5 · VALKUILEN
block("b-500", "a-50", "Inleiding")
text("c-500", "b-500", "Vier valkuilen",
     "<p>Deze vier komen het vaakst voor. Ze lijken op het moment zelf allemaal redelijk — dat is precies waarom het valkuilen zijn.</p>")

block("b-501", "a-50", "De valkuilen")
accordion("c-501", "b-501", "Wat er in de praktijk misgaat",
          "<p>Per valkuil: hoe je hem herkent, waarom hij zo verleidelijk is, en wat je eraan doet.</p>",
          [
              {"title": "Bij de stappen beginnen in plaats van bij het einddoel",
               "body": "<p><b>Hoe je het herkent:</b> je hebt binnen tien minuten een lijst taken, en niemand heeft het over wat er straks moet liggen.</p>"
                       "<p><b>Waarom het verleidelijk is:</b> taken opschrijven voelt productief. Een einddoel scherp krijgen voelt als tijd verliezen, omdat je nog niets \"doet\".</p>"
                       "<p><b>Wat je eraan doet:</b> begin altijd onderaan. Merk je dat je in het rond aan het praten bent over taken, leg dan alles weg en schets eerst het eindproduct.</p>"},
              {"title": "Alles als bekend aannemen",
               "body": "<p><b>Hoe je het herkent:</b> je laag 3 bestaat alleen uit witte vakken. Geen enkele leerstap.</p>"
                       "<p><b>Waarom het verleidelijk is:</b> toegeven dat je iets niet weet voelt als zwakte, zeker in een nieuwe groep waar je elkaar nog niet kent.</p>"
                       "<p><b>Wat je eraan doet:</b> vraag bij elke richting hardop: weten we écht hoe dit moet, of denken we dat alleen? Twijfel telt als nee. Een deconstructie zonder leerstappen is bijna altijd een deconstructie die niet eerlijk is ingevuld.</p>"},
              {"title": "Leerstappen niet markeren",
               "body": "<p><b>Hoe je het herkent:</b> je hébt benoemd wat je niet weet, maar het staat er net zo uit te zien als al het andere.</p>"
                       "<p><b>Waarom het verleidelijk is:</b> het lijkt een opmaakdetail. Dat is het niet.</p>"
                       "<p><b>Wat je eraan doet:</b> geef leerstappen een eigen kleur, stippellijn of sterretje. Alleen zo kun je ze er later uit vissen als onderzoekslijst. Doe je dat niet, dan verdwijnen ze in de massa en kom je er pas laat achter.</p>"},
              {"title": "Blijven vertakken",
               "body": "<p><b>Hoe je het herkent:</b> je zit een uur later nog te tekenen en er komen lagen bij, maar er staat nog geen enkele taak die je maandag kunt doen.</p>"
                       "<p><b>Waarom het verleidelijk is:</b> het schema wordt steeds mooier en completer, en dat voelt als vooruitgang.</p>"
                       "<p><b>Wat je eraan doet:</b> stop een laag zodra je bij concrete stappen bent. Een deconstructie is een <b>werkkaart, geen kunstwerk</b>. Hij mag rommelig zijn — hij moet alleen bruikbaar zijn.</p>"}
          ])

block("b-5011", "a-50", "Werkkaart of kunstwerk", classes="separator")
graphic("c-5011", "b-5011", "course/nl/images/werkkaart-vs-kunstwerk.svg",
        "Twee deconstructies naast elkaar. Links een kunstwerk: zeven lagen met veel kleine grijze blokjes, netjes en symmetrisch, met daaronder in rood de constatering dat er bovenaan geen enkele taak staat die je maandag kunt oppakken. Rechts een werkkaart: vier lagen met twee gemarkeerde leerstappen en bovenaan drie concrete taken, met daaronder in groen dat er drie taken voor deze week staan en twee zichtbare leerstappen.",
        "Links is mooier. Rechts is bruikbaar.",
        "Werkkaart tegenover kunstwerk")

block("b-5012", "a-50", "Uitleg werkkaart")
text("c-5012", "b-5012", "Waarom de linkerkant fout is",
     "<p>De linker deconstructie ziet er beter uit. Hij is symmetrisch, netjes uitgelijnd en er is duidelijk lang aan gewerkt. Precies daarom is hij mislukt.</p>"
     "<p>Tel de blokjes bovenaan: allemaal even groot, allemaal even vaag. Er staat geen enkele taak bij die iemand maandag kan oppakken. Alle energie is in het schema gaan zitten in plaats van in de vraag die het schema moest beantwoorden.</p>"
     "<p>De rechter is rommeliger en kleiner, maar levert wat je nodig hebt: drie taken voor deze week, en twee zichtbaar gemarkeerde leerstappen. Daar kun je morgen mee aan de slag.</p>")

block("b-502", "a-50", "Tips", classes="separator")
text("c-502", "b-502", "Twee dingen die het makkelijker maken",
     "<p><b>Werk met losse post-its of kaartjes.</b> Je gaat schuiven: blokken verhuizen tussen lagen, en soms voeg je er een laag tussen. Op een whiteboard of tafel gaat dat vanzelf. In een document ga je onbewust vasthouden aan wat er al staat.</p>"
     "<p><b>Begin echt onderaan.</b> De verleiding is groot om meteen aan stappen te denken — dat is waar je hoofd naartoe wil. Maar de kracht van deze methode zit in eerst je einddoel en richtingen scherp krijgen. De stappen rollen er daarna vanzelf uit, en ze kloppen dan ook nog.</p>")

block("b-503", "a-50", "Tussenvraag", classes="separator")
mcq("c-503", "b-503", "Even checken",
    "Een groep is anderhalf uur bezig. Het schema heeft inmiddels zes lagen en ziet er indrukwekkend uit, maar er staat nog geen taak op die deze week uitgevoerd kan worden. Welke valkuil is dit?",
    [{"text": "Blijven vertakken — het is een kunstwerk geworden in plaats van een werkkaart", "_shouldBeSelected": True},
     {"text": "Bij de stappen beginnen in plaats van bij het einddoel", "_shouldBeSelected": False},
     {"text": "Alles als bekend aannemen", "_shouldBeSelected": False},
     {"text": "Leerstappen niet markeren", "_shouldBeSelected": False}],
    {"title": "Even checken",
     "correct": "<p>Klopt. Zodra je bij uitvoerbare stappen bent, stop je. Meer lagen maken een deconstructie niet beter, alleen groter.</p>",
     "_incorrect": {"final": "<p>Nee. Ze zijn wél onderaan begonnen en hebben wél doorgedacht — het probleem is dat ze niet gestopt zijn. Een deconstructie is af zodra er taken staan die je maandag kunt oppakken.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Let op het signaal: veel lagen, geen uitvoerbare taken.</p>"}})

# ==================================================== 6 · MINI-VOORBEELD
block("b-600", "a-60", "Inleiding")
text("c-600", "b-600", "Een tweede geval, van begin tot eind",
     "<p>Het eerste voorbeeld ging over een infographic. Dit gaat over iets heel anders — een webpagina — zodat je het patroon leert herkennen los van het onderwerp.</p>"
     "<p><b>De opdracht:</b> een opdrachtgever in de bouw wil weten welk circulair isolatiemateriaal hij moet kiezen. Twee studenten gaan daarmee aan de slag.</p>")

block("b-601", "a-60", "Het schema", classes="separator")
graphic("c-601", "b-601", "course/nl/images/mini-voorbeeld.svg",
        "Deconstructie in vier lagen van een vergelijkingspagina. Onderaan in magenta het einddoel: een webpagina die drie circulaire isolatiematerialen vergelijkt. Daarboven drie richtingen naast elkaar: kloppende vergelijking, helder pagina-ontwerp, en manier om te bouwen. Daarboven per richting wat je moet weten of kunnen: links een wit vak met deels bekend over criteria en data, in het midden en rechts twee gestippelde roze vakken gemarkeerd als leerstap. Bovenaan drie concrete stappen voor deze week. Daarboven een gestippelde balk: deze drie stappen gaan naar de product backlog, de eerste twee in sprint 1.",
        "Zelfde patroon, ander project. Ook dit is een versimpelde weergave van een kleine opdracht.",
        "Deconstructie van een vergelijkingspagina")

block("b-602", "a-60", "Laag 1")
text("c-602", "b-602", "Laag 1 · Het einddoel",
     "<p><b>Een webpagina die drie circulaire isolatiematerialen vergelijkt voor de opdrachtgever.</b></p>"
     "<p>Let op drie keuzes die hier al gemaakt zijn. Het is een <i>webpagina</i>, geen rapport — dus er moet iets gebouwd worden. Het gaat om <i>drie</i> materialen, niet om alle — dus er moet gekozen worden. En het is <i>voor de opdrachtgever</i>, niet voor studenten — dus de toon en het detailniveau liggen daarmee vast.</p>"
     "<p>Elk van die drie keuzes bepaalt straks een richting. Was het einddoel \"iets over isolatie\" gebleven, dan was laag 2 een gokje geweest.</p>")

block("b-603", "a-60", "Laag 2", classes="separator")
text("c-603", "b-603", "Laag 2 · De richtingen",
     "<p>Wat heb je nodig voor zo'n pagina? Drie dingen, en meer niet:</p>"
     "<p><b>Een kloppende vergelijking.</b> Als de inhoud niet deugt, is de rest zinloos.</p>"
     "<p><b>Een helder pagina-ontwerp.</b> Een vergelijking van drie materialen op tien criteria wordt een brij als je hem niet goed opbouwt.</p>"
     "<p><b>Een manier om te bouwen.</b> Het moet een werkende pagina worden, en geen van beide studenten programmeert.</p>"
     "<p>Deze drie zijn niet origineel, en dat hoeft ook niet. Test ze met de vraag uit stap 2: haal er één weg, en het einddoel sneuvelt. Dat klopt bij alle drie.</p>")

block("b-604", "a-60", "Laag 3", classes="separator")
text("c-604", "b-604", "Laag 3 · Wat moeten we daarvoor weten of kunnen?",
     "<p>Nu per richting de eerlijke vraag. Kijk mee met het schema hierboven — één vak is wit, twee zijn gestippeld.</p>"
     "<p><b>Kloppende vergelijking → deels bekend.</b> Ze weten hoe je bronnen op betrouwbaarheid checkt. Maar welke criteria je vergelijkt (isolatiewaarde? prijs? herkomst? levensduur? recyclebaarheid?) ligt nog niet vast, en betrouwbare cijfers per materiaal hebben ze nog niet. Deels bekend dus: het gereedschap is er, het materiaal nog niet.</p>"
     "<p><b>Helder pagina-ontwerp → leerstap.</b> Geen van beiden heeft ooit een vergelijkingspagina opgebouwd. Hoe zorg je dat iemand in één blik ziet welk materiaal waarop wint? Dat weten ze niet.</p>"
     "<p><b>Manier om te bouwen → leerstap.</b> Ze kunnen niet programmeren, en weten niet welke tool je gebruikt om zonder code een nette pagina te maken.</p>"
     "<p>Twee van de drie richtingen zijn dus leerstappen. Dat is veel, en het is goed dat ze dat nú weten in plaats van over drie weken.</p>")

block("b-605", "a-60", "Laag 4", classes="separator")
text("c-605", "b-605", "Laag 4 · Wat we deze week doen",
     "<p>Elke uitkomst uit laag 3 wordt een taak. Let op hoe de twee leerstappen veranderen in gewone uitzoektaken:</p>"
     "<p><b>1. Drie materialen en de vergelijkingscriteria kiezen, daarna per materiaal data opzoeken en checken.</b> Dit komt uit het witte vak. De criteria eerst, want zonder criteria weet je niet welke data je zoekt.</p>"
     "<p><b>2. Ons verdiepen in de opbouw van een vergelijkingspagina: drie goede voorbeelden zoeken en ontleden.</b> Dit was de leerstap over ontwerp. Merk op dat de taak concreet is gemaakt — niet \"verdiepen in ontwerp\", maar drie voorbeelden zoeken en ontleden. Daar kun je donderdag klaar mee zijn.</p>"
     "<p><b>3. Een tool kiezen en de mini-briefing invullen.</b> Dit was de leerstap over bouwen. Er bestaat al een hulpmiddel voor, dus de taak is: dat hulpmiddel gebruiken.</p>")

block("b-606", "a-60", "Naar scrum", classes="separator")
text("c-606", "b-606", "En dan naar de backlog",
     "<p>Deze drie stappen gaan op de product backlog. De eerste twee worden in sprint 1 gepland, de derde volgt zodra duidelijk is hoe de pagina eruit moet zien.</p>"
     "<p><b>Kijk nog één keer naar de verhouding.</b> Twee van de drie taken voor deze week zijn uitzoekwerk. Voor een groep die \"gewoon even een pagina wilde maken\" voelt dat als vertraging.</p>"
     "<p>Dat is het niet. Zonder deze deconstructie waren ze maandag begonnen met data verzamelen, hadden ze in week drie ontdekt dat ze niet wisten hoe ze het moesten presenteren, en in week vier dat ze het niet konden bouwen. Nu staat dat allemaal in week één op de planning.</p>",
     classes="attention")

block("b-6065", "a-60", "Versimpeld", classes="separator")
text("c-6065", "b-6065", "Ook dit voorbeeld is versimpeld",
     "<p>Net als het vorige is dit een <b>uitgeklede versie</b>: een overzichtelijke opdracht waarbij al veel bekend was, met korte blokjes zodat alles op één schema past.</p>"
     "<p>In werkelijkheid zou dit duo bij laag 2 waarschijnlijk op vijf of zes elementen uitkomen — denk aan de afstemming met de opdrachtgever, de bronvermelding, en hoe de pagina straks onderhouden wordt. En bij laag 3 zouden er bij elk element meerdere regels staan in plaats van één.</p>"
     "<p>De voorbeelden laten het <b>patroon</b> zien: waar je begint, hoe de lagen uit elkaar volgen, en hoe een leerstap bovenaan een taak wordt. Ze laten niet zien hoe vol je eigen deconstructie hoort te worden.</p>",
     classes="attention")

block("b-607", "a-60", "Tussenvraag", classes="separator")
mcq("c-607", "b-607", "Even checken",
    "In dit voorbeeld is 'kloppende vergelijking' als deels bekend gemarkeerd, en niet als volledige leerstap. Waarom?",
    [{"text": "Ze weten wél hoe je bronnen checkt, maar de criteria en de data zelf hebben ze nog niet", "_shouldBeSelected": True},
     {"text": "Omdat inhoud altijd minder belangrijk is dan ontwerp en techniek", "_shouldBeSelected": False},
     {"text": "Omdat een richting nooit helemaal een leerstap kan zijn", "_shouldBeSelected": False},
     {"text": "Omdat ze de data al verzameld hadden voordat ze begonnen", "_shouldBeSelected": False}],
    {"title": "Even checken",
     "correct": "<p>Precies. Het gereedschap is er, het materiaal nog niet. Daarom staat er in laag 4 ook een taak voor: criteria kiezen en data checken.</p>",
     "_incorrect": {"final": "<p>Nee. Een richting kan prima deels bekend zijn: je hebt de vaardigheid al, maar de invulling nog niet. Hier weten ze hoe je bronnen checkt, maar welke criteria ze vergelijken en welke cijfers erbij horen moeten ze nog uitzoeken.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Kijk naar het onderscheid tussen kunnen en hebben.</p>"}})

# ==================================================== 6b · OEFENING
block("b-650", "a-65", "Opdracht")
text("c-650", "b-650", "De opdracht",
     "<p>Tijd om het zelf te doen, op iets wat losstaat van je eigen project. Dat is bewust: op een vreemd onderwerp vallen eigen aannames sneller op.</p>"
     "<p><b>Deconstrueer dit einddoel: een eigen 30 seconds-kaartspel maken.</b> Een doos met kaarten, waarbij het team in dertig seconden vijf begrippen moet raden zonder dat het woord zelf mag vallen.</p>"
     "<p>Klinkt overzichtelijk. Dat is het niet. Zodra je gaat ontleden kom je uit op begrippenkeuze, moeilijkheidsgraad, categorieën, aantal kaarten, spelregels, de zandloper, het scoresysteem, de doos, drukwerk, testspelen. En bij elk van die elementen weer: hoe maken we dit <i>echt goed</i>, en wat moeten we daarvoor weten?</p>")

block("b-651", "a-65", "Aanpak", classes="separator")
text("c-651", "b-651", "Zo pak je het aan",
     "<p><b>Werk eerst fysiek.</b> Pak post-its of een vel papier en bouw de deconstructie van onder naar boven op tafel. Vul de velden hieronder daarna in als uitwerking — niet andersom. Op tafel kun je schuiven, en dat ga je nodig hebben.</p>"
     "<p><b>Vul zoveel mogelijk in.</b> Er staan bewust veel velden. Als je er maar drie gevuld krijgt, ben je nog niet klaar met ontleden. Bij een spel als dit hoort elke laag vol te lopen.</p>"
     "<p><b>Blijf niveau-verhogend denken.</b> Niet \"hoe krijgen we een stapel kaarten af\", maar \"hoe maken we een spel dat mensen een tweede keer willen spelen — en wat moeten we daarvoor weten?\"</p>"
     "<p><b>Laat hem daarna checken door je coach.</b> Gebruik de kopieerknop onderaan en neem je uitwerking mee naar je begeleidingsgesprek.</p>",
     classes="attention")

block("b-6515", "a-65", "De ketting", classes="separator")
text("c-6515", "b-6515", "Elke laag komt uit de laag eronder",
     "<p>Voordat je begint, het belangrijkste van deze oefening: <b>de lagen staan niet los van elkaar</b>. Je verzint per laag niets nieuws — je haalt hem uit de laag eronder.</p>"
     "<p><b>Laag 1 is je schets.</b> Breed, rommelig, alles wat je al voor je ziet. Hoe het spel eruitziet, hoe je het speelt, wie het speelt, hoe lang, wat het moet kosten, hoe goed het moet zijn.</p>"
     "<p><b>Laag 2 haal je uit die schets.</b> Je leest je eigen schets terug en streept de onderdelen aan die erin zitten. Schreef je \"je raadt begrippen in dertig seconden\", dan zitten daar de elementen <i>begrippen</i> en <i>tijdmechanisme</i> in.</p>"
     "<p><b>Laag 3 gaat over de elementen uit laag 2.</b> Je pakt ze één voor één en stelt bij elk dezelfde vraag: hoe maken we dit echt goed, en wat moeten we daarvoor weten?</p>"
     "<p><b>Laag 4 komt uit laag 3.</b> Elke leerstap wordt een taak die begint met uitzoeken.</p>"
     "<p>Loop je bij een laag vast, dan is dat vrijwel altijd een teken dat de laag eronder te dun is. Ga dan terug naar beneden.</p>",
     classes="attention")

block("b-652", "a-65", "Oefening laag 1", classes="separator")
canvas("c-652", "b-652", "Laag 1 · Einddoel",
       "<p><b>Begin hier.</b> Schets het spel zo breed mogelijk: hoe ziet het eruit, wat zit erin, hoe speel je het, voor wie is het, hoe lang duurt het, wanneer is het goed? Alles wat je al voor je ziet mag erin — dit is geen lijstje eisen maar een beeld.</p>"
       "<p>Hoe voller je hier bent, hoe meer je straks uit laag 2 kunt halen.</p>",
       [("oef-l1-1", "Hoe ziet het eruit", "Een doos met... kaarten van... met daarop..."),
        ("oef-l1-2", "Hoe speel je het", "Je pakt een kaart, en dan..."),
        ("oef-l1-3", "Voor wie en met hoeveel", "Bijvoorbeeld: 4 tot 8 spelers vanaf 12 jaar"),
        ("oef-l1-4", "Hoe lang en hoe vaak", "Bijvoorbeeld: 20 minuten, en je wilt het vaker spelen"),
        ("oef-l1-5", "Wanneer is het goed", "Waaraan merk je dat dit spel gelukt is?"),
        ("oef-l1-6", "Wat weet je verder al", "Alles wat hierboven nog niet stond")])

block("b-653", "a-65", "Oefening laag 2", classes="separator")
canvas("c-653", "b-653", "Laag 2 · Richtingen",
       "<p><b>Lees je schets hierboven terug</b> en haal er de onderdelen uit. Niet nieuw bedenken — aanstrepen wat er al staat.</p>"
       "<p>Schreef je bij laag 1 iets over raden binnen dertig seconden? Dan zitten daar minstens twee elementen in: de begrippen, en iets wat de tijd bijhoudt. Losse elementen van twee tot vier woorden.</p>",
       [("oef-l2-1", "Element 1", "Welk onderdeel zit er in je schets?"),
        ("oef-l2-2", "Element 2", "Welk onderdeel zit er in je schets?"),
        ("oef-l2-3", "Element 3", "Welk onderdeel zit er in je schets?"),
        ("oef-l2-4", "Element 4", "Kijk ook naar het fysieke: doos, kaarten, timer"),
        ("oef-l2-5", "Element 5", "Kijk ook naar de regels en het scoresysteem"),
        ("oef-l2-6", "Element 6", "Kijk ook naar testen en verbeteren"),
        ("oef-l2-7", "Element 7", "Er zit er vaak nog eentje in die je nu overslaat")])

block("b-654", "a-65", "Oefening laag 3", classes="separator")
canvas("c-654", "b-654", "Laag 3 · Hoe maken we dit echt goed?",
       "<p><b>Pak je elementen uit laag 2 één voor één.</b> Stel bij elk dezelfde vraag: hoe maken we dit echt goed, en wat moeten we daarvoor kunnen en weten?</p>"
       "<p><b>Deel je antwoord op in stukken</b> in plaats van er één zin van te maken. Bovenin de stukken waarvan je weet wat er moet gebeuren, onderin de leerstappen die je nog moet uitzoeken.</p>""<p>Zet er het element bij waar je antwoord over gaat, zodat de ketting zichtbaar blijft.</p>",
       [("oef-l3-1", "Element 1 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("oef-l3-2", "Element 2 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("oef-l3-3", "Element 3 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("oef-l3-4", "Element 4 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("oef-l3-5", "Leerstap 1", "Dit weten we nog niet, hoort bij element..."),
        ("oef-l3-6", "Leerstap 2", "Dit weten we nog niet, hoort bij element..."),
        ("oef-l3-7", "Leerstap 3", "Dit weten we nog niet, hoort bij element...")])

block("b-655", "a-65", "Oefening laag 4", classes="separator")
canvas("c-655", "b-655", "Laag 4 · Concrete stappen",
       "<p><b>Maak van elke leerstap uit laag 3 een taak.</b> Beginnend met uitzoeken, zo concreet dat iemand anders hem kan uitvoeren. Wat al bekend was uit laag 3 wordt hier gewoon een taak.</p>",
       [("oef-l4-1", "Stap 1", "Uit leerstap 1: eerst uitzoeken hoe..."),
        ("oef-l4-2", "Stap 2", "Uit leerstap 2: eerst uitzoeken hoe..."),
        ("oef-l4-3", "Stap 3", "Uit leerstap 3: eerst uitzoeken hoe..."),
        ("oef-l4-4", "Stap 4", "Een taak die uit het bekende deel volgt"),
        ("oef-l4-5", "Stap 5", "Een taak die uit het bekende deel volgt")])

block("b-656", "a-65", "Oefening meenemen", classes="separator")
text("c-656", "b-656", "Neem je oefening mee naar je coach",
     "<p>Kopieer je uitwerking en neem hem mee naar je begeleidingsgesprek. Vraag je coach vooral naar twee dingen: welke elementen je gemist hebt in laag 2, en of je leerstappen echt leerstappen zijn of verkapte aannames.</p>"
     "<div class=\"canvas-acties\">"
     "<button type=\"button\" class=\"btn-canvas js-canvas-kopieren\">Kopieer als tekst</button> "
     "<button type=\"button\" class=\"btn-canvas btn-canvas--stil js-canvas-wissen\">Wis deze oefening</button>"
     "<span class=\"canvas-melding js-canvas-melding\" role=\"status\" aria-live=\"polite\"></span>"
     "</div>")

block("b-657", "a-65", "Hulp", classes="separator")
accordion("c-657", "b-657", "Vastgelopen? Klap open voor hulp",
          "<p>Probeer het eerst zelf. Deze hints zijn er voor als je er echt niet uit komt.</p>",
          [
              {"title": "Ik kom niet verder dan drie elementen in laag 2",
               "body": "<p>Loop het spel na alsof je het speelt. Je pakt een doos, haalt kaarten eruit, leest een regel, zet een timer, roept begrippen, houdt de score bij. Elk werkwoord in die zin wijst naar een element.</p>"
                       "<p>Denk daarnaast aan wat er omheen zit: de selectie van begrippen, de verdeling over moeilijkheidsgraden, het testen met echte spelers, en de fysieke productie.</p>"},
              {"title": "Alles voelt als iets wat we wel kunnen",
               "body": "<p>Dan leg je de lat op af, niet op goed. Vraag het scherper: hoe zorg je dat de begrippen niet te makkelijk en niet te moeilijk zijn? Hoe weet je dat de speelduur klopt? Hoe voorkom je dat de ene ronde veel zwaarder is dan de andere?</p>"
                       "<p>Dat zijn ontwerpvragen met echte antwoorden, en vrijwel niemand kent die uit z'n hoofd. Dus: leerstap.</p>"},
              {"title": "Waar zit het meeste verborgen werk?",
               "body": "<p>Bij de begrippen en bij het testen. De begrippenlijst bepaalt of het spel leuk is, en die maak je niet in een middag. Testspelen met echte mensen is de enige manier om te weten of de balans klopt — en dat vergeet bijna iedereen op te nemen in laag 2.</p>"}
          ])

# ==================================================== 7 · KENNISCHECK
block("b-700", "a-70", "Intro")
text("c-700", "b-700", "Vijf vragen",
     "<p>Vijf situaties uit de praktijk. Beantwoord ze één voor één; na elke vraag kun je doorgaan naar de volgende. Je uitslag verschijnt onderaan zodra je alle vijf hebt ingestuurd.</p>"
     "<p>Je hebt 75% nodig om te slagen, en je mag het zo vaak proberen als je wilt.</p>")

block("b-701", "a-70", "Vraag 1", classes="separator")
mcq("c-701", "b-701", "Vraag 1 · Waar begin je?",
    "Je groep start een nieuw project en pakt de post-its erbij. Waar plak je het eerste blok?",
    [{"text": "Onderaan: het eindproduct dat je wilt opleveren", "_shouldBeSelected": True},
     {"text": "Bovenaan: de eerste taak die je deze week gaat doen", "_shouldBeSelected": False},
     {"text": "In het midden: het onderwerp waar het project over gaat", "_shouldBeSelected": False},
     {"text": "Bovenaan: de deadline die de opdrachtgever heeft gesteld", "_shouldBeSelected": False}],
    {"title": "Vraag 1",
     "correct": "<p>Goed. Alles wat daarboven komt, volgt uit dat ene blok.</p>",
     "_incorrect": {"final": "<p>Onjuist. Je begint altijd onderaan met je einddoel. Een onderwerp in het midden is een mindmap, en beginnen bij taken of deadlines bovenaan is precies wat deze methode wil voorkomen.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Onderaan, bij het eindproduct.</p>"}})

block("b-702", "a-70", "Vraag 2", classes="separator")
matching("c-702", "b-702", "Vraag 2 · In welke laag hoort het?",
         "Een groep maakt een keuzehulp voor duurzaam reizen. Zet elke uitspraak uit hun overleg in de juiste laag.",
         [
             {"text": "\"Uiteindelijk moet er een keuzehulp liggen die reizigers helpt kiezen tussen trein, bus en vliegtuig.\"",
              "_options": laagopties("Laag 1 · Einddoel")},
             {"text": "\"Daar hebben we CO2-cijfers voor nodig, een rekenmodel en een manier om het te tonen.\"",
              "_options": laagopties("Laag 2 · Richtingen")},
             {"text": "\"We hebben geen idee waar je betrouwbare CO2-cijfers per vervoermiddel vandaan haalt.\"",
              "_options": laagopties("Laag 3 · Weten of kunnen")},
             {"text": "\"Tim zoekt woensdag drie bronnen met CO2-cijfers en vergelijkt ze op methode.\"",
              "_options": laagopties("Laag 4 · Concrete stappen")}
         ],
         {"title": "Vraag 2",
          "correct": "<p>Goed. Je herkent de lagen aan het soort zin: een wens, een behoefte, een gebrek aan kennis, en een afspraak.</p>",
          "_incorrect": {"final": "<p>Onjuist. Let op de signaalwoorden: \"uiteindelijk moet er liggen\" is laag 1, \"nodig hebben\" is laag 2, \"geen idee hoe\" is laag 3, en een naam met een dag erbij is laag 4.</p>"},
          "_partlyCorrect": {"final": "<p>Deels goed. Het lastigste verschil zit tussen laag 3 en 4: laag 3 constateert dat je iets niet weet, laag 4 maakt daar een afspraak van.</p>"}})

block("b-703", "a-70", "Vraag 3", classes="separator")
mcq("c-703", "b-703", "Vraag 3 · Welke twee zijn leerstappen?",
    "Een groep vult laag 3 in voor een project over circulair meubilair. Welke twee uitspraken zijn leerstappen?",
    [{"text": "\"We weten niet hoe je de levensduur van een meubelstuk onderbouwt.\"", "_shouldBeSelected": True},
     {"text": "\"Niemand van ons heeft ooit een prototype in 3D getekend.\"", "_shouldBeSelected": True},
     {"text": "\"We hebben een werkende website nodig om het te laten zien.\"", "_shouldBeSelected": False},
     {"text": "\"Lisa maakt vrijdag de eerste schets van het ontwerp.\"", "_shouldBeSelected": False}],
    {"title": "Vraag 3",
     "correct": "<p>Goed. Een leerstap is altijd een gebrek aan kennis of vaardigheid — niet een behoefte en niet een afspraak.</p>",
     "_incorrect": {"final": "<p>Onjuist. \"Een werkende website nodig hebben\" is een richting (laag 2), en \"Lisa maakt vrijdag een schets\" is een concrete stap (laag 4). Alleen de twee uitspraken over niet weten en nooit gedaan hebben zijn leerstappen.</p>"},
     "_partlyCorrect": {"final": "<p>Eén goed. Zoek naar de zinnen die gaan over iets níet weten of kunnen — niet over iets nodig hebben of afspreken.</p>"}},
    multi=True)

block("b-704", "a-70", "Vraag 4", classes="separator")
mcq("c-704", "b-704", "Vraag 4 · Wanneer stop je?",
    "Wanneer is een deconstructie af?",
    [{"text": "Als de bovenste laag bestaat uit taken die iemand deze week kan oppakken", "_shouldBeSelected": True},
     {"text": "Als er geen leerstappen meer over zijn", "_shouldBeSelected": False},
     {"text": "Als je alle vier de lagen minstens vijf blokken hebt gegeven", "_shouldBeSelected": False},
     {"text": "Als het schema er verzorgd genoeg uitziet om te delen met de opdrachtgever", "_shouldBeSelected": False}],
    {"title": "Vraag 4",
     "correct": "<p>Goed. Uitvoerbare stappen zijn het stopsignaal. Een deconstructie is een werkkaart, geen kunstwerk.</p>",
     "_incorrect": {"final": "<p>Onjuist. Leerstappen hóren te blijven staan — die worden juist taken. Er is ook geen minimum aantal blokken, en hoe het eruitziet doet niet ter zake. Je stopt zodra de bovenste laag uitvoerbaar is.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Het stopsignaal is: de bovenste laag is uitvoerbaar.</p>"}})

block("b-705", "a-70", "Vraag 5", classes="separator")
mcq("c-705", "b-705", "Vraag 5 · Wat gaat hier mis?",
    "Een groep laat hun deconstructie zien. Laag 3 bestaat volledig uit uitspraken als \"dat kunnen we wel\" en \"dat regelen we onderweg\". Er staat geen enkele leerstap. Wat is hier het probleem?",
    [{"text": "Wat ze niet weten blijft onzichtbaar, dus komt het pas boven als het hen blokkeert", "_shouldBeSelected": True},
     {"text": "Er is niets mis: een deconstructie zonder leerstappen betekent dat de groep goed voorbereid is", "_shouldBeSelected": False},
     {"text": "Ze zijn bij de verkeerde laag begonnen", "_shouldBeSelected": False},
     {"text": "Ze hebben te veel richtingen benoemd in laag 2", "_shouldBeSelected": False}],
    {"title": "Vraag 5",
     "correct": "<p>Precies. De onderzoekslijst blijft leeg, en dat is bijna nooit omdat er niets uit te zoeken valt — het is omdat er niet eerlijk gekeken is.</p>",
     "_incorrect": {"final": "<p>Onjuist. Een lege onderzoekslijst is een waarschuwingssignaal, geen goed teken. Bij een project dat de moeite waard is, zijn er altijd dingen die je nog niet weet. Blijven die onbenoemd, dan struikel je er later over.</p>"},
     "_partlyCorrect": {"final": "<p>Nog niet. Het probleem zit in de lege onderzoekslijst.</p>"}})

block("b-710", "a-71", "Uitslag")
components.append({
    "_id": "c-710", "_parentId": "b-710", "_type": "component",
    "_component": "assessmentResults", "_classes": "", "_layout": "full",
    "title": "Je resultaat", "displayTitle": "Je resultaat",
    "body": "Je uitslag verschijnt hier zodra je alle vijf de vragen hebt ingestuurd.",
    "instruction": "",
    "_assessmentId": "kennischeck",
    "_setCompletionOn": "inview",
    "_isVisibleBeforeCompletion": False,
    "_resetType": "inherit",
    "_completionBody": "Je score: <b>{{{score}}} van de {{{maxScore}}}</b> ({{{scoreAsPercent}}}%).<br>{{{feedback}}}",
    "_retry": {"button": "Opnieuw proberen",
               "feedback": "Je mag het zo vaak proberen als je wilt.",
               "_routeToAssessment": True},
    "_bands": [
        {"_score": 0,
         "feedback": "Dat is nog niet voldoende. Loop <b>De vier lagen</b> en <b>Valkuilen en tips</b> nog eens door — daar zit het meeste wat hier gevraagd wordt — en probeer het daarna opnieuw.",
         "_allowRetry": True},
        {"_score": 75,
         "feedback": "Voldoende. Je herkent de lagen en weet wanneer je stopt. Door naar het canvas: daar pas je de methode toe op je eigen project.",
         "_allowRetry": True}
    ]
})

# ==================================================== 8 · CANVAS
block("b-800", "a-80", "Inleiding")
text("c-800", "b-800", "Vul je eigen deconstructie in",
     "<p>Nu je eigen project. Bouw van onder naar boven: begin bij laag 1 en werk omhoog naar laag 4. Wat je typt wordt vanzelf bewaard.</p>"
     "<p>Er is geen goed of fout. Dit is jouw werkkaart, en je mag hem zo vaak herzien als je wilt — dat is juist de bedoeling. Loop je vast bij een laag, kijk dan terug naar het <b>mini-voorbeeld</b>: daar staat elke laag uitgeschreven.</p>")

block("b-801", "a-80", "Opslag", classes="separator")
text("c-801", "b-801", "Waar blijft dit?",
     "<p>Wat je typt wordt bewaard in <b>deze browser op dit apparaat</b>. Op een andere computer staat het er niet, en bij het wissen van je browsergegevens verdwijnt het.</p>"
     "<p>Gebruik daarom de knop <b>Kopieer als tekst</b> onderaan zodra je klaar bent, en plak je deconstructie in je projectmap.</p>",
     classes="attention")

block("b-802", "a-80", "Laag 1", classes="separator")
canvas("c-802", "b-802", "Laag 1 · Einddoel",
       "<p><b>Beschrijf het beeld zo uitgebreid mogelijk.</b> Dit is de laag waar je de meeste tijd in stopt, en het is geen lijstje eisen maar een compleet beeld van wat er straks ligt.</p>"
       "<p>Hoe ziet het eruit, waar bestaat het uit, hoe gebruikt iemand het, voor wie is het, waar moet het werken, wat mag het kosten, hoe lang duurt het, wanneer is het gelukt? Alles wat je nu al voor je ziet hoort hier.</p>"
       "<p>Er staan bewust veel velden. Krijg je ze niet vol, dan is je beeld nog te vaag — en dan valt er in laag 2 straks niets uit te halen.</p>",
       [("laag1-wat", "Wat is het", "Wat lever je op? Een product, geen onderwerp"),
        ("laag1-uiterlijk", "Hoe ziet het eruit", "Vorm, formaat, omvang, opbouw"),
        ("laag1-onderdelen", "Waar bestaat het uit", "Welke delen zie je nu al voor je?"),
        ("laag1-gebruik", "Hoe gebruikt iemand het", "Wat doet iemand ermee, stap voor stap"),
        ("laag1-voorwie", "Voor wie is het", "Doelgroep, opdrachtgever, situatie"),
        ("laag1-waar", "Waar moet het werken", "Platform, plek, omstandigheden"),
        ("laag1-grenzen", "Grenzen en randvoorwaarden", "Tijd, budget, techniek, regels"),
        ("laag1-goed", "Wanneer is het echt goed", "Waaraan merk je dat het gelukt is?"),
        ("laag1-rest", "Wat je verder al ziet", "Alles wat hierboven nog niet paste")])

block("b-803", "a-80", "Laag 2", classes="separator")
canvas("c-803", "b-803", "Laag 2 · Richtingen",
       "<p><b>Lees je schets hierboven terug en streep de onderdelen aan.</b> Je verzint hier niets nieuws — je haalt eruit wat er al staat. Losse elementen van twee tot vier woorden.</p>"
       "<p>Denk niet alleen aan het zichtbare product, maar ook aan wat eromheen hoort: inhoud, vorm, techniek, testen, afstemming met je opdrachtgever, oplevering.</p>",
       [("laag2-el-1", "Element 1", "Welk onderdeel zit er in je schets?"),
        ("laag2-el-2", "Element 2", "Welk onderdeel zit er in je schets?"),
        ("laag2-el-3", "Element 3", "Welk onderdeel zit er in je schets?"),
        ("laag2-el-4", "Element 4", "Welk onderdeel zit er in je schets?"),
        ("laag2-el-5", "Element 5", "Denk aan de inhoud"),
        ("laag2-el-6", "Element 6", "Denk aan de vorm of het ontwerp"),
        ("laag2-el-7", "Element 7", "Denk aan techniek of gereedschap"),
        ("laag2-el-8", "Element 8", "Denk aan testen, afstemmen, opleveren")])

block("b-804", "a-80", "Laag 3", classes="separator")
canvas("c-804", "b-804", "Laag 3 · Hoe maken we dit echt goed?",
       "<p><b>Pak elk element uit laag 2 apart</b> en stel er dezelfde vraag bij: hoe maken we dit echt goed, en wat moeten we daarvoor kunnen en weten? Niet hoe je het áf krijgt — hoe je het <i>goed</i> krijgt.</p>"
       "<p><b>Deel op in stukken.</b> Maak er geen één zin van maar benoem de losse dingen die nodig zijn. Hoe fijner je hier opdeelt, hoe makkelijker laag 4 wordt.</p>""<p>Bovenin zet je de stukken waarvan je weet wat er moet gebeuren. Onderin de <b>leerstappen</b>: wat je nog moet uitzoeken. Zet er telkens bij over welk element het gaat, zodat de ketting zichtbaar blijft.</p>",
       [("laag3-w-1", "Element 1 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("laag3-w-2", "Element 2 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("laag3-w-3", "Element 3 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("laag3-w-4", "Element 4 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("laag3-w-5", "Element 5 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("laag3-w-6", "Element 6 · wat is er nodig", "Element: ... — hiervoor is nodig: ..., ..., ..."),
        ("laag3-ls-1", "Leerstap 1", "Dit weten we nog niet — hoort bij element..."),
        ("laag3-ls-2", "Leerstap 2", "Dit weten we nog niet — hoort bij element..."),
        ("laag3-ls-3", "Leerstap 3", "Dit weten we nog niet — hoort bij element..."),
        ("laag3-ls-4", "Leerstap 4", "Dit weten we nog niet — hoort bij element..."),
        ("laag3-ls-5", "Leerstap 5", "Dit weten we nog niet — hoort bij element...")])

block("b-805", "a-80", "Laag 4", classes="separator")
canvas("c-805", "b-805", "Laag 4 · Concrete stappen",
       "<p><b>Maak van elke regel uit laag 3 een taak.</b> Elke leerstap wordt een taak die begint met uitzoeken; wat al bekend was wordt gewoon een taak.</p>"
       "<p>Zo concreet dat iemand anders hem kan uitvoeren zonder jou erbij. Dit is wat er straks op je backlog komt.</p>",
       [("laag4-s-1", "Stap 1", "Uit leerstap 1: eerst uitzoeken hoe..."),
        ("laag4-s-2", "Stap 2", "Uit leerstap 2: eerst uitzoeken hoe..."),
        ("laag4-s-3", "Stap 3", "Uit leerstap 3: eerst uitzoeken hoe..."),
        ("laag4-s-4", "Stap 4", "Uit leerstap 4: eerst uitzoeken hoe..."),
        ("laag4-s-5", "Stap 5", "Uit leerstap 5: eerst uitzoeken hoe..."),
        ("laag4-s-6", "Stap 6", "Een taak die volgt uit wat al bekend was"),
        ("laag4-s-7", "Stap 7", "Een taak die volgt uit wat al bekend was"),
        ("laag4-s-8", "Stap 8", "Een taak die volgt uit wat al bekend was"),
        ("laag4-s-9", "Stap 9", "Een taak die volgt uit wat al bekend was"),
        ("laag4-s-10", "Stap 10", "Er is vaak nog eentje die je nu overslaat")])

block("b-806", "a-80", "Canvas meenemen", classes="separator")
text("c-806", "b-806", "Neem je canvas mee",
     "<p>Je deconstructie staat hierboven. Kopieer hem en plak hem in je projectmap — dan raak je hem niet kwijt.</p>"
     "<div class=\"canvas-acties\">"
     "<button type=\"button\" class=\"btn-canvas js-canvas-kopieren\">Kopieer als tekst</button> "
     "<button type=\"button\" class=\"btn-canvas btn-canvas--stil js-canvas-wissen\">Wis mijn canvas</button>"
     "<span class=\"canvas-melding js-canvas-melding\" role=\"status\" aria-live=\"polite\"></span>"
     "</div>")

block("b-807", "a-80", "Afronding", classes="separator")
text("c-807", "b-807", "En dan naar je backlog",
     "<p>Je <b>bovenste laag</b> is je startpunt voor de product backlog. Geef elke stap een prioriteit en een eigenaar, en plan de eerste twee in sprint 1.</p>"
     "<p>Je <b>leerstappen</b> vormen je onderzoekslijst. Plan die vroeg in: zolang ze open staan, blokkeren ze alles wat erachter komt.</p>"
     "<p>Kom hier terug zodra je een grote nieuwe stap tegenkomt. Dan deconstrueer je opnieuw, vanaf je nieuwe einddoel.</p>")

# ============================================ navigatie onderaan elke pagina
for i, (pid, titel, _b, _d) in enumerate(PAGES):
    n = pid.split('-')[1]
    volgende = PAGES[i + 1] if i + 1 < len(PAGES) else None
    if volgende:
        link = ('<a class="paginanav__knop" href="#/id/%s">'
                '<span class="paginanav__label">Volgende onderdeel</span>'
                '<span class="paginanav__titel">%s</span></a>' % (volgende[0], volgende[1]))
    else:
        link = ('<a class="paginanav__knop paginanav__knop--stil" href="#/id/co-10">'
                '<span class="paginanav__label">Terug naar het begin</span>'
                '<span class="paginanav__titel">Waarom deconstructie?</span></a>')
    block("b-%s90" % n, "a-" + n, "Navigatie", classes="separator paginanav")
    text("c-%s90" % n, "b-%s90" % n, "", '<div class="paginanav__rij">%s</div>' % link)

print('Wegschrijven naar', ROOT)
w('course.json', course)
w('contentObjects.json', contentObjects)
w('articles.json', articles)
w('blocks.json', blocks)
w('components.json', components)
tekens = sum(len(c.get('body', '')) for c in components)
print("\n%d pagina's, %d artikelen, %d blokken, %d componenten, ~%d tekens inhoud"
      % (len(contentObjects), len(articles), len(blocks), len(components), tekens))

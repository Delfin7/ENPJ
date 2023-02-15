var dict = {
    "W": ["Znaki ostrzegawcze", "Znaki zakazu", "Znaki informacyjne", "Znaki poziome", "Sygnalizacja świetlna", "Pierwszeństwo na skrzyżowaniach równorzędnych", "Pierwszeństwo na skrzyżowaniach ze znakami", "Skrzyżowania z sygnalizacją świetlną", "Zarządzaniem ruchem przez osoby uprawnione", "Właściwe miejsce pojazdu na drodze", "Zmiana pasa ruchu i kierunku jazdy", "Manewry wyprzedzania", "Manewry wymijania i omijania", "Światła samochodowe i sygnały dźwiękowe", "Zachowanie szczególnej ostrożności", "Znajomość zasad postępowania podczas szczególny sytuacji", "Zachowanie wobec rowerzystów i dzieci", "Przejazdy kolejowe", "Wypadki, kolizje, awarie i udzielenie pomocy", "Postępowanie w sytuacjach nadzwyczajnych, wpływ używek i leków na kierowcę"],
    "A": ["Prędkość pojazdu", "Zasady bezpieczeństwa z zakresu ubioru", "Bezpieczna odległość między pojazdami", "Zagrożenia związane z ruchem drogowym", "Obowiązki kierowcy i posiadacza pojazdu", "Pierwsza pomoc"],
    "B": ["Prędkość pojazdu", "Wyposażenie pojazdu związane z bezpieczeństwem", "Bezpieczna odległość między pojazdami", "Zagrożenia związane z ruchem drogowym", "Obowiązki kierowcy i posiadacza pojazdu", "Pierwsza pomoc"],
    "C": ["Prędkość pojazdu", "Wyposażenie pojazdu związane z bezpieczeństwem oraz czas pracy i odpoczynku", "Bezpieczna odległość między pojazdami", "Zagrożenia związane z ruchem drogowym", "Obowiązki kierowcy i posiadacza pojazdu", "Pierwsza pomoc i towary niebezpieczne"],
    "D": ["Prędkość pojazdu", "Wyposażenie pojazdu związane z bezpieczeństwem oraz czas pracy i odpoczynku", "Bezpieczna odległość między pojazdami", "Zagrożenia związane z ruchem drogowym", "Obowiązki kierowcy i posiadacza pojazdu", "Pierwsza pomoc i bezpieczeństwo pasażerów"],
    "T": ["Poruszanie się po drodze publicznej", "Wyposażenie pojazdu związane z bezpieczeństwem", "Bezpieczna odległość między pojazdami", "Zagrożenia związane z ruchem drogowym", "Obowiązki kierowcy i posiadacza pojazdu", "Pierwsza pomoc"],
    "P": ["Prędkość pojazdu", "Wyposażenie tramwaju", "Bezpieczna odległość między pojazdami", "Zagrożenia związane z ruchem drogowym", "Technika kierowania pojazdem", "Wymagane dokumenty", "Mechanika tramwaju", "Pierwsza pomoc"],
    "PT": ["Znaki drogowe", "Sygnalizacja świetlna", "Pierwszeństwo na drodze", "Bezpieczne poruszanie się po drodze", "Manewry cofania, omijania i wyprzedzania", "Światła pojazdu", "Zachowanie szczególnej ostrożności", "Zachowanie wobec pieszych, rowerzystów i dzieci", "Bezpieczne wysiadanie motorniczego i pasażerów", "Postępowanie w razie wypadku", "Wpływ używek i leków na kierowcę"]
}

$.ajaxSetup({
    data: {csrfmiddlewaretoken: importCsrfToken },
});

function chooseModule(category){
    for(var i=1;i<=26;i++){
        document.getElementById( "r"+i ).style.display = 'block';
    }
    if(category == "PT"){
        for(var i=20;i<=26;i++){
            document.getElementById( "r"+i ).style.display = 'none';
        }
        var modules = dict["PT"].concat(dict["P"])
    }
    else{
        var modules = dict["W"].concat(dict[category[0]]) 
    }
    for(var i=0;i<modules.length;i++){
        $("#r"+ (i+1)).html(modules[i]);
        document.getElementById( "r" +  (i+1)).setAttribute( "onClick", ("startLearning('" + category + "','" + (i+1) + "');") );
    }
}
    
function startLearning(category, number){
    window.location.href = 'learning?category=' + category + '&module=' + number;    
}

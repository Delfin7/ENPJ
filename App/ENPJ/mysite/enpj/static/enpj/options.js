$.ajaxSetup({
    data: {csrfmiddlewaretoken: importCsrfToken },
});

function save(){
    newLanguage = document.getElementById("language").value
    newSignLanguage = document.getElementById("signLanguage").checked

    if(importActualLanguage == newLanguage && importActualSignLanguage == newSignLanguage){
        pass
    }
    else{
        $.ajax({
        type:"POST",
        url: 'update-options',
        async: false,
        data: {
            'language': newLanguage,
            'signLanguage': newSignLanguage,
        },
        dataType: 'json',
        error: (error) => {
            if(error.status == 400){
                window.location.href = 'login';
            }
            else if(error.status > 400){
                $("#info").html("Błąd! Dane nie zostały zaktualizowane!");
            }
            else{
                importActualLanguage = newLanguage
                importActualSignLanguage = newSignLanguage
                $("#info").html("Ustawienia zostały zaktualizowane!");
            }
}});}}

document.getElementById(importActualLanguage).selected = true;
document.getElementById("signLanguage").checked = importActualSignLanguage;

$.ajaxSetup({
    data: {csrfmiddlewaretoken: importCsrfToken },
});

function takeExam(category){
    $.ajax({
        url: 'check-active-exams',
        type: "GET",
        async: false,
        dataType: "json",
        success: (data) => {
            if(data.info){
                if (confirm("Nie zakończyłeś poprzedniego egzaminu. Czy chesz anulować poprzedni egzamin i rozpocząć nowy?")){
                    $.ajax({
                        type:"POST",
                        url: 'cancel-exam',
                        async: false,
                        data: {
                            'cancel': true,
                        },
                        dataType: 'json'
                    });                   
                    $.ajax({
                        type:"POST",
                        url: 'generate-exam',
                        async: false,
                        data: {
                            'category': category,
                        },
                        dataType: 'json'
                    });
                    window.location.href = 'exam';
                }
            }
            else{
                $.ajax({
                    type:"POST",
                    url: 'generate-exam',
                    async: false,
                    data: {
                        'category': category,
                    },
                    dataType: 'json'
                });
                window.location.href = 'exam';
            }
        },
        error: (error) => {
            console.log(error);
        }
        });       
}

if(importContinueExam == 'new'){
    document.getElementById("buttonContinue").style.display = 'none';
}
else{
    function ifContinue(){
        if(importContinueExam == 'True'){
            window.location.href = 'exam'
        }
        else{
            window.location.href = 'exam-result'
        }
        }
}

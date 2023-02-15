language = {"PL": {"points": "Wartość punktowa", "category": "Aktualna kategoria", "timeToEnd": "Czas do końca egzaminu",
    "endExam": "Zakończ egzamin", "primaryQuestions": "Pytania podstawowe",
    "specQuestions": "Pytania specjalistyczne", "timeToRead": "Czas na zapoznanie się z pytaniem",
    "timeToChooseAnswer": "Czas na udzielenie odpowiedzi",  "nextQuestion": "Następne pytanie",
    "yes": "TAK", "no": "NIE", "question": "Pytanie", "answer": "Odpowiedź"},
    "ENG": {"points": "Points", "category": "Category", "timeToEnd": "Time to end",
    "endExam": "Finish exam", "primaryQuestions": "Basic knowledge questions",
    "specQuestions": "Advanced knowledge questions", "timeToRead": "Time for reading the task",
    "timeToChooseAnswer": "Time for answer",  "nextQuestion": "Next question",
    "yes": "YES", "no": "NO", "question": "Question", "answer": "Answer"},
    "DE": {"points": "Ergebnis", "category": "Kategorie", "timeToEnd": "Zeit bis zum Ende",
    "endExam": "Beenden Sie das Lernen", "primaryQuestions": "Fragen des Grundwissens",
    "specQuestions": "Erweiterte Wissensfragen", "timeToRead": "Zeit fürs Lesen der Aufgabe",
    "timeToChooseAnswer": "Zeit zum Antworten",  "nextQuestion": "Nächste Frage",
    "yes": "JA", "no": "NEIN", "question": "Frage", "answer": "Antwort"}
}
const videoSignLanguage = document.querySelector('videoSignLanguage');
var queue = [importSignLanguageQuestion];
var queueIterator = 0;
const video = document.querySelector('video');
var choice = "x";
var minutes = 25;
var seconds = 0;
var id;

function translateAnswers(a, b, c){
    if(importSignLanguageAnswerA != ""){
        queue[1] = a;
        queue[2] = b;
        queue[3] = c;
    }
}

function generateBlocks(start = false){
    if(importMedia.slice(-3) == "mp4" && start){
        document.getElementById("img").style.display = "none"; 
        document.getElementById("video").style.display = "inline";
        document.getElementById("startColumn").style.display = "inline";  
    }
    else if(importMedia.slice(-3) == "mp4"){
        document.getElementById("video").style.display = "none"; 
        document.getElementById("img").style.display = "inline"; 
        document.getElementById("img").src = "/static/enpj/media/video-camera-2806.png";
        document.getElementById("startColumn").style.display = "inline"; 
    }
    else{
        document.getElementById("video").style.display = "none"; 
        document.getElementById("img").style.display = "inline"; 
        document.getElementById("startColumn").style.display = "none"; 
    }

    var buttons = document.getElementsByClassName("button");
    for(var i = 0; i < buttons.length; i++){
        buttons[i].style.display = "none";
    }
    if(importExampleAnswer == ""){
        document.getElementById("buttonT").style.display = "inline"; 
        document.getElementById("buttonN").style.display = "inline"; 
    }
    else{
        document.getElementById("buttonA").style.display = "inline"; 
        document.getElementById("buttonB").style.display = "inline"; 
        document.getElementById("buttonC").style.display = "inline"; 
    }
}

function move(timeLimit, step, type) {
var elem = document.getElementById("myBar");   
id = setInterval(frame, 1000);
    function frame() {
        if (timeLimit <= 0 && type == 'P1') {
            generateBlocks(true);
            clearInterval(id);
            document.getElementById("startColumn").style.display = "none"; 
            document.getElementById("outerBar").style.display = 'none';
                if(importMedia.slice(-3) == "jpg"){
                    $("#timeFor").html(language[importLanguage]["timeToChooseAnswer"]);
                    document.getElementById("outerBar").style.display = 'block';
                    document.getElementById("myBar").style.width = '100%';
                    document.getElementById("myBar").innerHTML = 15;
                    move(15, 6, 'P2');
                }   
        } 
        else if(timeLimit <= 0 && type == 'P2'){
            clearInterval(id);
            nextQuestion();
        }
        else if(timeLimit <= 0 && type == 'S'){
            clearInterval(id);
            nextQuestion();
        }
        else {
            timeLimit--; 
            elem.style.width = timeLimit * step + '%'; 
            elem.innerHTML = timeLimit * 1;
        }
    }
}

function typeOfTimer(){
    if(importQuestionNumber<=20){
        $("#timeFor").html(language[importLanguage]["timeToRead"]);
        document.getElementById("outerBar").style.display = 'block';
        document.getElementById("myBar").style.width = '100%';
        document.getElementById("myBar").innerHTML = 20;
        move(20, 5, "P1");
    }
    else{
        $("#timeFor").html(language[importLanguage]["timeToChooseAnswer"]);
        document.getElementById("outerBar").style.display = 'block';
        document.getElementById("myBar").style.width = '100%';
        document.getElementById("myBar").innerHTML = 50;
        move(50, 2, "S");
    }
}

function startButton(){
    generateBlocks(true);
    document.getElementById("outerBar").style.display = 'none';
    document.getElementById("startColumn").style.display = "none"; 
    clearInterval(id);
}

function timePrepare(){
    setInterval(function(){}, 500);
}

function startTimer(duration, display) {
    setInterval(function () {
        minutes = parseInt(duration / 60, 10);
        seconds = parseInt(duration % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(minutes + ":" + seconds);
        
        if (--duration < 0) {
            finishExam();
        }
    }, 1000);
}
    
jQuery(function ($) {
    var fiveMinutes = importTimerSeconds, display = $('#time');
    startTimer(fiveMinutes, display);
});

function takeAnswer(ans){
    choice = ans;
    var buttons = document.getElementsByClassName("button");
    for(var i = 0; i < buttons.length; i++){
        buttons[i].style.backgroundColor = "#e0e094";
    }
    switch(ans){
        case "T":
            document.getElementById("buttonT").style.backgroundColor = "#FF10F0";
            break;
        case "N":
            document.getElementById("buttonN").style.backgroundColor = "#FF10F0";
            break;
        case "A":
            document.getElementById("buttonA").style.backgroundColor = "#FF10F0";
            break;
        case "B":
            document.getElementById("buttonB").style.backgroundColor = "#FF10F0";
            break;
        case "C":
            document.getElementById("buttonC").style.backgroundColor = "#FF10F0";
            break;
    }
}

function finishExam(){
    $.ajax({
        type:"POST",
        url: 'exam-next-question',
        async: false,
        data: {
            'answer': choice,
            'examId': importIdExam,
            'questionId': importQuestionId,
            'questionNumber': importQuestionNumber,
            'end': true
        },
        dataType: 'json'
    });
    window.location.href = 'exam-result';
}

function finishExamButton(){
    if (confirm("Czy na pewno chcesz zakończyć egzamin?")){
        finishExam();
    }
}

function ifLastQuestionHideNextQuestionButton(){
    if (importQuestionNumber == 32){
        document.getElementById("buttonNextQuestion").style.display = 'none';
    }
}

$.ajaxSetup({
    data: {csrfmiddlewaretoken: importCsrfToken },
});

function nextQuestion() {
    clearInterval(id);
    $.ajax({
        type:"POST",
        url: 'exam-next-question',
        async: false,
        data: {
            'answer': choice,
            'examId': importIdExam,
            'questionId': importQuestionId,
            'questionNumber': importQuestionNumber,
            'time': minutes * 60 + seconds
        },
        dataType: 'json',
        error: (error) => {
            if(error.status == 400){
            window.location.href = 'login';
            }
        }
    });

    if(importQuestionNumber<32){
        $.ajax({
            url: 'exam-get',
            type: "GET",
            async: false,
            dataType: "json",
            success: (data) => {
                choice = null;
                importQuestionId = data.id_question;
                $("#points").html(data.points);
                document.getElementById("img").src= "/static/enpj/media/" + data.media;
                document.getElementById("video").src= "/static/enpj/media/" + data.media;
                $("#question").html(data.question);
                $("#buttonA").html(data.answer_a);
                $("#buttonB").html(data.answer_b);
                $("#buttonC").html(data.answer_c);
                importMedia = data.media;
                importExampleAnswer = data.answer_a;
                generateBlocks();
                $("#primary_number").html(data.primary_number + " / 20");
                $("#spec_number").html(data.spec_number + " / 12");
                takeAnswer("x");
                importQuestionNumber = data.question_number;
                typeOfTimer();
                if(importSignLanguageQuestion != ""){
                    queue = [data.signLanguageQuestion];
                    translateAnswers(data.signLanguageAnswerA, data.signLanguageAnswerB, data.signLanguageAnswerC);
                    $("#labelSignLanguageInfo").html(language[importLanguage]["question"]);
                    document.getElementById("videoSignLanguage").src = "/static/enpj/media/" + data.signLanguageQuestion;
                    queueIterator = 0;
                }
                ifLastQuestionHideNextQuestionButton();
            },
            error: (error) => {
                if(error.status == 400){
                    window.location.href = 'login';
                }
            }
        });
    }
    else{
        window.location.href = 'exam-result';
    }
}

$("#labelPoints").html(language[importLanguage]["points"]);
$("#labelCategory").html(language[importLanguage]["category"]);
$("#labelTimeToEnd").html(language[importLanguage]["timeToEnd"]);
$("#buttonFinish").html(language[importLanguage]["endExam"]);
$("#labelPrimaryQuestions").html(language[importLanguage]["primaryQuestions"]);
$("#labelSpecQuestions").html(language[importLanguage]["specQuestions"]);
$("#buttonNextQuestion").html(language[importLanguage]["nextQuestion"]);
$("#buttonT").html(language[importLanguage]["yes"]);
$("#buttonN").html(language[importLanguage]["no"]);

if(importSignLanguageQuestion != ""){
    document.getElementById("videoSignLanguage").style.display = 'inline';
    document.getElementById("videoSignLanguage").src = "/static/enpj/media/" + importSignLanguageQuestion;
    $("#labelSignLanguageInfo").html(language[importLanguage]["question"]);
    document.getElementById("videoSignLanguage").addEventListener('ended', (event) => {
        queueIterator = queueIterator +1;
        switch(queueIterator){
            case 1:
                answerText = " A";
                break;
            case 2:
                answerText = " B";
                break;
            case 3:
                answerText = " C";
                break;
            }
        if(queueIterator>=queue.length){
            queueIterator = 0;
            $("#labelSignLanguageInfo").html(language[importLanguage]["question"]);
        }
        else{
            $("#labelSignLanguageInfo").html(language[importLanguage]["answer"] + answerText);
        }
        document.getElementById("videoSignLanguage").src = "/static/enpj/media/" + queue[queueIterator];
    });
}

translateAnswers(importSignLanguageAnswerA, importSignLanguageAnswerB, importSignLanguageAnswerC);

video.addEventListener('ended', (event) => {
    $("#timeFor").html(language[importLanguage]["timeToChooseAnswer"]);
    document.getElementById("outerBar").style.display = 'block';
    document.getElementById("myBar").style.width = '100%';
    document.getElementById("myBar").innerHTML = 15;
    move(15, 6, 'P2');
});

typeOfTimer();
generateBlocks();
ifLastQuestionHideNextQuestionButton();
function generateBlocks(questionNumber, media, answer, correctAnswer, ans1 = 'TAK', ans2 = 'NIE', ans3 = ''){
    if(media.slice(-3) == "mp4"){
        document.getElementById("img").style.display = "none"; 
        document.getElementById("video").style.display = "inline";
    }
    else{
        document.getElementById("video").style.display = "none"; 
        document.getElementById("img").style.display = "inline"; 
    }

    if(questionNumber<=20){
        document.getElementById("button3").style.display = "none"; 
        $("#button1").html('TAK');
        $("#button2").html('NIE');
    }
    else{
        document.getElementById("button3").style.display = "inline"; 
        $("#button1").html(ans1);
        $("#button2").html(ans2);
        $("#button3").html(ans3);
    }

    for(var i = 1; i <= 3; i++){
        document.getElementById('button'+i).classList.remove("questionPositive");
        document.getElementById('button'+i).classList.remove("questionNegative");
    }

    switch(correctAnswer){
        case "T":
        case "A":
            document.getElementById('button1').classList.add("questionPositive");
            break;
        case "N":
        case "B":
            document.getElementById('button2').classList.add("questionPositive");
            break;
        case "C":
            document.getElementById('button3').classList.add("questionPositive");
            break;
        }

    switch(answer){
        case "T":
        case "A":
            document.getElementById('button1').classList.add("questionNegative");
            $("#button1").append(" (Zaznaczona odpowiedź)");
            break;
        case "N":
        case "B":
            document.getElementById('button2').classList.add("questionNegative");
            $("#button2").append(" (Zaznaczona odpowiedź)");
            break;
        case "C":
            document.getElementById('button3').classList.add("questionNegative");
            $("#button3").append(" (Zaznaczona odpowiedź)");
            break;
        case null:
            break;
        }
}

function checkQuestions(questionNumber){
    $.ajax({
    url: 'exam-check-answers-get?id=' + importIdExam + '&question=' + questionNumber,
    type: "GET",
    async: true,
    dataType: "json",
    success: (data) => {
        $("#points").html(data.points);
        document.getElementById("img").src= "/static/enpj/media/" + data.media;
        document.getElementById("video").src= "/static/enpj/media/" + data.media;
        $("#question").html(data.question);
        generateBlocks(questionNumber, data.media, data.answer, data.correct_answer, data.answer_a, data.answer_b, data.answer_c)
    },
    error: (error) => {
        if(error.status == 400){
            window.location.href = 'login';
        }
    }
    });
}

for(var i = 1; i <= 32; i++){
    if (importCorrectAnswerList.includes(i)){
        document.getElementById('q'+i).classList.add("questionPositive")
        document.getElementById('q'+i).classList.remove("questionNegative")
    }
    else{
        document.getElementById('q'+i).classList.add("questionNegative")
        document.getElementById('q'+i).classList.remove("questionPositive")
    }
}

generateBlocks(1, importMedia, importAnswer, importCorrectAnswer)

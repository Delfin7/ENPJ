function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function generate_blocks(media){
    if(media.slice(-3) == "mp4"){
        document.getElementById("img").style.display = "none"; 
        document.getElementById("video").style.display = "inline";
        document.getElementById("video").src= "/static/enpj/media/" + media;
    }
    else{
        document.getElementById("video").style.display = "none"; 
        document.getElementById("img").style.display = "inline"; 
        document.getElementById("img").src= "/static/enpj/media/" + media;
    }
    if(questionId +1 == importQuestionsArray.length){
        document.getElementById("next").style.display = 'none';
    }
    else{
        document.getElementById("next").style.display = 'inline';
    }
    if(questionId == 0){
        document.getElementById("prev").style.display = 'none';
    }
    else{
        document.getElementById("prev").style.display = 'inline';
    }
    var buttons = document.getElementsByClassName("button");
    for(var i = 0; i < buttons.length; i++){
        buttons[i].style.backgroundColor = "#e0e094";
    }
}

function changeQuestion(){
    questionId = Number(getCookie("category" + importCategory + "m" + importModule))
    questionDetails = importQuestionsArray[questionId]
    $("#questionNumber").html(questionId + 1);
    $("#question").html(questionDetails["question"]);
    $("#source").html(questionDetails["source"]);
    document.getElementById("inputQuestionNumber").value = questionId + 1;
    media = questionDetails["media"]
    generate_blocks(media)
}

function take_answer(ans){
    correctAnswer = questionDetails["correctAnswer"]
    if(correctAnswer == ans){
        document.getElementById("button" + ans).style.backgroundColor = "green"
    }
    else{
        document.getElementById("button" + ans).style.backgroundColor = "red"
        document.getElementById("button" + correctAnswer).style.backgroundColor = "green"
    }
}

function next(){
    document.cookie = "category" + importCategory + "m" + importModule + "=" + (questionId + 1)
    changeQuestion()
}

function prev(){
    document.cookie = "category" + importCategory + "m" + importModule + "=" + (questionId - 1)
    changeQuestion()
}

function confirm(){
    questionNumber = document.getElementById("inputQuestionNumber").value
    if(questionNumber<1 || questionNumber>importQuestionsArray.length){
        document.getElementById("inputQuestionNumber").value = questionId + 1
    }
    else{
        document.cookie = "category" + importCategory + "m" + importModule + "=" + (questionNumber - 1)
        changeQuestion()
    }
}

$.ajaxSetup({
    data: {csrfmiddlewaretoken: importCsrfToken },
});

if(importType == "podst"){
    document.getElementById("buttonT").style.display = "inline"; 
    document.getElementById("buttonN").style.display = "inline"; 
}
else{
    document.getElementById("buttonA").style.display = "inline"; 
    document.getElementById("buttonB").style.display = "inline"; 
    document.getElementById("buttonC").style.display = "inline"; 
}

if(getCookie("category" + importCategory + "m" + importModule) == ""){
    document.cookie = "category" + importCategory + "m" + importModule + "=0"
}

$("#questionsCount").html(importQuestionsArray.length);
document.getElementById("inputQuestionNumber").max = importQuestionsArray.length;
changeQuestion()

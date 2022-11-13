// getting started button
document.getElementById('getting').addEventListener("click", () => {
    document.getElementById('getting-started').style.display = "block";
    document.getElementById('chat-show').style.display = "none";
    document.getElementById('email-show').style.display = "none";
    document.getElementById('guide-show').style.display = "none";
})

var i = 0;
document.getElementById('drop1').addEventListener("click", () => {
    if (i == 0) {
        document.getElementById('description1').style.display = "block";
        i = 1;
    }
    else {
        document.getElementById('description1').style.display = "none";
        i = 0;
    }
})
var j = 0;
document.getElementById('drop2').addEventListener("click", () => {
    if (j == 0) {
        document.getElementById('description2').style.display = "block";
        j = 1;
    }
    else {
        document.getElementById('description2').style.display = "none";
        j = 0;
    }
})
var k = 0;
document.getElementById('drop3').addEventListener("click", () => {
    if (k == 0) {
        document.getElementById('description3').style.display = "block";
        k = 1;
    }
    else {
        document.getElementById('description3').style.display = "none";
        k = 0;
    }
})
var l = 0;
document.getElementById('drop4').addEventListener("click", () => {
    if (l == 0) {
        document.getElementById('description4').style.display = "block";
        l = 1;
    }
    else {
        document.getElementById('description4').style.display = "none";
        l = 0;
    }
})


// email channel button
document.getElementById('email').addEventListener("click", () => {
    document.getElementById('email-show').style.display = "block";
    document.getElementById('getting-started').style.display = "none";
    document.getElementById('chat-show').style.display = "none";
    document.getElementById('guide-show').style.display = "none";
})

var a = 0;
document.getElementById('drop5').addEventListener("click", () => {
    if (a == 0) {
        document.getElementById('description5').style.display = "block";
        a = 1;
    }
    else {
        document.getElementById('description5').style.display = "none";
        a = 0;
    }
})
var b = 0;
document.getElementById('drop6').addEventListener("click", () => {
    if (b == 0) {
        document.getElementById('description6').style.display = "block";
        b = 1;
    }
    else {
        document.getElementById('description6').style.display = "none";
        b = 0;
    }
})

// chatbot button
document.getElementById('chatbot').addEventListener("click", () => {
    document.getElementById('chat-show').style.display = "block";
    document.getElementById('getting-started').style.display = "none";
    document.getElementById('email-show').style.display = "none";
    document.getElementById('guide-show').style.display = "none";
})

var a = 0;
document.getElementById('drop7').addEventListener("click", () => {
    if (a == 0) {
        document.getElementById('description7').style.display = "block";
        a = 1;
    }
    else {
        document.getElementById('description7').style.display = "none";
        a = 0;
    }
})
var b = 0;
document.getElementById('drop8').addEventListener("click", () => {
    if (b == 0) {
        document.getElementById('description8').style.display = "block";
        b = 1;
    }
    else {
        document.getElementById('description8').style.display = "none";
        b = 0;
    }
})

// guide channel button
document.getElementById('guide').addEventListener("click", () => {
    document.getElementById('guide-show').style.display = "block";
    document.getElementById('chat-show').style.display = "none";
    document.getElementById('getting-started').style.display = "none";
    document.getElementById('email-show').style.display = "none";
})

var a = 0;
document.getElementById('drop9').addEventListener("click", () => {
    if (a == 0) {
        document.getElementById('description9').style.display = "block";
        a = 1;
    }
    else {
        document.getElementById('description9').style.display = "none";
        a = 0;
    }
})
var b = 0;
document.getElementById('drop10').addEventListener("click", () => {
    if (b == 0) {
        document.getElementById('description10').style.display = "block";
        b = 1;
    }
    else {
        document.getElementById('description10').style.display = "none";
        b = 0;
    }
})

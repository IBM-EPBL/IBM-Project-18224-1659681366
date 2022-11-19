var i = 0;
document.getElementById('drop').addEventListener("click", () => {
    if (i == 0) {
        document.getElementById('description').style.display = "block";
        i = 1;
    }
    else {
        document.getElementById('description').style.display = "none";
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

var a = 0;
document.getElementById('down1').addEventListener("click", () => {
    if (a == 0) {
        document.getElementById('description-s1').style.display = "block";
        a = 1;
    }
    else {
        document.getElementById('description-s1').style.display = "none";
        a = 0;
    }
})
var b = 0;
document.getElementById('down2').addEventListener("click", () => {
    if (b == 0) {
        document.getElementById('description-s2').style.display = "block";
        b = 1;
    }
    else {
        document.getElementById('description-s2').style.display = "none";
        b = 0;
    }
})


document.getElementById('login').addEventListener("click", () => {
    document.getElementById('dropdown-signup').style.display = "none";
    document.getElementById('dropdown-login').style.display = "grid";
})

document.getElementById('signup').addEventListener("click", () => {
    document.getElementById('dropdown-login').style.display = "none";
    document.getElementById('dropdown-signup').style.display = "grid";
})


function clickme1() {
    document.getElementById('paracontet').innerHTML = "Customer Care Registry is a kinda application that is used for providing services for an organization or management. The service or support is provided for an organization and then the solution is provided for the end users who are all using that organization's product or other things. The major and minor issues that are faced by the end users are solved by the helpdesk team. The issues are raised to the helpdesk team with the help of tickets. Using the ticketing system, the issues of endusers are raised to the helpdesk team. Then, tickets are assigned to theagents and the agents will receive the tickets via Omni channels. The Omnichannels are nothing but Knowledge based channels, Email, and live chat. Using these channels, the agent receives the issues on his dashboard."
    document.getElementById('popup1').style.display = "block";
}
function clickme2() {
    document.getElementById('paracontet').innerHTML = "Customer Care Registry is mainly established and developed for the people. Our team provides a continuous 24/7 customer support for the people who arrives here for the help."
    document.getElementById('popup1').style.display = "block";
}
function clickme3() {
    document.getElementById('paracontet').innerHTML = "The queries that are raised by the user/customer is automatically routed internally for the agent. Here, the agent will be specialized in a specific field and based on that, the internal routing occurs. So that, the query is solved for the customer in a quick span of time."
    document.getElementById('popup1').style.display = "block";
}
function clickme4() {
    document.getElementById('paracontet').innerHTML = "The user gets a quick response if he/she comes up with a query to us. Here, our agent delivers instant replies to the customer/user. And at last, the query is resolved quickly based on the priority."
    document.getElementById('popup1').style.display = "block";
}
function clickme5() {
    document.getElementById('paracontet').innerHTML = "At first time when you enter Customer Care Registry, you'll be landed in our landing page. There, you need to sign up with your basic credentials. Once completing the sign up process, you need to log in with the details and after that process, you'll be able to see the customer dashboard. Finally, in that there will be a button named RAISE A QUERY. By clicking that button, you can be able to contact the support team."
    document.getElementById('popup1').style.display = "block";
}
function clickme6() {
    document.getElementById('paracontet').innerHTML = "The Omni channels are nothing but Knowledge based channels, Email, and live chat. Using these channels, the agent receives the issues on his dashboard."
    document.getElementById('popup1').style.display = "block";
}
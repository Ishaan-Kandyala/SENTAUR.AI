const SERVERCODE = "";

const API = "";

function getToken() {
    return localStorage.getItem("token");
}

/* SIGNUP */
async function signup() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(API + "/auth/signup", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: new URLSearchParams({ username: email, password })
    });

    const data = await res.json();
    if (res.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location = "chat.html";
    } else {
        alert("Signup failed");
    }
}

/* LOGIN */
async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(API + "/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: new URLSearchParams({ username: email, password })
    });

    const data = await res.json();
    if (res.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location = "chat.html";
    } else {
        alert("Invalid login");
    }
}

/* CHAT */
async function sendMessage() {
    const msgInput = document.getElementById("msg");
    const msg = msgInput.value.trim();
    if (!msg) return;

    addMessage("user", msg);
    msgInput.value = "";
    document.getElementById("typing").style.display = "block";

    const res = await fetch(API + "/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    document.getElementById("typing").style.display = "none";

    if (res.ok) {
        addMessage("bot", data.response);
    } else {
        addMessage("bot", "Auth error. Please log in again.");
    }
}

function addMessage(sender, text) {
    const box = document.getElementById("chatbox");

    const div = document.createElement("div");
    div.className = "message " + sender;

    if (sender === "bot") {
        div.innerHTML = marked.parse(text);
    } else {
        div.innerText = text;
    }

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
let balance = 0;
let clickPower = 1;

document.getElementById("clickButton").onclick = () => {
    balance += clickPower;
    document.getElementById("balance").innerText = balance;
};

document.getElementById("upgradeButton").onclick = () => {
    if (balance >= 100) {
        balance -= 100;
        clickPower += 1;
        document.getElementById("balance").innerText = balance;
        document.getElementById("clickPower").innerText = clickPower;
    } else {
        alert("Недостаточно монет!");
    }
};

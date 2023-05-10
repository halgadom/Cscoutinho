document.getElementById("btn-convert").addEventListener("click", function() {
    const amount = document.getElementById("amount").value;
    const conversionRate = 4.99;
    const result = amount / conversionRate;
    document.getElementById("result").setAttribute("style", "display:block");
    document.getElementById("txt-primary").innerText = amount + " Real = ";
    document.getElementById("txt-secondary").innerText = result.toFixed(2) + " Dollar";
});
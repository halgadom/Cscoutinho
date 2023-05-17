function avaliarResultado() {
    let contador = 0;

    if (document.getElementById("pergunta1").checked) contador++;
    if (document.getElementById("pergunta2").checked) contador++;
    if (document.getElementById("pergunta3").checked) contador++;
    if (document.getElementById("pergunta4").checked) contador++;
    if (document.getElementById("pergunta5").checked) contador++;

    let resultado = document.getElementById("resultado");

    if (contador < 2) {
        resultado.innerHTML = "Inocente";
    } else if (contador === 2) {
        resultado.innerHTML = "Suspeita";
    } else if (contador >= 3 && contador <= 4) {
        resultado.innerHTML = "Cúmplice";
    } else if (contador === 5) {
        resultado.innerHTML = "Assassina";
    }
}

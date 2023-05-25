document.getElementById('calcular').addEventListener('click', function() {
  const populacaoInicial = parseFloat(document.getElementById('populacao_inicial').value);
  const taxaCrescimento = parseFloat(document.getElementById('taxa_crescimento').value);
  const anoInicial = parseInt(document.getElementById('ano_inicial').value);
  const anoFinal = parseInt(document.getElementById('ano_final').value);

  let populacaoFinal = populacaoInicial;
  const listaResultados = document.getElementById('resultado');

  listaResultados.innerHTML = '';

  let anoAtual = anoInicial;
  while (anoAtual <= anoFinal) {
    const li = document.createElement('li');
    li.innerText = `Ano ${anoAtual}: ${populacaoFinal.toFixed(0)} habitantes`;
    listaResultados.appendChild(li);

    populacaoFinal += (populacaoFinal * (taxaCrescimento / 100));
    anoAtual++;
  }

  listaResultados.style.display = 'block';
});

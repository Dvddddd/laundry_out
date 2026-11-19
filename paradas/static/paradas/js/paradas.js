const botaoParada = document.querySelector('[data-toggle-parada]');
if (botaoParada) {
    const formulario = document.querySelector('[data-form-parada]');
    botaoParada.addEventListener('click', () => {
        formulario.hidden = !formulario.hidden;
        botaoParada.setAttribute('aria-expanded', String(!formulario.hidden));
    });
}

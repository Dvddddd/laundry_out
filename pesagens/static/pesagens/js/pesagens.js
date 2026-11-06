const botaoNovaPesagem = document.querySelector('[data-toggle-pesagem]');

if (botaoNovaPesagem) {
    const painel = document.getElementById(botaoNovaPesagem.getAttribute('aria-controls'));

    botaoNovaPesagem.addEventListener('click', () => {
        painel.hidden = !painel.hidden;
        botaoNovaPesagem.setAttribute('aria-expanded', String(!painel.hidden));
    });
}

document.querySelectorAll('[data-form-pesagem]').forEach((form) => {
    const campo = form.querySelector('[data-peso]');
    const display = form.querySelector('[data-display-peso]');

    function atualizarPeso() {
        display.textContent = campo.value ? `${campo.value.replace('.', ',')} kg` : '—';
    }

    campo.addEventListener('input', atualizarPeso);
    atualizarPeso();
});

document.querySelectorAll('[data-excluir-pesagem]').forEach((form) => {
    form.addEventListener('submit', (evento) => {
        if (!window.confirm('Excluir esta pesagem?')) {
            evento.preventDefault();
        }
    });
});

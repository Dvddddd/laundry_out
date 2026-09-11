document.addEventListener('DOMContentLoaded', () => {
    const tabela = document.querySelector('#lista-maquinas');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    if (!tabela || !csrfToken) {
        return;
    }

    const alternarEdicao = (linha, editando) => {
        linha.querySelectorAll('[data-display]').forEach((elemento) => {
            elemento.classList.toggle('d-none', editando);
        });
        linha.querySelectorAll('[data-input]').forEach((elemento) => {
            elemento.classList.toggle('d-none', !editando);
        });

        linha.querySelector('[data-acao="editar"]').classList.toggle('d-none', editando);
        linha.querySelector('[data-acao="salvar"]').classList.toggle('d-none', !editando);
        linha.querySelector('[data-acao="cancelar"]').classList.toggle('d-none', !editando);
    };

    const mensagemDeErro = (dados) => {
        if (dados.erro) {
            return dados.erro;
        }

        if (dados.erros) {
            return Object.values(dados.erros).flat().join('\n');
        }

        return 'Não foi possível concluir a operação.';
    };

    const salvar = async (linha) => {
        const codigo = linha.querySelector('[data-input="codigo"]').value.trim();
        const nome = linha.querySelector('[data-input="nome"]').value.trim();
        const botaoSalvar = linha.querySelector('[data-acao="salvar"]');

        botaoSalvar.disabled = true;

        try {
            const resposta = await fetch(linha.dataset.urlAtualizar, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ codigo, nome }),
            });
            const dados = await resposta.json();

            if (!resposta.ok) {
                throw new Error(mensagemDeErro(dados));
            }

            linha.querySelector('[data-display="codigo"]').textContent = dados.codigo;
            linha.querySelector('[data-display="nome"]').textContent = dados.nome;
            alternarEdicao(linha, false);
        } catch (erro) {
            window.alert(erro.message);
        } finally {
            botaoSalvar.disabled = false;
        }
    };

    const cancelar = (linha) => {
        linha.querySelectorAll('[data-input]').forEach((input) => {
            const campo = input.dataset.input;
            input.value = linha.querySelector(`[data-display="${campo}"]`).textContent.trim();
        });
        alternarEdicao(linha, false);
    };

    const excluir = async (linha) => {
        const nome = linha.querySelector('[data-display="nome"]').textContent.trim();

        if (!window.confirm(`Deseja realmente excluir a máquina "${nome}"?`)) {
            return;
        }

        try {
            const resposta = await fetch(linha.dataset.urlExcluir, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
            });

            if (!resposta.ok) {
                throw new Error('Não foi possível excluir a máquina.');
            }

            linha.remove();

            if (!tabela.querySelector('[data-maquina-id]')) {
                tabela.innerHTML = `
                    <tr data-estado-vazio>
                        <td colspan="3" class="text-center text-secondary py-4">
                            Nenhuma máquina cadastrada.
                        </td>
                    </tr>`;
            }
        } catch (erro) {
            window.alert(erro.message);
        }
    };

    tabela.addEventListener('click', (evento) => {
        const botao = evento.target.closest('[data-acao]');
        const linha = botao?.closest('[data-maquina-id]');

        if (!botao || !linha) {
            return;
        }

        const acoes = {
            editar: () => alternarEdicao(linha, true),
            salvar: () => salvar(linha),
            cancelar: () => cancelar(linha),
            excluir: () => excluir(linha),
        };

        acoes[botao.dataset.acao]?.();
    });
});

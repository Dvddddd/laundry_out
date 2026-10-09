document.addEventListener('DOMContentLoaded', () => {
    const tabela = document.querySelector('#lista-uniformes');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const mensagem = document.querySelector('#mensagem-uniformes');

    if (!tabela || !csrfToken) {
        return;
    }

    const exibirMensagem = (texto, tipo = 'danger') => {
        mensagem.textContent = texto;
        mensagem.className = `alert alert-${tipo}`;
    };

    const limparMensagem = () => {
        mensagem.textContent = '';
        mensagem.className = 'alert d-none';
    };

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

    const restaurarCampos = (linha) => {
        linha.querySelector('[data-input="ordem"]').value = linha.querySelector('[data-display="ordem"]').textContent.trim();
        linha.querySelector('[data-input="nome"]').value = linha.querySelector('[data-display="nome"]').textContent.trim();
        linha.querySelector('[data-input="status"]').value = linha.dataset.status;
        linha.querySelector('[data-input="imagem"]').value = '';
    };

    const atualizarImagem = (linha, url, nome) => {
        const container = linha.querySelector('[data-display="imagem"]');
        container.replaceChildren();

        if (url) {
            const imagem = document.createElement('img');
            imagem.src = url;
            imagem.alt = nome;
            container.appendChild(imagem);
            linha.dataset.imagemUrl = url;
            return;
        }

        const texto = document.createElement('span');
        texto.className = 'sem-imagem';
        texto.textContent = 'Sem imagem';
        container.appendChild(texto);
        linha.dataset.imagemUrl = '';
    };

    tabela.querySelectorAll('[data-uniforme-id]').forEach((linha) => {
        linha.dataset.status = linha.querySelector('[data-input="status"]').value;
    });

    tabela.addEventListener('click', async (evento) => {
        const botao = evento.target.closest('[data-acao]');
        const linha = evento.target.closest('[data-uniforme-id]');

        if (!botao || !linha) {
            return;
        }

        limparMensagem();
        const acao = botao.dataset.acao;

        if (acao === 'editar') {
            alternarEdicao(linha, true);
            linha.querySelector('[data-input="nome"]').focus();
            return;
        }

        if (acao === 'cancelar') {
            restaurarCampos(linha);
            alternarEdicao(linha, false);
            return;
        }

        if (acao === 'salvar') {
            const dados = new FormData();
            const arquivo = linha.querySelector('[data-input="imagem"]').files[0];
            dados.append('ordem', linha.querySelector('[data-input="ordem"]').value);
            dados.append('nome', linha.querySelector('[data-input="nome"]').value);
            dados.append('status', linha.querySelector('[data-input="status"]').value);
            if (arquivo) {
                dados.append('imagem', arquivo);
            }

            const resposta = await fetch(linha.dataset.urlAtualizar, {
                method: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                body: dados,
            });
            const conteudo = await resposta.json();

            if (!resposta.ok) {
                const erros = Object.values(conteudo.erros || {}).flat().join(' ');
                exibirMensagem(erros || 'Não foi possível atualizar o uniforme.');
                return;
            }

            linha.querySelector('[data-display="ordem"]').textContent = conteudo.ordem;
            linha.querySelector('[data-display="nome"]').textContent = conteudo.nome;

            const status = linha.querySelector('[data-display="status"]');
            status.textContent = conteudo.status_label;
            status.className = `badge ${conteudo.status === 'ativo' ? 'text-bg-success' : 'text-bg-secondary'}`;
            status.dataset.display = 'status';
            linha.dataset.status = conteudo.status;

            atualizarImagem(linha, conteudo.imagem_url, conteudo.nome);
            linha.querySelector('[data-input="imagem"]').value = '';
            alternarEdicao(linha, false);
            exibirMensagem('Uniforme atualizado com sucesso.', 'success');
            return;
        }

        if (acao === 'excluir') {
            const nome = linha.querySelector('[data-display="nome"]').textContent.trim();
            if (!window.confirm(`Excluir o uniforme “${nome}”?`)) {
                return;
            }

            const resposta = await fetch(linha.dataset.urlExcluir, {
                method: 'POST',
                headers: {'X-CSRFToken': csrfToken},
            });

            if (!resposta.ok) {
                exibirMensagem('Não foi possível excluir o uniforme.');
                return;
            }

            linha.remove();
            exibirMensagem('Uniforme excluído com sucesso.', 'success');

            if (!tabela.querySelector('[data-uniforme-id]')) {
                const estadoVazio = document.createElement('tr');
                estadoVazio.dataset.estadoVazio = '';
                estadoVazio.innerHTML = '<td colspan="5" class="text-center text-secondary py-4">Nenhum uniforme cadastrado.</td>';
                tabela.appendChild(estadoVazio);
            }
        }
    });
});

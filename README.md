# Vellora Online — Recursos oficiais

Repositório público de pacotes opcionais de personalização. **Não contém dados de jogadores.**

## Downloads atuais (v7–v9)

[**Pacotes v7, v8 e v9 revisados — packs-v2**](https://github.com/dk-77a/Vellora-Assets/releases/tag/packs-v2)

- **v7:** 32 formatos de nariz e boca; 32 miniaturas PNG. As alterações são aplicadas à malha skinned 3D do rosto, não são GLBs separados
- **v8:** 46 opções de maquiagem, cílios e tatuagens; 16 texturas originais de tatuagem e 46 miniaturas PNG
- **v9:** 56 modelos/estilos de brincos, piercings e óculos, com 56 miniaturas PNG. O motor Godot cria a geometria 3D e prende os acessórios ao osso Head

Todos os PNGs são validados por SHA-256 durante a instalação. Os tamanhos dos ZIPs variam conforme sua compressão — **mais MB não significa um modelo 3D melhor**.

## Compatibilidade dos catálogos

- `manifest.json` → **packs-v1**, preservado para APKs antigos
- [`manifest-v2.json`](https://raw.githubusercontent.com/dk-77a/Vellora-Assets/main/manifest-v2.json) → novos ZIPs v7/v8/v9 e os mesmos v2–v6 anteriores

O Vellora atualizado consulta `manifest-v2.json` e recorre ao catálogo antigo se a nova versão estiver indisponível. **Não atualize `manifest.json` com os novos ZIPs**, pois APKs sem suporte a miniaturas rejeitariam a instalação.

## Como usar no Vellora

No seletor de personagens, toque no botão **RECURSOS** no canto superior direito. Na central, use **ATUALIZAR**, **BAIXAR FALTANTES** ou **VOLTAR**. O botão **JOGAR** leva diretamente à seleção de spawn; downloads são opcionais.

## Como gerar e publicar (mantenedor)

Os geradores ficam em [`tools/`](https://github.com/dk-77a/Vellora-Assets/tree/main/tools). A automação `Publish Vellora Appearance Packs v7-v9 (Preview Edition)` cria os três ZIPs, testa as imagens e os hashes, publica a release `packs-v2` e só então publica `manifest-v2.json`. A publicação é segura contra catálogos apontando para arquivos inexistentes.

Não publique senhas, tokens ou informações privadas.

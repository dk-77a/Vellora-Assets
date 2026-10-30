# Vellora Assets

Repositório público de **pacotes opcionais do Vellora Online**: cabelos, roupas, rostos, maquiagem e acessórios 3D (v2–v9).

**O código-fonte do jogo e dados dos jogadores não ficam neste repositório.**

## Como publicar os arquivos pelo Android

1. Abra **Releases** neste repositório e toque em **Draft a new release**.
2. Crie a tag `packs-v1` e anexe os arquivos ZIP dos pacotes **v2, v3, v4, v5, v6, v7, v8 e v9**, sem renomeá-los.
3. Publique a release. Depois faça upload de `manifest.json` para a raiz da branch `main`.
4. Confirme que o catálogo pode ser aberto sem login: https://raw.githubusercontent.com/dk-77a/Vellora-Assets/main/manifest.json

> **Importante:** publique o `manifest.json` **apenas depois** que os oito ZIPs estiverem disponíveis na release; caso contrário, o jogo encontrará links de download que ainda não funcionam.

## Como funciona dentro do Vellora

Na seleção de personagens, o botão **JOGAR** abre a Central de Downloads. Os jogadores escolhem entre baixar os ZIPs faltantes ou **JOGAR AGORA** sem downloads. O jogo confere o SHA-256, o tamanho do ZIP e a versão antes de instalar na pasta do aplicativo.

## Publicação de atualizações

Quando substituir um ZIP, atualize `sha256` e `bytes` no `manifest.json` e publique um novo arquivo na release. Não publique chaves, credenciais, código-fonte privado nem arquivos pessoais dos jogadores.

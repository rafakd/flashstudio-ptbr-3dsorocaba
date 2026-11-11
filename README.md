# Flash Studio PT-BR — 3D Sorocaba

Instalador da tradução em Português do Brasil para o **Flash Studio / Orca-Flashforge**, distribuído pela [3D Sorocaba](https://3dsorocaba.com.br).

## Download

Baixe o arquivo **3D-Sorocaba-Flash-Studio-PTBR.exe** na [última release](../../releases/latest), feche o Flash Studio e execute.
Dentro do programa, o botão **Verificar atualizações** busca novas versões direto daqui.

## Como funciona este repositório

Esta é uma versão modificada do projeto original [lexone/flashstudio_ptbr](https://github.com/lexone/flashstudio_ptbr) (3D Brasília).
Todos os dias o workflow [`build-sorocaba.yml`](.github/workflows/build-sorocaba.yml):

1. confere a última release do projeto original;
2. aplica a identidade 3D Sorocaba com [`branding/apply_branding.py`](branding/apply_branding.py) (nome, logo, ícone, cores, créditos e canal de atualização);
3. compila e publica uma release aqui, com o `.exe`, o SHA-256 e o código-fonte completo (`codigo-fonte.zip`).

Para gerar manualmente: **Actions → Gerar instalador 3D Sorocaba → Run workflow**.
Para republicar após mudar só a marca: aumente `BRANDING_REVISION` em `branding/apply_branding.py` e rode o workflow.

## Créditos e licença

- Instalador original: **lexone / 3D Brasília** — https://github.com/lexone/flashstudio_ptbr
- Catálogos e terminologia: projetos [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) e [Orca-Flashforge](https://github.com/FlashForge/Orca-Flashforge)
- Modificações de marca: **3D Sorocaba**

Distribuído sob a **GNU Affero General Public License v3** (veja [LICENSE](LICENSE)).
Projeto independente, sem afiliação oficial com a FlashForge.

# Flash Studio PT-BR — 3D Sorocaba

Instalador da tradução em Português do Brasil para o **Flash Studio / Orca-Flashforge**, distribuído pela [3D Sorocaba](https://3dsorocaba.com.br).

## Download

Baixe o arquivo **3D-Sorocaba-Flash-Studio-PTBR.exe** na [última release](../../releases/latest), feche o Flash Studio e execute.
Dentro do programa, o botão **Verificar atualizações** busca novas versões direto daqui.

## Como funciona a tradução

O instalador **não altera o programa Flash Studio** (nenhum `.exe` ou `.dll` é modificado), não precisa de administrador e não cria serviços nem tarefas agendadas. Ele mexe apenas nos arquivos de idioma do seu usuário:

| O que | Onde |
|---|---|
| Catálogo de textos em português (`strings.<md5>.json`, `active.json`) | `%APPDATA%\Orca-Flashforge\i18n\slice` |
| Idioma do programa (`"language": "pt_BR"`) | `%APPDATA%\Orca-Flashforge\Orca-Flashforge.conf` |
| Backup automático, feito antes de qualquer mudança | `%APPDATA%\Orca-Flashforge\i18n\backups-3dsorocaba` |

- **Feche o Flash Studio** antes de instalar. Abra-o pelo menos uma vez antes, para que a pasta de configuração exista.
- **Só traduz o que reconhece:** textos de versões mais novas do Flash Studio que ainda não estão no catálogo continuam em inglês, sem quebrar nada.
- **Proteção (opcional, vem marcada):** deixa os arquivos de idioma como somente leitura, para o Flash Studio não voltar ao inglês quando atualizar. O botão **Liberar atualizações** remove essa proteção.
- **Desfazer:** o botão **Restaurar último backup** volta os arquivos exatamente como estavam antes da instalação.

## Créditos e licença

- Instalador original: **lexone / 3D Brasília** — https://github.com/lexone/flashstudio_ptbr
- Catálogos e terminologia: projetos [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) e [Orca-Flashforge](https://github.com/FlashForge/Orca-Flashforge)
- Modificações de marca: **3D Sorocaba**. As versões são geradas automaticamente a partir do projeto original; o código-fonte completo de cada uma está na release (`codigo-fonte.zip`).

Distribuído sob a **GNU Affero General Public License v3** (veja [LICENSE](LICENSE)).
Projeto independente, sem afiliação oficial com a FlashForge.

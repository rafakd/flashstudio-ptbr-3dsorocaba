"""
Aplica a identidade 3D Sorocaba sobre o código-fonte original de
github.com/lexone/flashstudio_ptbr (AGPL-3.0).

Uso:  python branding/apply_branding.py <pasta-do-upstream> <owner/repo-da-3d-sorocaba>

O script falha (exit 1) se algum trecho esperado não for encontrado,
para que o workflow pare em vez de gerar um instalador quebrado.
"""
import os
import re
import shutil
import sys

# Aumente quando mudar algo na marca sem mudar a versão original.
BRANDING_REVISION = 1

# Para trocar a logo: suba branding/logo.png (tem prioridade sobre o .b64).
LOGO_SHA256 = "2abfa1b37cdcf4fbc6628a235ba68d1c58a8b7d9bc45e8f6ecd056760f4ef264"

HERE = os.path.dirname(os.path.abspath(__file__))


def fail(msg):
    print("ERRO DE BRANDING: " + msg)
    sys.exit(1)


def read(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def write(path, text):
    # BOM em .cs/.ps1 garante leitura UTF-8 pelo csc e pelo PowerShell 5
    enc = "utf-8" if path.endswith(".md") else "utf-8-sig"
    with open(path, "w", encoding=enc) as f:
        f.write(text)


def replace_once(text, old, new, where):
    n = text.count(old)
    if n != 1:
        fail("trecho esperado em %s aparece %d vez(es): %r" % (where, n, old[:80]))
    return text.replace(old, new)


def main():
    if len(sys.argv) != 3:
        fail("uso: apply_branding.py <pasta-upstream> <owner/repo>")
    root, repo = sys.argv[1], sys.argv[2]
    src = os.path.join(root, "src")

    # 1) Logo e ícone (gerados a partir de branding/logo.png, ou de logo.webp.b64)
    import base64
    import hashlib
    import io
    from PIL import Image
    png = os.path.join(HERE, "logo.png")
    b64 = os.path.join(HERE, "logo.webp.b64")
    if os.path.exists(png):
        im = Image.open(png)
    elif os.path.exists(b64):
        data = base64.b64decode("".join(read(b64).split()))
        if hashlib.sha256(data).hexdigest() != LOGO_SHA256:
            fail("branding/logo.webp.b64 está corrompido (SHA-256 não confere)")
        im = Image.open(io.BytesIO(data))
    else:
        fail("branding/logo.png ou branding/logo.webp.b64 não encontrado")
    im = im.convert("RGBA")
    im = im.crop(im.getbbox())
    side = max(im.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(im, ((side - im.size[0]) // 2, (side - im.size[1]) // 2))
    square = square.resize((256, 256), Image.LANCZOS)
    square.save(os.path.join(root, "assets", "logo.png"))
    square.save(os.path.join(root, "assets", "logo.ico"),
                sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

    # 2) Troca de nome em todos os .cs e no build.ps1
    renames = [
        ("TresDBrasilia", "TresDSorocaba"),
        ("3D Brasília", "3D Sorocaba"),
        ("backups-3dbrasilia", "backups-3dsorocaba"),
        (".3dbrasilia-", ".3dsorocaba-"),
        ("3DBrasilia", "3DSorocaba"),
        ("3D-Brasilia-Flash-Studio-PTBR", "3D-Sorocaba-Flash-Studio-PTBR"),
    ]
    files = [os.path.join(src, f) for f in os.listdir(src) if f.endswith(".cs")]
    files.append(os.path.join(root, "build.ps1"))
    for path in files:
        text = read(path)
        if os.path.basename(path) == "UpdateService.cs":
            # Atualizações passam a vir do repositório da 3D Sorocaba
            if "lexone/flashstudio_ptbr" not in text:
                fail("URL de atualização não encontrada em UpdateService.cs")
            text = text.replace("lexone/flashstudio_ptbr", repo)
        for old, new in renames:
            text = text.replace(old, new)
        write(path, text)

    # 3) Versão: mesma do original + revisão da 3D Sorocaba no 4º número
    info_path = os.path.join(src, "AssemblyInfo.cs")
    info = read(info_path)
    m = re.search(r'AssemblyVersion\("(\d+)\.(\d+)\.(\d+)(?:\.\d+)?"\)', info)
    if not m:
        fail("AssemblyVersion não encontrado")
    version = "%s.%s.%s.%d" % (m.group(1), m.group(2), m.group(3), BRANDING_REVISION)
    info = re.sub(r'(Assembly(?:File)?Version\(")[^"]+("\))', r"\g<1>" + version + r"\g<2>", info)
    info = re.sub(r'AssemblyCopyright\("[^"]*"\)',
                  'AssemblyCopyright("Copyright © lexone / 3D Brasília; modificações © 3D Sorocaba")', info)
    write(info_path, info)

    # 4) Visual (cores da logo), botão do site e créditos
    p = os.path.join(src, "MainForm.cs")
    s = read(p)
    w = "MainForm.cs"
    s = replace_once(s, "using System.Drawing;\n", "using System.Drawing;\nusing System.Drawing.Drawing2D;\n", w)
    s = replace_once(s, "        private string operation;", """        // Paleta 3D Sorocaba (cores da logo)
        internal static readonly Color Magenta = Color.FromArgb(230, 0, 126);
        internal static readonly Color MagentaDark = Color.FromArgb(150, 0, 90);
        internal static readonly Color Amarelo = Color.FromArgb(255, 196, 0);
        internal static readonly Color FundoClaro = Color.FromArgb(253, 244, 249);

        private string operation;""", w)
    s, n = re.subn(r"BackColor = Color\.FromArgb\(247, 109, 20\)\s*\n(\s*)\};", r"""BackColor = Magenta
\1};
\1header.Paint += delegate(object sender, PaintEventArgs e)
\1{
\1    var r = header.ClientRectangle;
\1    if (r.Width <= 0 || r.Height <= 0) return;
\1    using (var brush = new LinearGradientBrush(r, MagentaDark, Magenta, LinearGradientMode.Horizontal))
\1        e.Graphics.FillRectangle(brush, r);
\1    using (var stripe = new SolidBrush(Amarelo))
\1        e.Graphics.FillRectangle(stripe, 0, r.Height - 6, r.Width, 6);
\1};
\1header.Resize += delegate { header.Invalidate(); };""", s)
    if n != 1:
        fail("cor do cabeçalho não encontrada")
    s = replace_once(s, "Location = new Point(24, 16),\n                Size = new Size(110, 110),",
                     "Location = new Point(22, 8),\n                Size = new Size(124, 124),", w)
    s = replace_once(s, "ForeColor = Color.White,\n                Location = new Point(155, 25),",
                     "ForeColor = Color.White,\n                BackColor = Color.Transparent,\n                Location = new Point(165, 25),", w)
    s = replace_once(s, "ForeColor = Color.White,\n                Location = new Point(158, 79),",
                     "ForeColor = Amarelo,\n                BackColor = Color.Transparent,\n                Location = new Point(168, 79),", w)
    s = s.replace("BackColor = Color.FromArgb(248, 248, 248);", "BackColor = FundoClaro;")
    s = replace_once(s, "            actions.Controls.Add(installButton);", """            installButton.FlatStyle = FlatStyle.Flat;
            installButton.BackColor = Magenta;
            installButton.ForeColor = Color.White;
            installButton.Font = new Font("Segoe UI Semibold", 9.5f, FontStyle.Bold);
            installButton.FlatAppearance.BorderSize = 0;
            installButton.FlatAppearance.MouseOverBackColor = MagentaDark;
            installButton.FlatAppearance.MouseDownBackColor = MagentaDark;
            installButton.UseVisualStyleBackColor = false;
            installButton.EnabledChanged += delegate
            {
                installButton.BackColor = installButton.Enabled ? Magenta : Color.FromArgb(225, 190, 210);
            };
            actions.Controls.Add(installButton);""", w)
    s = replace_once(s, 'Font = new Font("Segoe UI Semibold", 10f, FontStyle.Bold),\n                Location = new Point(24, 166),',
                     'Font = new Font("Segoe UI Semibold", 10f, FontStyle.Bold),\n                ForeColor = MagentaDark,\n                Location = new Point(24, 166),', w)
    # Créditos (AGPL: manter autoria original e indicar a modificação)
    s, n = re.subn(r'"\\r\\n\\r\\nImplementação independente do instalador: 3D Sorocaba\.\\r\\n" \+\s*\n'
                   r'(\s*)"Catálogos e terminologia derivados dos projetos OrcaSlicer e Orca-Flashforge\.\\r\\n" \+\s*\n'
                   r'\s*"Licença e código-fonte: github\.com/lexone/flashstudio_ptbr\\r\\n\\r\\n" \+',
                   lambda mm: (
                       '"\\r\\n\\r\\nVersão modificada e distribuída por 3D Sorocaba (3dsorocaba.com.br).\\r\\n" +\n'
                       + mm.group(1) + '"Código-fonte desta versão: github.com/' + repo + '\\r\\n" +\n'
                       + mm.group(1) + '"Baseado no projeto original de lexone / 3D Brasília: github.com/lexone/flashstudio_ptbr\\r\\n" +\n'
                       + mm.group(1) + '"Catálogos e terminologia derivados dos projetos OrcaSlicer e Orca-Flashforge.\\r\\n" +\n'
                       + mm.group(1) + '"Licença: GNU Affero General Public License v3 (AGPL-3.0).\\r\\n\\r\\n" +'), s)
    if n != 1:
        fail("texto de créditos não encontrado")
    # Botão do site ao lado de "Verificar atualizações"
    s = replace_once(s, "            ConfigureButton(backupsButton", """            var siteButton = new Button();
            ConfigureButton(siteButton, "3dsorocaba.com.br", new Point(194, 603), 140);
            siteButton.Anchor = AnchorStyles.Right | AnchorStyles.Bottom;
            siteButton.ForeColor = MagentaDark;
            siteButton.Click += delegate
            {
                try { Process.Start(new ProcessStartInfo { FileName = "https://3dsorocaba.com.br", UseShellExecute = true }); }
                catch { }
            };
            Controls.Add(siteButton);
            ConfigureButton(backupsButton""", w)
    s = s.replace('activity.Size = new Size(310, 25);', 'activity.Size = new Size(165, 25);')
    write(p, s)

    # 5) Atribuição
    attr = os.path.join(root, "ATTRIBUTION.md")
    if os.path.exists(attr):
        write(attr, read(attr) + """
## Versão 3D Sorocaba

Versão modificada do projeto original de **lexone / 3D Brasília** (https://github.com/lexone/flashstudio_ptbr),
redistribuída por **3D Sorocaba** (https://3dsorocaba.com.br) sob a GNU Affero General Public License v3.
Alterações: nome, logo, ícone e cores 3D Sorocaba; créditos; canal de atualização apontando para
https://github.com/%s. Catálogo de tradução e lógica de instalação sem alterações.
""" % repo)

    print("VERSION=" + version)
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write("version=%s\n" % version)


if __name__ == "__main__":
    main()

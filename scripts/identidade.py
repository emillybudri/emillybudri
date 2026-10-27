"""Tratamentos próprios para cada componente, unidos pela identidade Budri."""
import re

SECOES = {"manifesto", "servicos", "stack", "diferenciais", "leidodia", "telemetria"}


def aplicar(nome, svg):
    if nome not in SECOES or 'id="budri-componente"' in svg:
        return svg
    # Migra as peças diárias já geradas pela moldura anterior sem alterar dados.
    if 'id="budri-frame"' in svg:
        corpo = svg.split('<g transform="translate(30 68) scale(.94)">', 1)[1]
        corpo = corpo.split('      <rect x=".75"', 1)[0].rstrip()
        if corpo.endswith('</g>'):
            corpo = corpo[:-4]
        altura = 248 if nome == "leidodia" else 448
        abertura = svg.split('>', 1)[0]
        abertura = re.sub(r'height="\d+"', f'height="{altura}"', abertura)
        abertura = re.sub(r'viewBox="[^"]+"', f'viewBox="0 0 1000 {altura}"', abertura)
        svg = abertura + '>' + corpo + '</svg>'
    altura = int(re.search(r'viewBox="0 0 1000 (\d+)"', svg)[1])
    abertura, corpo = svg.split('>', 1)
    corpo = corpo.rsplit('</svg>', 1)[0]
    corpo = re.sub(r'<rect width="1000" height="\d+" fill="url\(#[^)]*\)"\s*/>', '', corpo)
    corpo = re.sub(r'<ellipse\b[^>]*fill="url\(#[^)]*\)"[^>]*/>', '', corpo)
    corpo = re.sub(r'<rect x="1" y="1" width="998"[^>]*/>', '', corpo)
    corpo = re.sub(r' filter="url\(#[^"]+\)"', '', corpo)
    corpo = re.sub(r'<rect class="luz[^>]+/>', '', corpo)
    corpo = corpo.replace('Jost, Century Gothic, Futura, Segoe UI, Arial, sans-serif', 'Segoe UI, Arial, sans-serif')
    topo = 0
    fundo = ''
    frente = ''
    if nome == "manifesto":
        # Composição editorial aberta: mancha orgânica à esquerda, protótipo à direita.
        fundo = f'''<path class="marca-move" d="M-50 14 C130 -43 180 48 143 137 S222 304 467 {altura} H-50Z" fill="#e9d5ff" opacity=".38"/><path d="M18 28V{altura-28}" stroke="#9333ea" stroke-width="3"/><circle class="marca-move" cx="440" cy="46" r="17" fill="none" stroke="#a677e9" stroke-opacity=".5"/>'''
    elif nome == "servicos":
        # Quatro cartões independentes, alternando superfícies e cantos.
        corpo = corpo.replace('rx="28"', 'rx="12"')
        corpo = corpo.replace('x="265" y="12" width="226" height="264" rx="12" fill="#fffdff"', 'x="265" y="12" width="226" height="264" rx="12" fill="#f3e8ff"')
        corpo = corpo.replace('x="753" y="12" width="226" height="264" rx="12" fill="#fffdff"', 'x="753" y="12" width="226" height="264" rx="12" fill="#f3e8ff"')
        frente = '<path d="M45 276h178 M289 276h178 M533 276h178 M777 276h178" stroke="#9333ea" stroke-width="3"/>'
    elif nome == "stack":
        # Janela de ferramentas, com barra de título e divisórias de categorias.
        topo = 40
        fundo = f'''<rect x="1" y="1" width="998" height="{altura+38}" rx="12" fill="#fffdff" stroke="#e9d5ff"/><path d="M1 40H999" stroke="#e9d5ff"/><g fill="#a677e9"><circle cx="24" cy="21" r="4"/><circle cx="39" cy="21" r="4" opacity=".65"/><circle cx="54" cy="21" r="4" opacity=".35"/></g><text x="500" y="25" text-anchor="middle" font-family="Consolas,monospace" font-size="11" fill="#6b7280">budri / creative-toolkit</text><path d="M188 78V{altura+12}" stroke="#e9d5ff"/>'''
    elif nome == "diferenciais":
        # Três pilares sem caixas: hierarquia tipográfica e linhas verticais.
        corpo = re.sub(r'<rect x="(?:30|350|670)" y="16" width="300" height="216"[^>]*/>', '', corpo)
        fundo = '<path d="M340 38V222 M660 38V222" stroke="#a677e9" stroke-opacity=".3"/><path d="M56 18h42 M376 18h42 M696 18h42" stroke="#9333ea" stroke-width="3"/>'
    elif nome == "leidodia":
        # Nota editorial com margem lilás e dobra no canto.
        fundo = f'''<path d="M16 1H960L999 40V{altura-1}H16Q1 {altura-1} 1 {altura-16}V16Q1 1 16 1Z" fill="#faf5ff" stroke="#e9d5ff"/><path d="M960 1V40H999" fill="#e9d5ff"/><path d="M18 20V{altura-20}" stroke="#9333ea" stroke-width="4"/>'''
    elif nome == "telemetria":
        # Painel de dados sóbrio, grade discreta e indicador de atividade.
        topo = 34
        fundo = f'''<rect x="1" y="1" width="998" height="{altura+32}" rx="16" fill="#fffdff" stroke="#e9d5ff"/><path d="M25 34H975" stroke="#e9d5ff"/><circle class="marca-pulse" cx="30" cy="18" r="3" fill="#9333ea"/><text x="42" y="22" font-size="10" letter-spacing="2" font-family="Segoe UI,Arial,sans-serif" fill="#6b7280">GITHUB / ATIVIDADE</text>'''
    total = altura + topo
    abertura = re.sub(r'height="\d+"', f'height="{total}"', abertura)
    abertura = re.sub(r'viewBox="[^"]+"', f'viewBox="0 0 1000 {total}"', abertura)
    estilo = f'''<defs><clipPath id="budri-componente"><rect width="1000" height="{total}"/></clipPath><style>
      .marca-move{{animation:marca-move 15s ease-in-out infinite}}
      .marca-pulse{{animation:marca-pulse 4s ease-in-out infinite}}
      @keyframes marca-move{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(9px,-8px)}}}}
      @keyframes marca-pulse{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
      @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style></defs>'''
    return abertura + '>' + estilo + '<g clip-path="url(#budri-componente)">' + fundo + f'<g transform="translate(0 {topo})">' + corpo + frente + '</g></g></svg>\n'

#!/usr/bin/env python3
"""Gera assets/leidodia.svg - a Lei de UX do Dia.

Toda madrugada o painel troca de lei: nome, explicacao em uma frase e um
diagrama desenhado a mao que mostra a ideia funcionando. A escolha e uma
rotacao fixa pela data: nenhuma lei repete antes de todas terem aparecido,
e o ciclo inteiro leva tantos dias quanto o tamanho da lista.
Sem API, sem dependencia externa.
"""

from datetime import datetime, timedelta, timezone

import temas

BR_TZ = timezone(timedelta(hours=-3))

ROXO, AZUL, ROSA, TINTA, SUAVE, LINHA = "#7e22ce", "#2563eb", "#db2777", "#111827", "#4b5563", "#e9d5ff"
VERDE = "#16a34a"


def pilula(x, y, w, h, cor=LINHA, fill="none", op=1):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}" '
            f'stroke="{cor}" stroke-width="1.6" opacity="{op}"/>')


# ── os diagramas ─────────────────────────────────────────────────────────
# cada um vive numa caixa de 360x166, com a origem no canto superior esquerdo

FITTS = f"""
  <g stroke-dasharray="4 5" stroke-width="1.4" fill="none" opacity=".55">
    <path d="M40 136 L108 76" stroke="{ROXO}"/>
    <path d="M40 136 L278 58" stroke="{SUAVE}"/>
  </g>
  <circle cx="120" cy="64" r="30" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="2"/>
  <circle class="pulso" cx="120" cy="64" r="30" fill="none" stroke="{ROXO}" stroke-width="2"/>
  <path d="M111 64 l6 6.5 12 -13" fill="none" stroke="{ROXO}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="288" cy="54" r="9" fill="{SUAVE}" fill-opacity=".16" stroke="{SUAVE}" stroke-width="1.8"/>
  <g class="seta"><path d="M32 128 l0 22 5.5 -6.5 5.5 12 5 -2.4 -5.5 -12 7.5 0 z" fill="{TINTA}"/></g>
  <text x="120" y="118" font-size="9.5" letter-spacing="1.4" text-anchor="middle" fill="{ROXO}">PERTO E GRANDE</text>
  <text x="288" y="80" font-size="9.5" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">LONGE E PEQUENO</text>
"""

HICK = f"""
  {''.join(pilula(24, 34 + i * 28, 116, 18, ROXO, ROXO + '22') for i in range(3))}
  {''.join(pilula(214, 22 + i * 19, 116, 13, SUAVE, 'none', .8) for i in range(6))}
  <rect class="barra" x="24" y="140" width="44" height="7" rx="3.5" fill="{ROXO}"/>
  <rect class="barra b2" x="214" y="140" width="116" height="7" rx="3.5" fill="{ROSA}"/>
  <text x="82" y="164" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{ROXO}">DECIDE RÁPIDO</text>
  <text x="272" y="164" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{ROSA}">TRAVA</text>
"""


def _tela(x, destaque=False):
    cor = ROXO if destaque else SUAVE
    op = "1" if destaque else ".55"
    return f"""
  <g opacity="{op}">
    <rect x="{x}" y="26" width="92" height="114" rx="12" fill="none" stroke="{cor}" stroke-width="1.8"/>
    <rect x="{x + 12}" y="40" width="68" height="9" rx="4.5" fill="{cor}"/>
    <rect x="{x + 12}" y="58" width="46" height="6" rx="3" fill="{cor}" opacity=".5"/>
    <rect x="{x + 12}" y="70" width="56" height="6" rx="3" fill="{cor}" opacity=".5"/>
    <rect x="{x + 12}" y="88" width="68" height="34" rx="8" fill="{cor}" opacity=".18"/>
  </g>"""


JAKOB = f"""
  {_tela(24)}{_tela(134)}{_tela(244, True)}
  <text x="290" y="158" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{ROXO}">O SEU</text>
"""

MILLER = f"""
  {''.join(f'<rect x="{24 + i * 44}" y="30" width="30" height="30" rx="8" fill="{SUAVE}" fill-opacity=".18" stroke="{SUAVE}" stroke-width="1.5"/>' for i in range(7))}
  <text x="180" y="80" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">SETE SOLTOS</text>
  <g>
    {''.join(f'<rect x="{28 + i * 34}" y="104" width="26" height="26" rx="7" fill="{ROXO}" fill-opacity=".18" stroke="{ROXO}" stroke-width="1.5"/>' for i in range(2))}
    {''.join(f'<rect x="{136 + i * 34}" y="104" width="26" height="26" rx="7" fill="{ROXO}" fill-opacity=".18" stroke="{ROXO}" stroke-width="1.5"/>' for i in range(3))}
    {''.join(f'<rect x="{278 + i * 34}" y="104" width="26" height="26" rx="7" fill="{ROXO}" fill-opacity=".18" stroke="{ROXO}" stroke-width="1.5"/>' for i in range(2))}
    <g stroke="{ROXO}" stroke-width="1.6" fill="none" opacity=".6">
      <path d="M24 138 v6 h64 v-6"/><path d="M132 138 v6 h98 v-6"/><path d="M274 138 v6 h64 v-6"/>
    </g>
  </g>
  <text x="180" y="162" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{ROXO}">TRÊS GRUPOS</text>
"""

VON_RESTORFF = f"""
  {''.join(f'<rect x="{28 + (i % 3) * 108}" y="{38 + (i // 3) * 56}" width="88" height="40" rx="12" fill="{SUAVE}" fill-opacity=".14" stroke="{SUAVE}" stroke-width="1.5" opacity=".7"/>' for i in range(6) if i != 4)}
  <g class="destaca" style="transform-origin:180px 114px">
    <rect x="136" y="94" width="88" height="40" rx="12" fill="{ROSA}" fill-opacity=".2" stroke="{ROSA}" stroke-width="2.4"/>
  </g>
  <circle class="pulso" cx="180" cy="114" r="30" fill="none" stroke="{ROSA}" stroke-width="1.6"/>
"""

ZEIGARNIK = f"""
  <rect x="28" y="60" width="304" height="16" rx="8" fill="{SUAVE}" fill-opacity=".18"/>
  <rect class="enche" x="28" y="60" width="188" height="16" rx="8" fill="{ROXO}"/>
  <text x="332" y="46" font-size="10" letter-spacing="1.2" text-anchor="end" fill="{ROXO}">62%</text>
  <g>
    {''.join(f'<circle cx="{52 + i * 64}" cy="118" r="13" fill="{ROXO}" fill-opacity=".18" stroke="{ROXO}" stroke-width="1.8"/>'
             f'<path d="M{45 + i * 64} 118 l5 5.4 9.5 -10.4" fill="none" stroke="{ROXO}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>' for i in range(3))}
    {''.join(f'<circle cx="{244 + i * 64}" cy="118" r="13" fill="none" stroke="{SUAVE}" stroke-width="1.8" stroke-dasharray="4 4"/>' for i in range(2))}
    <path d="M65 118 H231 M257 118 H295" stroke="{SUAVE}" stroke-width="1.4" opacity=".5"/>
  </g>
  <text x="180" y="152" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">FALTAM DOIS - E ISSO INCOMODA</text>
"""

PICO_FIM = f"""
  <path d="M28 130 L332 130" stroke="{SUAVE}" stroke-width="1.2" opacity=".5"/>
  <path class="curva" d="M28 112 C70 108, 84 44, 124 42 C164 40, 172 104, 214 108 C252 112, 268 96, 300 62"
        fill="none" stroke="{ROXO}" stroke-width="2.6" stroke-linecap="round"/>
  <g stroke-dasharray="4 4" stroke="{ROSA}" stroke-width="1.4" opacity=".7">
    <path d="M124 42 V130"/><path d="M300 62 V130"/>
  </g>
  <circle cx="124" cy="42" r="6" fill="{ROSA}"/>
  <circle class="pulso" cx="124" cy="42" r="6" fill="none" stroke="{ROSA}" stroke-width="1.8"/>
  <circle cx="300" cy="62" r="6" fill="{ROSA}"/>
  <text x="124" y="30" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{ROSA}">PICO</text>
  <text x="300" y="50" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{ROSA}">FIM</text>
  <text x="200" y="152" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">O MEIO QUASE NÃO CONTA</text>
"""

PROXIMIDADE = f"""
  <g fill="{ROXO}">
    {''.join(f'<circle cx="{52 + (i % 3) * 26}" cy="{56 + (i // 3) * 26}" r="7"/>' for i in range(9))}
  </g>
  <circle cx="78" cy="82" r="52" fill="none" stroke="{ROXO}" stroke-width="1.6" stroke-dasharray="5 5" opacity=".6"/>
  <g fill="{AZUL}">
    {''.join(f'<circle cx="{246 + (i % 3) * 26}" cy="{56 + (i // 3) * 26}" r="7"/>' for i in range(9))}
  </g>
  <circle cx="272" cy="82" r="52" fill="none" stroke="{AZUL}" stroke-width="1.6" stroke-dasharray="5 5" opacity=".6"/>
  <text x="180" y="88" font-size="22" font-weight="700" text-anchor="middle" fill="{SUAVE}" opacity=".45">|</text>
  <text x="180" y="156" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">DOIS GRUPOS, SEM PRECISAR DE TÍTULO</text>
"""

TESLER = f"""
  <text x="96" y="32" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">PESSOA</text>
  <text x="264" y="32" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{ROXO}">SISTEMA</text>
  <path d="M180 42 V142" stroke="{SUAVE}" stroke-width="1.4" stroke-dasharray="4 5" opacity=".55"/>
  {''.join(f'<rect x="52" y="{62 + i * 34}" width="88" height="26" rx="9" fill="{SUAVE}" fill-opacity=".16" stroke="{SUAVE}" stroke-width="1.5"/>' for i in range(2))}
  {''.join(f'<rect x="220" y="{52 + i * 34}" width="88" height="26" rx="9" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="1.5"/>' for i in range(3))}
  <g class="seta"><path d="M148 100 h22 m-7 -5 l7 5 -7 5" fill="none" stroke="{ROSA}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>
  <text x="180" y="162" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">O TRABALHO MUDA DE LADO, NÃO SOME</text>
"""

PRAGNANZ = f"""
  <g fill="none" stroke="{SUAVE}" stroke-width="1.8" opacity=".75">
    <circle cx="74" cy="68" r="26"/><circle cx="104" cy="84" r="26"/><circle cx="98" cy="50" r="20"/>
  </g>
  <g class="seta"><path d="M164 76 h32 m-10 -7 l10 7 -10 7" fill="none" stroke="{ROSA}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>
  <circle cx="272" cy="76" r="34" fill="{ROXO}" fill-opacity=".18" stroke="{ROXO}" stroke-width="2.4"/>
  <circle class="pulso" cx="272" cy="76" r="34" fill="none" stroke="{ROXO}" stroke-width="2"/>
  <text x="180" y="150" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">O OLHO PROCURA A FORMA MAIS SIMPLES</text>
"""

SIMILARIDADE = f"""
  {''.join(f'<circle cx="{62 + (i % 6) * 48}" cy="{46 + (i // 6) * 30}" r="9" fill="{ROXO if (i % 6) in (1, 4) else SUAVE}" fill-opacity="{1 if (i % 6) in (1, 4) else .3}"/>' for i in range(24))}
  <text x="180" y="156" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">A COR AGRUPA EM COLUNAS, SEM UMA LINHA SEQUER</text>
"""

REGIAO_COMUM = f"""
  <rect x="30" y="50" width="152" height="64" rx="18" fill="{ROXO}" fill-opacity=".1" stroke="{ROXO}" stroke-width="1.8"/>
  {''.join(f'<circle cx="{60 + i * 44}" cy="82" r="10" fill="{ROXO}"/>' for i in range(3))}
  {''.join(f'<circle cx="{216 + i * 44}" cy="82" r="10" fill="{SUAVE}" fill-opacity=".4"/>' for i in range(3))}
  <text x="180" y="150" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">A MOLDURA CRIA UM GRUPO SOZINHA</text>
"""

DOHERTY = f"""
  <rect x="40" y="50" width="252" height="14" rx="7" fill="{SUAVE}" fill-opacity=".18"/>
  <rect class="enche" x="40" y="50" width="66" height="14" rx="7" fill="{VERDE}"/>
  <circle cx="122" cy="57" r="11" fill="{VERDE}" fill-opacity=".18"/>
  <path d="M116 57 l4.4 4.6 8 -9" fill="none" stroke="{VERDE}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="332" y="61" font-size="10" text-anchor="end" fill="{VERDE}">0,3s</text>
  <rect x="40" y="100" width="252" height="14" rx="7" fill="{SUAVE}" fill-opacity=".18"/>
  <rect class="enche" x="40" y="100" width="214" height="14" rx="7" fill="{ROSA}"/>
  <circle cx="270" cy="107" r="11" fill="{ROSA}" fill-opacity=".18"/>
  <path d="M265 102 l10 10 M275 102 l-10 10" fill="none" stroke="{ROSA}" stroke-width="2.2" stroke-linecap="round"/>
  <text x="332" y="111" font-size="10" text-anchor="end" fill="{ROSA}">2,4s</text>
  <text x="180" y="150" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">PASSOU DE 0,4s, A ATENÇÃO JÁ FOI EMBORA</text>
"""

POSICAO_SERIAL = f"""
  {''.join(f'<rect x="66" y="{34 + i * 18}" width="234" height="12" rx="6" fill="{SUAVE}" fill-opacity=".22"/>' for i in range(1, 6))}
  <rect x="66" y="34" width="234" height="12" rx="6" fill="{ROXO}"/>
  <rect x="66" y="124" width="234" height="12" rx="6" fill="{ROXO}"/>
  <circle class="pulso" cx="48" cy="40" r="6" fill="none" stroke="{ROXO}" stroke-width="1.8"/>
  <circle cx="48" cy="40" r="4.5" fill="{ROXO}"/>
  <circle cx="48" cy="130" r="4.5" fill="{ROXO}"/>
  <text x="180" y="160" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">O COMEÇO E O FIM SÃO O QUE FICA</text>
"""

ESTETICA = f"""
  <g opacity=".5">
    <rect x="34" y="32" width="130" height="96" rx="10" fill="none" stroke="{SUAVE}" stroke-width="1.8"/>
    <rect x="48" y="48" width="70" height="10" rx="3" fill="{SUAVE}"/>
    <rect x="48" y="66" width="102" height="7" rx="3" fill="{SUAVE}" opacity=".6"/>
    <rect x="48" y="80" width="86" height="7" rx="3" fill="{SUAVE}" opacity=".6"/>
    <rect x="48" y="98" width="64" height="18" rx="4" fill="{SUAVE}" opacity=".5"/>
  </g>
  <g>
    <rect x="196" y="32" width="130" height="96" rx="18" fill="{ROXO}" fill-opacity=".08" stroke="{ROXO}" stroke-width="1.8"/>
    <rect x="212" y="48" width="70" height="10" rx="5" fill="{ROXO}"/>
    <rect x="212" y="66" width="102" height="7" rx="3.5" fill="{ROXO}" opacity=".45"/>
    <rect x="212" y="80" width="86" height="7" rx="3.5" fill="{ROXO}" opacity=".45"/>
    <rect x="212" y="98" width="64" height="18" rx="9" fill="{ROXO}"/>
  </g>
  <g class="bate" style="transform-origin:328px 38px">
    <path d="M328 44 c-5.6 -3.8 -8.2 -6.9 -8.2 -10 a4 4 0 0 1 8.2 -1.9 a4 4 0 0 1 8.2 1.9 c0 3.1 -2.6 6.2 -8.2 10 z" fill="{ROSA}"/>
  </g>
  <text x="180" y="152" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">O MESMO FLUXO PARECE MAIS FÁCIL NO BONITO</text>
"""

OCCAM = f"""
  {''.join(f'<rect x="98" y="{34 + i * 22}" width="176" height="14" rx="7" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="1.4"/>' for i in range(3))}
  {''.join(f'<rect x="98" y="{100 + i * 22}" width="176" height="14" rx="7" fill="none" stroke="{SUAVE}" stroke-width="1.4" stroke-dasharray="4 4" opacity=".6"/>' for i in range(2))}
  <g stroke="{ROSA}" stroke-width="2" stroke-linecap="round" opacity=".8">
    <path d="M70 100 l16 16 M86 100 l-16 16"/>
    <path d="M70 122 l16 16 M86 122 l-16 16"/>
  </g>
  <text x="180" y="158" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">TIRE ATÉ COMEÇAR A FAZER FALTA</text>
"""

STATUS = f"""
  <rect x="40" y="42" width="196" height="14" rx="7" fill="{SUAVE}" fill-opacity=".18"/>
  <rect class="enche" x="40" y="42" width="90" height="14" rx="7" fill="{ROXO}"/>
  <text x="248" y="53" font-size="10" fill="{ROXO}">46%</text>
  <g transform="translate(302,49)">
    <circle r="14" fill="none" stroke="{SUAVE}" stroke-width="3" opacity=".28"/>
    <path class="curva" d="M0 -14 a14 14 0 0 1 14 14" fill="none" stroke="{ROXO}" stroke-width="3" stroke-linecap="round"/>
  </g>
  <rect x="40" y="88" width="280" height="40" rx="14" fill="{VERDE}" fill-opacity=".12" stroke="{VERDE}" stroke-width="1.5"/>
  <circle cx="68" cy="108" r="11" fill="{VERDE}" fill-opacity=".2"/>
  <path d="M62 108 l4.4 4.6 8 -9" fill="none" stroke="{VERDE}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="90" y="102" width="124" height="9" rx="4.5" fill="{VERDE}" opacity=".5"/>
  <rect x="90" y="116" width="82" height="7" rx="3.5" fill="{VERDE}" opacity=".3"/>
  <text x="180" y="156" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">A PESSOA NUNCA FICA NO ESCURO</text>
"""

PREVENIR = f"""
  <rect x="30" y="44" width="142" height="34" rx="10" fill="none" stroke="{VERDE}" stroke-width="1.8"/>
  <rect x="44" y="56" width="76" height="9" rx="4.5" fill="{VERDE}" opacity=".45"/>
  <circle cx="150" cy="61" r="9" fill="{VERDE}" fill-opacity=".2"/>
  <path d="M145 61 l3.6 3.8 6.6 -7.4" fill="none" stroke="{VERDE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="30" y="98" font-size="8.5" letter-spacing="1.2" fill="{VERDE}">AVISA ENQUANTO SE DIGITA</text>
  <rect x="196" y="44" width="142" height="34" rx="10" fill="none" stroke="{ROSA}" stroke-width="1.8"/>
  <rect x="210" y="56" width="76" height="9" rx="4.5" fill="{ROSA}" opacity=".45"/>
  <circle cx="316" cy="61" r="9" fill="{ROSA}" fill-opacity=".2"/>
  <path d="M312 57 l8 8 M320 57 l-8 8" fill="none" stroke="{ROSA}" stroke-width="2" stroke-linecap="round"/>
  <text x="196" y="98" font-size="8.5" letter-spacing="1.2" fill="{ROSA}">RECLAMA DEPOIS DE ENVIAR</text>
  <text x="180" y="142" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">ERRO EVITADO VALE MAIS QUE ERRO EXPLICADO</text>
"""

RECONHECER = f"""
  <rect x="32" y="50" width="140" height="34" rx="10" fill="none" stroke="{SUAVE}" stroke-width="1.8" opacity=".65"/>
  <rect class="cur" x="46" y="58" width="6" height="18" fill="{SUAVE}"/>
  <text x="102" y="118" font-size="24" font-weight="700" text-anchor="middle" fill="{SUAVE}" opacity=".4">?</text>
  <rect x="196" y="40" width="142" height="30" rx="10" fill="{ROXO}" fill-opacity=".12" stroke="{ROXO}" stroke-width="1.8"/>
  <path d="M316 51 l6 7 6 -7" fill="none" stroke="{ROXO}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  {''.join(f'<rect x="196" y="{78 + i * 22}" width="142" height="16" rx="6" fill="{ROXO}" fill-opacity="{.2 - i * 0.05}"/>' for i in range(3))}
  <text x="180" y="152" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">MOSTRE AS OPÇÕES EM VEZ DE COBRAR MEMÓRIA</text>
"""

DESFAZER = f"""
  <rect x="60" y="36" width="240" height="34" rx="10" fill="{SUAVE}" fill-opacity=".16"/>
  <rect x="76" y="48" width="120" height="10" rx="5" fill="{SUAVE}" opacity=".5"/>
  <g stroke="{ROSA}" stroke-width="2" stroke-linecap="round">
    <path d="M266 47 l12 12 M278 47 l-12 12"/>
  </g>
  <rect x="60" y="90" width="240" height="42" rx="14" fill="{ROXO}" fill-opacity=".14" stroke="{ROXO}" stroke-width="1.8"/>
  <path d="M98 111 h-14 m6 -6 l-6 6 6 6" fill="none" stroke="{ROXO}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="114" y="115" font-size="11" letter-spacing="1.6" fill="{ROXO}">DESFAZER</text>
  <text x="180" y="158" font-size="9" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">TODA AÇÃO PRECISA DE UM CAMINHO DE VOLTA</text>
"""

# ── primitivas de diagrama ───────────────────────────────────────────────
# O cânone de UX tem dezenas de princípios e quase todos se explicam com o
# mesmo punhado de formas: comparar dois lados, agrupar pontos, destacar item
# de uma lista, encher uma barra. Montar cada diagrama a partir daqui mantém a
# família visual e evita repetir marcação.

def legenda(t, y=158):
    return (f'<text x="180" y="{y}" font-size="9" letter-spacing="1.4" '
            f'text-anchor="middle" fill="{SUAVE}">{t}</text>')


def rotulo(x, t, cor=SUAVE, y=34):
    return (f'<text x="{x}" y="{y}" font-size="9" letter-spacing="1.4" '
            f'text-anchor="middle" fill="{cor}">{t}</text>')


def divisor(y1=42, y2=140):
    return (f'<path d="M180 {y1} V{y2}" stroke="{SUAVE}" stroke-width="1.4" '
            f'stroke-dasharray="4 5" opacity=".5"/>')


def seta(x1, y, x2, cor=ROSA):
    return (f'<g class="seta"><path d="M{x1} {y} H{x2} m-8 -6 l8 6 -8 6" fill="none" '
            f'stroke="{cor}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>')


def caixa(x, y, w, h, cor=SUAVE, op=".12", r=12, tracejada=False, sw=1.6):
    d = ' stroke-dasharray="5 5"' if tracejada else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{cor}" '
            f'fill-opacity="{op}" stroke="{cor}" stroke-width="{sw}"{d}/>')


def barra_h(x, y, w, pct, cor=ROXO, h=14):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{SUAVE}" fill-opacity=".18"/>'
            f'<rect class="enche" x="{x}" y="{y}" width="{round(w * pct)}" height="{h}" rx="{h / 2}" fill="{cor}"/>')


def linhas(x, y, n, w=150, passo=18, alt=11, cor=SUAVE, op=".28", destaque=(), cor_d=None):
    cor_d = cor_d or ROXO
    saida = []
    for i in range(n):
        forte = i in destaque
        saida.append(f'<rect x="{x}" y="{y + i * passo}" width="{w}" height="{alt}" rx="{alt / 2}" '
                     f'fill="{cor_d if forte else cor}" fill-opacity="{1 if forte else op}"/>')
    return "".join(saida)


def pontos(x0, y0, cols, rows, passo=30, r=8, destaque=None, cor=SUAVE, cor_d=None):
    cor_d = cor_d or ROXO
    destaque = destaque or (lambda c, l: False)
    saida = []
    for l in range(rows):
        for c in range(cols):
            forte = destaque(c, l)
            saida.append(f'<circle cx="{x0 + c * passo}" cy="{y0 + l * passo}" r="{r}" '
                         f'fill="{cor_d if forte else cor}" fill-opacity="{1 if forte else .3}"/>')
    return "".join(saida)


def certo(cx, cy, cor=None, r=11):
    cor = cor or VERDE
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cor}" fill-opacity=".18"/>'
            f'<path d="M{cx - 5.4} {cy} l4.4 4.6 8 -9" fill="none" stroke="{cor}" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


def errado(cx, cy, cor=None, r=11):
    cor = cor or ROSA
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cor}" fill-opacity=".18"/>'
            f'<path d="M{cx - 5} {cy - 5} l10 10 M{cx + 5} {cy - 5} l-10 10" fill="none" '
            f'stroke="{cor}" stroke-width="2.2" stroke-linecap="round"/>')


def dedo(x, y, cor=None):
    cor = cor or TINTA
    return f'<g class="seta"><path d="M{x} {y} l0 22 5.5 -6.5 5.5 12 5 -2.4 -5.5 -12 7.5 0 z" fill="{cor}"/></g>'


def cartao(x, y, w=132, h=96, cor=None, apagado=False):
    """Uma telinha genérica: cabeçalho, duas linhas e um botão."""
    cor = cor or ROXO
    op = ".45" if apagado else "1"
    return f"""
  <g opacity="{op}">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{cor}" stroke-width="1.8"/>
    <rect x="{x + 14}" y="{y + 16}" width="{w - 60}" height="10" rx="5" fill="{cor}"/>
    <rect x="{x + 14}" y="{y + 34}" width="{w - 30}" height="7" rx="3.5" fill="{cor}" opacity=".45"/>
    <rect x="{x + 14}" y="{y + 48}" width="{w - 46}" height="7" rx="3.5" fill="{cor}" opacity=".45"/>
    <rect x="{x + 14}" y="{y + 66}" width="{w - 68}" height="16" rx="8" fill="{cor}" opacity=".75"/>
  </g>"""


# ── os diagramas do cânone ───────────────────────────────────────────────

CARGA = f"""
  {linhas(40, 34, 7, 120, passo=15, alt=9, cor=ROSA, op=".5")}
  {rotulo(100, "TUDO DE UMA VEZ", ROSA, 154)}
  {divisor(30, 140)}
  {linhas(220, 52, 3, 120, passo=24, alt=11, cor=ROXO, op="1")}
  {rotulo(280, "SÓ O QUE IMPORTA AGORA", ROXO, 154)}
"""

CHUNKING = f"""
  <text x="180" y="52" font-size="20" letter-spacing="3" text-anchor="middle" fill="{SUAVE}" font-family="SFMono-Regular, Consolas, monospace">11987654321</text>
  {rotulo(180, "ILEGÍVEL", SUAVE, 74)}
  {seta(150, 96, 210)}
  <text x="180" y="132" font-size="20" letter-spacing="3" text-anchor="middle" fill="{ROXO}" font-family="SFMono-Regular, Consolas, monospace">11 98765-4321</text>
  {legenda("O MESMO NÚMERO, EM PEDAÇOS QUE A CABEÇA SEGURA")}
"""

FLOW = f"""
  <path d="M28 130 L332 130" stroke="{SUAVE}" stroke-width="1.2" opacity=".4"/>
  <path class="curva" d="M34 126 C90 120, 120 60, 180 58 C240 56, 272 100, 328 44"
        fill="none" stroke="{ROXO}" stroke-width="2.6" stroke-linecap="round"/>
  {caixa(120, 44, 120, 60, ROXO, ".1", 14, True)}
  {rotulo(180, "ZONA DE FLUXO", ROXO, 40)}
  {legenda("DESAFIO E HABILIDADE EM EQUILÍBRIO")}
"""

GOAL_GRADIENT = f"""
  {''.join(f'<circle cx="{54 + i * 52}" cy="70" r="14" fill="{ROXO}" fill-opacity="{.14 + i * 0.17}" stroke="{ROXO}" stroke-width="1.8"/>' for i in range(6))}
  <path d="M68 70 H92 M120 70 H144 M172 70 H196 M224 70 H248 M276 70 H300" stroke="{ROXO}" stroke-width="1.4" opacity=".4"/>
  {certo(314, 70, ROXO)}
  {legenda("QUANTO MAIS PERTO DO FIM, MAIS RÁPIDO O PASSO", 120)}
  {legenda("POR ISSO O CARTÃO JÁ COMEÇA COM UM SELO", 142)}
"""

CONEXAO_UNIFORME = f"""
  {pontos(60, 56, 3, 2, 34, 8, lambda c, l: True, cor_d=ROXO)}
  <path d="M60 56 H128 M60 90 H128" stroke="{ROXO}" stroke-width="2.4" opacity=".55"/>
  {pontos(232, 56, 3, 2, 34, 8)}
  {rotulo(94, "CONECTADO", ROXO, 126)}
  {rotulo(266, "SOLTO", SUAVE, 126)}
  {legenda("A LINHA UNE MAIS FORTE QUE A DISTÂNCIA", 154)}
"""

MODELO_MENTAL = f"""
  {cartao(28, 36, 132, 96, SUAVE, True)}
  {seta(174, 84, 200)}
  {cartao(212, 36, 132, 96, ROXO)}
  {rotulo(94, "O QUE A PESSOA ESPERA", SUAVE, 150)}
  {rotulo(278, "O QUE VOCÊ ENTREGA", ROXO, 150)}
"""

PARADOXO_ATIVO = f"""
  {caixa(30, 40, 140, 96, SUAVE, ".1", 14)}
  {rotulo(100, "MANUAL FECHADO", SUAVE, 62)}
  <path d="M76 78 h48 v34 h-48 z M76 78 l24 -14 24 14" fill="none" stroke="{SUAVE}" stroke-width="1.8" stroke-linejoin="round" opacity=".7"/>
  {caixa(190, 40, 140, 96, ROXO, ".1", 14)}
  {rotulo(260, "JÁ CLICANDO", ROXO, 62)}
  {dedo(252, 76, ROXO)}
  {legenda("NINGUÉM LÊ ANTES: A INTERFACE PRECISA ENSINAR NO CAMINHO")}
"""

PARETO = f"""
  {''.join(f'<rect x="{40 + i * 26}" y="{120 - (58 if i < 2 else 14)}" width="18" height="{58 if i < 2 else 14}" rx="5" fill="{ROXO if i < 2 else SUAVE}" fill-opacity="{1 if i < 2 else .3}"/>' for i in range(10))}
  <path d="M34 120 H316" stroke="{SUAVE}" stroke-width="1.2" opacity=".5"/>
  {rotulo(64, "20% DAS TELAS", ROXO, 48)}
  {rotulo(230, "O RESTO", SUAVE, 48)}
  {legenda("CARREGAM 80% DO USO: É NELAS QUE O CAPRICHO RENDE", 146)}
"""

PARKINSON = f"""
  {barra_h(40, 50, 280, 1.0, ROSA)}
  {rotulo(180, "PRAZO DE DUAS SEMANAS: LEVA DUAS SEMANAS", ROSA, 82)}
  {barra_h(40, 100, 280, 0.32, VERDE)}
  {rotulo(180, "PRAZO DE TRÊS DIAS: LEVA TRÊS DIAS", VERDE, 132)}
  {legenda("O TRABALHO SE ESPALHA ATÉ PREENCHER O TEMPO DADO")}
"""

POSTEL = f"""
  {caixa(28, 46, 130, 74, VERDE, ".1", 14)}
  <text x="93" y="78" font-size="11" text-anchor="middle" fill="{VERDE}" font-family="SFMono-Regular, Consolas, monospace">(11) 9 8765</text>
  <text x="93" y="98" font-size="11" text-anchor="middle" fill="{VERDE}" font-family="SFMono-Regular, Consolas, monospace">11987654321</text>
  {seta(170, 84, 200)}
  {caixa(212, 46, 130, 74, ROXO, ".12", 14)}
  <text x="277" y="90" font-size="12" text-anchor="middle" fill="{ROXO}" font-family="SFMono-Regular, Consolas, monospace">11987654321</text>
  {rotulo(93, "ACEITE TORTO", VERDE, 140)}
  {rotulo(277, "GUARDE RETO", ROXO, 140)}
"""

ATENCAO_SELETIVA = f"""
  {caixa(30, 34, 300, 100, SUAVE, ".08", 14)}
  {linhas(48, 50, 3, 180, passo=20, alt=10, cor=SUAVE, op=".35")}
  <rect x="248" y="46" width="66" height="34" rx="8" fill="{ROSA}" fill-opacity=".2" stroke="{ROSA}" stroke-width="1.6" stroke-dasharray="4 4"/>
  <text x="281" y="67" font-size="8" letter-spacing="1" text-anchor="middle" fill="{ROSA}">ANÚNCIO</text>
  <path d="M244 42 l76 44 M320 42 l-76 44" stroke="{ROSA}" stroke-width="1.6" opacity=".5"/>
  {linhas(48, 108, 1, 180, alt=10, cor=ROXO, op="1", destaque=(0,))}
  {legenda("O QUE PARECE PROPAGANDA VIRA INVISÍVEL")}
"""

MUNDO_REAL = f"""
  {caixa(30, 44, 140, 76, ROSA, ".1", 14)}
  <text x="100" y="90" font-size="11" text-anchor="middle" fill="{ROSA}" font-family="SFMono-Regular, Consolas, monospace">ERR_TX_0x2F</text>
  {seta(182, 82, 208)}
  {caixa(220, 44, 118, 76, VERDE, ".1", 14)}
  <text x="279" y="78" font-size="10" text-anchor="middle" fill="{VERDE}">Cartão</text>
  <text x="279" y="96" font-size="10" text-anchor="middle" fill="{VERDE}">recusado</text>
  {legenda("FALE A LÍNGUA DE QUEM USA, NÃO A DO BANCO DE DADOS", 146)}
"""

CONSISTENCIA = f"""
  {''.join(f'<rect x="{34 + i * 78}" y="52" width="62" height="30" rx="15" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="1.6"/>' for i in range(3))}
  <rect x="268" y="52" width="62" height="30" rx="4" fill="{ROSA}" fill-opacity=".16" stroke="{ROSA}" stroke-width="1.6" stroke-dasharray="4 4"/>
  {errado(299, 100)}
  {legenda("O MESMO BOTÃO NÃO PODE MUDAR DE CARA A CADA TELA", 138)}
"""

ATALHOS = f"""
  {linhas(40, 40, 4, 150, passo=22, alt=12, cor=SUAVE, op=".3")}
  {rotulo(115, "CAMINHO LONGO", SUAVE, 140)}
  {divisor(34, 128)}
  <rect x="210" y="60" width="52" height="30" rx="8" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="1.6"/>
  <text x="236" y="80" font-size="11" text-anchor="middle" fill="{ROXO}" font-family="SFMono-Regular, Consolas, monospace">Ctrl</text>
  <rect x="272" y="60" width="52" height="30" rx="8" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="1.6"/>
  <text x="298" y="80" font-size="11" text-anchor="middle" fill="{ROXO}" font-family="SFMono-Regular, Consolas, monospace">K</text>
  {rotulo(267, "ATALHO PARA QUEM JÁ SABE", ROXO, 140)}
"""

MINIMALISMO = f"""
  {linhas(40, 34, 6, 118, passo=17, alt=10, cor=SUAVE, op=".3")}
  {rotulo(99, "TUDO NA TELA", SUAVE, 152)}
  {seta(190, 84, 216)}
  {linhas(246, 60, 3, 84, passo=22, alt=11, cor=ROXO, op="1", destaque=(0, 1, 2))}
  {rotulo(288, "SÓ O ESSENCIAL", ROXO, 152)}
"""

RECUPERAR_ERRO = f"""
  {caixa(30, 40, 300, 60, ROSA, ".1", 14)}
  {errado(60, 70)}
  <text x="84" y="64" font-size="10.5" fill="{ROSA}">A senha precisa de 8 caracteres</text>
  <text x="84" y="84" font-size="10" fill="{SUAVE}">Você digitou 5. Faltam 3.</text>
  <rect x="30" y="112" width="130" height="30" rx="15" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="1.6"/>
  <text x="95" y="132" font-size="10.5" letter-spacing="1.2" text-anchor="middle" fill="{ROXO}">CORRIGIR AGORA</text>
  {legenda("DIGA O QUE HOUVE, EM LÍNGUA DE GENTE, E COMO SAIR", 160)}
"""

AJUDA = f"""
  {caixa(30, 44, 130, 76, SUAVE, ".08", 14)}
  <circle cx="95" cy="76" r="16" fill="none" stroke="{SUAVE}" stroke-width="1.8"/>
  <text x="95" y="83" font-size="18" font-weight="700" text-anchor="middle" fill="{SUAVE}">?</text>
  {rotulo(95, "ESCONDIDA NO RODAPÉ", SUAVE, 138)}
  {caixa(200, 44, 138, 76, ROXO, ".1", 14)}
  <rect x="214" y="58" width="90" height="10" rx="5" fill="{ROXO}"/>
  <rect x="214" y="76" width="110" height="7" rx="3.5" fill="{ROXO}" opacity=".45"/>
  <rect x="214" y="90" width="80" height="7" rx="3.5" fill="{ROXO}" opacity=".45"/>
  {rotulo(269, "AO LADO DO CAMPO DIFÍCIL", ROXO, 138)}
"""

FECHAMENTO = f"""
  <g fill="none" stroke="{ROXO}" stroke-width="3" stroke-linecap="round">
    <path d="M120 44 a44 44 0 0 1 38 22"/>
    <path d="M164 88 a44 44 0 0 1 -22 38"/>
    <path d="M120 132 a44 44 0 0 1 -38 -22"/>
    <path d="M76 88 a44 44 0 0 1 22 -38"/>
  </g>
  {seta(196, 88, 222)}
  <circle cx="278" cy="88" r="44" fill="{ROXO}" fill-opacity=".16" stroke="{ROXO}" stroke-width="2"/>
  {legenda("A CABEÇA FECHA O QUE FALTA SOZINHA", 152)}
"""

CONTINUIDADE = f"""
  <path class="curva" d="M30 110 C90 110, 110 50, 180 50 C250 50, 270 110, 330 110"
        fill="none" stroke="{ROXO}" stroke-width="2.4" opacity=".35"/>
  {''.join(f'<circle cx="{34 + i * 27}" cy="{110 - int(60 * (1 - ((i - 5.5) / 5.5) ** 2))}" r="7" fill="{ROXO}"/>' for i in range(12))}
  {legenda("PONTOS EM LINHA VIRAM UM CAMINHO SÓ", 148)}
"""

FIGURA_FUNDO = f"""
  <rect x="60" y="34" width="240" height="100" rx="16" fill="{SUAVE}" fill-opacity=".16"/>
  {cartao(112, 50, 136, 68, ROXO)}
  <rect x="60" y="34" width="240" height="100" rx="16" fill="none" stroke="{SUAVE}" stroke-width="1.4" opacity=".5"/>
  {legenda("O QUE ESTÁ NA FRENTE PEDE A ATENÇÃO; O RESTO RECUA")}
"""

DESTINO_COMUM = f"""
  {pontos(60, 56, 3, 2, 34, 8, lambda c, l: True, cor_d=ROXO)}
  <g stroke="{ROXO}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".7">
    {''.join(f'<path d="M{72 + c * 34} {50 + l * 34} h16 m-6 -5 l6 5 -6 5"/>' for c in range(3) for l in range(2))}
  </g>
  {pontos(244, 56, 2, 2, 34, 8)}
  {legenda("QUEM SE MOVE JUNTO É LIDO COMO UM GRUPO", 132)}
"""

SIMETRIA = f"""
  {divisor(38, 142)}
  {cartao(34, 44, 126, 92, ROXO)}
  {cartao(200, 44, 126, 92, ROXO)}
  {legenda("O ARRANJO SIMÉTRICO É PROCESSADO MAIS RÁPIDO")}
"""

AFFORDANCE = f"""
  <rect x="34" y="56" width="128" height="36" rx="18" fill="{ROXO}" fill-opacity=".18" stroke="{ROXO}" stroke-width="2"/>
  <text x="98" y="79" font-size="11" letter-spacing="1.4" text-anchor="middle" fill="{ROXO}">COMPRAR</text>
  {rotulo(98, "PARECE BOTÃO", ROXO, 122)}
  <text x="262" y="79" font-size="11" letter-spacing="1.4" text-anchor="middle" fill="{SUAVE}">COMPRAR</text>
  {rotulo(262, "PARECE TEXTO", SUAVE, 122)}
  {legenda("A FORMA JÁ CONTA O QUE DÁ PARA FAZER", 150)}
"""

SIGNIFICANTES = f"""
  {caixa(30, 46, 140, 74, SUAVE, ".08", 14)}
  <rect x="46" y="70" width="108" height="26" rx="6" fill="{SUAVE}" fill-opacity=".2"/>
  {rotulo(100, "ARRASTA? CLICA?", SUAVE, 136)}
  {caixa(196, 46, 140, 74, ROXO, ".1", 14)}
  <rect x="212" y="70" width="108" height="26" rx="6" fill="{ROXO}" fill-opacity=".18"/>
  <g stroke="{ROXO}" stroke-width="2" stroke-linecap="round">
    <path d="M226 79 h8 M226 85 h8 M226 91 h8"/>
  </g>
  {rotulo(266, "A PEGA DIZ: ARRASTE", ROXO, 136)}
"""

MAPEAMENTO = f"""
  {pontos(66, 52, 2, 2, 34, 11, lambda c, l: True, cor_d=SUAVE)}
  {rotulo(83, "BOCAS", SUAVE, 30)}
  {''.join(f'<rect x="{50 + i * 26}" y="106" width="16" height="16" rx="8" fill="{ROSA}" fill-opacity=".5"/>' for i in range(4))}
  {rotulo(88, "BOTÕES EM FILA", ROSA, 140)}
  {divisor(30, 144)}
  {pontos(238, 52, 2, 2, 34, 11, lambda c, l: True, cor_d=ROXO)}
  {''.join(f'<rect x="{230 + (i % 2) * 34 - 8}" y="{104 + (i // 2) * 18}" width="16" height="12" rx="6" fill="{ROXO}"/>' for i in range(4))}
  {rotulo(272, "BOTÕES NO MESMO ARRANJO", ROXO, 148)}
"""

FEEDBACK = f"""
  <rect x="40" y="46" width="120" height="34" rx="17" fill="{SUAVE}" fill-opacity=".16" stroke="{SUAVE}" stroke-width="1.6"/>
  <text x="100" y="68" font-size="10.5" letter-spacing="1.2" text-anchor="middle" fill="{SUAVE}">ENVIAR</text>
  {rotulo(100, "NADA ACONTECE", SUAVE, 100)}
  {seta(176, 62, 202)}
  <rect x="216" y="46" width="120" height="34" rx="17" fill="{ROXO}" fill-opacity=".18" stroke="{ROXO}" stroke-width="1.6"/>
  <text x="276" y="68" font-size="10.5" letter-spacing="1.2" text-anchor="middle" fill="{ROXO}">ENVIANDO…</text>
  {certo(276, 108)}
  {legenda("TODA AÇÃO PRECISA DE UMA RESPOSTA VISÍVEL", 146)}
"""

RESTRICOES = f"""
  {caixa(30, 46, 140, 60, ROSA, ".08", 12)}
  <text x="100" y="82" font-size="11" text-anchor="middle" fill="{ROSA}" font-family="SFMono-Regular, Consolas, monospace">32/13/2026</text>
  {rotulo(100, "CAMPO LIVRE ACEITA TUDO", ROSA, 124)}
  {caixa(196, 46, 140, 60, ROXO, ".1", 12)}
  {''.join(f'<rect x="{210 + (i % 5) * 24}" y="{58 + (i // 5) * 20}" width="18" height="14" rx="4" fill="{ROXO}" fill-opacity=".3"/>' for i in range(10))}
  {rotulo(266, "CALENDÁRIO SÓ DEIXA O QUE EXISTE", ROXO, 124)}
"""

ANCORAGEM = f"""
  <text x="110" y="74" font-size="20" font-weight="700" text-anchor="middle" fill="{SUAVE}" opacity=".55">R$ 499</text>
  <path d="M70 68 H150" stroke="{ROSA}" stroke-width="2.4" stroke-linecap="round"/>
  <text x="110" y="106" font-size="26" font-weight="700" text-anchor="middle" fill="{ROXO}">R$ 299</text>
  {divisor(40, 130)}
  <text x="262" y="92" font-size="26" font-weight="700" text-anchor="middle" fill="{SUAVE}" opacity=".6">R$ 299</text>
  {rotulo(110, "PARECE BARATO", ROXO, 142)}
  {rotulo(262, "PARECE CARO", SUAVE, 142)}
"""

AVERSAO_PERDA = f"""
  {caixa(30, 46, 140, 64, SUAVE, ".1", 14)}
  <text x="100" y="84" font-size="11" text-anchor="middle" fill="{SUAVE}">Ganhe R$ 20</text>
  {caixa(196, 46, 140, 64, ROXO, ".12", 14)}
  <text x="266" y="84" font-size="11" text-anchor="middle" fill="{ROXO}">Não perca R$ 20</text>
  <path d="M266 118 v14 m-6 -6 l6 6 6 -6" fill="none" stroke="{ROXO}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  {legenda("PERDER DÓI MAIS DO QUE GANHAR AGRADA")}
"""

PROVA_SOCIAL = f"""
  {''.join(f'<circle cx="{62 + i * 26}" cy="62" r="14" fill="{ROXO}" fill-opacity="{.5 - i * 0.08}" stroke="{ROXO}" stroke-width="1.4"/>' for i in range(4))}
  <text x="196" y="67" font-size="12" fill="{ROXO}">+2.480 pessoas</text>
  {''.join(f'<path d="M{60 + i * 22} 108 l4 8 9 1 -6.5 6 1.5 9 -8 -4.5 -8 4.5 1.5 -9 -6.5 -6 9 -1 z" fill="{ROXO}" opacity=".8"/>' for i in range(5))}
  <text x="196" y="116" font-size="12" fill="{SUAVE}">4,8 de 5</text>
  {legenda("A ESCOLHA DOS OUTROS É ATALHO PARA A NOSSA")}
"""

ESCASSEZ = f"""
  {''.join(f'<rect x="{56 + i * 46}" y="52" width="34" height="34" rx="8" fill="{SUAVE}" fill-opacity=".18"/>' for i in range(5))}
  <rect x="56" y="52" width="34" height="34" rx="8" fill="{ROSA}" fill-opacity=".3" stroke="{ROSA}" stroke-width="1.8"/>
  <text x="180" y="118" font-size="11" letter-spacing="1.2" text-anchor="middle" fill="{ROSA}">RESTA 1 EM ESTOQUE</text>
  {legenda("O QUE É RARO PARECE VALER MAIS - SE FOR VERDADE")}
"""

PADRAO = f"""
  {caixa(40, 44, 130, 76, SUAVE, ".08", 14)}
  <circle cx="66" cy="70" r="9" fill="none" stroke="{SUAVE}" stroke-width="2"/>
  <circle cx="66" cy="98" r="9" fill="none" stroke="{SUAVE}" stroke-width="2"/>
  {rotulo(105, "NADA MARCADO", SUAVE, 138)}
  {caixa(196, 44, 130, 76, ROXO, ".1", 14)}
  <circle cx="222" cy="70" r="9" fill="{ROXO}" fill-opacity=".25" stroke="{ROXO}" stroke-width="2"/>
  <circle cx="222" cy="70" r="4" fill="{ROXO}"/>
  <circle cx="222" cy="98" r="9" fill="none" stroke="{ROXO}" stroke-width="2" opacity=".4"/>
  {rotulo(261, "A MAIORIA FICA NO PADRÃO", ROXO, 138)}
"""

ISCA = f"""
  {caixa(24, 44, 96, 84, SUAVE, ".1", 14)}
  <text x="72" y="80" font-size="16" font-weight="700" text-anchor="middle" fill="{SUAVE}">R$ 19</text>
  {rotulo(72, "BÁSICO", SUAVE, 104)}
  {caixa(132, 44, 96, 84, SUAVE, ".06", 14, True)}
  <text x="180" y="80" font-size="16" font-weight="700" text-anchor="middle" fill="{SUAVE}" opacity=".7">R$ 38</text>
  {rotulo(180, "A ISCA", SUAVE, 104)}
  {caixa(240, 44, 96, 84, ROXO, ".14", 14)}
  <text x="288" y="80" font-size="16" font-weight="700" text-anchor="middle" fill="{ROXO}">R$ 39</text>
  {rotulo(288, "O ESCOLHIDO", ROXO, 104)}
  {legenda("A OPÇÃO DO MEIO EXISTE PARA VALORIZAR A TERCEIRA", 150)}
"""

RECIPROCIDADE = f"""
  {caixa(30, 46, 132, 70, ROXO, ".12", 14)}
  <text x="96" y="80" font-size="10.5" text-anchor="middle" fill="{ROXO}">Guia grátis</text>
  <path d="M176 74 h30 m-9 -6 l9 6 -9 6" fill="none" stroke="{ROXO}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M206 96 h-30 m9 -6 l-9 6 9 6" fill="none" stroke="{ROSA}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  {caixa(220, 46, 116, 70, ROSA, ".12", 14)}
  <text x="278" y="80" font-size="10.5" text-anchor="middle" fill="{ROSA}">E-mail</text>
  {legenda("QUEM RECEBE PRIMEIRO SE SENTE EM DÍVIDA", 146)}
"""

IKEA = f"""
  {linhas(46, 44, 3, 116, passo=22, alt=12, cor=ROXO, op="1", destaque=(0, 1, 2))}
  {dedo(174, 60, ROSA)}
  {caixa(216, 44, 120, 70, AZUL, ".14", 14)}
  <text x="276" y="86" font-size="11" text-anchor="middle" fill="{AZUL}">O SEU PERFIL</text>
  {legenda("O QUE A PESSOA AJUDA A MONTAR ELA PASSA A DEFENDER", 146)}
"""

CUSTO_IRRECUPERAVEL = f"""
  {''.join(f'<circle cx="{70 + i * 48}" cy="70" r="13" fill="{ROXO}" fill-opacity="{.9 if i < 4 else .15}" stroke="{ROXO}" stroke-width="1.6"/>' for i in range(5))}
  <path d="M83 70 H105 M131 70 H153 M179 70 H201 M227 70 H249" stroke="{ROXO}" stroke-width="1.4" opacity=".4"/>
  <text x="180" y="112" font-size="11" letter-spacing="1.2" text-anchor="middle" fill="{ROXO}">FALTA SÓ 1 DE 5</text>
  {legenda("MOSTRAR O QUE JÁ FOI FEITO SEGURA QUEM IA DESISTIR")}
"""

ENQUADRAMENTO = f"""
  {caixa(30, 46, 140, 64, VERDE, ".1", 14)}
  <text x="100" y="84" font-size="11" text-anchor="middle" fill="{VERDE}">90% aprovado</text>
  {caixa(196, 46, 140, 64, ROSA, ".1", 14)}
  <text x="266" y="84" font-size="11" text-anchor="middle" fill="{ROSA}">10% recusado</text>
  {legenda("O MESMO NÚMERO, DUAS SENSAÇÕES DIFERENTES", 140)}
"""

CONTRASTE = f"""
  <rect x="30" y="44" width="140" height="76" rx="14" fill="#f0e6fd"/>
  <text x="100" y="88" font-size="13" text-anchor="middle" fill="#c8b6e4">texto claro</text>
  {errado(100, 136)}
  <rect x="196" y="44" width="140" height="76" rx="14" fill="#f0e6fd"/>
  <text x="266" y="88" font-size="13" font-weight="700" text-anchor="middle" fill="{TINTA}">texto legível</text>
  {certo(266, 136)}
  {rotulo(100, "2,1:1", SUAVE, 36)}
  {rotulo(266, "4,5:1 OU MAIS", VERDE, 36)}
"""

TECLADO = f"""
  {linhas(60, 44, 4, 160, passo=24, alt=14, cor=SUAVE, op=".25")}
  <rect x="56" y="88" width="168" height="22" rx="11" fill="none" stroke="{ROXO}" stroke-width="2.4"/>
  <rect x="252" y="60" width="66" height="34" rx="8" fill="{ROXO}" fill-opacity=".14" stroke="{ROXO}" stroke-width="1.6"/>
  <text x="285" y="82" font-size="10.5" text-anchor="middle" fill="{ROXO}" font-family="SFMono-Regular, Consolas, monospace">Tab</text>
  {legenda("O FOCO PRECISA APARECER PARA QUEM NÃO USA MOUSE", 146)}
"""

PERCEPTIVEL = f"""
  <rect x="34" y="44" width="128" height="76" rx="14" fill="{SUAVE}" fill-opacity=".18"/>
  <path d="M52 106 l26 -30 20 22 16 -14 22 22" fill="none" stroke="{SUAVE}" stroke-width="2" stroke-linejoin="round" opacity=".6"/>
  {rotulo(98, "SEM DESCRIÇÃO", SUAVE, 138)}
  <rect x="198" y="44" width="128" height="76" rx="14" fill="{ROXO}" fill-opacity=".12"/>
  <path d="M216 106 l26 -30 20 22 16 -14 22 22" fill="none" stroke="{ROXO}" stroke-width="2" stroke-linejoin="round"/>
  <rect x="198" y="126" width="128" height="9" rx="4.5" fill="{ROXO}" opacity=".5"/>
  {rotulo(262, "COM TEXTO ALTERNATIVO", ROXO, 150)}
"""

DIVULGACAO = f"""
  {caixa(30, 50, 130, 40, ROXO, ".12", 12)}
  <rect x="46" y="64" width="76" height="10" rx="5" fill="{ROXO}" opacity=".6"/>
  <path d="M136 66 l6 7 6 -7" fill="none" stroke="{ROXO}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  {rotulo(95, "COMEÇA FECHADO", ROXO, 112)}
  {caixa(200, 34, 136, 108, ROXO, ".08", 12)}
  <rect x="216" y="48" width="76" height="10" rx="5" fill="{ROXO}" opacity=".6"/>
  {linhas(216, 68, 3, 104, passo=20, alt=10, cor=ROXO, op=".35")}
  {rotulo(268, "ABRE SÓ QUANDO PRECISA", ROXO, 156)}
"""


# A ordem é a ordem em que as leis aparecem, um dia após o outro. Alterna
# entre as famílias (lei clássica, heurística de Nielsen, Gestalt, princípio
# de Norman, viés de produto, acessibilidade) para dois dias seguidos nunca
# soarem parecidos.
LEIS = [
    ("LEI DE FITTS",
     ["Quanto maior e mais perto o alvo, mais rápido a mão chega nele.",
      "Botão importante não merece ser pequeno nem ficar escondido",
      "num canto que ninguém alcança."], FITTS),
    ("VISIBILIDADE DO STATUS",
     ["A interface deve dizer o tempo todo o que está acontecendo.",
      "Barra de progresso, spinner e confirmação não são enfeite:",
      "são o que impede a pessoa de achar que travou."], STATUS),
    ("LEI DA PROXIMIDADE",
     ["O que está perto parece do mesmo grupo, mesmo sem título.",
      "Antes de desenhar mais uma linha divisória, tente",
      "só mexer no espaçamento."], PROXIMIDADE),
    ("AFFORDANCE",
     ["A forma de um elemento já anuncia o que dá para fazer com ele.",
      "Botão com cara de botão dispensa instrução; texto com cara",
      "de texto não recebe clique nenhum."], AFFORDANCE),
    ("ANCORAGEM",
     ["O primeiro número visto vira a régua de todos os outros.",
      "O mesmo preço parece caro ou barato dependendo do que",
      "apareceu antes dele na tela."], ANCORAGEM),
    ("LEI DE HICK",
     ["Cada opção a mais na tela é um segundo a mais de decisão.",
      "Menu enxuto não é menu pobre: é menu que respeita o tempo",
      "de quem está do outro lado."], HICK),
    ("CONTRASTE SUFICIENTE",
     ["Texto claro sobre fundo claro exclui gente de verdade.",
      "A régua da WCAG é 4,5:1 para texto normal. Abaixo disso,",
      "boa parte das pessoas simplesmente não lê."], CONTRASTE),
    ("EFEITO ZEIGARNIK",
     ["Tarefa começada incomoda até terminar.",
      "Mostrar o progresso não é enfeite: é o que faz a pessoa",
      "voltar para fechar o que ficou pela metade."], ZEIGARNIK),
    ("LEI DO FECHAMENTO",
     ["Diante de uma forma incompleta, o olho fecha o que falta.",
      "Por isso um contorno interrompido ainda lê como círculo,",
      "e menos traço costuma bastar."], FECHAMENTO),
    ("LEI DE TESLER",
     ["Toda complexidade que não dá para eliminar alguém carrega.",
      "A escolha é sua: ou o sistema resolve, ou a conta sobra",
      "para quem está usando."], TESLER),
    ("PROVA SOCIAL",
     ["Na dúvida, a gente faz o que os outros fizeram.",
      "Nota, número de clientes e avaliação encurtam a decisão",
      "mais do que qualquer descrição de produto."], PROVA_SOCIAL),
    ("LEI DE JAKOB",
     ["As pessoas passam a maior parte do tempo em outros sites.",
      "Elas esperam que o seu funcione igual. Originalidade fica",
      "na identidade visual, não no lugar do carrinho."], JAKOB),
    ("FEEDBACK",
     ["Ação sem resposta vira dúvida: clicou ou não clicou?",
      "Todo toque precisa de um sinal imediato, nem que seja",
      "o botão mudando de estado."], FEEDBACK),
    ("LIMIAR DE DOHERTY",
     ["Acima de 0,4 segundo de espera, a atenção começa a vazar.",
      "Abaixo disso a pessoa entra em ritmo com a interface e",
      "produz mais sem perceber."], DOHERTY),
    ("CARGA COGNITIVA",
     ["A cabeça tem banda limitada e ela é gasta com o conteúdo,",
      "não com a interface. Cada decisão a mais que a tela pede",
      "é menos energia para o que a pessoa veio fazer."], CARGA),
    ("LEI DE MILLER",
     ["A memória de trabalho segura mais ou menos sete coisas.",
      "Agrupar é o truque: três blocos de dois cansam menos",
      "que sete itens soltos na mesma lista."], MILLER),
    ("PREVENÇÃO DE ERROS",
     ["Mensagem de erro boa é a que nunca precisou aparecer.",
      "Validar enquanto a pessoa digita evita o formulário que",
      "só reclama depois de tudo preenchido."], PREVENIR),
    ("LEI DA CONTINUIDADE",
     ["Elementos alinhados em uma curva ou reta são lidos como",
      "um caminho só. É o que faz uma trilha de passos parecer",
      "um processo, e não itens soltos."], CONTINUIDADE),
    ("EFEITO VON RESTORFF",
     ["O item diferente do resto é o único que fica na memória.",
      "Se tudo está em destaque, nada está. Escolha um botão",
      "para gritar e deixe os outros sussurrarem."], VON_RESTORFF),
    ("AVERSÃO À PERDA",
     ["Perder machuca cerca de duas vezes mais do que ganhar agrada.",
      "'Não perca seu desconto' move mais gente que",
      "'ganhe um desconto', com o mesmo valor em jogo."], AVERSAO_PERDA),
    ("CHUNKING",
     ["Quebrar informação em blocos curtos multiplica o quanto",
      "a memória segura. Telefone, cartão e CPF existem em",
      "pedaços exatamente por isso."], CHUNKING),
    ("CORRESPONDÊNCIA COM O REAL",
     ["Fale a língua de quem usa, não a do banco de dados.",
      "'Cartão recusado' resolve; 'ERR_TX_0x2F' só empurra",
      "a pessoa para o suporte."], MUNDO_REAL),
    ("LEI DA SIMILARIDADE",
     ["Elementos parecidos são lidos como um conjunto, mesmo",
      "espalhados pela tela. Cor, forma e tamanho agrupam",
      "sem precisar de moldura nem de rótulo."], SIMILARIDADE),
    ("EFEITO DO PADRÃO",
     ["A maioria não muda a opção que já vem marcada.",
      "Isso dá um poder enorme e uma responsabilidade junto:",
      "o padrão precisa ser o que é melhor para quem usa."], PADRAO),
    ("REGRA DO PICO-FIM",
     ["A lembrança de uma experiência não é a média dela.",
      "É o momento mais intenso somado ao final. Capriche na",
      "confirmação do pedido, e não só no formulário."], PICO_FIM),
    ("SIGNIFICANTES",
     ["Affordance é o que dá para fazer; significante é a pista",
      "visual que conta isso. A alcinha de arrastar, a seta,",
      "o cursor que muda: tudo é significante."], SIGNIFICANTES),
    ("RECONHECER, NÃO LEMBRAR",
     ["Reconhecer é barato, lembrar é caro.",
      "Deixe as opções à vista em vez de exigir que a pessoa",
      "guarde na cabeça o que viu na tela anterior."], RECONHECER),
    ("PRINCÍPIO DE PARETO",
     ["Cerca de 20% das telas respondem por 80% do uso.",
      "Descobrir quais são elas diz onde vale gastar tempo de",
      "polimento e onde o suficiente já basta."], PARETO),
    ("LEI DE PRÄGNANZ",
     ["Diante de uma forma complexa, o olho procura a versão",
      "mais simples possível. Formas limpas são entendidas",
      "mais rápido e cansam menos."], PRAGNANZ),
    ("ESCASSEZ",
     ["O que parece raro parece valer mais.",
      "Estoque baixo e prazo curto funcionam, mas só sobrevivem",
      "à segunda visita se forem verdade."], ESCASSEZ),
    ("CONTROLE E LIBERDADE",
     ["Gente erra, e erra o tempo todo.",
      "Toda ação precisa de um caminho de volta bem visível:",
      "desfazer, cancelar, sair sem perder o que já foi feito."], DESFAZER),
    ("MAPEAMENTO NATURAL",
     ["O controle deve ficar arrumado como a coisa controlada.",
      "Botões em fila para bocas em quadrado obrigam a pensar;",
      "botões no mesmo arranjo dispensam etiqueta."], MAPEAMENTO),
    ("EFEITO DE POSIÇÃO SERIAL",
     ["De uma lista, ficam o primeiro e o último item.",
      "O que estiver no meio some da memória, então coloque",
      "o que importa nas pontas."], POSICAO_SERIAL),
    ("DIVULGAÇÃO PROGRESSIVA",
     ["Mostre o essencial e guarde o avançado a um clique.",
      "A tela fica simples para quem está começando sem tirar",
      "poder de quem já sabe o que quer."], DIVULGACAO),
    ("LEI DA REGIÃO COMUM",
     ["Um contorno em volta cria um grupo na hora, mesmo que",
      "os elementos estejam longe uns dos outros.",
      "É o agrupamento mais forte da Gestalt."], REGIAO_COMUM),
    ("EFEITO ISCA",
     ["Uma terceira opção pior existe para fazer a do meio",
      "parecer boa. Usar isso para orientar é design;",
      "usar para enganar é o oposto disso."], ISCA),
    ("CONSISTÊNCIA E PADRÕES",
     ["A mesma coisa deve se parecer e se comportar igual",
      "em todo lugar do produto. Cada exceção obriga a pessoa",
      "a reaprender o que já sabia."], CONSISTENCIA),
    ("MODELO MENTAL",
     ["Cada pessoa chega com uma ideia pronta de como aquilo",
      "funciona. Quando o produto contraria essa ideia, a culpa",
      "do estranhamento é do produto, nunca dela."], MODELO_MENTAL),
    ("EFEITO ESTÉTICA-USABILIDADE",
     ["Interface bonita é percebida como mais fácil de usar,",
      "mesmo quando o fluxo é idêntico. O capricho visual",
      "compra paciência para os tropeços que sobrarem."], ESTETICA),
    ("RESTRIÇÕES",
     ["A melhor forma de evitar um erro é tornar ele impossível.",
      "Um seletor de data não deixa digitar 32 de janeiro;",
      "um campo livre deixa, e depois reclama."], RESTRICOES),
    ("LEI DO DESTINO COMUM",
     ["Elementos que se movem na mesma direção viram um grupo,",
      "mesmo distantes. É por isso que animar itens juntos",
      "conta que eles pertencem à mesma coisa."], DESTINO_COMUM),
    ("EFEITO GOAL-GRADIENT",
     ["Quanto mais perto da linha de chegada, mais forte o",
      "empurrão. Por isso o cartão de fidelidade já vem com",
      "dois selos preenchidos de brinde."], GOAL_GRADIENT),
    ("DESIGN MINIMALISTA",
     ["Cada elemento a mais compete com os que importam.",
      "Tirar não é empobrecer: é devolver o palco para",
      "o que a pessoa veio fazer."], MINIMALISMO),
    ("RECIPROCIDADE",
     ["Quem recebe algo primeiro se sente em dívida.",
      "Um material útil de graça abre mais portas do que",
      "qualquer formulário pedindo dados de cara."], RECIPROCIDADE),
    ("LEI DA CONEXÃO UNIFORME",
     ["Uma linha, uma caixa ou um fundo compartilhado unem",
      "elementos com mais força do que a proximidade.",
      "É o agrupamento que vence os outros."], CONEXAO_UNIFORME),
    ("AJUDAR A SAIR DO ERRO",
     ["Quando o erro escapa, a mensagem tem três obrigações:",
      "dizer o que houve, em língua de gente, e oferecer",
      "o caminho de saída no mesmo lugar."], RECUPERAR_ERRO),
    ("ATENÇÃO SELETIVA",
     ["O olho aprende a ignorar o que parece propaganda.",
      "Aviso importante desenhado como banner é aviso",
      "que ninguém vai ver."], ATENCAO_SELETIVA),
    ("EFEITO IKEA",
     ["A gente valoriza mais o que ajudou a construir.",
      "Personalizar o perfil, montar a lista, escolher o tema:",
      "cada gesto desses amarra a pessoa ao produto."], IKEA),
    ("FIGURA E FUNDO",
     ["O olho separa na hora o que está na frente do que está",
      "atrás. Sombra, contraste e profundidade decidem quem",
      "recebe a atenção e quem recua."], FIGURA_FUNDO),
    ("FLEXIBILIDADE E ATALHOS",
     ["O caminho longo serve para quem chegou agora.",
      "Quem usa todo dia precisa de acelerador: atalho de",
      "teclado, ação em massa, busca por comando."], ATALHOS),
    ("LEI DE PARKINSON",
     ["A tarefa se espalha até preencher o tempo disponível.",
      "Prazo declarado e barra de progresso encurtam formulário",
      "melhor do que qualquer pedido de pressa."], PARKINSON),
    ("NAVEGAÇÃO POR TECLADO",
     ["Nem todo mundo usa mouse, por escolha ou por necessidade.",
      "Se o foco não aparece ao apertar Tab, uma parte das",
      "pessoas simplesmente não consegue avançar."], TECLADO),
    ("PARADOXO DO USUÁRIO ATIVO",
     ["Ninguém lê o manual: a pessoa já começa clicando.",
      "Então o aprendizado precisa acontecer dentro da tarefa,",
      "e não numa tela de boas-vindas que todo mundo pula."], PARADOXO_ATIVO),
    ("CUSTO IRRECUPERÁVEL",
     ["Quem já investiu tempo hesita em desistir.",
      "Mostrar o quanto já foi feito segura quem ia abandonar",
      "o cadastro no meio do caminho."], CUSTO_IRRECUPERAVEL),
    ("LEI DA SIMETRIA",
     ["Arranjos simétricos são processados mais rápido e",
      "passam sensação de ordem. Assimetria funciona como",
      "exceção proposital, não como descuido."], SIMETRIA),
    ("ENQUADRAMENTO",
     ["O mesmo dado muda de sentido conforme a moldura.",
      "'90% aprovado' e '10% recusado' são o mesmo número",
      "e provocam reações opostas."], ENQUADRAMENTO),
    ("CONTEÚDO PERCEPTÍVEL",
     ["Imagem sem texto alternativo não existe para quem usa",
      "leitor de tela. Descrever não é acessório de acessibilidade:",
      "é o conteúdo chegando inteiro."], PERCEPTIVEL),
    ("LEI DE POSTEL",
     ["Seja tolerante no que aceita e rigoroso no que devolve.",
      "Aceite o telefone com ponto, traço ou espaço, e guarde",
      "sempre no mesmo formato limpo."], POSTEL),
    ("AJUDA NO LUGAR CERTO",
     ["Documentação escondida no rodapé não ajuda ninguém.",
      "A explicação precisa aparecer ao lado do campo difícil,",
      "no momento exato da dúvida."], AJUDA),
    ("FLOW",
     ["Existe um ponto em que o desafio bate com a habilidade",
      "e o tempo some. Interface que interrompe demais nunca",
      "deixa a pessoa chegar lá."], FLOW),
    ("NAVALHA DE OCCAM",
     ["Entre duas soluções que resolvem, fique com a mais simples.",
      "Vá tirando elemento até começar a fazer falta:",
      "o que sobrou era o necessário."], OCCAM),
]


def indice(data):
    """Rotação fixa: uma lei por dia, na ordem da lista.

    Usa o número ordinal do dia, que anda de um em um. Assim nenhuma lei
    repete antes de todas as outras terem aparecido, e o ciclo inteiro leva
    exatamente len(LEIS) dias. O sorteio anterior era aleatório com
    reposição: repetia a mesma lei em dias seguidos e deixava outras de fora
    por semanas.
    """
    return data.toordinal() % len(LEIS)


def montar(agora):
    nome, frases, diagrama = LEIS[indice(agora)]
    # o quadro do diagrama comeca em x=600; nome comprido encolhe para nao encostar
    corpo_nome = 30 if len(nome) <= 26 else 25
    linhas = "".join(
        f'<text x="40" y="{146 + i * 21}" font-size="12.5" fill="{SUAVE}">{t}</text>'
        for i, t in enumerate(frases))
    data_br = agora.strftime("%d.%m.%Y")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 248" width="1000" height="248" role="img" aria-label="Lei de UX do dia {data_br}: {nome}. {' '.join(frases)}">
  <defs>
    <linearGradient id="lFundo" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#fffdff"/><stop offset="55%" stop-color="#faf5ff"/><stop offset="100%" stop-color="#f3e8ff"/>
    </linearGradient>
    <radialGradient id="lB1" cx="50%" cy="50%"><stop offset="0%" stop-color="#b06cf0" stop-opacity=".16"/><stop offset="100%" stop-color="#b06cf0" stop-opacity="0"/></radialGradient>
    <linearGradient id="lRegua" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#9333ea"/><stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>
    <clipPath id="lCard"><rect width="1000" height="248" rx="28"/></clipPath>
    <clipPath id="lQuadro"><rect x="600" y="32" width="360" height="166" rx="20"/></clipPath>
    <style>
      .sobe{{animation:sobe .9s cubic-bezier(.2,.7,.3,1) both}}
      .s2{{animation-delay:.1s}}.s3{{animation-delay:.2s}}.s4{{animation-delay:.3s}}
      @keyframes sobe{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
      .vivo{{animation:vivo 2.4s ease-in-out infinite}}
      @keyframes vivo{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
      .pulso{{animation:pulso 3s ease-in-out infinite}}
      @keyframes pulso{{0%{{opacity:.7}}70%,100%{{opacity:0}}}}
      .seta{{animation:seta 4s ease-in-out infinite}}
      @keyframes seta{{0%,100%{{transform:translate(0,0)}}45%,55%{{transform:translate(74px,-64px)}}}}
      .barra{{transform-origin:24px 0;animation:cresce 1.2s cubic-bezier(.2,.7,.3,1) .4s both}}
      .b2{{transform-origin:214px 0;animation-delay:.55s}}
      .enche{{transform-origin:28px 0;animation:cresce 1.4s cubic-bezier(.2,.7,.3,1) .4s both}}
      @keyframes cresce{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
      .curva{{stroke-dasharray:420;stroke-dashoffset:420;animation:curva 2s ease-out .4s forwards}}
      @keyframes curva{{to{{stroke-dashoffset:0}}}}
      .cur{{animation:cur 1s steps(1) infinite}}
      @keyframes cur{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
      .bate{{animation:bate 2.6s ease-in-out infinite}}
      @keyframes bate{{0%,100%{{transform:scale(1)}}30%{{transform:scale(1.12)}}45%{{transform:scale(1)}}60%{{transform:scale(1.06)}}}}
      .destaca{{animation:destaca 3.4s ease-in-out infinite}}
      @keyframes destaca{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.06)}}}}
      @media (prefers-reduced-motion: reduce){{
        *{{animation:none !important}}
        .curva{{stroke-dashoffset:0}} .pulso{{opacity:.4}}
      }}
    </style>
  </defs>

  <g clip-path="url(#lCard)">
    <rect width="1000" height="248" fill="url(#lFundo)"/>
    <ellipse cx="60" cy="230" rx="300" ry="160" fill="url(#lB1)"/>

    <g font-family="Jost, Century Gothic, Futura, Segoe UI, Arial, sans-serif">
      <g class="sobe">
        <circle class="vivo" cx="45" cy="44" r="4.5" fill="#16a34a"/>
        <text x="59" y="48" font-size="10.5" letter-spacing="3" fill="{ROXO}">LEI DE UX DO DIA &#183; {data_br}</text>
      </g>
      <text class="sobe s2" x="38" y="104" font-size="{corpo_nome}" font-weight="700" letter-spacing="1.2" fill="{TINTA}">{nome}</text>
      <rect class="sobe s3" x="40" y="118" width="80" height="4" rx="2" fill="url(#lRegua)"/>
      <g class="sobe s3">{linhas}</g>
      <text class="sobe s4" x="40" y="216" font-size="9" letter-spacing="1.4" fill="#6b7280" font-family="SFMono-Regular, Consolas, Menlo, monospace">ATUALIZADA AUTOMATICAMENTE TODA MADRUGADA &#183; UMA LEI DIFERENTE POR DIA</text>

      <g class="sobe s4">
        <rect x="600" y="32" width="360" height="166" rx="20" fill="#fffdff" stroke="{LINHA}" stroke-width="1.6"/>
        <g clip-path="url(#lQuadro)"><g transform="translate(600,32)">{diagrama}</g></g>
      </g>
    </g>

    <rect x="1" y="1" width="998" height="246" rx="28" fill="none" stroke="#9333ea" stroke-opacity=".2" stroke-width="2"/>
  </g>
</svg>
"""


if __name__ == "__main__":
    temas.gravar("leidodia", montar(datetime.now(BR_TZ)))
    print("lei do dia gerada nos dois temas")

#!/usr/bin/env python3
"""Gera os dois temas de cada peça a partir de um único arquivo-mestre.

Cada SVG em `assets/src/` é escrito no tema CLARO (o padrão da marca, igual ao
budri.com.br). Este script troca os tokens de cor de uma vez só e grava:

    assets/<nome>.svg        → tema claro   (fallback do <picture>)
    assets/<nome>-dark.svg   → tema escuro

A paleta da marca é aplicada antes da conversão de tema, inclusive nas
peças dinâmicas, para manter roxo, preto e branco nas atualizações diárias.
"""

import os
import re
from identidade import aplicar

PALETA = {
    "#2563eb": "#7e22ce", "#1e40af": "#5b21b6",
    "#5b8def": "#a78bfa", "#93bffb": "#c4b5fd",
    "#dbeafe": "#ede9fe", "#db2777": "#9333ea",
    "#f7b0d3": "#d8b4fe", "#fde4f1": "#f3e8ff",
    "#16a34a": "#7e22ce", "#ea580c": "#6b21a8",
    "#ca8a04": "#9333ea", "#a930cb": "#9333ea",
    "#c25ae0": "#a78bfa", "#f0abfc": "#c4b5fd",
    "#111827": "#111015", "#4b5563": "#57515f",
    "#6b7280": "#716979",
}

TOKENS = {
    # fundos e superfícies
    "#faf5ff": "#0c0911",   # fundo base
    "#f3e8ff": "#171020",   # fundo 2
    "#fffdff": "#131017",   # superfície do card
    "#f5f0fe": "#201729",   # trilho / inset
    "#e9d5ff": "#39264d",   # linhas e bordas

    # tinta
    "#111827": "#f7f5ff",   # texto forte (e o contorno preto das bolhas)
    "#4b5563": "#b8b0d6",   # texto suave
    "#6b7280": "#8d85ac",   # texto discreto
    "#111015": "#faf8ff",
    "#57515f": "#c4bdcf",
    "#716979": "#aaa0b7",

    # marca
    "#6b21a8": "#e9d5ff",   # roxo forte
    "#7e22ce": "#c084fc",   # roxo
    "#9333ea": "#a855f7",   # roxo da marca
    "#c084fc": "#d8b4fe",   # roxo claro

    # acentos discretos: apenas ícones e indicadores
    "#4676b8": "#8aafe0",
    "#ba5188": "#df95bb",
    "#3b8a70": "#83c5ad",

    # semânticas
    "#2563eb": "#60a5fa",
    "#db2777": "#f472b6",
    "#16a34a": "#4ade80",
    "#ea580c": "#fb923c",
    "#ca8a04": "#facc15",

    "#bfdbfe": "#254a70",
    "#a5b4fc": "#586bc4",

    # escala de calor do calendário de contribuições
    "#f0e6fd": "#241645",
    "#ddc7fb": "#3d2168",
    "#c08bf5": "#6d35b8",
    "#9b4dee": "#a05ef0",
}

_PADRAO = re.compile("|".join(sorted(TOKENS, key=len, reverse=True)), re.IGNORECASE)
_CORES_MARCA = re.compile("|".join(PALETA), re.IGNORECASE)


def escurecer(svg):
    """Troca todos os tokens de uma vez - nunca em cascata."""
    return _PADRAO.sub(lambda m: TOKENS[m.group(0).lower()], svg)


def gravar(nome, svg_claro, raiz=None):
    svg_claro = aplicar(nome, svg_claro)
    # Diagramas e dados mantêm suas cores funcionais; demais peças usam acentos sutis.
    colorido = nome in {"manifesto", "leidodia", "telemetria"}
    neutros = {"#111827", "#4b5563", "#6b7280"}
    svg_claro = _CORES_MARCA.sub(
        lambda m: m.group(0) if colorido and m.group(0).lower() not in neutros
        else PALETA[m.group(0).lower()], svg_claro)
    # Pequenas áreas recuperam as cores antigas; superfícies e títulos seguem roxos.
    acentos = {
        "servicos": [(r'<g class="ico i2">.*?</g>', "#4676b8"),
                     (r'<g class="ico i3">.*?</g>', "#ba5188")],
        "stack": [(r'<circle class="pisca g2"[^>]*/>', "#4676b8"),
                  (r'<circle class="pisca g3"[^>]*/>', "#ba5188"),
                  (r'<circle class="pisca g4"[^>]*/>', "#3b8a70")],
        "diferenciais": [(r'<g class="bate"[^>]*>.*?</g>', "#ba5188"),
                         (r'<rect class="sobebar[^>]*/>', "#4676b8")],
        "telemetria": [(r'<circle class="(?:vivo|marca-pulse)"[^>]*/>', "#3b8a70")],
    }
    for padrao, cor in acentos.get(nome, []):
        def colorir(m, cor=cor):
            trecho = m.group(0)
            if trecho.startswith('<rect class="sobebar'):
                trecho = re.sub(r' fill="[^"]*"', '', trecho)
                return trecho.replace('/>', f' fill="{cor}"/>')
            return re.sub(r'(fill|stroke)="#(?:7e22ce|9333ea)"',
                          lambda tinta: f'{tinta[1]}="{cor}"', trecho)
        svg_claro = re.sub(padrao, colorir, svg_claro, flags=re.DOTALL)
    svg_claro = "\n".join(linha.rstrip() for linha in svg_claro.splitlines()) + "\n"
    raiz = raiz or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destino = os.path.join(raiz, "assets")
    os.makedirs(destino, exist_ok=True)
    for sufixo, conteudo in ((".svg", svg_claro), ("-dark.svg", escurecer(svg_claro))):
        caminho = os.path.join(destino, nome + sufixo)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
    return nome


def main():
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    origem = os.path.join(raiz, "assets", "src")
    if not os.path.isdir(origem):
        raise SystemExit(f"pasta de mestres nao encontrada: {origem}")

    feitos = []
    for arquivo in sorted(os.listdir(origem)):
        if not arquivo.endswith(".svg"):
            continue
        with open(os.path.join(origem, arquivo), encoding="utf-8") as f:
            feitos.append(gravar(arquivo[:-4], f.read(), raiz))
    print(f"{len(feitos)} pecas em dois temas: {', '.join(feitos)}")


if __name__ == "__main__":
    main()

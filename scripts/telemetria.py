#!/usr/bin/env python3
"""Gera assets/telemetria.svg e assets/telemetria-dark.svg.

Le os dados publicos direto da API do GitHub e desenha um painel proprio:
acessos ao perfil, commits do ano, seguidores, o calendario de contribuicoes
e a mistura de linguagens. Sem servico de terceiros para desenhar nada -
so a biblioteca padrao do Python.
"""

import io
import json
import os
import urllib.error
import urllib.request
from collections import OrderedDict
from datetime import datetime, timedelta, timezone

import temas

USER = os.environ.get("GH_USER", "emillybudri")
# BUDRI_TOKEN e um token pessoal guardado nos secrets do repositorio.
#   read:user -> os commits dos repositorios privados entram na contagem
#   repo      -> libera o trafego real do perfil (visitas dos ultimos 14 dias).
#                so um token pessoal alcanca esse endpoint: o GITHUB_TOKEN da
#                Action nao tem como, nao existe permissao de workflow para ele.
# Sem ele o painel ainda funciona, so com dados publicos.
TOKEN = os.environ.get("BUDRI_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
TOKEN_PESSOAL = bool(os.environ.get("BUDRI_TOKEN"))
BR_TZ = timezone(timedelta(hours=-3))

CORES = ["#7e22ce", "#2563eb", "#db2777", "#16a34a", "#ea580c", "#ca8a04"]
CALOR = ["#f0e6fd", "#ddc7fb", "#c08bf5", "#9b4dee", "#7e22ce"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def _req(url, data=None, headers=None, bruto=False, token=None):
    hdrs = {"User-Agent": "budri-readme", "Accept": "application/vnd.github+json"}
    usar = TOKEN if token is None else token
    if usar:
        hdrs["Authorization"] = f"Bearer {usar}"
    hdrs.update(headers or {})
    corpo = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=corpo, headers=hdrs)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace") if bruto else json.load(r)


def _meus_repos():
    """Com token, inclui os privados. Sem token, so os publicos."""
    base = ("https://api.github.com/user/repos?affiliation=owner&visibility=all"
            if TOKEN else f"https://api.github.com/users/{USER}/repos?type=owner")
    todos = []
    for pagina in (1, 2, 3):
        lote = _req(f"{base}&per_page=100&page={pagina}")
        if not lote:
            break
        todos += lote
        if len(lote) < 100:
            break
    return [r for r in todos if not r.get("fork")]


def seguidores_e_linguagens():
    dados = {"seguidores": None, "linguagens": {}}
    try:
        dados["seguidores"] = _req(f"https://api.github.com/users/{USER}").get("followers")
    except Exception as e:
        print("perfil indisponivel:", e)
    try:
        repos = _meus_repos()
        # o campo "language" do repo so devolve a linguagem dominante, e o campo
        # "size" conta imagem e asset junto. Somar os bytes de codigo repo a repo
        # e o unico jeito de a mistura refletir o que foi mesmo escrito.
        for r in repos:
            try:
                for lang, bytes_ in _req(r["languages_url"]).items():
                    dados["linguagens"][lang] = dados["linguagens"].get(lang, 0) + bytes_
            except Exception as e:
                print("linguagens de", r.get("name"), "indisponiveis:", e)
        print(f"mistura calculada sobre {len(repos)} repositorios")
    except Exception as e:
        print("repositorios indisponiveis:", e)
    return dados


ARQUIVO_ACESSOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "acessos.json")


def acessos():
    """Acessos ao perfil, acumulados dia a dia a partir do trafego do GitHub.

    A API so devolve os ultimos 14 dias, entao cada execucao grava as contagens
    por data em acessos.json. Guardar por data torna a soma idempotente: como as
    janelas de dias diferentes se sobrepoem, regravar a mesma data nao conta duas
    vezes. O campo "herdado" carrega o total acumulado antes da troca de usuario.
    """
    registro = {"herdado": 0, "dias": {}}
    try:
        with io.open(ARQUIVO_ACESSOS, encoding="utf-8") as f:
            registro.update(json.load(f))
    except FileNotFoundError:
        print("acessos.json ainda nao existe, comecando do zero")
    except Exception as e:
        print("acessos.json ilegivel:", e)

    # o caminho vem do proprio contexto da Action, entao renomear o repositorio
    # nao quebra nada; localmente cai no palpite usuario/usuario
    caminho = os.environ.get("GITHUB_REPOSITORY") or f"{USER}/{USER}"
    tentativas = [("BUDRI_TOKEN", os.environ.get("BUDRI_TOKEN")),
                  ("GITHUB_TOKEN", os.environ.get("GITHUB_TOKEN"))]

    unicos = None
    for nome, tok in tentativas:
        if not tok:
            continue
        try:
            t = _req(f"https://api.github.com/repos/{caminho}/traffic/views", token=tok)
            unicos = t.get("uniques")
            for dia in t.get("views", []):
                registro["dias"][dia["timestamp"][:10]] = dia["count"]
            with io.open(ARQUIVO_ACESSOS, "w", encoding="utf-8") as f:
                json.dump(registro, f, ensure_ascii=False, indent=2, sort_keys=True)
            print(f"trafego lido com {nome}: {len(t.get('views', []))} dias gravados")
            break
        except urllib.error.HTTPError as e:
            recado = {403: "o token nao tem permissao de leitura de trafego",
                      404: "o token nao enxerga o repositorio " + caminho,
                      401: "o token e invalido ou expirou"}.get(e.code, "erro inesperado")
            print(f"trafego negado com {nome}: HTTP {e.code} - {recado}")
        except Exception as e:
            print(f"trafego falhou com {nome}:", e)
    else:
        if unicos is None:
            print("nenhum token conseguiu ler o trafego; os acessos ficam no total ja acumulado")

    total = registro["herdado"] + sum(registro["dias"].values())
    rodape = f"{n(unicos)} PESSOAS EM 14 DIAS" if unicos is not None else "DESDE SEMPRE"
    return (total or None), rodape


GQL = """
query($login:String!){
  user(login:$login){
    contributionsCollection{
      restrictedContributionsCount
      contributionCalendar{
        totalContributions
        weeks{ firstDay contributionDays{ date weekday contributionCount } }
      }
    }
  }
}"""


def calendario():
    if not TOKEN:
        return None
    try:
        r = _req("https://api.github.com/graphql",
                 {"query": GQL, "variables": {"login": USER}},
                 {"Accept": "application/json"})
        c = r["data"]["user"]["contributionsCollection"]
        cal = c["contributionCalendar"]
        # o que a API nao detalha por dia mas conta: commits em repo privado
        cal["privados"] = c.get("restrictedContributionsCount") or 0
        return cal
    except Exception as e:
        print("graphql indisponivel:", e)
        return None


def calendario_por_eventos():
    """Sem token: monta um calendario aproximado com os eventos publicos."""
    contagem = {}
    try:
        for pagina in (1, 2, 3):
            eventos = _req(f"https://api.github.com/users/{USER}/events/public?per_page=100&page={pagina}")
            if not eventos:
                break
            for ev in eventos:
                dia = (ev.get("created_at") or "")[:10]
                if not dia:
                    continue
                peso = len(ev.get("payload", {}).get("commits", [])) if ev.get("type") == "PushEvent" else 1
                contagem[dia] = contagem.get(dia, 0) + max(peso, 1)
    except Exception as e:
        print("eventos indisponiveis:", e)

    hoje = datetime.now(BR_TZ).date()
    fim = hoje + timedelta(days=(6 - hoje.weekday()) % 7)      # completa a semana (dom)
    inicio = fim - timedelta(days=52 * 7 - 1)
    semanas, atual = [], []
    d = inicio
    while d <= fim:
        atual.append({"date": d.isoformat(), "weekday": (d.weekday() + 1) % 7,
                      "contributionCount": contagem.get(d.isoformat(), 0)})
        if len(atual) == 7:
            semanas.append({"contributionDays": atual})
            atual = []
        d += timedelta(days=1)
    if atual:
        semanas.append({"contributionDays": atual})
    return {"totalContributions": sum(contagem.values()), "weeks": semanas, "privados": 0}


def sequencias(dias):
    atual = 0
    for i, d in enumerate(reversed(dias)):
        if d["contributionCount"] > 0:
            atual += 1
        elif i == 0:
            continue                       # o dia de hoje ainda esta acontecendo
        else:
            break
    melhor = corrida = 0
    for d in dias:
        corrida = corrida + 1 if d["contributionCount"] > 0 else 0
        melhor = max(melhor, corrida)
    return atual, melhor


def n(v):
    if v is None:
        return "-"
    if v >= 1000:
        return f"{v / 1000:.1f}k".replace(".0k", "k")
    return f"{v:,}".replace(",", ".")


def indicador(x, rotulo, valor, rodape, cor, atraso):
    return f"""
    <g class="ind" style="animation-delay:{atraso}s">
      <g filter="url(#teSombra)"><rect x="{x}" y="28" width="294" height="96" rx="24" fill="#fffdff" stroke="{cor}" stroke-opacity=".26" stroke-width="1.5"/></g>
      <circle cx="{x + 28}" cy="56" r="4.5" fill="{cor}"/>
      <text x="{x + 42}" y="60" font-size="9.5" letter-spacing="2.4" fill="{cor}">{rotulo}</text>
      <text x="{x + 26}" y="102" font-size="34" font-weight="700" fill="#111827">{valor}</text>
      <text x="{x + 268}" y="102" font-size="9.5" letter-spacing="1.4" text-anchor="end" fill="#6b7280" font-family="SFMono-Regular, Consolas, Menlo, monospace">{rodape}</text>
    </g>"""


def grade(cal):
    """O calendario de contribuicoes - 52 semanas, uma coluna por semana."""
    celula, vao, x0, y0 = 13, 4, 76, 186
    passo = celula + vao
    semanas = cal["weeks"][-52:]
    dias = [d for s in semanas for d in s["contributionDays"]]
    pico = max((d["contributionCount"] for d in dias), default=0) or 1

    quadros, marcos, ultimo_mes = [], [], None
    for si, s in enumerate(semanas):
        for d in s["contributionDays"]:
            wd = d.get("weekday")
            if wd is None:
                wd = (datetime.strptime(d["date"], "%Y-%m-%d").weekday() + 1) % 7
            nivel = 0 if d["contributionCount"] == 0 else min(4, 1 + int(3 * d["contributionCount"] / pico))
            quadros.append(f'<rect class="dia" style="animation-delay:{round(si * .012, 3)}s" '
                           f'x="{x0 + si * passo}" y="{y0 + wd * passo}" width="{celula}" height="{celula}" '
                           f'rx="3.5" fill="{CALOR[nivel]}"/>')
        primeiro = s["contributionDays"][0]["date"]
        mes = int(primeiro[5:7])
        if mes != ultimo_mes and int(primeiro[8:10]) <= 7:
            marcos.append(f'<text x="{x0 + si * passo}" y="176" font-size="9.5" fill="#6b7280">{MESES[mes - 1]}</text>')
            ultimo_mes = mes

    rotulos = "".join(
        f'<text x="68" y="{y0 + i * passo + 10}" font-size="9" text-anchor="end" fill="#6b7280">{lab}</text>'
        for i, lab in ((1, "seg"), (3, "qua"), (5, "sex")))
    return "".join(quadros), "".join(marcos), rotulos, sequencias(dias)


def barra_de_linguagens(linguagens):
    todas = sorted(linguagens.items(), key=lambda kv: -kv[1])
    soma = sum(v for _, v in todas) or 1
    itens = [(k, v) for k, v in todas if v / soma >= 0.02][:6]
    total = sum(v for _, v in itens)
    if not itens or total == 0:
        return ('<rect x="76" y="344" width="880" height="16" rx="8" fill="#f0e6fd"/>', "")

    barra, legenda, x = [], [], 76
    for i, (nome, tam) in enumerate(itens):
        w = max(14, round(880 * tam / total)) - 3
        barra.append(f'<rect class="fatia" style="animation-delay:{round(i * .09, 2)}s" '
                     f'x="{x}" y="344" width="{w}" height="16" rx="8" fill="{CORES[i % 6]}"/>')
        lx = 76 + i * 152
        legenda.append(f'<g class="leg" style="animation-delay:{round(.4 + i * .07, 2)}s">'
                       f'<circle cx="{lx + 5}" cy="392" r="5" fill="{CORES[i % 6]}"/>'
                       f'<text x="{lx + 18}" y="396" font-size="11.5" fill="#111827">{nome}</text>'
                       f'<text x="{lx + 18 + 8 * len(nome)}" y="396" font-size="11.5" fill="#6b7280"> {100 * tam / total:.0f}%</text></g>')
        x += w + 3
    return "".join(barra), "".join(legenda)


def montar():
    p = seguidores_e_linguagens()
    vistas, rodape_acessos = acessos()
    cal = calendario() or calendario_por_eventos()
    privados = cal.get("privados", 0)
    commits = cal["totalContributions"] + privados
    rodape_commits = "PÚBLICOS + PRIVADOS" if (privados or TOKEN_PESSOAL) else "ÚLTIMOS 12 MESES"
    quadros, marcos, rotulos, (atual, melhor) = grade(cal)
    barra, legenda = barra_de_linguagens(p["linguagens"])
    carimbo = datetime.now(BR_TZ).strftime("%d.%m.%Y &#183; %Hh%M")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 448" width="1000" height="448" role="img" aria-label="Telemetria do GitHub de {USER}: acessos ao perfil, commits, seguidores, calendário de contribuições e mistura de linguagens">
  <defs>
    <linearGradient id="teFundo" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#fffdff"/><stop offset="55%" stop-color="#faf5ff"/><stop offset="100%" stop-color="#f3e8ff"/>
    </linearGradient>
    <radialGradient id="teB1" cx="50%" cy="50%"><stop offset="0%" stop-color="#b06cf0" stop-opacity=".16"/><stop offset="100%" stop-color="#b06cf0" stop-opacity="0"/></radialGradient>
    <radialGradient id="teB2" cx="50%" cy="50%"><stop offset="0%" stop-color="#5b8def" stop-opacity=".14"/><stop offset="100%" stop-color="#5b8def" stop-opacity="0"/></radialGradient>
    <filter id="teSombra" x="-20%" y="-30%" width="140%" height="180%">
      <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#7e22ce" flood-opacity="0.13"/>
    </filter>
    <clipPath id="teCard"><rect width="1000" height="448" rx="28"/></clipPath>
    <style>
      .ind{{animation:sobe .9s cubic-bezier(.2,.7,.3,1) both}}
      .leg{{animation:sobe .8s cubic-bezier(.2,.7,.3,1) both}}
      @keyframes sobe{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
      .dia{{animation:dia .5s ease-out both}}
      @keyframes dia{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1;transform:scale(1)}}}}
      .fatia{{transform-origin:76px 0;animation:fatia .9s cubic-bezier(.2,.7,.3,1) both}}
      @keyframes fatia{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
      .vivo{{animation:vivo 2.4s ease-in-out infinite}}
      @keyframes vivo{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
      .b1{{animation:fl1 9s ease-in-out infinite}}
      @keyframes fl1{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(5px,-12px)}}}}
      @media (prefers-reduced-motion: reduce){{*{{animation:none !important}}}}
    </style>
  </defs>
  <g clip-path="url(#teCard)">
    <rect width="1000" height="448" fill="url(#teFundo)"/>
    <ellipse cx="60" cy="20" rx="320" ry="180" fill="url(#teB1)"/>
    <ellipse cx="960" cy="440" rx="300" ry="170" fill="url(#teB2)"/>
    <g fill="none" stroke-width="3">
      <g class="b1" style="animation-delay:.6s" stroke="#7e22ce" opacity=".35"><circle cx="972" cy="196" r="12"/><circle cx="972" cy="196" r="6.5" stroke-width="2"/></g>
      <g class="b1" style="animation-delay:1.5s" stroke="#111827" opacity=".2"><circle cx="26" cy="300" r="9"/></g>
    </g>

    <g font-family="Jost, Century Gothic, Futura, Segoe UI, Arial, sans-serif">
      {indicador(40, "ACESSOS AO PERFIL", n(vistas), rodape_acessos, "#7e22ce", 0)}
      {indicador(353, "COMMITS NO ANO", n(commits), rodape_commits, "#db2777", .1)}
      {indicador(666, "SEGUIDORES", n(p["seguidores"]), "NO GITHUB", "#2563eb", .2)}

      <text x="76" y="158" font-size="9.5" letter-spacing="2.4" fill="#7e22ce">CALENDÁRIO DE CONTRIBUIÇÕES</text>
      <text x="956" y="158" font-size="10" letter-spacing="1.2" text-anchor="end" fill="#4b5563" font-family="SFMono-Regular, Consolas, Menlo, monospace">sequência {n(atual)}d &#183; recorde {n(melhor)}d</text>
      {marcos}{rotulos}{quadros}

      <text x="76" y="330" font-size="9.5" letter-spacing="2.4" fill="#2563eb">MISTURA DE LINGUAGENS</text>
      {barra}
      {legenda}

      <circle class="vivo" cx="45" cy="412" r="4" fill="#16a34a"/>
      <text x="59" y="416" font-size="9" letter-spacing="1.3" fill="#6b7280" font-family="SFMono-Regular, Consolas, Menlo, monospace">ATUALIZADO EM {carimbo}</text>
    </g>
    <rect x="1" y="1" width="998" height="446" rx="28" fill="none" stroke="#9333ea" stroke-opacity=".2" stroke-width="2"/>
  </g>
</svg>
"""


if __name__ == "__main__":
    temas.gravar("telemetria", montar())
    print("telemetria gerada nos dois temas")

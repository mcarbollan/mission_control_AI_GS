"""Visualização local do Mission Control AI para demonstração no navegador.

Não substitui a CLI obrigatória: apenas apresenta o mesmo motor em localhost.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from src.engine import MissionEngine


engine = MissionEngine()


PAGINA = r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mission Control AI | EnviroSat</title>
  <style>
    :root { color-scheme: dark; --ink:#eaf7ff; --muted:#9cb4c9; --line:#27445a; --panel:#102433; --bg:#07131e; --cyan:#47d7ff; --amber:#ffc857; --red:#ff6f6f; }
    * { box-sizing:border-box; } body { margin:0; font:16px/1.5 Inter,Segoe UI,Arial,sans-serif; color:var(--ink); background:radial-gradient(circle at top right,#16364a,transparent 45%),var(--bg); }
    main { max-width:1180px; margin:auto; padding:2rem 1.25rem 3rem; } h1 { margin:0; font-size:clamp(2rem,5vw,4rem); letter-spacing:.04em; color:var(--cyan); } h2 { margin-top:0; } .eyebrow { color:var(--cyan); letter-spacing:.15em; font-weight:700; text-transform:uppercase; } .sub { color:var(--muted); margin:.25rem 0 1.5rem; }
    .panel { border:1px solid var(--line); background:color-mix(in srgb,var(--panel) 90%,transparent); border-radius:16px; padding:1.25rem; box-shadow:0 16px 40px #0004; } .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(185px,1fr)); gap:.8rem; margin:1rem 0; } .metric { border:1px solid var(--line); border-radius:12px; padding:.85rem; } .metric span { color:var(--muted); display:block; font-size:.83rem; } .metric strong { font-size:1.45rem; }
    .toolbar { display:flex; flex-wrap:wrap; gap:.7rem; align-items:center; } button { cursor:pointer; color:var(--ink); background:#173b52; border:1px solid #3d6a83; border-radius:8px; padding:.65rem .95rem; font-weight:700; } button:hover { border-color:var(--cyan); } button[data-scenario="critico"] { background:#632d35; border-color:#a4545f; } .status { font-weight:800; } .status.NORMAL { color:#77e2a3; } .status.ATENÇÃO { color:var(--amber); } .status.CRÍTICO { color:var(--red); }
    .columns { display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem; } ul { padding-left:1.2rem; } li { margin:.5rem 0; } textarea { width:100%; min-height:100px; background:#091923; color:var(--ink); border:1px solid var(--line); border-radius:8px; padding:.75rem; font:inherit; } pre { white-space:pre-wrap; font:inherit; margin:0; } .muted { color:var(--muted); } footer { color:var(--muted); font-size:.9rem; margin-top:1rem; }
    @media (max-width:720px) { .columns { grid-template-columns:1fr; } }
  </style>
</head>
<body><main>
  <p class="eyebrow">Global Solution 2026.1 · Observação ambiental</p>
  <h1>MISSION CONTROL AI</h1>
  <p class="sub">EnviroSat-01 · Telemetria simulada, decisões em Python e análise contextual via Ollama Cloud.</p>
  <section class="panel"><div class="toolbar">
    <strong>Cenários de demonstração:</strong>
    <button data-scenario="normal">Operação normal</button>
    <button data-scenario="critico">Cenário crítico</button>
    <button data-scenario="aleatorio">Nova leitura aleatória</button>
    <span id="status" class="status">CARREGANDO</span>
  </div>
  <div id="metrics" class="grid"></div></section>
  <div class="columns"><section class="panel"><h2>Alertas e resposta automática</h2><div id="alerts" class="muted">Carregando telemetria…</div></section>
  <section class="panel"><h2>Pergunte ao operador IA</h2><textarea id="question">Faça um diagnóstico da missão, priorize as ações e explique o impacto para as brigadas ambientais.</textarea><p><button id="analyze">Gerar análise contextual</button></p><pre id="answer" class="muted">A análise usará a leitura de telemetria exibida acima.</pre></section></div>
  <footer>Protótipo acadêmico. Focos de calor exigem validação humana; a aplicação não aciona órgãos externos.</footer>
</main><script>
const metricLabels={temperatura_sensor_c:'Temperatura do sensor',qualidade_sensor_optico_pct:'Qualidade RGB+NIR',buffer_imagens_pct:'Buffer de imagens',energia_pct:'Energia disponível',precisao_geolocalizacao_m:'Precisão de geolocalização',focos_calor_detectados:'Focos de calor detectados'};
const units={temperatura_sensor_c:' °C',qualidade_sensor_optico_pct:'%',buffer_imagens_pct:'%',energia_pct:'%',precisao_geolocalizacao_m:' m',focos_calor_detectados:''};
async function api(path,body){const r=await fetch(path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});return r.json()}
function render(payload){const {dados,resultado}=payload; document.querySelector('#status').textContent='STATUS: '+resultado.status; document.querySelector('#status').className='status '+resultado.status; document.querySelector('#metrics').innerHTML=Object.entries(metricLabels).map(([key,label])=>`<div class="metric"><span>${label}</span><strong>${dados[key]}${units[key]}</strong></div>`).join(''); const a=resultado.alertas.length?'<ul>'+resultado.alertas.map(x=>`<li><strong>${x.nivel} · ${x.parametro}</strong><br>${x.mensagem}<br><span class="muted">Impacto: ${x.impacto}</span></li>`).join('')+'</ul>':'<p>Nenhum alerta. Manter monitoramento periódico.</p>'; document.querySelector('#alerts').innerHTML=a+'<h3>Ações automáticas</h3><ul>'+resultado.acoes_automaticas.map(x=>`<li>${x}</li>`).join('')+'</ul>';}
async function update(){render(await api('/api/status'))}
async function analyze(){const answer=document.querySelector('#answer');answer.textContent='Consultando a Ollama Cloud…';const r=await api('/api/analyze',{pergunta:document.querySelector('#question').value});answer.textContent=r.resposta}
document.querySelectorAll('[data-scenario]').forEach(b=>b.onclick=async()=>{await api('/api/scenario',{cenario:b.dataset.scenario}); await update()}); document.querySelector('#analyze').onclick=analyze;
(async()=>{await update(); if(new URLSearchParams(location.search).has('analyze')) await analyze()})();
</script></body></html>'''


class Handler(BaseHTTPRequestHandler):
    def responder_json(self, conteudo, status=200):
        corpo = json.dumps(conteudo, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def leitura_atual(self):
        dados, resultado = engine._coletar_e_avaliar()
        return {"dados": dados, "resultado": resultado}

    def do_GET(self):
        if self.path == "/":
            corpo = PAGINA.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
        elif self.path == "/api/status":
            self.responder_json(self.leitura_atual())
        else:
            self.responder_json({"erro": "Rota não encontrada."}, 404)

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        try:
            conteudo = json.loads(self.rfile.read(tamanho) or b"{}")
        except json.JSONDecodeError:
            self.responder_json({"erro": "JSON inválido."}, 400)
            return
        if self.path == "/api/scenario":
            engine.definir_cenario(conteudo.get("cenario", "aleatorio"))
            self.responder_json({"ok": True})
        elif self.path == "/api/analyze":
            pergunta = conteudo.get("pergunta", "Como está a missão?").strip()
            self.responder_json({"resposta": engine.analyze(pergunta)})
        else:
            self.responder_json({"erro": "Rota não encontrada."}, 404)

    def log_message(self, formato, *args):
        return


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Mission Control AI disponível em http://127.0.0.1:8000")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()

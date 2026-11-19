"""Motor de análise do Mission Control AI."""
import os
from pathlib import Path
from ollama import Client
from dotenv import load_dotenv
from src import telemetria, alertas

load_dotenv()
TRILHA = "envirosat"

def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia a análise para o modelo gpt-oss:120b na Ollama Cloud."""
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        return ("A chave OLLAMA_API_KEY não foi encontrada. "
                "Configure o arquivo .env para habilitar a análise generativa.")
    client = Client(
        host="https://ollama.com",
        headers={"Authorization": "Bearer " + api_key}
    )
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        resposta = client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )
        return resposta["message"]["content"].strip()
    except Exception as erro:
        return f"Não foi possível consultar a Ollama Cloud: {erro}"

def load_system_prompt():
    caminho = Path(__file__).resolve().parent.parent / "prompts" / "system_prompt.md"
    return caminho.read_text(encoding="utf-8") if caminho.exists() else "Você é um assistente de operações espaciais."

class MissionEngine:
    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.ultimo_dado = None
        self.ultimo_resultado = None
        self.cenario = "aleatorio"

    def is_ready(self):
        return True

    def definir_cenario(self, cenario):
        if cenario not in ("normal", "critico", "aleatorio"):
            return "Cenário inválido. Use normal, critico ou aleatorio."
        self.cenario = cenario
        self.ultimo_dado = None
        self.ultimo_resultado = None
        return f"Cenário alterado para: {cenario.upper()}"

    def _coletar_e_avaliar(self):
        self.ultimo_dado = telemetria.coletar(self.cenario)
        self.ultimo_resultado = alertas.avaliar(self.ultimo_dado)
        return self.ultimo_dado, self.ultimo_resultado

    def status_snapshot(self):
        dados, resultado = self._coletar_e_avaliar()
        linhas = [
            f"Satélite: {dados['satelite']} | Trilha: EnviroSat",
            f"Horário: {dados['horario']}",
            f"Temperatura do sensor: {dados['temperatura_sensor_c']} °C",
            f"Qualidade do sensor óptico RGB+NIR: {dados['qualidade_sensor_optico_pct']}%",
            f"Buffer de imagens: {dados['buffer_imagens_pct']}%",
            f"Energia disponível: {dados['energia_pct']}%",
            f"Precisão de geolocalização: {dados['precisao_geolocalizacao_m']} m",
            f"Focos de calor detectados: {dados['focos_calor_detectados']}",
            f"STATUS DA MISSÃO: {resultado['status']}",
        ]
        if resultado["alertas"]:
            linhas.append("Alertas: " + "; ".join(a["mensagem"] for a in resultado["alertas"]))
        else:
            linhas.append("Alertas: nenhum.")
        linhas.append("Ações automáticas: " + "; ".join(resultado["acoes_automaticas"]))
        return "\n".join(linhas)

    def analyze(self, pergunta_usuario):
        # A análise explica a mesma leitura exibida no último /status. Isso evita
        # que o operador veja uma telemetria e a IA responda sobre outra.
        if self.ultimo_dado is None or self.ultimo_resultado is None:
            dados, resultado = self._coletar_e_avaliar()
        else:
            dados, resultado = self.ultimo_dado, self.ultimo_resultado
        contexto = (
            f"TELEMETRIA: {dados}\n"
            f"AVALIAÇÃO DETERMINÍSTICA EM PYTHON: {resultado}\n"
            f"PERGUNTA DO OPERADOR: {pergunta_usuario}\n"
            "Produza diagnóstico, prioridade, ações recomendadas e impacto terrestre."
        )
        return llm(contexto, system=self.system_prompt)

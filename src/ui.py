"""Interface CLI estilo Claude Code para o Mission Control AI."""
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))

def show_banner():
    banner = pyfiglet.figlet_format("Mission Control", font="slant")
    console.print(Text(banner, style="bold #06B6D4"))
    console.print(Panel.fit(
        "Monitoramento ambiental orbital com análise por IA generativa.\n"
        "Trilha: EnviroSat · Modelo: gpt-oss:120b via Ollama Cloud\n"
        "Comandos: /help /status /about /normal /critico /aleatorio /clear /exit",
        title="◆ MISSION CONTROL", border_style="#06B6D4"
    ))

def show_response(conteudo):
    agora = datetime.now().strftime("%H:%M:%S")
    console.print(Panel(str(conteudo), title="◆ Mission Control", subtitle=agora,
                        border_style="#06B6D4"))

def show_help():
    tabela = Table(title="Comandos disponíveis")
    tabela.add_column("Comando", style="cyan")
    tabela.add_column("Função")
    for cmd, desc in [
        ("/help", "Mostra esta ajuda"),
        ("/status", "Coleta telemetria e mostra o estado da missão"),
        ("/normal", "Seleciona cenário simulado normal"),
        ("/critico", "Seleciona cenário simulado crítico"),
        ("/aleatorio", "Seleciona telemetria aleatória"),
        ("/about", "Mostra a proposta do projeto"),
        ("/clear", "Limpa o terminal"),
        ("/exit", "Encerra o sistema"),
    ]:
        tabela.add_row(cmd, desc)
    console.print(tabela)

def run_cli(engine):
    show_banner()
    console.print("[green]✓ Engine status: OPERACIONAL[/green]\n")
    while True:
        try:
            entrada = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not entrada:
            continue
        if entrada == "/exit":
            console.print("Encerrando a missão. Até logo!")
            break
        elif entrada == "/help":
            show_help()
        elif entrada == "/status":
            show_response(engine.status_snapshot())
        elif entrada == "/about":
            show_response(
                "O EnviroSat simula um satélite de observação ambiental. "
                "O sistema monitora sensores térmico e óptico, energia, buffer e geolocalização. "
                "A proposta é apoiar operadores ambientais e brigadas na priorização "
                "de áreas que precisam de verificação em terra."
            )
        elif entrada == "/clear":
            console.clear()
            show_banner()
        elif entrada in ("/normal", "/critico", "/aleatorio"):
            cenario = entrada[1:]
            show_response(engine.definir_cenario(cenario))
        else:
            show_response(engine.analyze(entrada))

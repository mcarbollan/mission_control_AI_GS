"""Geração de telemetria simulada para a trilha EnviroSat."""
import json
import random
from datetime import datetime
from pathlib import Path


CAMINHO_CENARIOS = Path(__file__).resolve().parent.parent / "data" / "cenarios.json"


def carregar_cenario(nome):
    """Lê os cenários fixos usados na demonstração e nos testes manuais."""
    with CAMINHO_CENARIOS.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)[nome]

def coletar(cenario="aleatorio"):
    """Retorna uma leitura simulada dos sensores do satélite ambiental."""
    if cenario in ("normal", "critico"):
        valores = carregar_cenario(cenario)
    else:
        valores = {
            "temperatura_sensor_c": round(random.uniform(25, 82), 1),
            "qualidade_sensor_optico_pct": random.randint(55, 100),
            "buffer_imagens_pct": random.randint(20, 100),
            "energia_pct": random.randint(10, 100),
            "precisao_geolocalizacao_m": round(random.uniform(3, 45), 1),
            "focos_calor_detectados": random.randint(0, 30),
        }
    return {
        "satelite": "EnviroSat-01",
        "trilha": "EnviroSat",
        "horario": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        **valores,
    }

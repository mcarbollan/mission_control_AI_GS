"""Testes básicos das regras essenciais da missão simulada."""
import unittest
from unittest.mock import patch

from src import alertas, telemetria
from src.engine import MissionEngine


class TestMissionControl(unittest.TestCase):
    def test_cenario_normal_sem_alertas(self):
        resultado = alertas.avaliar(telemetria.coletar("normal"))
        self.assertEqual(resultado["status"], "NORMAL")
        self.assertEqual(resultado["alertas"], [])

    def test_cenario_critico_tem_alertas_e_resposta_automatica(self):
        resultado = alertas.avaliar(telemetria.coletar("critico"))
        self.assertEqual(resultado["status"], "CRÍTICO")
        self.assertEqual(len(resultado["alertas"]), 6)
        self.assertTrue(resultado["acoes_automaticas"])

    def test_ia_recebe_a_mesma_leitura_exibida_no_status(self):
        motor = MissionEngine()
        motor.definir_cenario("critico")
        motor.status_snapshot()
        leitura_exibida = motor.ultimo_dado
        with patch("src.engine.llm", side_effect=lambda prompt, **_: prompt):
            contexto = motor.analyze("Como está a missão?")
        self.assertEqual(motor.ultimo_dado, leitura_exibida)
        self.assertIn(str(leitura_exibida), contexto)


if __name__ == "__main__":
    unittest.main()

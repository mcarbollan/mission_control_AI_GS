"""Regras determinísticas de alerta: a decisão crítica fica no Python."""
def avaliar(dados):
    alertas = []
    acoes = []

    if dados["temperatura_sensor_c"] > 60:
        alertas.append({
            "nivel": "CRÍTICO",
            "parametro": "Temperatura do sensor",
            "mensagem": "Temperatura acima de 60 °C.",
            "impacto": "O sensor térmico pode perder precisão na identificação de focos de calor."
        })
        acoes.append("Ativar protocolo de proteção térmica e reduzir temporariamente a carga do sensor.")

    if dados["qualidade_sensor_optico_pct"] < 75:
        alertas.append({
            "nivel": "ALTO",
            "parametro": "Sensor óptico RGB+NIR",
            "mensagem": "Qualidade do sensor óptico abaixo de 75%.",
            "impacto": "As imagens podem perder qualidade para análise de cobertura vegetal e áreas protegidas."
        })
        acoes.append("Programar calibração do sensor óptico e sinalizar a qualidade reduzida nos produtos de imagem.")

    if dados["buffer_imagens_pct"] >= 85:
        alertas.append({
            "nivel": "ALTO",
            "parametro": "Buffer de imagens",
            "mensagem": "Armazenamento de imagens acima de 85%.",
            "impacto": "Novas imagens de áreas ambientais podem deixar de ser armazenadas até o próximo downlink."
        })
        acoes.append("Priorizar a transmissão das imagens de áreas com focos de calor e liberar espaço após confirmação do envio.")

    if dados["energia_pct"] < 20:
        alertas.append({
            "nivel": "CRÍTICO",
            "parametro": "Energia",
            "mensagem": "Energia disponível abaixo de 20%.",
            "impacto": "A coleta e a transmissão de imagens ambientais podem ser interrompidas."
        })
        acoes.append("Ativar modo de economia de energia, preservando os sistemas essenciais.")

    if dados["precisao_geolocalizacao_m"] > 25:
        alertas.append({
            "nivel": "ALTO",
            "parametro": "Precisão de geolocalização",
            "mensagem": "Erro de localização acima de 25 metros.",
            "impacto": "Equipes em terra podem receber coordenadas imprecisas para verificar incêndios ou desmatamento."
        })
        acoes.append("Revalidar a solução de localização antes de distribuir coordenadas às equipes.")

    if dados["focos_calor_detectados"] >= 20:
        alertas.append({
            "nivel": "ALTO",
            "parametro": "Focos de calor",
            "mensagem": "Quantidade elevada de focos de calor detectados.",
            "impacto": "Pode haver aumento da demanda por análise e resposta das brigadas ambientais."
        })
        acoes.append("Priorizar imagens da região e encaminhar os pontos para validação por operadores.")

    return {
        "status": "CRÍTICO" if any(a["nivel"] == "CRÍTICO" for a in alertas)
                  else "ATENÇÃO" if alertas else "NORMAL",
        "alertas": alertas,
        "acoes_automaticas": acoes or ["Manter monitoramento periódico."]
    }

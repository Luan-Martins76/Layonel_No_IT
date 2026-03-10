from flask import Flask, render_template, request, jsonify
import random
import requests
import markdown

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

usuario = {
    "nome": "Visitante",
}

contadores = {
    "total": 0,
    "else": 0,
    "dia": 0,
    "meu_nome": 0,
    "calcuradora": 0
}

agenda = {
    "segunda": {
        "materia": "FUNDAMENTOS DE ENGENHARIA DE DADOS",
        "professor": "EDUARDO",
        "inicio": "19:00",
        "termino": "21:50",
        "local": "BLOCO H, SALA 110"
    },
    "terça": {
        "materia": "FUNDAMENTOS MATEMÁTICOS PARA COMPUTAÇÃO",
        "professor": "Otoniel",
        "inicio": "19:00",
        "termino": "21:50",
        "local": "BLOCO H, SALA 110"
    },
    "quarta": {
        "materia": "INTRODUÇÃO À ENGENHARIA DE SOLUÇÕES",
        "professor": "HENRIQUE LIMA",
        "inicio": "19:00",
        "termino": "22:40",
        "local": "BLOCO H, SALA 110"
    },
    "quinta": {
        "materia": "CIDADANIA, ÉTICA E ESPIRITUALIDADE",
        "professor": "HELEHON SANTOS",
        "inicio": "19:00",
        "termino": "21:40",
        "local": "BLOCO H, SALA 110"
    },
    "sexta": {
        "materia": "FUNDAMENTO DE COMPUTAÇÃO E INFRAESTRUTURA",
        "professor": "ARAÚJO",
        "inicio": "19:00",
        "termino": "21:40",
        "local": "BLOCO H, SALA 110"
    },
    "sabado": {
        "materia": "LEITURA E INTERPRETAÇÃO DE TEXTO - ONLINE",
        "professor": "[NÃO TEM, AUTODIDATA MAN]",
        "inicio": "[QUANDO QUISER (SÓ NÃO INVENTA DE NÃO FAZER)]",
        "termino": "[NO SEU TEMPO IRMÃO]",
        "local": "[SUA CASA]"
    }
}

respostas = [
    "Calma lá paizão, aqui só tem um if só. Seloko...",
    "Seloko, sou rede neural não man",
    "Luan quando me configurou não pensou nesta possibilidade",
    "Você poderia escrever um dia da semana para eu mostrar a minha utilidade né?",
    "*pensando para dar uma resposta* Atahhh eu não penso, não sou rede neural...",
    "Meu sonho era ser o GPT, mas desisti quando vi isso ai. Seloko, não compensa.",
    "Interessante... Vou fingir que processei isso.",
    "Isso parece importante, mas não o suficiente para eu virar uma IA e te responder",
    "Entendi. Não concordo, mas entendi.",
    "Se eu tivesse sentimentos, estaria julgando agora.",
    "Ótimo ponto. Próximo.",
    "Você digitou isso com convicção né? Eu respeito isso.",
    "Isso diz mais sobre você do que sobre mim",
    "Anotado mentalmente (mentira)",
    "Vou responder isso na próxima atualização... Talvez.",
    "Essa pergunta foi corajosa.",
    "Processando... *erro 404: paciência não encontrada*.",
    "Se isso fosse um teste, você passou. Em que? Eu não sei.",
    "Não fui treinado para lidar com isso. Na verdade, não fui treinado para nada - sou um agente baseado em regras.",
    "Essa foi uma escolha de palavras.",
    "Martins tá no primeiro período... Se acha que isso aqui responde essa interação ai? kkkkkkk"
]


def call_llm(model, prompt, temperature=0.3):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
    )
    return response.json()["response"]


@app.route('/')
def index():
    return render_template('interface.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensagem = data.get('mensagem', '').strip().lower()  # ✅ chave correta e consistente

    contadores['total'] += 1
    resposta = ""
    respondeu = False  #flag para saber se as regras já resolveram

    # --- REGRAS FIXAS (agenda, nome, etc.) ---

    dia_encontrado = None
    for dia in agenda:
        if dia in mensagem:
            dia_encontrado = dia
            break

    if dia_encontrado:
        aula = agenda[dia_encontrado]
        contadores['dia'] += 1

        if contadores['dia'] == 4:
            resposta = "🥴 Tá bom, tá bom... VOCÊ venceu, parabéns? 🤨 Vou responder só o que o Martins falou para eu fazer 🤡"
        elif contadores['dia'] == 3:
            resposta = "É uma aula só que tu vai ter hoje seu maldito! Tá me perguntando os dias tudo porque? 🤨"
        else:
            resposta = (
                f"Tem uma aula do balacobaco de {aula['materia']} com o professor {aula['professor']}. "
                f"Começa às {aula['inicio']} e termina às {aula['termino']}. "
                f"Local é {aula['local']} 📚"
            )
        respondeu = True  # ✅ marca que já tem resposta

    elif "criador" in mensagem:
        resposta = "Martins 😀. Olha o instagram do man: luan_henrique76l"
        respondeu = True

    elif "nome" in mensagem and ("seu" in mensagem or "qual" in mensagem):
        contadores['meu_nome'] += 1
        if contadores['meu_nome'] >= 4:
            resposta = "Skynet 🤖"
        elif contadores['meu_nome'] == 3:
            resposta = "Acho que eu escolhi outro... 😑"
        else:
            resposta = "Meu nome é Lionel No IT 😉"
        respondeu = True

    elif "calculadora" in mensagem:
        resposta = "Calculadora? Cara, tem uma no seu celular... Mas tudo bem, me manda os números e a operação (+, -, *, /) 🧮"
        respondeu = True

    elif mensagem in ["sair", "tchau", "bye", "falou"]:
        resposta = "Falou man 👋 Até mais!"
        respondeu = True

    # Só vai pro LLM se nenhuma regra respondeu
    if not respondeu:
        try:
            resposta = call_llm("gemma3:4b", mensagem)
            if resposta and len(resposta) > 5:
                resposta_html = markdown.markdown(resposta)
                return jsonify({"source": "llm_small", "resposta": resposta_html})
        except Exception:
            pass  # gemma falhou, tenta o maior

        try:
            resposta = call_llm("mistral-nemo:12b", mensagem)
            resposta_html = markdown.markdown(resposta)
            return jsonify({"source": "llm_big", "resposta": resposta_html})
        except Exception:
            # Se até o LLM grande falhar, cai no random das respostas
            resposta = random.choice(respostas)
            return jsonify({"source": "fallback", "resposta": resposta})

    return jsonify({"source": "regras", "resposta": resposta})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

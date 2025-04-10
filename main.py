
import openai
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import os
from datetime import datetime, timedelta
import random

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

atendentes = [
    {"nome": "Clara", "especialidade": "recuperação pós-parto"},
    {"nome": "Renata", "especialidade": "nutrição e compressão"},
    {"nome": "Paula", "especialidade": "autoestima e bem-estar"},
    {"nome": "Camila", "especialidade": "orientação emocional e leveza no dia a dia"},
]

sessoes = {}
saudacoes_simples = ['oi', 'olá', 'boa noite', 'bom dia', 'boa tarde', 'e aí', 'opa']

def quebrar_texto(texto, limite=3800):
    partes = []
    while len(texto) > limite:
        quebra = texto.rfind("\n", 0, limite)
        if quebra == -1:
            quebra = limite
        partes.append(texto[:quebra])
        texto = texto[quebra:]
    partes.append(texto)
    return partes

def calcular_delay_realista(texto):
    tamanho = len(texto)
    if tamanho < 300:
        return random.uniform(4, 6)
    elif tamanho < 800:
        return random.uniform(6, 9)
    else:
        return random.uniform(8, 12)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    atendente = random.choice(atendentes)
    sessoes[chat_id] = {
        "atendente": atendente,
        "ultimo_contato": datetime.now(),
        "boas_vindas_dada": True
    }
    await asyncio.sleep(random.uniform(2.5, 4))
    await update.message.reply_text(
        f"Oi, tudo certinho por aí? Eu sou a {atendente['nome']}, tô por aqui de plantão pra te ajudar com o que precisar, viu? 💛"
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    agora = datetime.now()
    pergunta = update.message.text.strip().lower()

    if chat_id not in sessoes:
        atendente = random.choice(atendentes)
        sessoes[chat_id] = {
            "atendente": atendente,
            "ultimo_contato": agora,
            "boas_vindas_dada": False
        }

    ultima = sessoes[chat_id]["ultimo_contato"]
    if agora - ultima > timedelta(minutes=10):
        atendente = random.choice(atendentes)
        sessoes[chat_id] = {
            "atendente": atendente,
            "ultimo_contato": agora,
            "boas_vindas_dada": False
        }
        await update.message.reply_text(
            f"A conversa anterior foi encerrada por inatividade. Agora quem continua com você sou eu, {atendente['nome']} 💛"
        )

    sessoes[chat_id]["ultimo_contato"] = agora
    atendente = sessoes[chat_id]["atendente"]

    if not sessoes[chat_id]["boas_vindas_dada"]:
        sessoes[chat_id]["boas_vindas_dada"] = True
        if pergunta in saudacoes_simples:
            await asyncio.sleep(random.uniform(2.5, 4))
            await update.message.reply_text(
                f"Oiê! Aqui é a {atendente['nome']} da equipe FDZ. Me fala o que você precisa que eu te ajudo!"
            )
            return
        else:
            await asyncio.sleep(random.uniform(2.5, 4))
            await update.message.reply_text(
                f"Oi, tudo certo? Aqui é a {atendente['nome']}, da equipe FDZ. Pode mandar sua dúvida, tá bom?"
            )

    if pergunta in saudacoes_simples and sessoes[chat_id]["boas_vindas_dada"]:
        return

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Você é a {atendente['nome']}, especialista em {atendente['especialidade']}. "
                                          f"Fale como uma mulher real, simpática, acolhedora e objetiva. "
                                          f"Não cumprimente de novo no meio da conversa. Seja prática e carinhosa, como quem tá ajudando de verdade no WhatsApp."},
            {"role": "user", "content": pergunta}
        ]
    )

    texto = resposta.choices[0].message.content
    partes = quebrar_texto(texto)

    for parte in partes:
        await asyncio.sleep(calcular_delay_realista(parte))
        await update.message.reply_text(parte.strip())

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
app.run_polling()

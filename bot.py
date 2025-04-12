#Instalar la librerias
#apikey Google AIzaSyAd2TLhNj5taMGmwtwD6p6LlBsIK9PCMiY
#token telegram: 7908199923:AAEOmmyKmDFQpnxYmAlAlhH53nqBJw30L1Y

#PASO 1. Importar las librerias
import os
from dotenv import load_dotenv
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler,ContextTypes, filters
import google.generativeai as genai

#PASO 2. CARGAR LAS VARIABLES DE ENTORNO
load_dotenv()
telegramToken=os.getenv("telegramToken")
geminiApi=os.getenv("geminiApi")

#PASO 3. COMUNICARNOS CON GEMINI Y CONFIGURARLO
genai.configure(api_key=geminiApi)

#PASO 4. CREAR EL MODELO
modelo=genai.GenerativeModel("gemini-1.5-pro-002")

#PASO 5. CARGADO DEL MODELO
logging.basicConfig(level=logging.INFO)

#PASO 6. CREAR UNA FUNCION PARA EL MANEJO DE LOS MENSAJES
async def obtenerMensajes(update:Update, context:ContextTypes.DEFAULT_TYPE):
    mensajeUsuario=update.message.text
    respuesta=modelo.generate_content(mensajeUsuario)
    await update.message.reply_text(respuesta.text)

#PASO 7. FUNCION PARA INICIAR EL MODELO
async def inicar(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola bienvenido al modulo iaPython en Ucatec. Cual es tu consulta?")

#PASO 8. EJECUTAR EL BOT
if __name__=="__main__":
    app=ApplicationBuilder().token(telegramToken).build()

    app.add_handler(CommandHandler("start",inicar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, obtenerMensajes))

    print("Bot iniciado...")
    app.run_polling()
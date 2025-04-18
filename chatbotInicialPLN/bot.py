#Instalar la librerias

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


#PROCESAR EL CONOCIMIENTO BASE DE LA EMPRESA
with open("entrenamiento.txt","r",encoding="utf-8")as file:
    entrenamiento=file.read()

#PASO 3. COMUNICARNOS CON GEMINI Y CONFIGURARLO
genai.configure(api_key=geminiApi)

#PASO 4. CREAR EL MODELO
modelo=genai.GenerativeModel("gemini-1.5-pro-002")

#PASO 5. CARGADO DEL MODELO
logging.basicConfig(level=logging.INFO)

#PASO 6. CREAR UNA FUNCION PARA EL MANEJO DE LOS MENSAJES
async def obtenerMensajes(update:Update, context:ContextTypes.DEFAULT_TYPE):
    mensajeUsuario=update.message.text
    prompt=f"""Tomaras el rol de agente de ventas virtual de la empresa UCATEC solo usaras la siguiente informacion para responder:
    {entrenamiento} pregunta al usuario: {mensajeUsuario} 
    Responde de forma breve, clara y profesional.
"""
    try:

        respuesta=modelo.generate_content(prompt)
        await update.message.reply_text(respuesta.text)
    except Exception as e:
        await update.message.reply_text("Ocurrio un error al procesar...")

        
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
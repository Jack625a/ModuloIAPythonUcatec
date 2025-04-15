#Paso 1. Importar las librerias 
import os
from dotenv import load_dotenv
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler,ContextTypes, filters
from PIL import Image
import google.generativeai as genai

load_dotenv()
tokenTelegram=os.getenv("telegramToken")
geminiApi=os.getenv("geminiApi")

#Configuracion
genai.configure(api_key=geminiApi)
modeloVision=genai.GenerativeModel("gemini-1.5-flash-002")
modeloTexto=genai.GenerativeModel("gemini-1.5-pro-002")

#cARGAR EL ENTRENAMIENTO
with open("chatbotVision\entrenamiento.txt","r",encoding="utf-8")as f:
    contexto=f.read()

#Funcion para iniciar el modelo
async def inciar(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola bienvenido a UCATEC...")


async def responderUsuario(update:Update,context:ContextTypes.DEFAULT_TYPE):
    pregunta=update.message.text
    prompt=f"""
    Informacion de empresa: {contexto}

    Pregunta al cliente: {pregunta}
    Responde profesionalmente solo con la informacion proporcionada.
    No puedes salirte de la informacion proporcionada
      """
    
    respuesta=modeloTexto.generate_content(prompt)
    await update.message.reply_text(respuesta.text.strip())

#ANALISIS DEL COMPROBANTE
async def analizarImagen(update:Update,context:ContextTypes.DEFAULT_TYPE):
    foto=update.message.photo[-1]
    archivo=await foto.get_file()
    rutaImagen="comprobanteBot.jpg"
    await archivo.download_to_drive(rutaImagen)

    #Entrenamiento a la vision
    prompt="""
        Observa el comprobante de pago, donde extraeras el monto total, nombre del enviante y la fecha de la cancelacion
        El monto total del comprobante debera ser el mismo del producto seleccionado 
        Si no encuentras esos datos informaras al usuario que: "Pago no Verificado, porfavor vuelve a enviar tu comprobante de pago..."
     """
    imagen=Image.open(rutaImagen)
    respuesta=modeloVision.generate_content([prompt,imagen])

    await update.message.reply_text(f"{respuesta.text.strip()}")


app=ApplicationBuilder().token(tokenTelegram).build()
app.add_handler(CommandHandler("start",inciar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,responderUsuario))
app.add_handler(MessageHandler(filters.PHOTO, analizarImagen))

print("BOT ESTA INICIADO")
app.run_polling()


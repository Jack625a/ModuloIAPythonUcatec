#TESTEO DE LA VISION POR COMPUTADOR DE GEMINI

#Paso 1. Importar las librerias
import os
import google.generativeai as genai
from PIL import Image

#Paso 2. Configuraicon de la conexion
genai.configure(api_key="")

#Paso3. Crear el modelo de gemini vision
visionModelo=genai.GenerativeModel("gemini-1.5-flash-002")

#Paso 4. Crear la funcion para analizar imagenes (Ej. Comprobantes de pagos)
def analizarComprobante(imagen):
    imagenCargar=Image.open(imagen)

    #Prompt de entrenamiento
    prompt="""Observa el comprobante de pago enviado. Deberas extraer el monto total,  el nombre del enviante y la fecha que aparece en el comprobante
      Si no se encuentra deberas notificar al usuario con: "Pago no verificado"  """

    #Respuesta del modelo
    respuesta=visionModelo.generate_content([prompt,imagenCargar])
    return respuesta.text.strip()


#comprobante=Image.open("chatbotVision\comprobante.jpeg")
#comprobante.show()

print(analizarComprobante("chatbotVision\p.png"))
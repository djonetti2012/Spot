import pyttsx3
import speech_recognition as sr
import os
import os
from groq import Groq

# Establecer la variable de entorno
os.environ["GROQ_API_KEY"] = "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"
llamar_pregunta = ["tengo una pregunta", "pregunta", "tengo una duda", "duda", "responde", "explicame"]

client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
)

engine = pyttsx3.init()
reconocedor = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()



def escuchar_comando():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = reconocedor.listen(source)
        try:
            comando = reconocedor.recognize_google(audio, language="es-ES")
            print(f"Comando: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("No entendí el comando.")
            speak("No entendí el comando.")
            return None
        except sr.RequestError:
            print("Error en el servicio de reconocimiento de voz.")
            speak("Error en el servicio de reconocimiento de voz.")
            return None


def procesar_comando(comando):
    if comando is None:
        speak("No entendí el comando. Intenta de nuevo.")
        return

    if any(frase in comando for frase in llamar_pregunta):
        speak("¿que duda tiene señor?")
        pregunta = escuchar_comando()
        if pregunta is not None:
            # Inicializar el cliente de Groq con la clave API desde la variable de entorno
            

            # Crear la solicitud de chat completion
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": pregunta,
                    }
                ],
                model="llama3-8b-8192",
            )

            # Imprimir la respuesta
            print(chat_completion.choices[0].message.content)
            speak(chat_completion.choices[0].message.content)
            



    elif "salir" in comando or "adios" in comando or "buenas noches" in comando:
        pass

    

        
    else:
        speak("No entendí el comando. Intenta de nuevo.")

def main():
    speak("Buenos Dias señor")
    while True:
        comando = escuchar_comando()
        if comando is not None:
            if "spot" in comando:
                speak("Que quiere señor")
                comando = escuchar_comando()
                if "salir" in comando or "adios" in comando or "buenas noches" in comando:
                    speak("Buenas noches señor")
                    procesar_comando(comando)
                    break
        
                else:
                    procesar_comando(comando)
        

if __name__ == '__main__':
    main()



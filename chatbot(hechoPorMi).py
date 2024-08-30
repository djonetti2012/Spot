import pyttsx3
import speech_recognition as sr
import os
from groq import Groq

# Establecer la variable de entorno
os.environ["GROQ_API_KEY"] = "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"
llamar_pregunta = ["tengo una pregunta", "pregunta", "tengo una duda", "duda", "responde", "explicame"]
llamar_pregunta_ingenieria = ["ayudame en robotica", "ayudame en informatica", "ayudame en ingenieria", "ayudame con esta pregunta de robotica", "tengo una duda en robotica", "tengo una duda en informatica", "ayudame en informatica"]
client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
)

engine = pyttsx3.init()
reconocedor = sr.Recognizer()
carpeta_notas = "notas"
comandos = {
    "pregunta": "puedes preguntar cualquier cosa que la inteligencia artificial te lo respondera",
    "crear nota": "podras crear todo tipo de notas o apuntes",
    "ver nota": "podras ver las notas creadas",
    "preguntas robotica": "podras preguntarle cualquier cosa de ingenieria",
    }
ruta_actual = os.getcwd()

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
            texto_chat = chat_completion.choices[0].message.content
            
            speak("¿te gustaria guardar el texto del chat?")
            te_gustaria_guardar_el_texto_del_chat = escuchar_comando()
            if te_gustaria_guardar_el_texto_del_chat is not None:
                if "si" in te_gustaria_guardar_el_texto_del_chat or "sí" in te_gustaria_guardar_el_texto_del_chat:
                    os.chdir(carpeta_notas)
                    speak("¿Cual es el titulo del chat?")
                    titulo_chat = escuchar_comando()
                    if titulo_chat is not None:
                        speak(f"¿El titulo para el chat es {titulo_chat}?")
                        confirmacion = escuchar_comando()
                        if confirmacion is not None:
                            if "sí" in confirmacion or "si" in confirmacion:
                                f = open(f"{titulo_chat}.txt", "w")
                                f.write(f"{texto_chat}")
                                os.chdir(ruta_actual)
                                speak("chat guardado correctamente")
                            elif "no" in confirmacion:
                                speak("de acuerdo señor")
            else:
                speak("No recibi confirmación")


    elif any(frase in comando for frase in llamar_pregunta_ingenieria):
            speak("¿que duda tiene señor?")
            pregunta = escuchar_comando()
            if pregunta is not None:

                # Crear la solicitud de chat completion
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "eres un ayudante personal para un adolescente en robotica, programacion, ingenieria aerospacial y ingenieria, tienes que ayudarle a crear todo lo que te pida dandole componentes, codigo, muchos detalles y ayudarle en lo que necesite",
                        },
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
                texto_chat = chat_completion.choices[0].message.content
            
                speak("¿te gustaria guardar el texto del chat?")
                te_gustaria_guardar_el_texto_del_chat = escuchar_comando()
                if te_gustaria_guardar_el_texto_del_chat is not None:
                    if "si" in te_gustaria_guardar_el_texto_del_chat or "sí" in te_gustaria_guardar_el_texto_del_chat:
                        os.chdir(carpeta_notas)
                        speak("¿Cual es el titulo del chat?")
                        titulo_chat = escuchar_comando()
                        if titulo_chat is not None:
                            speak(f"¿El titulo para el chat es {titulo_chat}?")
                            confirmacion = escuchar_comando()
                            if confirmacion is not None:
                                if "sí" in confirmacion or "si" in confirmacion:
                                    f = open(f"{titulo_chat}.txt", "w")
                                    f.write(f"{texto_chat}")
                                    os.chdir(ruta_actual)
                                    speak("chat guardado correctamente")
                                elif "no" in confirmacion:
                                    speak("de acuerdo señor")
                else:
                    speak("No recibi confirmación")


            
            


    elif "crear nota" in comando:
        os.chdir(carpeta_notas)
        speak("¿Cual es el titulo de la nota?")
        titulo_nota = escuchar_comando()
        if titulo_nota is not None:
            speak(f"¿El titulo para la nota es {titulo_nota}?")
            confirmacion = escuchar_comando()
            if confirmacion is not None: 
                if "sí" in confirmacion or "si" in confirmacion:
                    f = open(f"{titulo_nota}.txt", "w")
                    speak("¿cual es el texto de la nota?")
                    texto_nota = escuchar_comando()
                    if texto_nota is not None:
                        speak(f"el texto que quiere para la nota es{texto_nota}")
                        confirmacion = escuchar_comando()
                        if confirmacion is not None:
                            if "sí" in confirmacion or "si" in confirmacion:
                                f.write(f"{texto_nota}")
                                speak("nota creada")
                                os.chdir(ruta_actual)
                            else:
                                speak("no se pudo confirmar")
                                os.chdir(ruta_actual)
                        else:
                            speak("no entendi el mensaje")
                            os.chdir(ruta_actual)
                else:
                    speak("no se pudo confirmar")
                    os.chdir(ruta_actual)
            else:
                speak("no pude entender el mensaje")
                os.chdir(ruta_actual)

    elif "ver notas" in comando or "listar notas" in comando:
        os.chdir(carpeta_notas)
        notas = os.listdir()
        if notas:
            # Enumerar y anunciar las notas disponibles
            for i, nota in enumerate(notas):
                print(f"{i + 1}. {nota}")
                speak(f"Nota número {i + 1}: {nota}")

            # Diccionario para convertir palabras a números
            palabras_a_numeros = {
                "uno": 1,
                "dos": 2,
                "tres": 3,
                "cuatro": 4,
                "cinco": 5,
                "seis": 6,
                "siete": 7,
                "ocho": 8,
                "nueve": 9,
                "diez": 10,
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
            }

            speak("¿Qué número de nota quieres ver?")
            num_palabra = escuchar_comando()

            if num_palabra in palabras_a_numeros:
                num_nota = palabras_a_numeros[num_palabra]
                if 1 <= num_nota <= len(notas):
                    nombre_archivo = notas[num_nota - 1]
                    with open(nombre_archivo, "r") as f:
                        contenido = f.read()
                        print(f"Contenido de {nombre_archivo}:")
                        print(contenido)
                        speak(f"El contenido de la nota es: {contenido}")
                else:
                    speak("Número de nota inválido.")
            else:
                speak("No entendí el número. Intenta de nuevo.")
        else:
            speak("No hay notas en la carpeta.")

    elif "borrar nota" in comando:
        os.chdir(carpeta_notas)
        notas = os.listdir()
    
        if notas:
            # Enumerar y anunciar las notas disponibles
            for i, nota in enumerate(notas):
                print(f"{i + 1}. {nota}")
                speak(f"Nota número {i + 1}: {nota}")

            # Diccionario para convertir palabras a números
            palabras_a_numeros = {
                "uno": 1,
                "dos": 2,
                "tres": 3,
                "cuatro": 4,
                "cinco": 5,
                "seis": 6,
                "siete": 7,
                "ocho": 8,
                "nueve": 9,
                "diez": 10,
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
            }

            speak("¿Qué número de nota quieres borrar?")
            num_palabra = escuchar_comando()

            if num_palabra in palabras_a_numeros:
                num_nota = palabras_a_numeros[num_palabra]
                if 1 <= num_nota <= len(notas):
                    nombre_archivo = notas[num_nota - 1]
                    os.remove(nombre_archivo)
                    speak(f"Nota {nombre_archivo} borrada.")
                    print(f"Nota {nombre_archivo} borrada.")
                else:
                    speak("Número de nota inválido.")
            else:
                speak("No entendí el número. Intenta de nuevo.")
        else:
            speak("No hay notas en la carpeta.")

        os.chdir(ruta_actual)
        

    elif "di" in comando:
        speak("que quieres que diga")
        text_to_say = escuchar_comando()
        if text_to_say is not None:
            speak(text_to_say)

    elif "apagar pc" in comando or "apagar ordenador" in comando or "apagar" in comando:
        speak("¿seguro?")
        seguro = escuchar_comando()
        if seguro is not None:
            if "si" in seguro or "sí" in seguro:
                os.system("shutdown -s -t 5")
            elif "no" in seguro:
                speak("de acuerdo señor")
            else:
                speak("no pude entender la confirmacion")

    elif "comandos" in comando:
        print(comandos)
        speak(comandos)
            
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
                if comando is not None:
                    if "salir" in comando or "adios" in comando or "buenas noches" in comando:
                        speak("Buenas noches señor")
                        procesar_comando(comando)
                        break
        
                    else:
                        procesar_comando(comando)
                else:
                    speak("no entendí el comando")
        

if __name__ == '__main__':
    main()



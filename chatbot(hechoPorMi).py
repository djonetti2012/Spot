import pyttsx3
import speech_recognition as sr
import os
from groq import Groq
import pyautogui as pg
import pygame
import random

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
carpeta_musica = "musica"
comandos = {
    "pregunta": "puedes preguntar cualquier cosa que la inteligencia artificial te lo respondera",
    "crear nota": "podras crear todo tipo de notas o apuntes",
    "ver nota": "podras ver las notas creadas",
    "preguntas ingenieria": "podras preguntarle cualquier cosa de ingenieria",
    "apagar": "podras apagar el pc",
    "di": "podras hacer que spot diga cualquier cosa",
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

def reproducir_musica(nombre_archivo):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(nombre_archivo)
        pygame.mixer.music.play()
        
        # Esperar hasta que termine de reproducir
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        speak(f"Error al reproducir el archivo de música: {e}")


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
                elif "no":
                    speak("de acuerdo señor")
                    print("de acuerdo señor")
                    
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

    elif "modo desarrollo" in comando:
        ModoDesarrollo = True
        carpeta_musica = "musica"  # Asegúrate de tener una carpeta llamada "musica" con archivos de música
        ruta_actual = os.getcwd()  # Guarda la ruta actual
        os.chdir(carpeta_musica)

        # Inicializar pygame mixer
        pygame.mixer.init()
    
        while ModoDesarrollo:
            speak("¿Qué música quiere escuchar, señor?")
    
            # Cambia el directorio a la carpeta de música
            
    
            # Obtener la lista de archivos de música
            musicas = os.listdir()
            if musicas:
                # Enumerar y anunciar las opciones de música disponibles
                for i, musica in enumerate(musicas):
                    print(f"{i + 1}. {musica}")
                    speak(f"Música número {i + 1}: {musica}")
            
                # Ofrecer la opción de seleccionar aleatoriamente
                speak("Puede decir un número o decir 'aleatoria' para reproducir una música al azar.")
            
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
                    "aleatoria": "aleatoria",
                }

                num_palabra = escuchar_comando()

                if num_palabra in palabras_a_numeros:
                    if num_palabra == "aleatoria":
                        nombre_archivo = random.choice(musicas)
                    else:
                        num_musica = palabras_a_numeros[num_palabra]
                        if 1 <= num_musica <= len(musicas):
                            nombre_archivo = musicas[num_musica - 1]
                        else:
                            speak("Número de música inválido.")
                            continue

                    print(f"Reproduciendo {nombre_archivo}...")
                    speak(f"Reproduciendo {nombre_archivo}")
                    reproducir_musica(nombre_archivo)

                    # Preguntar si se quiere seguir en modo desarrollo
                    speak("¿Todavía está desarrollando, señor?")
                    confirmacion = escuchar_comando()
                    if "si" in confirmacion or "sí" in confirmacion:
                        speak("De acuerdo, señor")
                    else:
                        os.chdir(ruta_actual)
                        speak("Desactivando modo desarrollo")
                        ModoDesarrollo = False
                else:
                    speak("No entendí el comando. Intenta de nuevo.")
            else:
                speak("No hay música en la carpeta.")
                os.chdir(ruta_actual)
                ModoDesarrollo = False

        

    elif "modo hackeo" in comando:
        speak("modo hackeo activado")
        ModoHackeoActivado = True
        while ModoHackeoActivado == True:
            speak("ha dicho que quiere el modo hackeo")
            confirmacion = escuchar_comando()
            if "si" in confirmacion or "sí" in confirmacion:
                speak("Modo hackeo Activado")
                print("Modo hackeo Activado")

            elif "no" in confirmacion:
                speak("Activacion del modo hackeo cancelada")
                print("Activacion del modo hackeo cancelada")
                ModoHackeoActivado = False
            else:
                speak("No Entendi la confirmación, desactivando modo hackeo")
                print("No Entendi la confirmación, desactivando modo hackeo")
                ModoHackeoActivado = False

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



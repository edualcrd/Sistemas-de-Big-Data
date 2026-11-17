import os
import re
import json
from dotenv import load_dotenv
from atproto import Client
from anthropic import Anthropic
from pymongo import MongoClient
from bson import json_util
#Cargamos las variables de entorno desde el .env
load_dotenv()
BSKY_IDENTIFIER = os.getenv('BSKY_IDENTIFIER')
BSKY_PASSWORD = os.getenv('BSKY_PASSWORD')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')


#Esta función la he creado para que elimine automáticamente llos enlaces y espacios extras para que el LLM reciba el texto más limpio.
def limpiar_texto(texto):
    texto = re.sub(r'http\S+', '', texto)
    return texto.strip()



def main():
    #Comprobación de seguridad básica
    if not all([BSKY_IDENTIFIER, BSKY_PASSWORD, ANTHROPIC_API_KEY]):
        print("ERROR: Pueden faltar algunas credenciales en el archivo .env")
        return

    #Conexión a Bluesky y extracción
    print("Conectando a Bluesky")
    bsky_client = Client()
    bsky_client.login(BSKY_IDENTIFIER, BSKY_PASSWORD)#Identificador y contraseña de la app
    
    actor_a_analizar = 'midu.dev' #En este caso analizamos a Midudev
    feed_data = bsky_client.get_author_feed(actor_a_analizar, limit=20) #Con el limit 20 cogemos los últimos 20 posts.
    
    textos_feed = []
    #Iteramos para extraer solo el texto de cada post
    for item in feed_data.feed:
        if hasattr(item.post.record, 'text'):
            texto_limpio = limpiar_texto(item.post.record.text)
            if texto_limpio:
                textos_feed.append(texto_limpio)
                
    #Guardado en MongoDB
    print("Guardando el feed en MongoDB")
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client['bluesky_analysis']
    coleccion = db['feeds']
    #JSON  a insertar (sin análisis)
    documento = {
        "actor": actor_a_analizar,
        "feed_textos": textos_feed,
        "analisis_llm": ""
    }
    doc_id = coleccion.insert_one(documento).inserted_id

    #Análisis con Claude
    print("Enviándole el prompt a Claude")
    claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    contexto = f"Actúa como el mejor analista de redes sociales. Analiza estos recientes posts del usuario '{actor_a_analizar}' en Bluesky.\n\n"
    feed_str = "\n".join([f"- {t}" for t in textos_feed])
    instrucciones = "\n\nAnaliza el tono, los temas principales y elabora un breve perfil de intereses en formato Markdown."
    
    prompt = contexto + "POSTS:\n" + feed_str + instrucciones
    
    response = claude_client.messages.create(
        model="claude-haiku-4-5-20251001", # Haiku es muy rápido y consume poquísimo saldo
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    respuesta_llm = response.content[0].text
    
    #Actualización en MongoDB y volcado a archivos
    coleccion.update_one({"_id": doc_id}, {"$set": {"analisis_llm": respuesta_llm}})
    

    #Respuesta del LLM en un txt
    nombre_txt = os.path.basename(__file__).replace(".py", ".txt")
    with open(nombre_txt, "w", encoding="utf-8") as f:
        f.write(respuesta_llm)
        
    
    
    documento_actualizado = coleccion.find_one({"_id": doc_id})
        
    nombre_json = os.path.basename(__file__).replace(".py", ".json")
    with open(nombre_json, "w", encoding="utf-8") as f:
        json.dump(json.loads(json_util.dumps(documento_actualizado)), f, ensure_ascii=False, indent=4) #json_util de bson permite serializar bien el ObjectId de Mongo
        
    print(f"El proceso ha sido completado. Archivos generados: {nombre_txt} y {nombre_json}")

if __name__ == "__main__":
    main()
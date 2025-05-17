import os
from huggingface_hub import InferenceClient
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.core.files.base import ContentFile
import base64
from io import BytesIO
from PIL import Image
import logging
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

API_URL = "https://router.huggingface.co/cerebras/v1/chat/completions"

def get_hf_headers():
    return {
        "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY', '')}",
    }

def test_hf_chat_api(payload):
    response = requests.post(API_URL, headers=get_hf_headers(), json=payload)
    return response.json()

class AIGameGenerator:
    def __init__(self):
        logger.info("Initialisation de AIGameGenerator")
        try:
            self.use_openai = False
            openai_api_key = os.environ.get('OPENAI_API_KEY')
            if openai_api_key:
                self.openai_client = OpenAI(api_key=openai_api_key)
                self.use_openai = True
                logger.info("Client OpenAI initialisé avec succès")
            else:
                hf_api_key = os.environ.get('HUGGINGFACE_API_KEY')
                if not hf_api_key:
                    raise ValueError("Aucune clé API trouvée pour OpenAI ou Hugging Face")
                # Utilisation d'un modèle très petit : gpt2 (fallback)
                self.client = InferenceClient(
                    model="gpt2",
                    token=hf_api_key,
                    timeout=120,
                    provider="hf-inference"
                )
                logger.info("Client GPT-2 initialisé avec succès (fallback)")
            # Configuration du client Stable Diffusion
            self.stable_diffusion = InferenceClient(
                model="stabilityai/stable-diffusion-xl-base-1.0",
                token=os.environ.get('HUGGINGFACE_API_KEY', ''),
                timeout=120,
                provider="hf-inference"
            )
            logger.info("Client Stable Diffusion initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation des clients: {str(e)}")
            if "API key" in str(e).lower():
                raise ValueError("Erreur d'authentification avec l'API. Veuillez vérifier vos clés API.")
            elif "timeout" in str(e).lower():
                raise TimeoutError("Le temps de connexion à l'API a dépassé la limite.")
            else:
                raise

    def _check_rate_limit(self, user):
        """Vérifie si l'utilisateur a dépassé sa limite d'utilisation"""
        logger.debug(f"Vérification de la limite d'utilisation pour l'utilisateur {user.id}")
        cache_key = f"ai_usage_{user.id}"
        usage = cache.get(cache_key, 0)
        
        if usage >= settings.MAX_AI_REQUESTS_PER_DAY:
            logger.warning(f"Limite d'utilisation atteinte pour l'utilisateur {user.id}")
            return False
        
        cache.set(cache_key, usage + 1, 86400)
        logger.debug(f"Utilisation mise à jour pour l'utilisateur {user.id}: {usage + 1}")
        return True

    def _generate_with_prompt(self, prompt):
        """Génère du texte avec OpenAI ou Hugging Face"""
        logger.info("Début de la génération de texte")
        try:
            if self.use_openai:
                logger.info("Génération via OpenAI API (nouvelle syntaxe)")
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un concepteur de jeux vidéo créatif et tu réponds toujours en français."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=0.8,
                    top_p=0.95
                )
                result = response.choices[0].message.content
                logger.debug(f"Réponse OpenAI: {result[:100]}...")
                return result
            else:
                logger.info("Génération via Hugging Face API (fallback)")
                formatted_prompt = f"<s>[INST] {prompt} [/INST]"
                response = self.client.text_generation(
                    formatted_prompt,
                    max_new_tokens=800,
                    temperature=0.8,
                    top_p=0.95,
                    repetition_penalty=1.1,
                    do_sample=True
                )
                if not response or len(response.strip()) < 100:
                    raise ValueError("La réponse du modèle est trop courte ou vide")
                response = response.strip()
                response = response.replace('[INST]', '').replace('[/INST]', '')
                response = response.replace('<s>', '').replace('</s>', '')
                logger.debug(f"Réponse HF: {response[:100]}...")
                return response
        except Exception as e:
            logger.error(f"Erreur lors de la génération de texte: {str(e)}")
            if "rate limit" in str(e).lower():
                raise ValueError("Limite de requêtes API atteinte. Veuillez réessayer plus tard.")
            elif "timeout" in str(e).lower():
                raise TimeoutError("Le temps de génération a dépassé la limite.")
            else:
                raise ValueError(f"Erreur lors de la génération du texte: {str(e)}")

    def _generate_image(self, prompt):
        """Génère une image avec Stable Diffusion et la convertit en fichier"""
        logger.info("Début de la génération d'image")
        try:
            if not prompt or len(prompt.strip()) < 10:
                raise ValueError("Le prompt pour l'image est trop court ou vide")
                
            enhanced_prompt = f"high quality, detailed, professional concept art, {prompt}"
            negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, text, watermark"
            
            logger.debug(f"Prompt image: {enhanced_prompt}")
            logger.info("Appel de l'API Stable Diffusion")
            
            image_bytes = self.stable_diffusion.text_to_image(
                enhanced_prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=30,
                guidance_scale=7.5
            )
            
            if not image_bytes:
                raise ValueError("Aucune image n'a été générée")
                
            logger.info("Image générée avec succès")
            
            logger.debug("Conversion de l'image en fichier")
            image = Image.open(BytesIO(image_bytes))
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            logger.info("Image convertie en fichier avec succès")
            
            return ContentFile(buffer.getvalue(), name=f'generated_{timezone.now().timestamp()}.png')
        except Exception as e:
            logger.error(f"Erreur lors de la génération d'image: {str(e)}")
            if "rate limit" in str(e).lower():
                raise ValueError("Limite de requêtes API atteinte pour la génération d'images.")
            elif "timeout" in str(e).lower():
                raise TimeoutError("Le temps de génération d'image a dépassé la limite.")
            else:
                raise ValueError(f"Erreur lors de la génération d'image: {str(e)}")

    def generate_game_content(self, title, genre, ambiance, keywords=None, references=None):
        """Génère le contenu complet d'un jeu (texte uniquement, sans images)"""
        logger.info(f"Début de la génération du jeu: {title}")
        try:
            prompt = f"""En tant que concepteur de jeux vidéo expérimenté, crée un concept de jeu vidéo original et détaillé avec les caractéristiques suivantes :

Titre : {title}
Genre : {genre}
Ambiance : {ambiance}
Mots-clés : {keywords if keywords else 'Non spécifiés'}
Références : {references if references else 'Non spécifiées'}

Génère une structure complète et détaillée en suivant ce format exact :

DESCRIPTION:
[Une description concise et accrocheuse du jeu, mettant en avant son concept unique]

GAMEPLAY:
[Les mécaniques de jeu principales, les systèmes de gameplay et les interactions clés]

STORY:
[Une histoire en 3 actes avec un retournement narratif, incluant les moments clés]

CHARACTERS:
[2-4 personnages principaux avec leurs rôles, motivations, capacités et arcs narratifs]

ENVIRONMENT:
[Les lieux emblématiques, l'ambiance générale et l'atmosphère du monde du jeu]

IMAGE_PROMPTS:
[Un prompt détaillé pour générer une image de personnage principal]
[Un prompt détaillé pour générer une image d'environnement emblématique]"""

            logger.info("Génération du contenu avec OpenAI/HF")
            content = self._generate_with_prompt(prompt)
            logger.info("Contenu généré avec succès")
            
            # Parsing robuste des sections
            import re
            sections = {
                'description': '',
                'gameplay': '',
                'story': '',
                'characters': '',
                'environment': ''
            }
            current = None
            buffer = []
            # On découpe ligne par ligne pour plus de robustesse
            for line in content.splitlines():
                line = line.strip()
                if re.match(r'^DESCRIPTION[:：]', line, re.IGNORECASE):
                    if current and buffer:
                        sections[current] = '\n'.join(buffer).strip()
                    current = 'description'
                    buffer = []
                elif re.match(r'^GAMEPLAY[:：]', line, re.IGNORECASE):
                    if current and buffer:
                        sections[current] = '\n'.join(buffer).strip()
                    current = 'gameplay'
                    buffer = []
                elif re.match(r'^STORY[:：]', line, re.IGNORECASE):
                    if current and buffer:
                        sections[current] = '\n'.join(buffer).strip()
                    current = 'story'
                    buffer = []
                elif re.match(r'^CHARACTERS[:：]', line, re.IGNORECASE):
                    if current and buffer:
                        sections[current] = '\n'.join(buffer).strip()
                    current = 'characters'
                    buffer = []
                elif re.match(r'^ENVIRONMENT[:：]', line, re.IGNORECASE):
                    if current and buffer:
                        sections[current] = '\n'.join(buffer).strip()
                    current = 'environment'
                    buffer = []
                elif re.match(r'^IMAGE_PROMPTS[:：]', line, re.IGNORECASE):
                    if current and buffer:
                        sections[current] = '\n'.join(buffer).strip()
                    current = None
                    buffer = []
                elif current:
                    buffer.append(line)
            if current and buffer:
                sections[current] = '\n'.join(buffer).strip()
            logger.debug(f"Sections extraites : {sections}")
            result = {k: v for k, v in sections.items()}
            logger.info("Génération du jeu terminée avec succès (texte uniquement)")
            return result
        except Exception as e:
            logger.error(f"Erreur lors de la génération du contenu du jeu: {str(e)}")
            raise

    def generate_random_game(self):
        """Génère un jeu complètement aléatoire"""
        logger.info("Début de la génération aléatoire")
        try:
            genres = ['RPG', 'FPS', 'Metroidvania', 'Visual Novel', 'Action-RPG', 'Stratégie']
            ambiances = ['Post-apo', 'Onirique', 'Cyberpunk', 'Dark Fantasy', 'Steampunk', 'Médiéval']
            
            import random
            genre = random.choice(genres)
            ambiance = random.choice(ambiances)
            title = f"Projet {random.randint(1000, 9999)}"
            
            logger.info(f"Paramètres aléatoires générés: {title} ({genre}, {ambiance})")
            return self.generate_game_content(title, genre, ambiance)
        except Exception as e:
            logger.error(f"Erreur lors de la génération aléatoire: {str(e)}")
            raise

    # Si besoin d'OpenAI :
    def get_openai_api_key(self):
        return os.environ.get('OPENAI_API_KEY') 
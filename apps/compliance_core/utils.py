import google.generativeai as genai
from PIL import Image
import io

class ComplianceChecker:
    """
    Utility class to check compliance for campaigns.
    """
    def __init__(self, api_key):
        # Initialize the ComplianceChecker with the provided API key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash') # Model for text and images
    
    def verify_campaign(self, data):
        """
        Verifies the compliance of a campaign based on the provided data.
        """
        # Extract image metadata
        image_data = data.get('image')
        if not image_data:
            return {'status': 'Error', 'reason': 'No se proporcionó ninguna imagen.'}
        
        image_metadata = {
            'filename': image_data.name,
            'content_type': image_data.content_type,
            'size_bytes': image_data.size,
        }

        # Call the Gemini API to check compliance
        try:
            # Read bytes from the image file
            image_bytes = image_data.read()

            # Open the image using PIL from bytes
            image = Image.open(io.BytesIO(image_bytes))

            contents = [
                # "¿Esta imagen cumple con las políticas de compliance para publicidad? Responde estrictamente con 'Sí' o 'No', seguido de una breve justificación si la respuesta es 'No'.",
                "¿Esta imagen cumple con las políticas de compliance para publicidad? Sí o no.",
                image,
            ]

            response = self.model.generate_content(contents, stream=False)
            print(response.text)
            
            # Check response errors
            print('response.prompt_feedback: ', response.prompt_feedback)
            print('response.prompt_feedback.block_reason: ', response.prompt_feedback.block_reason)
            print('response.candidates: ', response.candidates)
            print('response.candidates[0].finish_reason: ', response.candidates[0].finish_reason)
            print('response.text: ', response.text)
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return {'status': 'Error', 'reason': 'La solicitud fue bloqueada por la API de Gemini: {r}'.format(r=response.prompt_feedback.block_reason)}
            # elif response.candidates and response.candidates[0].finish_reason != 'STOP':
            #     return {'status': 'Error', 'reason': 'La generación de contenido no finalizó correctamente: {r}'.format(r=response.candidates[0].finish_reason)}
            elif not response.text:
                return {'status': 'Error', 'reason': 'La API de Gemini no devolvió ninguna respuesta de texto.'}

            gemini_reply = response.text.strip()

            return_dict = {
                'image_metadata': image_metadata,
                'response': gemini_reply,
            }

            if 'Sí' in gemini_reply:
                return_dict['status'] = 'Aprobado'
                return_dict['reason'] = 'Cumple con los requisitos según Gemini.'
            else:
                return_dict['status'] = 'Rechazado'
                return_dict['reason'] = 'No cumple con los requisitos según Gemini.'
            return return_dict

        except Exception as e:
            return {'status': 'Error', 'reason': 'Error al comunicarse con la API de Gemini: {e}'.format(e=e)}

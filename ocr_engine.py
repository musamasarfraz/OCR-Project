import requests

def extract_text_from_image(image_bytes: bytes) -> str:
    # Get a free API key from https://ocr.space/ocrapi
    api_key = "You API Key Here"
    
    payload = {
        'apikey': api_key,
        'language': 'eng',  # It also has auto-detection features
        'isOverlayRequired': False,
    }
    
    # Send the image to the cloud instead of processing it locally
    files = {'file': ('image.jpg', image_bytes)}
    # response = requests.post('https://api.ocr.space/parse/image', files=files, data=payload)
    
    # To this (adding verify=False):
    response = requests.post(
        'https://api.ocr.space/parse/image', 
        files=files, 
        data=payload, 
        verify=False
    )
    
    result = response.json()
    if result.get("OCRExitCode") == 1:
        # Extract text from all regions
        parsed_results = result.get("ParsedResults", [])
        return "\n".join([text.get("ParsedText") for text in parsed_results])
    
    return "Error: Could not extract text."
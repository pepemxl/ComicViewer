import zipfile
import os
from PIL import Image
from io import BytesIO
from typing import Optional


COMICS_DIR = os.path.join(os.path.dirname(__file__), "../../comics")
os.makedirs(COMICS_DIR, exist_ok=True)
SUPPORTED_ZIP_FORMATS=set({'cbr', 'cbz', 'pdf', 'zip', 'rar'})

def save_comic_file(file_content: bytes, filename: str) -> str:
    filepath = os.path.join(COMICS_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file_content)
    return filepath

def extract_pages_list(filepath: str):
    with zipfile.ZipFile(filepath) as z:
        files = [f for f in z.namelist() if not f.startswith("__MACOSX") and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        files.sort()  # orden natural
        return files

#def get_page_image(filepath: str, page_name: str) -> BytesIO:
#    with zipfile.ZipFile(filepath) as z:
#        with z.open(page_name) as img_file:
#            return BytesIO(img_file.read())

def get_page_image(filepath: str, page_name: str) -> Optional[BytesIO]:
    """
    Extrae una imagen específica de un archivo ZIP.
    
    Args:
        filepath: Ruta al archivo ZIP
        page_name: Nombre del archivo dentro del ZIP
        
    Returns:
        BytesIO con los datos de la imagen o None si hay error
    """
    # Verificar que el archivo existe
    if not os.path.exists(filepath):
        print(f"Error: El archivo no existe: {filepath}")
        return None
    
    # Verificar que no esté vacío
    if os.path.getsize(filepath) == 0:
        print(f"Error: El archivo está vacío: {filepath}")
        return None
    
    # Verificar firma ZIP
    def check_zip_signature(file_path):
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                return header.startswith(b'PK\x03\x04') or header.startswith(b'PK\x05\x06') or header.startswith(b'PK\x07\x08')
        except Exception:
            return False
    
    if not check_zip_signature(filepath):
        print(f"Error: El archivo no es un ZIP válido: {filepath}")
        return None
    
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            # Verificar que el archivo existe dentro del ZIP
            if page_name not in z.namelist():
                print(f"Error: El archivo '{page_name}' no existe en el ZIP")
                return None
            
            # Verificar integridad del archivo específico
            corrupt_file = z.testzip()
            if corrupt_file is not None:
                print(f"Advertencia: Archivo corrupto en ZIP: {corrupt_file}")
                # Continuar pero con precaución
            
            with z.open(page_name) as img_file:
                image_data = img_file.read()
                if not image_data:
                    print(f"Error: El archivo '{page_name}' está vacío")
                    return None
                
                return BytesIO(image_data)

    except zipfile.BadZipFile as e:
        print(f"Error: Archivo ZIP corrupto o inválido: {e}")
        return None
    except KeyError as e:
        print(f"Error: Archivo no encontrado en el ZIP: {e}")
        return None
    except PermissionError as e:
        print(f"Error de permisos: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar el archivo ZIP: {e}")
        return None

# Versión alternativa que lanza excepciones en lugar de retornar None
def get_page_image_with_raise(filepath: str, page_name: str) -> BytesIO:
    """
    Versión que lanza excepciones específicas en caso de error.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo no existe: {filepath}")
    
    if os.path.getsize(filepath) == 0:
        raise ValueError(f"El archivo está vacío: {filepath}")
    
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            if page_name not in z.namelist():
                raise KeyError(f"El archivo '{page_name}' no existe en el ZIP")
            
            with z.open(page_name) as img_file:
                image_data = img_file.read()
                if not image_data:
                    raise ValueError(f"El archivo '{page_name}' está vacío")
                
                return BytesIO(image_data)
                
    except zipfile.BadZipFile as e:
        raise zipfile.BadZipFile(f"Archivo ZIP corrupto: {filepath}") from e

# Función de utilidad para verificar el ZIP antes de usarlo
def validate_zip_file(filepath: str) -> bool:
    """
    Valida que un archivo sea un ZIP válido antes de procesarlo.
    """
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            return z.testzip() is None
    except (zipfile.BadZipFile, FileNotFoundError, IsADirectoryError):
        return False



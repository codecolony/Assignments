from PIL import Image
from pytesseract import image_to_string
print image_to_string(Image.open('out_hor_cleaned2.jpg'))
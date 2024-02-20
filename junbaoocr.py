import easyocr
IMAGE_PATH = 'captcha.jfif'
reader = easyocr.Reader(['en'])
result = reader.readtext(IMAGE_PATH,paragraph="False")
print(result[0][-1])
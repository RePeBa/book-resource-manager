import easyocr

reader = easyocr.Reader(['en']) # need to run only once to load model into memory

result = reader.readtext('Flask.jpg', detail =0)

print (result)

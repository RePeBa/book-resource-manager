import easyocr

reader = easyocr.Reader(['en']) # need to run only once to load model into memory

result = reader.readtext('NEW.jpg', detail =0)
# result2 = reader.readtext('Adaptywny_Kod.png', detail =0)


print (result)
# print (result2)
import easyocr

reader = easyocr.Reader(['en']) # need to run only once to load model into memory

result = reader.readtext('/static/NEW.jpg', detail =0)



print (result)
# print (result2)
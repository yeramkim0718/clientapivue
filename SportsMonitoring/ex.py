import re
 
text = "6.4(72)"
 
text = text.split("(")[1][:-1]
print(text)
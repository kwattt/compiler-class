import re

text = """
 #asd# 
 ?lol? 
"""

pattern = r'(?<![\w#?])[a-zA-Z0-9]+(?![\w#?])'

matches = re.findall(pattern, text)

print(matches)

from json import load
from re import DOTALL, compile, escape

with open("./Source/Utils/data.json", "r", encoding="utf-8") as datafile:
    data = load(datafile)
    
def Replacer(string, replacers):
    str = compile("|".join([escape(i) for i in sorted(replacers, key=len, reverse=True)]), flags=DOTALL).sub(lambda x: replacers[x.group(0)], string)
    return str
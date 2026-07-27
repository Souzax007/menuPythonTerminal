import webbrowser
from urllib.parse import quote

def buscar_google():
    termo = input("Digite o termo de busca: ")
    termoInputFormatado = quote(termo)
    url = f"https://www.google.com/search?q={termoInputFormatado}" 
    webbrowser.open(url)
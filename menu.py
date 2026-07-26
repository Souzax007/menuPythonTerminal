import webbrowser
from urllib.parse import quote

def menu():
    menu = """
    =============
    *** menu ***
    =============
    1 - buscar no google
    2 - buscar no youtube
    3 - buscar no github
    4 - buscar no twitter
    5 - buscar no facebook
    6 - buscar no instagram
    0 - sair
    """
    print(menu)
    opcao = input("Digite uma opção: ")

    print(f"Você digitou: {opcao}")

    if opcao == "1":
        buscar_google()
    elif opcao == "2":
        buscar_youtube()
    elif opcao == "3":
        buscar_github()
    elif opcao == "0":
        return opcao

def buscar_google():
    termo = input("Digite o termo de busca: ")
    
    termoInputFormatado = quote(termo)

    url = f"https://www.google.com/search?q={termoInputFormatado}" 

    webbrowser.open(url)

def buscar_youtube():
    termo = input("Digite o termo de busca: ")
    print(f"https://www.youtube.com/results?search_query={termo}")

def buscar_github():
    termo = input("Digite o termo de busca: ")
    print(f"https://github.com/search?q={termo}")

def continuar():
    resposta = input("Deseja continuar? (yes/no):")
    if resposta == "yes":
        print("Continuando...") 
        main()
    else:
        print("Encerrando o programa...")

def main():
    escolha = menu()
    if escolha == "0":
        print("Encerrando o programa...")
    else:
        continuar()

main()
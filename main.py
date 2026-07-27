from modulos.buscar_google import buscar_google
from modulos.buscar_google_dorks import buscar_google_dorks

def menu():
    menu = """
    =============
    *** menu ***
    =============
    1 - buscar no google
    2 - busca avançada
    0 - sair
    """
    print(menu)
    opcao = input("Digite uma opção: ")

    print(f"Você digitou: {opcao}")

    if opcao == "1":
        buscar_google()
    elif opcao == "2":
        return buscar_google_dorks()
    elif opcao == "0":
        return opcao

def continuar():
    resposta = input("Deseja continuar? (yes/no):")
    if resposta == "yes":
        return True
    return False

def main():
    while True:
        escolha = menu()

        if escolha == "0":
            print("Encerrando o programa...")
            break

        # A opção 11 do submenu retorna este sinal e pula a pergunta "continuar".
        if escolha == "menu":
            continue

        if not continuar():
            print("Encerrando o programa...")
            break

if __name__ == "__main__":
    main()

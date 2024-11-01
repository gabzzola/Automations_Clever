def get_user_action():
    message = """
    Digite o número da vertical para indicar qual ação o bot deve realizar:
    1 - Cadastro de produtos com dados para comanda
    2 - Cadastro de produtos sem dados para comanda
    3 - Cadastro de produtos com dados para comanda, mas Grupo Delivery, Grupo de Itens e Insumos já estão cadastrados
    4 - Cadastro de bairros
    """
    print(message)

    while True:
        user_action = input("Informe o número da ação desejada: ")

        if user_action in ['1', '2', '3', '4']:
            return user_action
        else:
            print("Opção inválida, informe um número de 1 a 4.")
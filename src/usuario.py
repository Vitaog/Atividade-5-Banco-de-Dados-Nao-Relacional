import uuid
from datetime import datetime

def criar_usuario(connection):
    try:
        connection.connect()

        nome_usuario = input("Digite o nome do usuário: ")
        cpf = input("Digite o CPF do usuário: ")
        rua = input("Digite a rua do usuário: ")
        num = input("Digite o número do usuário: ")
        bairro = input("Digite o bairro do usuário: ")
        cidade = input("Digite a cidade do usuário: ")
        estado = input("Digite o estado do usuário: ")
        cep = input("Digite o CEP do usuário: ")

        usuario_id = str(uuid.uuid4())

        data_cadastro = datetime.now().strftime("%Y-%m-%d")

        query = (
            f"CREATE (:Usuario {{id: '{usuario_id}', nome_usuario: '{nome_usuario}', cpf: '{cpf}', "
            f"rua: '{rua}', num: '{num}', bairro: '{bairro}', cidade: '{cidade}', estado: '{estado}', cep: '{cep}', "
            f"data_cadastro: '{data_cadastro}'}})"
        )

        connection.query(query)

        print("Usuário criado com sucesso!")
    finally:
        connection.close()

def listar_usuarios(connection):
    try:
        connection.connect()

        query_listar_usuarios = (
            "MATCH (u:Usuario) RETURN u.id AS id, u.nome_usuario AS nome, u.cpf AS cpf, "
            "u.rua AS rua, u.num AS num, u.bairro AS bairro, u.cidade AS cidade, u.estado AS estado, u.cep AS cep"
        )

        usuarios = connection.query(query_listar_usuarios)

        print("Lista de Usuários:")
        for i, usuario in enumerate(usuarios, start=1):
            print(f"{i}. Nome: {usuario['nome']}")

        try:
            index_usuario = int(input("Digite o número do usuário desejado (0 para sair): "))
            if index_usuario == 0:
                return
            usuario_selecionado = usuarios[index_usuario - 1]

            print("\nDetalhes do Usuário:")
            print(f"ID: {usuario_selecionado['id']}")
            print(f"Nome: {usuario_selecionado['nome']}")
            print(f"CPF: {usuario_selecionado['cpf']}")
            print("Endereço:")
            print(f"Rua: {usuario_selecionado['rua']}")
            print(f"Número: {usuario_selecionado['num']}")
            print(f"Bairro: {usuario_selecionado['bairro']}")
            print(f"Cidade: {usuario_selecionado['cidade']}")
            print(f"Estado: {usuario_selecionado['estado']}")
            print(f"CEP: {usuario_selecionado['cep']}")

        except (ValueError, IndexError):
            print("Seleção inválida.")
    finally:
        connection.close()

def adicionar_compra(connection):
    try:
        connection.connect()

        query_usuarios = "MATCH (u:Usuario) RETURN u.id AS id, u.nome_usuario AS nome_usuario"
        usuarios = connection.query(query_usuarios)

        print("\nLista de Usuários:")
        for i, usuario in enumerate(usuarios, start=1):
            print(f"{i}. Nome: {usuario['nome_usuario']}")

        try:
            index_usuario = int(input("Digite o número do usuário desejado: "))
            usuario_selecionado = usuarios[index_usuario - 1]

            query_produtos = "MATCH (p:Produto) RETURN p.id AS id, p.nomeProduto AS nome_produto, p.descricao AS descricao, p.preco AS preco"
            produtos = connection.query(query_produtos)

            print("\nLista de Produtos:")
            for i, produto in enumerate(produtos, start=1):
                print(f"{i}. Nome: {produto['nome_produto']} - Descrição: {produto['descricao']} - Preço: {produto['preco']}")

            try:
                index_produto = int(input("Digite o número do produto desejado: "))
                produto_selecionado = produtos[index_produto - 1]

                query_vendedores_produto = (
                    f"MATCH (v:Vendedor)-[:Vende]->(p:Produto {{id: '{produto_selecionado['id']}'}}) "
                    "RETURN v.id AS id, v.nomeVendedor AS nome, p.preco AS preco"
                )
                vendedores_produto = connection.query(query_vendedores_produto)

                if not vendedores_produto:
                    print("Nenhum vendedor encontrado para o produto selecionado.")
                    return

                print("\nLista de Vendedores do Produto:")
                for i, vendedor in enumerate(vendedores_produto, start=1):
                    print(f"{i}. Nome: {vendedor['nome']} - Preço: {vendedor['preco']}")

                try:
                    index_vendedor = int(input("Digite o número do vendedor desejado: "))
                    vendedor_selecionado = vendedores_produto[index_vendedor - 1]

                    quantidade = int(input("Digite a quantidade desejada: "))

                    valor_total = quantidade * float(vendedor_selecionado['preco'])

                    query_compra = (
                        f"CREATE (c:Compra {{data_compra: '{datetime.now().strftime('%Y-%m-%d')}', quantidade:'{quantidade}', preco_produto: '{vendedor_selecionado['preco']}', nome_produto: '{produto_selecionado['nome_produto']}',  nome_vendedor: '{vendedor_selecionado['nome']}', "
                        f"valor_total: {valor_total}}})"
                    )
                    connection.query(query_compra)

                    query_relacao_usuario_compra = (
                        f"MATCH (u:Usuario), (c:Compra) "
                        f"WHERE u.id = '{usuario_selecionado['id']}' AND c.data_compra = '{datetime.now().strftime('%Y-%m-%d')}' "
                        "CREATE (u)-[:REALIZOU]->(c)"
                    )
                    connection.query(query_relacao_usuario_compra)

                    query_relacao_produto_compra = (
                        f"MATCH (p:Produto), (c:Compra) "
                        f"WHERE p.id = '{produto_selecionado['id']}' AND c.data_compra = '{datetime.now().strftime('%Y-%m-%d')}' "
                        "CREATE (p)-[:FOI_COMPRADO]->(c)"
                    )
                    connection.query(query_relacao_produto_compra)

                    query_relacao_vendedor_compra = (
                        f"MATCH (v:Vendedor), (c:Compra) "
                        f"WHERE v.id = '{vendedor_selecionado['id']}' AND c.data_compra = '{datetime.now().strftime('%Y-%m-%d')}' "
                        "CREATE (v)-[:REALIZOU_VENDA]->(c)"
                    )
                    connection.query(query_relacao_vendedor_compra)

                    print("Compra realizada com sucesso!")
                except (ValueError, IndexError):
                    print("Seleção inválida.")
            except (ValueError, IndexError):
                print("Seleção inválida.")
        except (ValueError, IndexError):
            print("Seleção inválida.")
    finally:
        connection.close()

def listar_compras(connection):
    try:
        connection.connect()

        query_listar_usuarios = (
            "MATCH (u:Usuario) RETURN u.id AS id, u.nome_usuario AS nome, u.cpf AS cpf, "
            "u.rua AS rua, u.num AS num, u.bairro AS bairro, u.cidade AS cidade, u.estado AS estado, u.cep AS cep"
        )

        usuarios = connection.query(query_listar_usuarios)

        print("Lista de Usuários:")
        for i, usuario in enumerate(usuarios, start=1):
            print(f"{i}. Nome: {usuario['nome']}")

        try:
            index_usuario = int(input("Digite o número do usuário desejado (0 para sair): "))
            if index_usuario == 0:
                return
            usuario_selecionado = usuarios[index_usuario - 1]

            # Exibir detalhes do Usuário
            print("\nDetalhes do Usuário:")
            print(f"ID: {usuario_selecionado['id']}")
            print(f"Nome: {usuario_selecionado['nome']}")
            print(f"CPF: {usuario_selecionado['cpf']}")

            # Listar Compras do Usuário
            query_compras_usuario = (
                f"MATCH (u:Usuario)-[:REALIZOU]->(c:Compra) "
                f"WHERE u.id = '{usuario_selecionado['id']}' "
                "RETURN c.data_compra AS data_compra, c.valor_total AS valor_total, c.preco_produto AS preco_produto, c.nome_produto AS nome_produto, c.nome_vendedor AS nome_vendedor, c.quantidade AS quantidade"
            )
            compras_usuario = connection.query(query_compras_usuario)

            if compras_usuario:
                print("\nCompras Realizadas:")
                for i, compra in enumerate(compras_usuario, start=1):
                    print(f"{i}. Nome do Produto: {compra['nome_produto']} \nValor Total: {compra['valor_total']} \nNome Vendedor: {compra['nome_vendedor']} \nPreço Produto: {compra['preco_produto']} \nQuantidade: {compra['quantidade']}")
            else:
                print("\nO usuário ainda não realizou nenhuma compra.")

        except (ValueError, IndexError):
            print("Seleção inválida.")
    finally:
        connection.close()

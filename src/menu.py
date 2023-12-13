from database_connect import Neo4jConnection
from produto import criar_produto, listar_produtos
from usuario import adicionar_compra, criar_usuario, listar_usuarios
from vendedor import adicionar_produto, criar_vendedor, listar_vendedores

neo4j_uri = "neo4j+s://8e60f93c.databases.neo4j.io"
neo4j_user = "neo4j"
neo4j_password = "a_ebP3yV2-8HgkHQtKcvUdh23LPNt26U-nDpbrPuDjg"

# Crie uma instância da classe Neo4jConnection
neo4j_connection = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)

key = 0
sub = 0

while (key != 'S' and key != 's'):
    print("|---------------------Bem Vindo---------------------------------|")
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("|---------------------------------------------------------------|")
    key = input("Digite a opção desejada? (S para sair) ")
    print ("")

    if (key == '1'):
        print("|-------------------Menu do Usuário-----------------------------|")
        print("1-Create Usuário")
        print("2-Read Usuário")
        print("|--------------------Funcionalidades----------------------------|")
        print("3-Adicionar Compra")
        print("4-Listar Compras")
        print("|---------------------------------------------------------------|")
        sub = input("Digite a opção desejada? (V para voltar) ")
        print ("")

        if (sub == '1'):
            print("|-------------------Criação de Usuário------------------------|")
            criar_usuario(neo4j_connection)
            print ("")
            
        elif (sub == '2'):
            print("|----------------Listagem de Usuário-------------------------|")
            listar_usuarios(neo4j_connection)
            print ("")
        
        elif (sub == '3'):
            print("|--------------------------------------------------------------|")
            adicionar_compra(neo4j_connection)
            print ("")

        elif (sub == '4'):
            print("|--------------------------------------------------------------|")
#            listar_compras_usuario(neo4j_connection)
            print ("")
        
            
    elif (key == '2'):
         print("|-------------------Menu do Vendedor----------------------------|")
         print("1-Create Vendedor")
         print("2-Read Vendedor")
         print("|--------------------Funcionalidades----------------------------|")
         print("3-Adicionar Produto")
         print("|---------------------------------------------------------------|")
         sub = input("Digite a opção desejada? (V para voltar) ")
         print ("") 

         if (sub == '1'):
             print("|-------------------Criação de Vendedor------------------------|")
             criar_vendedor(neo4j_connection)
             print ("")
        
         elif (sub == '2'):
             print("|----------------Listagem de Vendedor-------------------------|")
             listar_vendedores(neo4j_connection)
             print ("")

         elif (sub == '3'):
             print("|--------------------------------------------------------------|")
             adicionar_produto(neo4j_connection)
             print ("")   


    elif (key == '3'):
        print("|----------------------Menu de Produtos-------------------------|")
        print("1-Create Produto")
        print("2-Read Produto")
        print("|---------------------------------------------------------------|")
        sub = input("Digite a opção desejada? (V para voltar) ")
        print ("")      

        if (sub == '1'):
            print("|-------------------Criação de Produto-------------------------|")
            criar_produto(neo4j_connection)
            print ("")

        elif (sub == '2'):
            print("|----------------Listagem de Produto-------------------------|")
            listar_produtos(neo4j_connection)
            print ("")
        
neo4j_connection.close()
print("Vlw Flw...")
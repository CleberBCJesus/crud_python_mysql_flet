import flet as ft
import mysql.connector

# Função para conectar ao banco com tratamento de erro
def conectar_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="estoque"
        )
        return conn
    except mysql.connector.Error as err:
        print("Erro ao conectar:", err)
        return None

def main(page: ft.Page):
    page.title = "Cadastro de Produtos"
    page.scroll = ft.ScrollMode.ALWAYS

    # Campos do formulário
    nome = ft.TextField(label="Nome do Produto", width=300)
    quantidade = ft.TextField(label="Quantidade", width=150)
    preco_compra = ft.TextField(label="Preço de Compra", width=150)
    preco_venda = ft.TextField(label="Preço de Venda", width=150)
    cod_forn = ft.TextField(label="Código do Fornecedor", width=200)
    categoria = ft.TextField(label="Categoria", width=200)
    descricao = ft.TextField(label="Descrição", multiline=True, min_lines=2, max_lines=3, width=400)

    lista_produtos = ft.Column()  # Lista visível dos produtos
    produto_edicao = None         # Guarda o ID do produto que está sendo editado

    # Limpa os campos do formulário
    def limpar_campos():
        for campo in [nome, quantidade, preco_compra, preco_venda, cod_forn, categoria, descricao]:
            campo.value = ""
        nonlocal produto_edicao
        produto_edicao = None

        page.update() # atualiza a interface

    # Carrega todos os produtos do banco de dados
    def carregar_produtos():
        lista_produtos.controls.clear()
        conn = conectar_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, quantidade, preco_venda FROM produtos ORDER BY data_cadastro DESC")
                for id_, nome_, qtd, preco in cursor.fetchall():
                    linha = ft.Row([
                        ft.Text(f"{nome_} | {qtd} un | R$ {preco:.2f}", expand=True),
                        ft.TextButton( text="Editar", on_click=lambda e, pid=id_: carregar_para_edicao(pid)),
                        ft.TextButton(text="Excluir", on_click=lambda e, pid=id_: excluir_produto(pid))
                    ])
                    lista_produtos.controls.append(linha)
                cursor.close()
            except Exception as e:
                lista_produtos.controls.append(ft.Text(f"Erro: {e}", color="red"))
            finally:
                conn.close()
        page.update()

    # Insere ou atualiza produto no banco
    def salvar_produto(e):
        try:
            dados = (
                nome.value.strip(),
                int(quantidade.value),
                float(preco_compra.value),
                float(preco_venda.value),
                cod_forn.value.strip(),
                categoria.value.strip(),
                descricao.value.strip(),
            )
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Verifique os campos numéricos."))
            page.snack_bar.open = True
            page.update()
            return

        conn = conectar_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                if produto_edicao:  # Atualiza
                    cursor.execute("""
                        UPDATE produtos SET nome=%s, quantidade=%s, preco_compra=%s, preco_venda=%s,
                        codigo_fornecedor=%s, categoria=%s, descricao=%s WHERE id=%s
                    """, dados + (produto_edicao,))
                else:  # Insere novo
                    cursor.execute("""
                        INSERT INTO produtos (nome, quantidade, preco_compra, preco_venda, codigo_fornecedor, categoria, descricao)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, dados)
                conn.commit()
                cursor.close()
                limpar_campos()
                carregar_produtos()
            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao salvar: {e}"))
                page.snack_bar.open = True
            finally:
                conn.close()
        page.update()

    # Carrega os dados de um produto para edição
    def carregar_para_edicao(produto_id):
        conn = conectar_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT nome, quantidade, preco_compra, preco_venda, codigo_fornecedor, categoria, descricao FROM produtos WHERE id=%s", (produto_id,))
                dados = cursor.fetchone()
                if dados:
                    nome.value, quantidade.value, preco_compra.value, preco_venda.value, cod_forn.value, categoria.value, descricao.value = map(str, dados)
                    nonlocal produto_edicao
                    produto_edicao = produto_id
                cursor.close()
            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar produto: {e}"))
                page.snack_bar.open = True
            finally:
                conn.close()
        page.update()

    # Exclui produto do banco
    def excluir_produto(produto_id):
        conn = conectar_mysql()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM produtos WHERE id=%s", (produto_id,))
                conn.commit()
                cursor.close()
                carregar_produtos()
            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao excluir: {e}"))
                page.snack_bar.open = True
            finally:
                conn.close()
        page.update()

    # Layout da página
    page.add(
        ft.Text("Cadastro de Produto", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([nome, quantidade]),
        ft.Row([preco_compra, preco_venda]),
        ft.Row([cod_forn, categoria]),
        descricao,
        ft.Row([
            ft.ElevatedButton("Salvar", on_click=salvar_produto),
            ft.ElevatedButton("Limpar", on_click=lambda e: limpar_campos(), bgcolor="grey")
        ]),
        ft.Divider(),
        ft.Text("Produtos cadastrados:", size=20),
        lista_produtos
    )

    carregar_produtos()  # Inicializa com a lista

ft.app(target=main, view=ft.WEB_BROWSER)

from logging import root
from tkinter import *
import sqlite3

from tkinter import ttk


window = Tk()

class Validar_numeros:
    def validar_input(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100000000000

class Funcao():
    def limpar_dados(self):
        self.input_nome.delete(0, END)
        self.input_endereço.delete(0, END)
        self.input_contato.delete(0, END)
        self.input_material.delete(0, END)
    def limpar_dados2(self):

        self.input_nome_empresa.delete(0, END)
        self.input_endereço_2.delete(0, END)
        self.input_material_2.delete(0, END)

    def conecta_bd(self):
        self.conexao = sqlite3.connect("clientes.bd")
        self.cursor = self.conexao.cursor()

    def desconectar_bd(self):
        self.conexao.close()
        print("Desconectando Banco de dados criado")

    def Tabela_montada(self):
        self.conecta_bd()
        print("Conectando ao banco de dados")
        ############## Tabela ###################

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS nova_empresas (
                nome TEXT PRIMARY KEY,
                endereco TEXT NOT NULL,
                contato INTEGER,
                material TEXT NOT NULL
            );
        """)



        self.conexao.commit()

        print("Banco de dados criado")
        self.desconectar_bd()

    def variaveis(self):
        self.nome = self.input_nome.get()
        self.endereco = self.input_endereço.get()
        self.contato = self.input_contato.get()
        self.material = self.input_material.get()
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()



        self.cursor.execute("""INSERT INTO nova_empresas (nome, endereco, contato, material)
        VALUES (?, ?, ?,?)""", (self.nome, self.endereco, self.contato, self.material))
        self.conexao.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpar_dados()


    def select_lista(self):
        self.lista_empresa.delete(*self.lista_empresa.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT nome, endereco, contato, material FROM nova_empresas; """)
        for i in lista:
            self.lista_empresa.insert("", 'end', values=i)


        self.desconectar_bd()
        self.limpar_dados()

    def buscar(self):
        self.conecta_bd()
        self.lista_empresa.delete(*self.lista_empresa.get_children())

        self.input_nome_empresa.insert(END, '')
        nome = self.input_nome_empresa.get()
        self.cursor.execute("""
    SELECT nome, endereco, contato, material FROM nova_empresas
    WHERE nome LIKE ? ORDER BY nome ASC
""", ('%' + nome + '%',))
        buscarnome = self.cursor.fetchall()
        for i in buscarnome:
            self.lista_empresa.insert("", END, values=i)
            self.limpar_dados()
        self.desconectar_bd()

    def OnDoubleClick(self, event ):
        self.limpar_dados()
        self.lista_empresa.selection()

        for n in self.lista_empresa.selection():
            col1, col2, col3, col4 = self.lista_empresa.item(n, 'values')
            self.input_nome.insert(END, col1)
            self.input_endereço.insert(END, col2)
            self.input_contato.insert(END, col3)
            self.input_material.insert(END, col4)

    def deleta_cadastro(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM nova_empresas WHERE nome =? """, (self.nome,))
        self.conexao.commit()
        self.desconectar_bd()
        self.limpar_dados()
        self.select_lista()


class Application(Funcao,Validar_numeros):
    def __init__(self):

        self.window = window
        self.validar_entradas()
        self.tela()
        self.frames_tela()
        self.botoes()
        self.tabela_tela3()
        self.Tabela_montada()
        self.select_lista()

        window.mainloop()

    def tela(self):
        self.window.title("Apoio Descarte")
        self.window.configure(background='#71A6BD')
        self.window.geometry('900x620')
        self.window.resizable(False, False)


    def frames_tela(self):
        self.janela_1 = Frame(self.window, bd=4, bg='#C8E6F3', highlightbackground='#C7D9E0', highlightthickness=3)
        self.janela_1.place(relx=0.01, rely=0.01, relwidth=0.60, relheight=0.47)
        self.janela_2 = Frame(self.window, bd=4, bg='#C8E6F3', highlightbackground='#C8E6F3', highlightthickness=3)
        self.janela_2.place(relx=0.01, rely=0.5, relwidth=0.65, relheight=0.4)
        self.janela_3 = Frame(self.window, bd=4, bg='#C8E6F3', highlightbackground='#C7D9E0', highlightthickness=3)
        self.janela_3.place(relx=0.6, rely=0.01, relwidth=0.39, relheight=0.89, )

        self.abas = ttk.Notebook(self.janela_1)

        self.aba2 = Frame(self.abas)

        self.aba2.configure(background='#C8E6F3',highlightbackground='#C8E6F3', highlightthickness=0.1)
        self.label_info_detalhes = Label(self.aba2, text="A aplicação apresenta uma ideia\n de diminuir descartes irregulares,\nagrupando entidades autorizadas para\n essa ativade,\n possibilitando cadastro de volutários.",
                                         bg='#C8E6F3', font=("Arial", 8))
        self.label_info_detalhes.place(relx=0.05, rely=0.15)
        self.abas.add(self.aba2, text="Info")

        self.abas.place(relx=0.55, rely=0.25, relwidth=0.45, relheight=0.74)



    def botoes(self):
        # janela 1
        self.botao_apagar = Button(self.janela_1, text='Apagar', command=self.deleta_cadastro)
        self.botao_apagar.place(relx=0.03, rely=0.90, relwidth=0.1, relheight=0.10)
        self.botao_limpar_1 = Button(self.janela_1, text='Limpar', command=self.limpar_dados)
        self.botao_limpar_1.place(relx=0.15, rely=0.9, relwidth=0.1, relheight=0.10)
        self.botao_cadastrar = Button(self.janela_1, text='Cadastrar', command=self.add_cliente)
        self.botao_cadastrar.place(relx=0.27, rely=0.9, relwidth=0.1, relheight=0.10)
        self.botao_buscar = Button(self.janela_2, text='Buscar', command=self.buscar)
        self.botao_buscar.place(relx=0.03, rely=0.89, relwidth=0.1, relheight=0.12)
        #self.botao_limpar = Button(self.janela_2, text='Limpar')
        #self.botao_limpar.place(relx=0.15, rely=0.89, relwidth=0.1)
        # Label's
        self.label_texto = Label(self.janela_1, text='Nome da empresa (ou responsável)')
        self.label_texto.place(relx=0.02, rely=0.02)
        self.label_texto_2 = Label(self.janela_1, text='Endereço')
        self.label_texto_2.place(relx=0.02, rely=0.28)
        self.label_texto_3 = Label(self.janela_1, text='Contato')
        self.label_texto_3.place(relx=0.02, rely=0.55)
        self.label_texto_4 = Label(self.janela_1, text='Material para Coletar')
        self.label_texto_4.place(relx=0.60, rely=0.02)
        ########################### input's janela 1 #############################
        self.input_nome = Entry(self.janela_1)
        self.input_nome.place(relx=0.02, rely=0.15, relwidth=0.5)
        self.input_endereço = Entry(self.janela_1)
        self.input_endereço.place(relx=0.02, rely=0.42, relwidth=0.5)
        self.input_contato = Entry(self.janela_1, validate= "key", validatecommand= self.validacao)
        self.input_contato.place(relx=0.02, rely=0.69, relwidth=0.3)
        self.input_material = Entry(self.janela_1)
        self.input_material.place(relx=0.60, rely=0.15)
        ############################ janela 2 ######################################

        self.botao_limpar = Button(self.janela_2, text='Limpar', command=self.limpar_dados2)
        self.botao_limpar.place(relx=0.15, rely=0.89, relwidth=0.1, relheight=0.12)
        self.label_texto_empresa = Label(self.janela_2, text='Nome da empresa (ou responsável)')
        self.label_texto_empresa.place(relx=0.02, rely=0.02)
        self.label_texto_endereço = Label(self.janela_2, text='Endereço')
        self.label_texto_endereço.place(relx=0.02, rely=0.28)
        self.label_texto_material = Label(self.janela_2, text='Material para Coletar')
        self.label_texto_material.place(relx=0.02, rely=0.55)

        ############################ input janela 2 ##################################

        self.input_nome_empresa = Entry(self.janela_2)
        self.input_nome_empresa.place(relx=0.02, rely=0.15, relwidth=0.5)
        self.input_endereço_2 = Entry(self.janela_2)
        self.input_endereço_2.place(relx=0.02, rely=0.42, relwidth=0.5)
        self.input_material_2 = Entry(self.janela_2)
        self.input_material_2.place(relx=0.02, rely=0.69, relwidth=0.3)

    def tabela_tela3(self):
        self.lista_empresa = ttk.Treeview(self.janela_3, height=3, column=("col1", "col2", "col3", "col4"))
        self.lista_empresa.heading("#0", text="")
        self.lista_empresa.heading("#1", text="nome")
        self.lista_empresa.heading("#2", text="endereco")
        self.lista_empresa.heading("#3", text="telefone")
        self.lista_empresa.heading("#4", text="material")

        self.lista_empresa.column("#0", width=1)
        self.lista_empresa.column("#1", width=85)
        self.lista_empresa.column("#2", width=70)
        self.lista_empresa.column("#3", width=75)
        self.lista_empresa.column("#4", width=110)

        self.lista_empresa.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98, )

        self.rolagemlista = Scrollbar(self.janela_3, orient='vertical')
        self.lista_empresa.configure(yscroll=self.rolagemlista.set)
        self.rolagemlista.place(relx=0.95, rely=0.01, relwidth=0.05, relheight=0.98)
        self.lista_empresa.bind("<Double-1>", self.OnDoubleClick)

    def validar_entradas(self):
        self.validacao = (self.window.register(self.validar_input), "%P")



Application()



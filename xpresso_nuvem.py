
import mysql.connector
import customtkinter as ctk
from tkinter import *
from PIL import Image
from tkinter import messagebox

try:
    #Conexão com banco de dados MySQL em nuvem.
    conexao = mysql.connector.connect(
    host='**SEU HOST**',
    database='**BANCO DE DADOS**',
    user='**USUARIO**',
    password='**SENHA**'

    )

    cursor = conexao.cursor()

    print('conexão bem sucessida')

    janela = ctk.CTk()
except:
    msg = messagebox.showinfo(title='Erro', message='FALHA NA TENTATIVA DE CONEXÃO COM BANCO DE DADOS.')
    


#Definição da classe do aplicativo e inicializando o sistema.
class App():

    def __init__(self):
        self.janela=janela
        self.tema()
        self.tela()
        self.tela_login()
        

        
        janela.mainloop()


    #Definindo a aparencia da janela e sua configurações.
    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")


    def tela(self):
        janela.geometry('700x400')
        janela.resizable(False, False)
        janela.title('Xpresso')
        
    #Definições da tela de login da aplicação, botões, textos e imagens..
    def tela_login(self):

        font=ctk.CTkFont(family='Roboto', size=24)
        font=('Roboto', 24)


        logo = ctk.CTkImage(Image.open("xpresso.png"),size=(500,450))

        img1 = ctk.CTkLabel(janela, image=logo,text='')
        img1.place(x=-80,y=-20)


        frame_login = ctk.CTkFrame(master=janela,width=350, height=390)
        frame_login.pack(side=RIGHT)


        text_apre = ctk.CTkLabel(master=frame_login,text='Login Xpresso',font=('Roboto',24),text_color='#42f5a4').place(x=100, y=50)

        entry_usuario = ctk.CTkEntry(master=frame_login,placeholder_text="Usuario",width=300,height= 37,font=('Roboto', 14))
        entry_usuario.place(x=30,y=130)

        entry_senha = ctk.CTkEntry(master=frame_login,placeholder_text="Senha",width=300,height= 37, show='*',font=('Roboto', 14))
        entry_senha.place(x=30, y=180)

        
        #Definições da tela de inicio aonde deve ter todas as funções do app. 
        def tela_inicio():

            
            frame_incio = ctk.CTkFrame(master=janela,width=400, height=392)
            frame_incio.pack(side=RIGHT)

            text_apre = ctk.CTkLabel(master=frame_incio,text='SELECIONE OQUE DESEJA FAZER.',font=('Roboto',20),text_color='#42f5a4').place(x=50, y=20)


            #Definições de interação da função vender.
            def vender():
                frame_incio.pack_forget()

                frame_vender = ctk.CTkFrame(master=janela,width=350, height=390)
                frame_vender.pack(side=RIGHT)

                text_apre = ctk.CTkLabel(master=frame_vender,text='CONTABILIZAR VENDA',font=('Roboto',24),text_color='#42f5a4').place(x=50, y=40)
                
                entry_idcliente = ctk.CTkEntry(master=frame_vender,placeholder_text="ID do cliente",width=250,font=('Roboto', 14))
                entry_idcliente.place(x=50,y=120)

                entry_valor = ctk.CTkEntry(master=frame_vender,placeholder_text="Valor da venda $ ",width=250,font=('Roboto', 14))
                entry_valor.place(x=50, y=170)


                def back():
                    frame_vender.pack_forget()
                    tela_inicio()

                
                #Difinição da logica e interação com banco de dados para função vender.
                def enviar():
                    idcliente = entry_idcliente.get()
                    valor = entry_valor.get()
                    
                    try:

                        conexao.cursor()

                        cursor.execute('SELECT curdate()')
                        date = cursor.fetchall()[0][0]
                        

                        comando = f"""INSERT INTO vendas(id_cliente, valor, data_compra)
                        VALUES
                            ('{idcliente}', {valor}, '{date}')"""

                        cursor.execute(comando)
                        conexao.commit()
                        msg = messagebox.showinfo(title='Sucesso!', message='Venda concluida!')

                    except:
                        msg = messagebox.showinfo(title='Erro', message=' Venda não concluida!\n Verifique se preencheu todos campos.\n Verifique se não digitou algo incorreto.')
        
                    
                Button_enviar = ctk.CTkButton(master=frame_vender,text='Enviar',width=100,font=('Roboto', 14),command=enviar).place(x=180, y=240)
                Button_back = ctk.CTkButton(master=frame_vender,text='Voltar',width=100,font=('Roboto', 14), fg_color='gray', hover_color='#525252',command=back).place(x=60, y=240)
            
            #Definições de interação da função anotar.
            def anotar():
                frame_incio.pack_forget()

                frame_anotar = ctk.CTkFrame(master=janela,width=350, height=390)
                frame_anotar.pack(side=RIGHT)

                text_apre = ctk.CTkLabel(master=frame_anotar,text='ANOTAÇÃO DE VENDA.',font=('Roboto',24),text_color='#42f5a4').place(x=50, y=40)
                
                entry_idcliente = ctk.CTkEntry(master=frame_anotar,placeholder_text="ID do cliente",width=250,font=('Roboto', 14))
                entry_idcliente.place(x=50,y=120)

                entry_valor = ctk.CTkEntry(master=frame_anotar,placeholder_text="Valor da venda $ ",width=250,font=('Roboto', 14))
                entry_valor.place(x=50, y=170)

                def back():
                    frame_anotar.pack_forget()
                    tela_inicio()
                
                #Difinição da logica e interação com banco de dados para função anotar.
                def enviar_anotaçao():

                    try:
                        id_cliente = entry_idcliente.get()
                        valor_dig = float(entry_valor.get())

                        conexao.cursor()
                        cursor.execute(f"SELECT debito FROM anotaçoes WHERE idcliente = {id_cliente} " )
                        valor = float(cursor.fetchall()[0][0])
                        

                        valor_rg = valor_dig + valor

                        cursor.execute(f'UPDATE anotaçoes SET debito = {valor_rg} WHERE idcliente = {id_cliente} ')
                        
                        conexao.commit()

                        cursor.execute(f"SELECT setor FROM anotaçoes WHERE idcliente = {id_cliente} " )
                        setor = cursor.fetchall()[0][0]
                        
                        
                        cursor.execute(f"SELECT nome FROM anotaçoes WHERE idcliente = {id_cliente} " )
                        nome = cursor.fetchall()[0][0]
                        

                        

                        msg = messagebox.showinfo(title='Sucesso!', message=f'Anotação concluida!\nCliete numero: {id_cliente}.\nNome: {nome}.\nDebito: ({valor_rg} R$).\nSetor: {setor}. ')

                    except:

                        msg = messagebox.showinfo(title='Erro!', message='Anotação não concluida.\nVerifique se digitou tudo corretamente.')


                Button_enviar = ctk.CTkButton(master=frame_anotar,text='Enviar',width=100,font=('Roboto', 14),command=enviar_anotaçao).place(x=180, y=240)
                Button_back = ctk.CTkButton(master=frame_anotar,text='Voltar',width=100,font=('Roboto', 14), fg_color='gray', hover_color='#525252',command=back).place(x=60, y=240)

            #Definições de interação da função cadastrar novo cliente.
            def adc_cliente():
                frame_incio.pack_forget()

                cursor.execute('select count(idcliente) from anotaçoes')
                proximo = cursor.fetchall()[0][0] + 1
                

                

                frame_adc = ctk.CTkFrame(master=janela,width=350, height=390)
                frame_adc.pack(side=RIGHT)

                text_apre = ctk.CTkLabel(master=frame_adc,text='CADASTRAR CLIENTE',font=('Roboto',24),text_color='#42f5a4').place(x=50, y=40)
                text_apre2 = ctk.CTkLabel(master=frame_adc,text=f'O PRÓXIMO CLIENTE DEVE TER O ID {proximo}',font=('Roboto',12),text_color='#42f5a4').place(x=50, y=80)

                
                entry_idcliente = ctk.CTkEntry(master=frame_adc,placeholder_text="Novo ID",width=250,font=('Roboto', 14))
                entry_idcliente.place(x=50,y=120)

                entry_nome = ctk.CTkEntry(master=frame_adc,placeholder_text="Nome e sobrenome do cliente",width=250,font=('Roboto', 14))
                entry_nome.place(x=50, y=170)


                entry_setor = ctk.CTkEntry(master=frame_adc,placeholder_text="Setor da empresa",width=250,font=('Roboto', 14))
                entry_setor.place(x=50, y=220)


                def back():
                    frame_adc.pack_forget()
                    tela_inicio()

                
                #Difinição da logica e interação com banco de dados para função cadastrar novo cliente.
                def adc():
                    idcliente = entry_idcliente.get()
                    idcliente = int(idcliente)
                    nome = entry_nome.get()
                    setor = entry_setor.get()
                    conexao.cursor()


                    if idcliente == proximo and nome != None:

                        try:
                            cursor.execute(f"""INSERT INTO anotaçoes( idcliente, debito, nome, setor)
                            VALUES
                                ({idcliente}, 0 , '{nome}', '{setor}')""")
                            conexao.commit()
                            msg = messagebox.showinfo(title='Sucesso!', message='Cliente Cadastrado com Sucesso!')
                        except:
                            msg = messagebox.showinfo(title='Erro!', message='Cliente não Cadastrado!\nVerifique se preencheu o ID correto\nVerifique se o ID ou Nome ja estão cadastrados.')

                    else:
                        msg = messagebox.showinfo(title='Erro!', message=f'Verifiques O ID digitado.\nVocê digitou o ID {idcliente}\nE o proximo a ser cadastrado é o ID {proximo}.')

                #Difinição da função pesquiar por identificador do cliente.
                def pes():
                    frame_adc.pack_forget()

                    frame_pes = ctk.CTkFrame(master=janela,width=350, height=390)
                    frame_pes.pack(side=RIGHT)


                    text_apre = ctk.CTkLabel(master=frame_pes,text='PESQUISAR POR ID',font=('Roboto',24),text_color='#42f5a4').place(x=70, y=40)

                    entry_nome = ctk.CTkEntry(master=frame_pes,placeholder_text="Nome e sobrenome do cliente",width=250,font=('Roboto', 14))
                    entry_nome.place(x=50, y=120)

                    def pesId():
                        nome = entry_nome.get()
                        
                        try:
                            cursor.execute(f"SELECT idcliente FROM anotaçoes WHERE nome = '{nome}' " )
                            res = cursor.fetchall()[0][0]
                            msg = messagebox.showinfo(title='Sucesso!', message=f'O ID do cliente {nome} é ({res})')
                        except:
                            msg = messagebox.showinfo(title='Erro!', message=f'O cliente não foi encontrado.')


                        



                    def back2():
                        frame_pes.pack_forget()
                        tela_inicio()

                    Button_enviar = ctk.CTkButton(master=frame_pes,text='Enviar',width=100,font=('Roboto', 14),command=pesId).place(x=180, y=200)
                    Button_back = ctk.CTkButton(master=frame_pes,text='Voltar',width=100,font=('Roboto', 14), fg_color='gray', hover_color='#525252',command=back2).place(x=60, y=200)


                Button_enviar = ctk.CTkButton(master=frame_adc,text='Enviar',width=100,font=('Roboto', 14),command=adc).place(x=180, y=280)
                Button_back = ctk.CTkButton(master=frame_adc,text='Voltar',width=100,font=('Roboto', 14), fg_color='gray', hover_color='#525252',command=back).place(x=60, y=280)
                Button_pes = ctk.CTkButton(master=frame_adc,text='Pesquisar por ID',width=100,font=('Roboto', 14),command=pes).place(x=110, y=330)


            #Definição de interação com a função quitar anotação de um determiando cliente.
            def quitar():
                frame_incio.pack_forget()
                frame_quitar = ctk.CTkFrame(master=janela,width=350, height=390)
                frame_quitar.pack(side=RIGHT)

                text_apre = ctk.CTkLabel(master=frame_quitar,text='QUITAR CONTA DO CLIENTE',font=('Roboto',24),text_color='#42f5a4').place(x=20, y=40)

                entry_id = ctk.CTkEntry(master=frame_quitar,placeholder_text="ID do cliente",width=250,font=('Roboto', 14))
                entry_id.place(x=50, y=110)


                entry_valor = ctk.CTkEntry(master=frame_quitar,placeholder_text="Valor pago $",width=250,font=('Roboto', 14))
                entry_valor.place(x=50, y=160)




                def back():
                        frame_quitar.pack_forget()
                        tela_inicio()


                Button_back = ctk.CTkButton(master=frame_quitar,text='Voltar',width=100,font=('Roboto', 14), fg_color='gray', hover_color='#525252',command=back).place(x=130, y=310)
                
                #Difinição da função pesquiar o debito de um determinado cliente.
                def pes():
                    idcliente = entry_id.get()
                    try:
                        cursor.execute(f"SELECT debito FROM anotaçoes WHERE idcliente = {idcliente} " )
                        debito = cursor.fetchall()[0][0]
                        
                        cursor.execute(f"SELECT nome FROM anotaçoes WHERE idcliente = {idcliente} " )
                        nome = cursor.fetchall()[0][0]

                        cursor.execute(f"SELECT setor FROM anotaçoes WHERE idcliente = {idcliente} " )
                        setor = cursor.fetchall()[0][0]



                        msg = messagebox.showinfo(title='Sucesso!', message=f'Cliente numero: {idcliente}.\nNome: {nome}.\nDebito: ({debito} R$).\nSetor: {setor}.')
                    except:
                        msg = messagebox.showinfo(title='Erro', message=f'Cliente não encontrado')


                #Difinição da logica e interação com banco de dados para função quitar conta.
                def pagar():

                    try:
                        valor = float(entry_valor.get())
                        idcliente = entry_id.get()
                        conexao.cursor()

                        cursor.execute(f"SELECT debito FROM anotaçoes WHERE idcliente = {idcliente} " )
                        debito = float(cursor.fetchall()[0][0])
                        valor_atual = debito - valor


                        cursor.execute(f'UPDATE anotaçoes SET debito = {valor_atual} WHERE idcliente = {idcliente} ')
                        
                        conexao.commit()



                        cursor.execute('SELECT curdate()')
                        date = cursor.fetchall()[0][0]
                        

                        #Depois de pago, o valor que entrar em dinheiro sera automaticametente enviado a tabela vendas.
                        cursor.execute(f"""INSERT INTO vendas( id_cliente, valor, data_compra )
                        VALUES
	                        ({idcliente}, {valor}, '{date}')""")
                        conexao.commit()
                        


                        msg = messagebox.showinfo(title='Sucesso!', message=f'Debito pago com sucesso!, e adicionado a vendas.')
                        
                        


                    except:
                        msg = messagebox.showinfo(title='Erro', message=f'ERRO, Verifique se digitou o valor corretamente!')


                Button_pes = ctk.CTkButton(master=frame_quitar,text='Pesquisar Debito',width=155,font=('Roboto', 14),command=pes).place(x=100, y=210)

                Button_pagar = ctk.CTkButton(master=frame_quitar,text='Enviar',width=155,font=('Roboto', 14),command=pagar).place(x=100, y=260)

            #Definição da função visão geral de vendas, pode ser filtrado com base no mes e ano. (Apenas o valor que entrou liguido em caixa.)
            def vendas_geral():
                frame_incio.pack_forget()
                frame_vendas = ctk.CTkFrame(master=janela,width=350, height=390)
                frame_vendas.pack(side=RIGHT)

                text_apre = ctk.CTkLabel(master=frame_vendas,text='VISÃO GERAL DE VENDAS',font=('Roboto',20),text_color='#42f5a4').place(x=55, y=40)

                entry_mes = ctk.CTkEntry(master=frame_vendas,placeholder_text="Digite o MÊS que deseja filtar",width=250,font=('Roboto', 14))
                entry_mes.place(x=50, y=110)


                entry_ano = ctk.CTkEntry(master=frame_vendas,placeholder_text="Digite o ANO que deseja filtrar",width=250,font=('Roboto', 14))
                entry_ano.place(x=50, y=160)

                #Difinição da logica e interação com banco de dados para função visão geral de vendas.
                def vendas():
                    mes = entry_mes.get()
                    ano = entry_ano.get()

                    conexao.cursor()

                    try :
                        
                        cursor.execute(f"""select sum(valor) from vendas 
                                        where  month(data_compra) = '{mes}' 
                                        and year(data_compra) = '{ano}'""")


                        vendas_total = cursor.fetchall()[0][0]

                        if vendas_total == None:
                             msg = messagebox.showinfo(title='Erro', message=f'Não temos valores com esse filtro de data.\nPor favor selecione um filtro Valido.')
                             
                        else:
                             msg = messagebox.showinfo(title='Sucesso!', message=f'O valor líquido de vendas no mês {mes}/{ano}\nFoi de ({vendas_total} R$).\nCaso queira saber o valor de anotações não paga\nSelecione a opção a baixo!')


                    except:
                        msg = messagebox.showinfo(title='Erro', message=f'Não temos valores com esse filtro de data.\nPor favor selecione um filtro Valido.')
                        
                
                def back():
                        frame_vendas.pack_forget()
                        tela_inicio()


                #Difinição da logica e interação com banco de dados para função visão geral de anotação.(Aqui entra apenas valores de anotações)
                def pes():
    
                    cursor = conexao.cursor()

                    cursor.execute(f"""select sum(debito) from anotaçoes """)
                    valor = cursor.fetchall()[0][0]

                    msg = messagebox.showinfo(title='Anotações', message=f'Atualmete o total de debito anotado é de ({valor} R$)\nCaso queira visualisar o debito individual de cada cliente\nSeleciona a função "Pesquisar Debito" ou acesse a tabela.')




                Button_anot = ctk.CTkButton(master=frame_vendas,text='Pesquisar anotações',width=155,font=('Roboto', 14),command=pes).place(x=100, y=260)
                Button_back = ctk.CTkButton(master=frame_vendas,text='Voltar',width=100,font=('Roboto', 14), fg_color='gray', hover_color='#525252',command=back).place(x=130, y=310)
                Button_vendas = ctk.CTkButton(master=frame_vendas,text='Total de vendas',width=155,font=('Roboto', 14),command=vendas).place(x=100, y=210)

            #Definições de interação coma função Cadastrar novo administrador
            def register():
                frame_incio.pack_forget()
                frame_register = ctk.CTkFrame(master=janela,width=350, height=390)
                frame_register.pack(side=RIGHT)


                text_apre = ctk.CTkLabel(master=frame_register,text='CADASTRO DE ADMINISTRADOR',font=('Roboto',20),text_color='#42f5a4').place(x=30, y=40)


                entry_usuariorg = ctk.CTkEntry(master=frame_register,placeholder_text="Usuario",width=150,font=('Roboto', 14))
                entry_usuariorg.place(x=90, y=110)


                entry_senharg = ctk.CTkEntry(master=frame_register,placeholder_text="Senha",width=150,font=('Roboto', 14),show='*')
                entry_senharg.place(x=90, y=160)

                entry_nomerg = ctk.CTkEntry(master=frame_register,placeholder_text="Nome",width=150,font=('Roboto', 14))
                entry_nomerg.place(x=90, y=210)


                def back():
                        frame_register.pack_forget()
                        tela_inicio()
                
                #Difinição de logica e inteção ao banco de dados para cadastrar novo administrador do app.
                def salvar():

                    usuario = entry_usuariorg.get()
                    senha = entry_senharg.get()
                    nome = entry_nomerg.get()

                    if usuario and senha != None:
                        try:
                            conexao.cursor()
                            cursor.execute(f"""insert into adm(usuario, senha, nome)
                                                values 
                                                    ('{usuario}','{senha}', '{nome}')""")
                            conexao.commit()
                            
                            msg = messagebox.showinfo(title='Sucesso', message=f'Usuario cadastrado com sucesso!')
                        except:
                            msg = messagebox.showinfo(title='Erro', message=f'Usuario não cadastrado.\nVerifique se preencheu todos os campos.\nVerifique se o usuario ja esta cadastrado.')
                    else:
                        msg = messagebox.showinfo(title='Erro', message=f'Usuario não cadastrado.\nVerifique se preencheu todos os campos.\nVerifique se o usuario ja esta cadastrado.')



                    
                Button_back = ctk.CTkButton(master=frame_register,text='Voltar',width=100,font=('Roboto', 14), fg_color='gray', hover_color='#525252',command=back).place(x=113, y=310)
                Button_rg = ctk.CTkButton(master=frame_register,text='Cadastrar',width=100,font=('Roboto', 14),command=salvar).place(x=113, y=260)



            Button_vender = ctk.CTkButton(master=frame_incio,text='Vender',width=155,font=('Roboto', 14),command=vender).place(x=110, y=80)

            Button_anot = ctk.CTkButton(master=frame_incio,text='Anotar',width=155,font=('Roboto', 14),command=anotar).place(x=110, y=130)

            Button_adc = ctk.CTkButton(master=frame_incio,text='Adcionar novo cliente',width=155,font=('Roboto', 14),command=adc_cliente).place(x=110, y=230)

            Button_quitar = ctk.CTkButton(master=frame_incio,text='Quitar conta do cliente',width=155,font=('Roboto', 14),command=quitar).place(x=110, y=180)

            Button_grvenda = ctk.CTkButton(master=frame_incio,text='Visão geral de vendas',width=155,font=('Roboto', 14),command=vendas_geral).place(x=110, y=280)

            Button_rg = ctk.CTkButton(master=frame_incio,text='Cadastrar novo Adm',width=155,font=('Roboto', 14),command=register).place(x=110, y=330)

        #Definições de logica e interação ao banco de dados para a  função logar no app.
        def logar():
           
            usuario = entry_usuario.get()
            senha = entry_senha.get()

            try:
                cursor = conexao.cursor()
                cursor.execute(f"SELECT senha FROM adm WHERE usuario = '{usuario}' " )
                senha_bd = cursor.fetchall()
                
                
            
               

                if senha == senha_bd[0][0]:
                    msg = messagebox.showinfo(title='Sucesso!', message='Usuario Logado com Sucesso!')
                    frame_login.pack_forget()
                    tela_inicio()
                    
                

                    
                    
                elif senha != senha_bd[0][0]:
                    msg = messagebox.showinfo(title='ERRO!', message='Senha Incorreta, TENTE NOVAMENTE.')
                    
            except:
                msg = messagebox.showinfo(title='ERRO!', message='Usuario não encontrado TENTE NOVAMENTE.')
            

        Button_login = ctk.CTkButton(master=frame_login,text='Login',width=180,font=('Roboto', 14),command=logar).place(x=80, y=255)           

App()
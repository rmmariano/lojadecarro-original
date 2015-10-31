# coding: utf8
db = DAL('sqlite://storage.sqlite')

from gluon.tools import Crud, Auth
crud=Crud(globals(), db)
auth=Auth(globals(), db)
auth.define_tables()

#auth.settings.actions_disabled.append('register')

e_m={
    'empty':'Este campo é obrigatório',
    'in_db':'Este registro já existe no banco de dados',
    'not_in_db':'Este registro não existe no banco de dados',
    'email':'Você precisa inserir um e-mail válido',
    'image':'O arquivo precisa ser uma imagem válida',
    'not_in_set':'Você precisa escolher um valor válido',
    'not_in_range':'Digite um número entre %(min)s e %(max)s',
    }
            
config=dict(nmsite='Loja de Carro', dscsite='Só os melhores carros')

estados=('Novo', 'Usado')

cores=('Azul', 'Amarelo', 'Verde', 'Vermelho',\
    'Prata', 'Branco', 'Preto', 'Vinho')
    
    


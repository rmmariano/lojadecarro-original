# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index():
    
    #exibe a mensagem de boas vindas apenas uma vez
    if not session.flashed:
       response.flash=T('Welcome to carshop')
       session.flashed=True
    
    #consulta todos os registros da tabela de carros
    query=db.carro.id>0
    order=db.carro.id
    rows=db(query).select(orderby=order)    
    
    return dict(vitrine=VITRINE(rows), titulo='Ofertas')


def carros():
    
    #recupera o primeiro argumento, se não redireciona
    estado=request.args(0) or redirect(URL('index'))
    
    #aceita somente os argumentos da lista
    if estado not in ['usados', 'novos', 'Usados', 'Novos']:
        redirect(URL('index'))
    
    #determina qual view será renderizada
    response.view='default/index.html'
    
    #consulta apenas os registros com o critério
    query=db.carro.estado==estado[:-1].capitalize()        
    order=db.carro.id
    rows=db(query).select(orderby=order)            
    
    #cria os objetos de retorno        
    vitrine=VITRINE(rows)
    titulo='Carros %s' % estado.capitalize()
    
    return dict(vitrine=vitrine, titulo=titulo)


def detalhes():
    
    #recupera o primeiro argumento, ou redireciona
    id = request.args(0) or redirect(URL('index'))
    
    #efetua a consulta com argumentos
    query =db.carro.id==int(id)
    rows=db(query).select()   
    
    #cria um objeto de retorno
    vitrine = VITRINE(rows)
    
    # caso existam dados cria outros objetos    
    if rows:
        
        #Titulo para a página   
        row = rows[0]                  
        titulo = "%(marca)s - %(modelo)s - %(ano)s - %(estado)s" % \
            dict(marca=row.marca.nome,\
                 modelo=row.modelo,\
                 ano=row.ano,\
                 estado=row.estado)
        
        #Configurações para o formulário            
        db.comprador.id_carro.default = id
        db.comprador.id_carro.readable = False
        db.comprador.id_carro.writable = False 
        
        #criação do formulário       
        form = SQLFORM(db.comprador,formstyle='divs',submit_button='Enviar')
        
        #validação do formulário    
        if form.accepts(request.vars, session):
            response.flash = 'formulário aceito'
            
            #alteração do formulário em caso de sucesso
            form = DIV(H3('Sua mensagem foi enviada, em breve entraremos em contato'))
                
        elif form.errors:
            response.flash = 'formulário contém erros'
                                        
        return dict(vitrine=vitrine,titulo=titulo,form=form)
        
    else:
        return dict(vitrine=H1('Veículo não encontrado'))                 
    

def pesquisa():
    """Esta ação é um Ajax Callback"""
    
    #recupera o texto digitado
    txt = request.vars.busca
    
    #caso o texto não seja nulo
    if txt:
        
        #executa consulta no banco de dados usando %LIKE%
        rows = db(db.carro.modelo.like('%'+txt+'%')).select()
        
        #retorna um <ul><li>..
        return XML(UL(*[LI(A('%s - %s ' % (row.modelo,row.ano),_href=URL('detalhes',args=row.id)))\
                    for row in rows]))
                    
    else:
        return ''
    
@auth.requires_login()    
def admin():
    args = request.args
    titulo = 'administração'
    if not args:
        link = UL(*[LI(A(tab,_href=URL(args=tab))) for tab in db.tables])
        return dict(items=link,titulo=titulo)
    
    if not args(1):
        i = 0
    else:
        i =1
    
    for tab in db.tables:
        if tab==args(i):
            tb = db[tab]    
    
    if args(0)=='editar':
        form = crud.update(tb, args(2),next=URL(f='admin',args=args(1)))
        items = None
        titulo = 'Editar %s ' % args(i)
    else:
        form = crud.create(tb)
        rows = db().select(tb.ALL) 
        items = SQLTABLE(rows,linkto='editar')
        titulo = 'Inserir %s ' % args(i)        
    

    return dict(form=form,items=items,titulo=titulo)

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()



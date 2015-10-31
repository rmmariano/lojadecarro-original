# -*- coding: utf-8 -*-
def VITRINE(rows):
    """Cria uma vitrine de carros baseando-se nos campos:
    id,foto,marca,modelo,ano,estado,cor,itens,desc,valor
    do objeto Rows recebido como argumento"""
    
    #Armazena a estrutura do HTML que será interpolado    
    placeholder = """
    <div class='vcarro' style='width:500px;border:1px solid gray;'>
        <div class='vcfoto' style='float:left;margin:10px;'>
            <a href='%(url)s'>        
                <img border='0' width='100px' height='100px'
                    src='%(urlfoto)s'>
            </a>
        </div>
        <div class='vcdados' style='padding:10px;margin:10px;'>
            <span class='vcdtitulo'>
                <strong>
                %(marca)s - %(modelo)s - %(ano)s - %(estado)s
                </strong>
            </span>
            <div style='padding: 10px 100px 1px;'>
            <ul class='vcdinfo'>
                <li>%(cor)s</li>
                <li>%(estado)s</li>
                <li>%(itens)s</li>
            <ul>
            </div>
            <p class='vcdtexto'>
                <blockquote>
                %(desc)s
                </blockquote>
            </p>
            <span class='vcdvalor' 
                  style="float:right;color:blue;font-size:20px;">
                <strong>%(valor)s</strong>
            </span>                    
        </div>
    </div>
    """
    
    #Caso existam registros em "rows" efetua a interpolação
    if rows:
        vitrine = [placeholder % dict(url=URL('detalhes', args=row.id),\
                                    urlfoto=URL('download',args=row.foto),\
                                    marca=row.marca.nome,\
                                    modelo=row.modelo,\
                                    ano=row.ano,\
                                    estado=row.estado,\
                                    cor=row.cor,\
                                    itens=' | '.join(row.itens),\
                                    desc=row.desc,\
                                    valor=Moeda(row.valor),\
                                    ) for row in rows ]
                                
    else:
        vitrine = ["<h1 class='nada'>Não foram encontrados véiculos</h1>"]
    
    return vitrine
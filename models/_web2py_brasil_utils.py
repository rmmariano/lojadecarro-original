# coding: utf8
#web2py_brasil_utils
#####################################################################
#
# web2py Brasil Utils - http://www.web2pybrasil.com.br
#
# Coleção de functions e helpers que ajudam no desenvolvi-
# mento de uma aplicação web2py em idioma português brasil.
#
# How To: Inclua este arquivo em sua pasta models
# 
# SafeBRLocale() -> Efetua o acerto de localização - Thread Unsafe
# Moeda() -> Formata decimais, inteiros e flutuantes para R$
# Data() -> Formata datetima para data brasileira
#
#
# Colabore com este projeto
#
#
#####################################################################

# Define Locale Brasileiro sem bugs
def SafeBRLocale():
    from locale import setlocale, LC_ALL
    try:
       setlocale(LC_ALL,'pt_BR.UTF-8')
    except:
       setlocale(LC_ALL,'portuguese')    


# Formata moeda ###
def Moeda(valor, formatado=True):
    """
    >>> print Moeda(10000)
    R$ 10.000,00
    >>> print Moeda(10000,False)
    10.000,00
    """
    SafeBRLocale()
    from locale import currency
    if formatado:
        return 'R$ %s' % currency(valor, grouping=True, symbol=False)
    else:
        return currency(valor, grouping=False, symbol=False).replace(',','')
    

def Data(data,formato=1):
    """    
    >>> SafeBRLocale()
    >>> from datetime import datetime
    >>> data = datetime.strptime('2010-08-01','%Y-%m-%d')
    >>> print Data(data)
    01/08/2010
    >>> print Data(data,2)
    Dom, 01 Ago de 2010
    >>> print Data(data,3)
    domingo, 01 agosto de 2010
    """
    if formato == 2:
        format="%a, %d %b de %Y"
    elif formato == 3:
        format="%A, %d %B de %Y"
    else:
        format="%d/%m/%Y"
        
    return data.date().strftime(format)

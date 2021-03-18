import os
import yaml
import inspect
import requests
import re

from datetime import datetime
from ciscoconfparse import CiscoConfParse
from fpdf import FPDF

eleccio=input("Escribe el nombre del fichero a tratar: ")
with open(eleccio) as f:
        dd=yaml.load(f, Loader=yaml.FullLoader)

class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:  # Cabecera a tot menys a la primera pàgina
            # Set up a logo
            self.image('logo.png', 150, 10, 33)
            self.set_font('Times', '', 12)
            self.cell(
                0, 10, 'Informació infraestructura de Xarxa TecnoCampus ('+eleccio+')')
            # Line break
            self.ln(17)
        else:  # Portada de la pagina 1
            self.set_fill_color(245, 198, 66)
            self.rect(20, 20, 3, 250, 'F')
            self.image('logo.png', 150, 40, 50)
            self.set_font('Times', '', 24)
            self.ln(100)
            self.cell(0, 2, '         Informació infraestructura', 0, 0)
            self.set_font('Times', '', 24)
            self.ln(20)
            self.cell(0, 2, '         de Xarxa TecnoCampus', 0, 0)
            self.set_font('Times', '', 24)
            self.ln(20)
            self.cell(0, 2, '         ('+eleccio+')', 0, 0)
            self.set_font('Times', '', 24)
            self.ln(30)

            #Taking actual month
            aux=datetime.now()
            format=aux.strftime('%m')
            if format=='01': kk="Gener"
            elif format=='02': kk="Febrer"
            elif format=='03': kk="Març"
            elif format=='04': kk="Abril"
            elif format=='05': kk="Maig"
            elif format=='06': kk="Juni"
            elif format=='07': kk="Juliol"
            elif format=='08': kk="Agost"
            elif format=='09': kk="Septembre"
            elif format=='10': kk="Octubre"
            elif format=='11': kk="Novembre"
            elif format=='12': kk="Decembre" 
            self.cell(0, 2, '          '+kk+' 2021', 0, 0)
    # Page footer

    def footer(self):  # peu de pagina menys a la primera
        if self.page_no() != 1:
            self.set_y(-15)
            self.set_font('Times', 'B', 8)
            # Page number
            if eleccio=="Ex1":  
                self.cell(0, 10, 'Page '+str(self.page_no())+'/16', 0, 0, 'R')
            elif eleccio=="Ex2":
                self.cell(0, 10, 'Page '+str(self.page_no())+'/14', 0, 0, 'R')
            else:
                self.cell(0, 10, 'Page '+str(self.page_no())+'/16', 0, 0, 'R')
                
pdf = PDF()
pdf.add_page()
pdf.set_font('Times', 'B', 14)
pdf.add_page()
if eleccio=="Ex1":
    # INDEX
    pdf.cell(0, 10, 'ÍNDEX', 0, 1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.- Introducció............................................................................................................................................5', 0, 1)
    pdf.cell(10)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.1.- Descripció.................................................................................................................................5', 0, 1)
    pdf.cell(10)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.2.- Objectius..................................................................................................................................5', 0, 1)
    pdf.cell(10)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.3.- Descripció General de les infraestructures..........................................................................5', 0, 1)

    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '2.- Configuració dels dispositius................................................................................................................6', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times','B',12)
    ii=1
    npag=4
    for k in dd['nodes']:
        #if(ii==9):
         #   pdf.add_page()
        #else:
        #    pdf.ln(4)
        pdf.cell(10)
        if(ii==2):
            npag=6
        elif(ii==3):
            npag=9
        elif(ii==4):
            npag=11
        elif(ii==5):
            npag=14
        elif(ii==6):
        	npag=14
        elif(ii==7):
            npag=15
        pdf.cell(0, 10, '2.'+ str(ii) +'.- '+ k['label'] +'............................................................................................................... '+ str(npag),0,1,'L',False)
        cc=1
        if "Building configuration..." in k['configuration']:
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0,0,'2.'+ str(ii) +'.'+ str(cc) +'.- Configuració criptogràfica del dispositiu............................................................................ '+ str(npag),0,1,'L',False)
            cc=cc+1
        if(npag==8):
            npag=npag+1
        pdf.ln(4)
        pdf.cell(20)
        pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Interfícies............................................................................................................................. '+ str(npag),0,1,'L',False)
        cc=cc+1
        if "Building configuration..." in k['configuration']:
            if(npag==5):
                npag=npag+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració dels protocols d`enrutament......................................................................... '+ str(npag),0,1,'L',False)
            cc=cc+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració de Llistes de Control d`Accés....................................................................... '+ str(npag),0,1,'L',False)
            cc=cc+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració de Banners .................................................................................................. '+ str(npag),0,1,'L',False)
            cc=cc+1
        ii=ii+1
    
    pdf.ln(4)
    pdf.cell(0, 10, '3.- Interfícies....................................................................................................................................... '+ str(npag),0,1,'L',False)
    cont = 0
    indexList = list()
    parse = CiscoConfParse('Ex1')
    for intf_obj in parse.find_objects(r'nodes'):
        for c1_obj in intf_obj.children:
            for c2_obj in c1_obj.children:
                if "label:" in c2_obj.text:
                    indexList.append(str(c2_obj.text).replace("label:", ""))
    # Introduction
    pdf.add_page()
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 10, '1.- Introducció', 0, 1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.1- Descripció', 0, 1)
    pdf.set_font('Times', '', 12)

    parse = CiscoConfParse('Ex1')
    for intf_obj in parse.find_objects(r'lab'):
        for c1_obj in intf_obj.children:
            if "title:" in c1_obj.text:
                titul = str(c1_obj.text).replace("title:", "")

    pdf.multi_cell(0, 10, 'El present document descriu la topologia realitzada amb la configuració ' +
                titul+' a la \nempresa TecnoCampus.', 0, 1, 'L')

    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.2- Objectius', 0, 1)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 10, "El objectiu d'aquest document és la de formalitzar el traspàs d'informació al equip tècnic \nresponsable del manteniment de les infraestructures instal·lades. Aquesta informació fa \nreferencia al disseny, instal·lació i configuració dels dispositius i sistemes afectats per la implementació.", 0, 1, 'L')
    pdf.cell(0, 10, 'La present documentació inclou:', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150) +
            ' Descripció general de les infraestructures instal·lades', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+' Configuració de les interfícies de xarxa', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150) +
            ' Configuració de les polítiques per les connexions VPN', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+" Configuració dels protocols d'enrutament", 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+" Configuració de les llistes de control d'accés", 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+' Configuració dels banners', 0, 1)

    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 10, '1.3.- Descripció General de les infraestructures', 0, 1)
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, 'Actualment la topologia té la següent distribució: ', 0, 1)
    pdf.ln(10)
    pdf.image('Image1.png', x=None, y=None, w=150)
    pdf.ln(10)
    contId = 0
    parse = CiscoConfParse('Ex1')
    for intf_obj in parse.find_objects(r'nodes'):
        for c1_obj in intf_obj.children:
            if "id:" in c1_obj.text:
                contId = contId+1
    contLinks = 0
    idList = list()
    portList = list()
    parse = CiscoConfParse('Ex1')

    for intf_obj in parse.find_objects(r'nodes'):
        for c1_obj in intf_obj.children:
            if "id: n1" in c1_obj.text:
                for c2_obj in c1_obj.children:
                    if "interfaces:" in c2_obj.text:
                        for c3_obj in c2_obj.children:
                            if "- id: " in c3_obj.text:
                                contLinks = contLinks+1
                                idList.append(
                                    str(c3_obj.text).replace("- id:", ""))
                                for c4_obj in c3_obj.children:
                                    if "label:" in c4_obj.text:
                                        portList.append(
                                            str(c4_obj.text).replace("label:", ""))

    pdf.cell(10)
    pdf.cell(0, 5, 'En aquesta topologia tenim '+str(contId) +
            ' equips, connectats a través de '+str(contLinks)+' links', 0, 1, 'L')

   	pdf.cell(0, 10, '2.- Configuració dels dispositius', 0, 1, 'L')
   	pdf.cell(0, 10, 'A continuació, es detalla la configuració dels diferents dispositius:', 0, 1, 'L')
    
    ips= list()
    intf= list()
    term=list()
    xxs= list()
    idx=1
    for klk in dd['nodes']:
        pdf.set_font('Times', 'B', 12)
        pdf.ln(8)
        pdf.cell(0, 0, '2.'+str(idx)+'.- '+ klk['label'], 0, 1)
        pdf.ln(6)
        ms=1
        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', '', 10)
            #Date and Time
            xx='UTC'
            trobat=re.search(xx, klk['configuration'])
            ini=trobat.start()
            fin=trobat.end()
            time=klk['configuration'][(ini-9):(fin)]
            date=klk['configuration'][(fin+5):(fin+16)]

            pdf.cell(0, 10, 'El darrer canvi de la configuració va ser el '+ date +' a les '+ time, 0, 1)
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració criptogràfica del dispositiu', 0, 1)
            pdf.set_font('Times', '', 12)
            pdf.ln(7)
            if "crypto" in klk['configuration']:
                pdf.cell(0, 10, 'El dispositiu té la següent configuració de crypto:', 0, 1)
                pdf.ln(4)
                pdf.cell(20)
                xx='set peer'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                ip=klk['configuration'][(fin+1):(fin+9)]
                pdf.cell(0, 10, '-    Conexió amb '+ ip +':', 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                xx='isakmp policy'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                numero=klk['configuration'][(fin+1):(fin+3)]
                pdf.cell(0, 10, 'o   Política de regles número '+ numero +':', 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='encr aes'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                ee=klk['configuration'][(fin-3):(fin+4)]
                pdf.cell(0, 0, '·    Encriptació '+ ee, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='authentication'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                auth=klk['configuration'][(fin+1):(fin+10)]
                pdf.cell(0, 10, '·    Autenticació '+ auth, 0, 1)
                pdf.ln(2)
                pdf.cell(40)
                xx='group'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                group=klk['configuration'][(fin+1)]
                pdf.cell(0, 10, '·    Diffie-Helmann grup '+ group, 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                xx='isakmp key'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                key=klk['configuration'][(fin+1):(fin+8)]
                pdf.cell(0, 10, 'o   Contrasenya ISAKMP: '+ key, 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                pdf.cell(0, 10, 'o   Configuració VPN:', 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='ipsec transform-set'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                tt=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 10, '·    Conjunt de transformació '+ tt, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                enc=klk['configuration'][(fin+5):(fin+12)]
                pdf.cell(0, 10, '·    Configuració Encriptació ESP: '+ enc, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                sgn=klk['configuration'][(fin+13):(fin+25)]
                pdf.cell(0, 10, '·    Configuració Signatura ESP: '+ sgn, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                mod=klk['configuration'][(fin+32):(fin+38)]
                pdf.cell(0, 10, '·    Mode '+ mod, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='match address'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                acl=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 10, '·    ACL número '+ acl, 0, 1)
            else:
                pdf.cell(0, 10, 'El dispositiu no té configuració de crypto', 0, 1)
            
            ms=ms+1

        pdf.set_font('Times', 'B', 12)
        if "Building configuration..." in klk['configuration']:
            pdf.ln(4)
        pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Interfícies', 0, 1)
        pdf.set_font('Times', '', 11)
        pdf.cell(0, 10, 'Les interfícies i la seva configuració és:', 0, 1)
        pdf.ln(4)

        for q in klk['interfaces']:
            pdf.cell(25)
            xx=q['label']
            ff=re.search(xx, klk['configuration'])
            ipAddr=''
            if ff!=None:
                fin=ff.end()
                if "no" not in klk['configuration'][(fin):(fin+5)]:
                    ipAddr=klk['configuration'][(fin+13):(fin+38)]
                    xx='255.255'
                    ff=re.search(xx, ipAddr)
                    if ff != None:
                        s=ff.start()
                        term.append(klk['label'])
                        intf.append(q['id'])
                        ips.append(ipAddr[:s])

                        ipAddr=': '+ipAddr[:s]+'('+ipAddr[s:len(ipAddr)]+')'
                if 'alpine' in klk['node_definition']:
                    term.append(klk['label'])
                    intf.append(q['id'])

                    ipAddr=' (DG: '+ipAddr[13:]+')'
                    xx='ip addr add'
                    ff=re.search(xx, klk['configuration'])
                    fin=ff.end()
                    ips.append(klk['configuration'][(fin+1):(fin+12)])

                    ipAddr='. Configuració IP: '+klk['configuration'][(fin+1):(fin+15)]+ ipAddr
            
            pdf.cell(0, 10, '-    Link '+ q['id']+': '+ q['label']+ ipAddr, 0, 1)
            pdf.ln(5)
        ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(5)
            pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració dels protocols d enrutament', 0, 1)
            pdf.set_font('Times', '', 11)
            xx='router ospf'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                fin=trobat.end()
            protocol=klk['configuration'][(fin-4):(fin+4)]
            pdf.cell(0, 0, 'El protocol d enrutament utilitzat és '+ protocol.upper() +', amb la següent configuració (xarxes publicades):', 0, 1)
            pdf.ln(4)
            pdf.cell(10)
            xx='area'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                fin=trobat.end()
            area=klk['configuration'][fin+1]
            pdf.cell(0, 10, '-    Àrea '+ area+':', 0, 1)
            xx='network'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                s=trobat.end()
            s=s+1
            ntk=""
            while klk['configuration'][s]!='!':
                ntk=ntk+klk['configuration'][s]
                s=s+1
            num=klk['configuration'].count("area")
            ntk=ntk.replace("network", "")
            ntk=ntk.replace("area 0", "")
            while num>0:
                xx=' '
                trobat=re.search(xx, ntk)
                if(trobat!= None):
                    x=trobat.end()
                    if ntk[:x-1] not in xxs:
                        xxs.append(ntk[:x-1])
                    p1=ntk[:x-1]+' màscara invertida '
                    ntk=ntk[x:]
                    ntk=ntk[2:]
                    trobat=re.search(xx, ntk)
                    p2=ntk[:x-1]
                    ntk=ntk[x:]
                    net=p1+p2
                pdf.ln(7)
                pdf.cell(20)
                pdf.cell(0, 0, 'o   Xarxa '+ net, 0, 1)
                num=num-1 
            ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 0, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració de Llistes de Control d Accés', 0, 1)
            pdf.set_font('Times', '', 11)
            pdf.ln(7)
            if "access-list" in klk['configuration']:
                pdf.cell(0, 0, 'El dispositiu té configurada la següent ACL:', 0, 1)
                pdf.ln(7)
                pdf.cell(10)
                xx='access-list'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                acclist=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 0, '-    Número '+acclist, 0, 1)
                pdf.ln(5)
                pdf.cell(20)
                xx='permit'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                permit=klk['configuration'][(fin+1):(fin+3)]
                pdf.cell(0, 10, 'o   PERMIT ('+ permit.upper() +'):', 0, 1)
                pdf.ln(1)
                pdf.cell(30)
                xx='control-plane'
                trobat=re.search(xx, klk['configuration'])
                ini=trobat.start()
                origdest=klk['configuration'][(fin+4):(ini-2)]
                xx=' '
                trobat=re.search(xx, origdest)
                if(trobat!= None):
                    x=trobat.end()
                    origen=origdest[:x-1]+' màscara invertida '+origdest[x:x+9]
                    origdest=origdest[x:]
                    trobat=re.search(xx, klk['configuration'])
                    x=trobat.start()
                    origdest=origdest[x+2:]
                    trobat=re.search(xx, klk['configuration'])
                    x=trobat.start()
                    desti=origdest[:x+3]+' màscara invertida '+origdest[x+3:x+13]
                pdf.cell(0, 10, '·   ORIGEN: '+origen, 0, 1)
                pdf.ln(2)
                pdf.cell(30)
                pdf.cell(0, 10, '·   DESTÍ: '+desti, 0, 1)
            else:
                pdf.cell(0, 10, 'El dispositiu no té configurada cap ACL.', 0, 1)

            ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 0, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració de Banners', 0, 1)
            pdf.set_font('Times', '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(7)
            pdf.cell(0, 0, 'El dispositiu té configurats els següent Banners:', 0, 1)
            pdf.ln(7)
            xx='banner'
            trobat=re.search(xx, klk['configuration'])
            fin=trobat.end()
            xx='line con 0'
            trobat=re.search(xx, klk['configuration'])
            ini=trobat.start()
            ban=klk['configuration'][(fin+1):(ini-2)]
            ban="    -    "+ban
            ban=ban.replace("banner", "    -    ")
            ban=ban.replace("^CCC", " ")
            ban=ban.replace("^C", " ")
            pdf.cell(18)
            pdf.multi_cell(170, 8, ban, 0, 'J', False)
            ms=ms+1
        idx=idx+1 
    #3.- 
    pdf.set_font('Times', '', 20)
    pdf.ln(5)
    pdf.cell(18)
    pdf.cell(10, 10, '3.- Interfícies', 0, 1)
    pdf.set_font('Times', '', 10)
    pdf.ln(3)
    pdf.cell(18)
    pdf.cell(0, 10, 'La configuració de les interfícies (links) d interconnexió entre equips és:', 0, 1)
    pdf.ln(8)
    for q in dd['links']:
        pdf.cell(25)
        pdf.set_font('Times', 'B', 11)
        ids='1'+q['id'][1]
        pdf.cell(0, 0, '-    Link '+ids, 0, 1)
        pdf.set_font('Times', '', 11)
        pdf.cell(44)
        lab1=''
        lab2=''
        for n in dd['nodes']:
            if q['n1'] == n['id']:
                lab1=n['label']
            if q['n2'] == n['id']:
                lab2=n['label']

        pdf.cell(0, 0, ': conecta '+ q['i1'] +' ('+ lab1 +')'+' amb '+ q['i2']+' ('+ lab2 +')', 0, 1)
        pdf.ln(5)

    pdf.ln(3)
    pdf.cell(18)
    pdf.cell(0, 0, 'El resum de les adreces IP de les interfícies és:', 0, 1)
    #TABLA
    pdf.ln(5)
    pdf.cell(13)
    if len(xxs)!=0:
        pdf.cell(23, 10, "Xarxa", 1, 0)
    pdf.cell(23, 10, "Equip1", 1, 0)
    pdf.cell(23, 10, "Interfície1", 1, 0)
    pdf.cell(23, 10, "IP1", 1, 0)
    pdf.cell(23, 10, "Equip2", 1, 0)
    pdf.cell(23, 10, "Interfície2", 1, 0)
    pdf.cell(23, 10, "IP2", 1, 1)
    l=0
    while l< len(term):
        pdf.cell(13)
        if len(xxs)!=0:
            if l==0:
                pdf.cell(23, 10, xxs[l], 1, 0)
            else:
                pdf.cell(23, 10, xxs[int(l/2)], 1, 0)
        pdf.cell(23, 10, term[l], 1, 0)
        pdf.cell(23, 10, intf[l], 1, 0)
        pdf.cell(23, 10, ips[l], 1, 0)
        if(l+1!=len(term)):
            pdf.cell(23, 10, term[l+1], 1, 0)
            pdf.cell(23, 10, intf[l+1], 1, 0)
            pdf.cell(23, 10, ips[l+1], 1, 1)
        l=l+2
    pdf.output("Ex1.pdf")

elif eleccio=="Ex2":
    # INDEX
    pdf.cell(0, 10, 'ÍNDEX', 0, 1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.- Introducció...........................................................................................................................................4', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.1.- Descripció........................................................................................................................4', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.2.- Objectius..........................................................................................................................4', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.3.- Descripció General de les infraestructures...................................................................4', 0, 1)

    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '2.- Configuració dels dispositius................................................................................................................4', 0, 1)

    pdf.cell(20)
    pdf.set_font('Times','B',12)
    ii=1
    npag=5
    for k in dd['nodes']:
        #if(ii==9):
        #    pdf.add_page()
        #else:
        #    pdf.ln(4)
        pdf.cell(10)
        if(ii==2):
            npag=6
        elif(ii==3):
            npag=8
        elif(ii==4):
            npag=9
        elif(ii==5):
            npag=10
        elif(ii==7):
            npag=npag+1
        pdf.cell(0, 10, '2.'+ str(ii) +'.- '+ k['label'] +'............................................................................................................... '+ str(npag),0,1,'L',False)
        cc=1
        if "Building configuration..." in k['configuration']:
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0,0,'2.'+ str(ii) +'.'+ str(cc) +'.- Configuració criptogràfica del dispositiu............................................................................ '+ str(npag),0,1,'L',False)
            cc=cc+1
        if(npag==8):
            npag=npag+1
        pdf.ln(4)
        pdf.cell(20)
        pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Interfícies........................................................................................................................... '+ str(npag),0,1,'L',False)
        cc=cc+1
        if "Building configuration..." in k['configuration']:
            if(npag==5):
                npag=npag+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració dels protocols d`enrutament......................................................................... '+ str(npag),0,1,'L',False)
            cc=cc+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració de Llistes de Control d`Accés....................................................................... '+ str(npag),0,1,'L',False)
            cc=cc+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració de Banners .................................................................................................. '+ str(npag),0,1,'L',False)
            cc=cc+1
        ii=ii+1
    
    pdf.ln(4)
    pdf.cell(0, 10, '3.- Interfícies....................................................................................................................................... '+ str(npag),0,1,'L',False)
    cont = 0
    indexList = list()
    parse = CiscoConfParse('Ex1')
    for intf_obj in parse.find_objects(r'nodes'):
        for c1_obj in intf_obj.children:
            for c2_obj in c1_obj.children:
                if "label:" in c2_obj.text:
                    indexList.append(str(c2_obj.text).replace("label:", ""))
    # Introduction
    pdf.add_npage()
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 10, '1.- Introducció', 0, 1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.1- Descripció', 0, 1)
    pdf.set_font('Times', '', 12)

    parse = CiscoConfParse('Ex2')
    for intf_obj in parse.find_objects(r'lab'):
        for c1_obj in intf_obj.children:
            if "title:" in c1_obj.text:
                titul = str(c1_obj.text).replace("title:", "")

    pdf.multi_cell(0, 10, 'El present document descriu la topologia realitzada amb la configuració ' +
                titul+' a la \nempresa TecnoCampus.', 0, 1, 'L')

    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.2- Objectius', 0, 1)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 10, "El objectiu d'aquest document és la de formalitzar el traspàs d'informació al equip tècnic \nresponsable del manteniment de les infraestructures instal·lades. Aquesta informació fa \nreferencia al disseny, instal·lació i configuració dels dispositius i sistemes afectats per la implementació.", 0, 1, 'L')
    pdf.cell(0, 10, 'La present documentació inclou:', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150) +
            ' Descripció general de les infraestructures instal·lades', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+' Configuració de les interfícies de xarxa', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150) +
            ' Configuració de les polítiques per les connexions VPN', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+" Configuració dels protocols d'enrutament", 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+" Configuració de les llistes de control d'accés", 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+' Configuració dels banners', 0, 1)

    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 10, '1.3.- Descripció General de les infraestructures', 0, 1)
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, 'Actualment la topologia té la següent distribució: ', 0, 1)
    pdf.ln(10)
    contId = 0
    parse = CiscoConfParse('Ex2')
    for intf_obj in parse.find_objects(r'nodes'):
        for c1_obj in intf_obj.children:
            if "id:" in c1_obj.text:
                contId = contId+1
    contLinks = 0
    parse = CiscoConfParse('Ex2')
    for intf_obj in parse.find_objects(r'links'):
        for c1_obj in intf_obj.children:
            if "id:" in c1_obj.text:
                contLinks=contLinks+1
    pdf.cell(10)
    pdf.cell(0, 5, 'En aquesta topologia tenim '+str(contId) +
            ' equips, connectats a través de '+str(contLinks)+' links', 0, 1, 'L')

    pdf.cell(0, 10, '2.- Configuració dels dispositius', 0, 1, 'L')
   	pdf.cell(0, 10, 'A continuació, es detalla la configuració dels diferents dispositius:', 0, 1, 'L')
    
    ips= list()
    intf= list()
    term=list()
    xxs= list()
    idx=1
    for klk in dd['nodes']:
        pdf.set_font('Times', 'B', 12)
        pdf.ln(8)
        pdf.cell(0, 0, '2.'+str(idx)+'.- '+ klk['label'], 0, 1)
        pdf.ln(6)
        ms=1
        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', '', 10)
            #Date and Time
            xx='UTC'
            trobat=re.search(xx, klk['configuration'])
            ini=trobat.start()
            fin=trobat.end()
            time=klk['configuration'][(ini-9):(fin)]
            date=klk['configuration'][(fin+5):(fin+16)]

            pdf.cell(0, 10, 'El darrer canvi de la configuració va ser el '+ date +' a les '+ time, 0, 1)
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració criptogràfica del dispositiu', 0, 1)
            pdf.set_font('Times', '', 12)
            pdf.ln(7)
            if "crypto" in klk['configuration']:
                pdf.cell(0, 10, 'El dispositiu té la següent configuració de crypto:', 0, 1)
                pdf.ln(4)
                pdf.cell(20)
                xx='set peer'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                ip=klk['configuration'][(fin+1):(fin+9)]
                pdf.cell(0, 10, '-    Conexió amb '+ ip +':', 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                xx='isakmp policy'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                numero=klk['configuration'][(fin+1):(fin+3)]
                pdf.cell(0, 10, 'o   Política de regles número '+ numero +':', 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='encr aes'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                ee=klk['configuration'][(fin-3):(fin+4)]
                pdf.cell(0, 0, '·    Encriptació '+ ee, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='authentication'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                auth=klk['configuration'][(fin+1):(fin+10)]
                pdf.cell(0, 10, '·    Autenticació '+ auth, 0, 1)
                pdf.ln(2)
                pdf.cell(40)
                xx='group'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                group=klk['configuration'][(fin+1)]
                pdf.cell(0, 10, '·    Diffie-Helmann grup '+ group, 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                xx='isakmp key'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                key=klk['configuration'][(fin+1):(fin+8)]
                pdf.cell(0, 10, 'o   Contrasenya ISAKMP: '+ key, 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                pdf.cell(0, 10, 'o   Configuració VPN:', 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='ipsec transform-set'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                tt=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 10, '·    Conjunt de transformació '+ tt, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                enc=klk['configuration'][(fin+5):(fin+12)]
                pdf.cell(0, 10, '·    Configuració Encriptació ESP: '+ enc, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                sgn=klk['configuration'][(fin+13):(fin+25)]
                pdf.cell(0, 10, '·    Configuració Signatura ESP: '+ sgn, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                mod=klk['configuration'][(fin+32):(fin+38)]
                pdf.cell(0, 10, '·    Mode '+ mod, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='match address'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                acl=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 10, '·    ACL número '+ acl, 0, 1)
            else:
                pdf.cell(0, 10, 'El dispositiu no té configuració de crypto', 0, 1)
            
            ms=ms+1

        pdf.set_font('Times', 'B', 12)
        if "Building configuration..." in klk['configuration']:
            pdf.ln(4)
        pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Interfícies', 0, 1)
        pdf.set_font('Times', '', 11)
        pdf.cell(0, 10, 'Les interfícies i la seva configuració és:', 0, 1)
        pdf.ln(4)

        for q in klk['interfaces']:
            pdf.cell(25)
            xx=q['label']
            ff=re.search(xx, klk['configuration'])
            ipAddr=''
            if ff!=None:
                fin=ff.end()
                if "no" not in klk['configuration'][(fin):(fin+5)]:
                    ipAddr=klk['configuration'][(fin+13):(fin+38)]
                    xx='255.255'
                    ff=re.search(xx, ipAddr)
                    if ff != None:
                        s=ff.start()
                        term.append(klk['label'])
                        intf.append(q['id'])
                        ips.append(ipAddr[:s])

                        ipAddr=': '+ipAddr[:s]+'('+ipAddr[s:len(ipAddr)]+')'
                if 'alpine' in klk['node_definition']:
                    term.append(klk['label'])
                    intf.append(q['id'])

                    ipAddr=' (DG: '+ipAddr[13:]+')'
                    xx='ip addr add'
                    ff=re.search(xx, klk['configuration'])
                    fin=ff.end()
                    ips.append(klk['configuration'][(fin+1):(fin+12)])

                    ipAddr='. Configuració IP: '+klk['configuration'][(fin+1):(fin+15)]+ ipAddr
            
            pdf.cell(0, 10, '-    Link '+ q['id']+': '+ q['label']+ ipAddr, 0, 1)
            pdf.ln(5)
        ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(5)
            pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració dels protocols d enrutament', 0, 1)
            pdf.set_font('Times', '', 11)
            xx='router ospf'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                fin=trobat.end()
            protocol=klk['configuration'][(fin-4):(fin+4)]
            pdf.cell(0, 0, 'El protocol d enrutament utilitzat és '+ protocol.upper() +', amb la següent configuració (xarxes publicades):', 0, 1)
            pdf.ln(4)
            pdf.cell(10)
            xx='area'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                fin=trobat.end()
            area=klk['configuration'][fin+1]
            pdf.cell(0, 10, '-    Àrea '+ area+':', 0, 1)
            xx='network'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                s=trobat.end()
            s=s+1
            ntk=""
            while klk['configuration'][s]!='!':
                ntk=ntk+klk['configuration'][s]
                s=s+1
            num=klk['configuration'].count("area")
            ntk=ntk.replace("network", "")
            ntk=ntk.replace("area 0", "")
            while num>0:
                xx=' '
                trobat=re.search(xx, ntk)
                if(trobat!= None):
                    x=trobat.end()
                    if ntk[:x-1] not in xxs:
                        xxs.append(ntk[:x-1])
                    p1=ntk[:x-1]+' màscara invertida '
                    ntk=ntk[x:]
                    ntk=ntk[2:]
                    trobat=re.search(xx, ntk)
                    p2=ntk[:x-1]
                    ntk=ntk[x:]
                    net=p1+p2
                pdf.ln(7)
                pdf.cell(20)
                pdf.cell(0, 0, 'o   Xarxa '+ net, 0, 1)
                num=num-1 
            ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 0, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració de Llistes de Control d Accés', 0, 1)
            pdf.set_font('Times', '', 11)
            pdf.ln(7)
            if "access-list" in klk['configuration']:
                pdf.cell(0, 0, 'El dispositiu té configurada la següent ACL:', 0, 1)
                pdf.ln(7)
                pdf.cell(10)
                xx='access-list'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                acclist=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 0, '-    Número '+acclist, 0, 1)
                pdf.ln(5)
                pdf.cell(20)
                xx='permit'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                permit=klk['configuration'][(fin+1):(fin+3)]
                pdf.cell(0, 10, 'o   PERMIT ('+ permit.upper() +'):', 0, 1)
                pdf.ln(1)
                pdf.cell(30)
                xx='control-plane'
                trobat=re.search(xx, klk['configuration'])
                ini=trobat.start()
                origdest=klk['configuration'][(fin+4):(ini-2)]
                xx=' '
                trobat=re.search(xx, origdest)
                if(trobat!= None):
                    x=trobat.end()
                    origen=origdest[:x-1]+' màscara invertida '+origdest[x:x+9]
                    origdest=origdest[x:]
                    trobat=re.search(xx, klk['configuration'])
                    x=trobat.start()
                    origdest=origdest[x+2:]
                    trobat=re.search(xx, klk['configuration'])
                    x=trobat.start()
                    desti=origdest[:x+3]+' màscara invertida '+origdest[x+3:x+13]
                pdf.cell(0, 10, '·   ORIGEN: '+origen, 0, 1)
                pdf.ln(2)
                pdf.cell(30)
                pdf.cell(0, 10, '·   DESTÍ: '+desti, 0, 1)
            else:
                pdf.cell(0, 10, 'El dispositiu no té configurada cap ACL.', 0, 1)

            ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 0, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració de Banners', 0, 1)
            pdf.set_font('Times', '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(7)
            pdf.cell(0, 0, 'El dispositiu té configurats els següent Banners:', 0, 1)
            pdf.ln(7)
            xx='banner'
            trobat=re.search(xx, klk['configuration'])
            fin=trobat.end()
            xx='line con 0'
            trobat=re.search(xx, klk['configuration'])
            ini=trobat.start()
            ban=klk['configuration'][(fin+1):(ini-2)]
            ban="    -    "+ban
            ban=ban.replace("banner", "    -    ")
            ban=ban.replace("^CCC", " ")
            ban=ban.replace("^C", " ")
            pdf.cell(18)
            pdf.multi_cell(170, 8, ban, 0, 'J', False)
            ms=ms+1
        idx=idx+1 
    #3.- 
    pdf.set_font('Times', '', 20)
    pdf.ln(5)
    pdf.cell(18)
    pdf.cell(10, 10, '3.- Interfícies', 0, 1)
    pdf.set_font('Times', '', 10)
    pdf.ln(3)
    pdf.cell(18)
    pdf.cell(0, 10, 'La configuració de les interfícies (links) d interconnexió entre equips és:', 0, 1)
    pdf.ln(8)
    for q in dd['links']:
        pdf.cell(25)
        pdf.set_font('Times', 'B', 11)
        ids='1'+q['id'][1]
        pdf.cell(0, 0, '-    Link '+ids, 0, 1)
        pdf.set_font('Times', '', 11)
        pdf.cell(44)
        lab1=''
        lab2=''
        for n in dd['nodes']:
            if q['n1'] == n['id']:
                lab1=n['label']
            if q['n2'] == n['id']:
                lab2=n['label']

        pdf.cell(0, 0, ': conecta '+ q['i1'] +' ('+ lab1 +')'+' amb '+ q['i2']+' ('+ lab2 +')', 0, 1)
        pdf.ln(5)

    pdf.ln(3)
    pdf.cell(18)
    pdf.cell(0, 0, 'El resum de les adreces IP de les interfícies és:', 0, 1)
    #TABLA
    pdf.ln(5)
    pdf.cell(13)
    if len(xxs)!=0:
        pdf.cell(23, 10, "Xarxa", 1, 0)
    pdf.cell(23, 10, "Equip1", 1, 0)
    pdf.cell(23, 10, "Interfície1", 1, 0)
    pdf.cell(23, 10, "IP1", 1, 0)
    pdf.cell(23, 10, "Equip2", 1, 0)
    pdf.cell(23, 10, "Interfície2", 1, 0)
    pdf.cell(23, 10, "IP2", 1, 1)
    l=0
    while l< len(term):
        pdf.cell(13)
        if len(xxs)!=0:
            if l==0:
                pdf.cell(23, 10, xxs[l], 1, 0)
            else:
                pdf.cell(23, 10, xxs[int(l/2)], 1, 0)
        pdf.cell(23, 10, term[l], 1, 0)
        pdf.cell(23, 10, intf[l], 1, 0)
        pdf.cell(23, 10, ips[l], 1, 0)
        if(l+1!=len(term)):
            pdf.cell(23, 10, term[l+1], 1, 0)
            pdf.cell(23, 10, intf[l+1], 1, 0)
            pdf.cell(23, 10, ips[l+1], 1, 1)
        
        l=l+2
    pdf.output("Ex2.pdf")

else:
    # INDEX
    pdf.cell(0, 10, 'ÍNDEX', 0, 1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.- Introducció............................................................................................................................................4', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.1.- Descripció........................................................................................................................4', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.2.- Objectius..........................................................................................................................4', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.3.- Descripció General de les infraestructures...................................................................4', 0, 1)

    # 2
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '2.- Configuració dels dispositius................................................................................................................4', 0, 1)
    pdf.cell(20)
    pdf.set_font('Times','B',12)
    ii=1
    npag=4
    for k in dd['nodes']:
        #if(ii==9):
        #    pdf.add_page()
        #else:
        #    pdf.ln(4)
        pdf.cell(10)
        if(ii==2):
            npag=5
        elif(ii==3):
            npag=7
        elif(ii==4):
            npag=8
        elif(ii==5):
            npag=10
        elif(ii==7):
            npag=npag+1
        pdf.cell(0, 10, '2.'+ str(ii) +'.- '+ k['label'] +'............................................................................................................... '+ str(npag),0,1,'L',False)
        cc=1
        if "Building configuration..." in k['configuration']:
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0,0,'2.'+ str(ii) +'.'+ str(cc) +'.- Configuració criptogràfica del dispositiu............................................................................ '+ str(npag),0,1,'L',False)
            cc=cc+1
        if(npag==8):
            npag=npag+1
        pdf.ln(4)
        pdf.cell(20)
        pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Interfícies........................................................................................................................... '+ str(npag),0,1,'L',False)
        cc=cc+1
        if "Building configuration..." in k['configuration']:
            if(npag==5):
                npag=npag+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració dels protocols d`enrutament......................................................................... '+ str(npag),0,1,'L',False)
            cc=cc+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració de Llistes de Control d`Accés....................................................................... '+ str(npag),0,1,'L',False)
            cc=cc+1
            pdf.ln(4)
            pdf.cell(20)
            pdf.cell(0, 10, '2.'+ str(ii) +'.'+ str(cc) +'.- Configuració de Banners .................................................................................................. '+ str(npag),0,1,'L',False)
            cc=cc+1
        ii=ii+1
    
    pdf.ln(4)
    pdf.cell(0, 10, '3.- Interfícies....................................................................................................................................... '+ str(npag),0,1,'L',False)
    cont = 0
    indexList = list()
    parse = CiscoConfParse('Ex3')
    for intf_obj in parse.find_objects(r'nodes'):
        for c1_obj in intf_obj.children:
            for c2_obj in c1_obj.children:
                if "label:" in c2_obj.text:
                    indexList.append(str(c2_obj.text).replace("label:", ""))
    # Introduction
    pdf.add_npage()
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 10, '1.- Introducció', 0, 1)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.1- Descripció', 0, 1)
    pdf.set_font('Times', '', 12)

    parse = CiscoConfParse('Ex3')
    for intf_obj in parse.find_objects(r'lab'):
        for c1_obj in intf_obj.children:
            if "title:" in c1_obj.text:
                titul = str(c1_obj.text).replace("title:", "")

    pdf.multi_cell(0, 10, 'El present document descriu la topologia realitzada amb la configuració ' +
                titul+' a la \nempresa TecnoCampus.', 0, 1, 'L')

    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 10, '1.2- Objectius', 0, 1)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 10, "El objectiu d'aquest document és la de formalitzar el traspàs d'informació al equip tècnic \nresponsable del manteniment de les infraestructures instal·lades. Aquesta informació fa \nreferencia al disseny, instal·lació i configuració dels dispositius i sistemes afectats per la implementació.", 0, 1, 'L')
    pdf.cell(0, 10, 'La present documentació inclou:', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150) +
            ' Descripció general de les infraestructures instal·lades', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+' Configuració de les interfícies de xarxa', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150) +
            ' Configuració de les polítiques per les connexions VPN', 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+" Configuració dels protocols d'enrutament", 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+" Configuració de les llistes de control d'accés", 0, 1)
    pdf.cell(10)
    pdf.cell(0, 10, chr(150)+' Configuració dels banners', 0, 1)

    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 10, '1.3.- Descripció General de les infraestructures', 0, 1)
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, 'Actualment la topologia té la següent distribució: ', 0, 1)
    pdf.ln(10)
    contId = 0
    parse = CiscoConfParse('Ex3')
    for intf_obj in parse.find_objects(r'nodes'):
        for c1_obj in intf_obj.children:
            if "id:" in c1_obj.text:
                contId = contId+1
    contLinks = 0
    parse = CiscoConfParse('Ex3')
    for intf_obj in parse.find_objects(r'links'):
        for c1_obj in intf_obj.children:
            if "id:" in c1_obj.text:
                contLinks=contLinks+1
    pdf.cell(10)
    pdf.cell(0, 5, 'En aquesta topologia tenim '+str(contId) +
            ' equips, connectats a través de '+str(contLinks)+' links', 0, 1, 'L')
    
    ips= list()
    intf= list()
    term=list()
    xxs= list()
    idx=1
    for klk in dd['nodes']:
        pdf.set_font('Times', 'B', 12)
        pdf.ln(8)
        pdf.cell(0, 0, '2.'+str(idx)+'.- '+ klk['label'], 0, 1)
        pdf.ln(6)
        ms=1
        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', '', 10)
            #Date and Time
            xx='UTC'
            trobat=re.search(xx, klk['configuration'])
            ini=trobat.start()
            fin=trobat.end()
            time=klk['configuration'][(ini-9):(fin)]
            date=klk['configuration'][(fin+5):(fin+16)]

            pdf.cell(0, 10, 'El darrer canvi de la configuració va ser el '+ date +' a les '+ time, 0, 1)
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració criptogràfica del dispositiu', 0, 1)
            pdf.set_font('Times', '', 12)
            pdf.ln(7)
            if "crypto" in klk['configuration']:
                pdf.cell(0, 10, 'El dispositiu té la següent configuració de crypto:', 0, 1)
                pdf.ln(4)
                pdf.cell(20)
                xx='set peer'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                ip=klk['configuration'][(fin+1):(fin+9)]
                pdf.cell(0, 10, '-    Conexió amb '+ ip +':', 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                xx='isakmp policy'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                numero=klk['configuration'][(fin+1):(fin+3)]
                pdf.cell(0, 10, 'o   Política de regles número '+ numero +':', 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='encr aes'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                ee=klk['configuration'][(fin-3):(fin+4)]
                pdf.cell(0, 0, '·    Encriptació '+ ee, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='authentication'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                auth=klk['configuration'][(fin+1):(fin+10)]
                pdf.cell(0, 10, '·    Autenticació '+ auth, 0, 1)
                pdf.ln(2)
                pdf.cell(40)
                xx='group'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                group=klk['configuration'][(fin+1)]
                pdf.cell(0, 10, '·    Diffie-Helmann grup '+ group, 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                xx='isakmp key'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                key=klk['configuration'][(fin+1):(fin+8)]
                pdf.cell(0, 10, 'o   Contrasenya ISAKMP: '+ key, 0, 1)
                pdf.ln(6)
                pdf.cell(30)
                pdf.cell(0, 10, 'o   Configuració VPN:', 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='ipsec transform-set'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                tt=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 10, '·    Conjunt de transformació '+ tt, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                enc=klk['configuration'][(fin+5):(fin+12)]
                pdf.cell(0, 10, '·    Configuració Encriptació ESP: '+ enc, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                sgn=klk['configuration'][(fin+13):(fin+25)]
                pdf.cell(0, 10, '·    Configuració Signatura ESP: '+ sgn, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                mod=klk['configuration'][(fin+32):(fin+38)]
                pdf.cell(0, 10, '·    Mode '+ mod, 0, 1)
                pdf.ln(6)
                pdf.cell(40)
                xx='match address'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                acl=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 10, '·    ACL número '+ acl, 0, 1)
            else:
                pdf.cell(0, 10, 'El dispositiu no té configuració de crypto', 0, 1)
            
            ms=ms+1

        pdf.set_font('Times', 'B', 12)
        if "Building configuration..." in klk['configuration']:
            pdf.ln(4)
        pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Interfícies', 0, 1)
        pdf.set_font('Times', '', 11)
        pdf.cell(0, 10, 'Les interfícies i la seva configuració és:', 0, 1)
        pdf.ln(4)

        for q in klk['interfaces']:
            pdf.cell(25)
            xx=q['label']
            ff=re.search(xx, klk['configuration'])
            ipAddr=''
            if ff!=None:
                fin=ff.end()
                if "no" not in klk['configuration'][(fin):(fin+5)]:
                    ipAddr=klk['configuration'][(fin+13):(fin+38)]
                    xx='255.255'
                    ff=re.search(xx, ipAddr)
                    if ff != None:
                        s=ff.start()
                        term.append(klk['label'])
                        intf.append(q['id'])
                        ips.append(ipAddr[:s])

                        ipAddr=': '+ipAddr[:s]+'('+ipAddr[s:len(ipAddr)]+')'
                if 'alpine' in klk['node_definition']:
                    term.append(klk['label'])
                    intf.append(q['id'])

                    ipAddr=' (DG: '+ipAddr[13:]+')'
                    xx='ip addr add'
                    ff=re.search(xx, klk['configuration'])
                    fin=ff.end()
                    ips.append(klk['configuration'][(fin+1):(fin+12)])

                    ipAddr='. Configuració IP: '+klk['configuration'][(fin+1):(fin+15)]+ ipAddr
            
            pdf.cell(0, 10, '-    Link '+ q['id']+': '+ q['label']+ ipAddr, 0, 1)
            pdf.ln(5)
        ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(5)
            pdf.cell(0, 10, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració dels protocols d enrutament', 0, 1)
            pdf.set_font('Times', '', 11)
            xx='router ospf'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                fin=trobat.end()
            protocol=klk['configuration'][(fin-4):(fin+4)]
            pdf.cell(0, 0, 'El protocol d enrutament utilitzat és '+ protocol.upper() +', amb la següent configuració (xarxes publicades):', 0, 1)
            pdf.ln(4)
            pdf.cell(10)
            xx='area'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                fin=trobat.end()
            area=klk['configuration'][fin+1]
            pdf.cell(0, 10, '-    Àrea '+ area+':', 0, 1)
            xx='network'
            trobat=re.search(xx, klk['configuration'])
            if(trobat!=None):
                s=trobat.end()
            s=s+1
            ntk=""
            while klk['configuration'][s]!='!':
                ntk=ntk+klk['configuration'][s]
                s=s+1
            num=klk['configuration'].count("area")
            ntk=ntk.replace("network", "")
            ntk=ntk.replace("area 0", "")
            while num>0:
                xx=' '
                trobat=re.search(xx, ntk)
                if(trobat!= None):
                    x=trobat.end()
                    if ntk[:x-1] not in xxs:
                        xxs.append(ntk[:x-1])
                    p1=ntk[:x-1]+' màscara invertida '
                    ntk=ntk[x:]
                    ntk=ntk[2:]
                    trobat=re.search(xx, ntk)
                    p2=ntk[:x-1]
                    ntk=ntk[x:]
                    net=p1+p2
                pdf.ln(7)
                pdf.cell(20)
                pdf.cell(0, 0, 'o   Xarxa '+ net, 0, 1)
                num=num-1 
            ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 0, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració de Llistes de Control d Accés', 0, 1)
            pdf.set_font('Times', '', 11)
            pdf.ln(7)
            if "access-list" in klk['configuration']:
                pdf.cell(0, 0, 'El dispositiu té configurada la següent ACL:', 0, 1)
                pdf.ln(7)
                pdf.cell(10)
                xx='access-list'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                acclist=klk['configuration'][(fin+1):(fin+4)]
                pdf.cell(0, 0, '-    Número '+acclist, 0, 1)
                pdf.ln(5)
                pdf.cell(20)
                xx='permit'
                trobat=re.search(xx, klk['configuration'])
                fin=trobat.end()
                permit=klk['configuration'][(fin+1):(fin+3)]
                pdf.cell(0, 10, 'o   PERMIT ('+ permit.upper() +'):', 0, 1)
                pdf.ln(1)
                pdf.cell(30)
                xx='control-plane'
                trobat=re.search(xx, klk['configuration'])
                ini=trobat.start()
                origdest=klk['configuration'][(fin+4):(ini-2)]
                xx=' '
                trobat=re.search(xx, origdest)
                if(trobat!= None):
                    x=trobat.end()
                    origen=origdest[:x-1]+' màscara invertida '+origdest[x:x+9]
                    origdest=origdest[x:]
                    trobat=re.search(xx, klk['configuration'])
                    x=trobat.start()
                    origdest=origdest[x+2:]
                    trobat=re.search(xx, klk['configuration'])
                    x=trobat.start()
                    desti=origdest[:x+3]+' màscara invertida '+origdest[x+3:x+13]
                pdf.cell(0, 10, '·   ORIGEN: '+origen, 0, 1)
                pdf.ln(2)
                pdf.cell(30)
                pdf.cell(0, 10, '·   DESTÍ: '+desti, 0, 1)
            else:
                pdf.cell(0, 10, 'El dispositiu no té configurada cap ACL.', 0, 1)

            ms=ms+1

        if "Building configuration..." in klk['configuration']:
            pdf.set_font('Times', 'B', 12)
            pdf.ln(9)
            pdf.cell(0, 0, '2.'+ str(idx) +'.'+ str(ms) +'.- Configuració de Banners', 0, 1)
            pdf.set_font('Times', '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(7)
            pdf.cell(0, 0, 'El dispositiu té configurats els següent Banners:', 0, 1)
            pdf.ln(7)
            xx='banner'
            trobat=re.search(xx, klk['configuration'])
            fin=trobat.end()
            xx='line con 0'
            trobat=re.search(xx, klk['configuration'])
            ini=trobat.start()
            ban=klk['configuration'][(fin+1):(ini-2)]
            ban="    -    "+ban
            ban=ban.replace("banner", "    -    ")
            ban=ban.replace("^CCC", " ")
            ban=ban.replace("^C", " ")
            pdf.cell(18)
            pdf.multi_cell(170, 8, ban, 0, 'J', False)
            ms=ms+1
        idx=idx+1 
    #3.- 
    pdf.set_font('Times', '', 20)
    pdf.ln(5)
    pdf.cell(18)
    pdf.cell(10, 10, '3.- Interfícies', 0, 1)
    pdf.set_font('Times', '', 10)
    pdf.ln(3)
    pdf.cell(18)
    pdf.cell(0, 10, 'La configuració de les interfícies (links) d interconnexió entre equips és:', 0, 1)
    pdf.ln(8)
    for q in dd['links']:
        pdf.cell(25)
        pdf.set_font('Times', 'B', 11)
        ids='1'+q['id'][1]
        pdf.cell(0, 0, '-    Link '+ids, 0, 1)
        pdf.set_font('Times', '', 11)
        pdf.cell(44)
        lab1=''
        lab2=''
        for n in dd['nodes']:
            if q['n1'] == n['id']:
                lab1=n['label']
            if q['n2'] == n['id']:
                lab2=n['label']

        pdf.cell(0, 0, ': conecta '+ q['i1'] +' ('+ lab1 +')'+' amb '+ q['i2']+' ('+ lab2 +')', 0, 1)
        pdf.ln(5)

    pdf.ln(3)
    pdf.cell(18)
    pdf.cell(0, 0, 'El resum de les adreces IP de les interfícies és:', 0, 1)
    #TABLA
    pdf.ln(5)
    pdf.cell(13)
    if len(xxs)!=0:
        pdf.cell(23, 10, "Xarxa", 1, 0)
    pdf.cell(23, 10, "Equip1", 1, 0)
    pdf.cell(23, 10, "Interfície1", 1, 0)
    pdf.cell(23, 10, "IP1", 1, 0)
    pdf.cell(23, 10, "Equip2", 1, 0)
    pdf.cell(23, 10, "Interfície2", 1, 0)
    pdf.cell(23, 10, "IP2", 1, 1)
    l=0
    while l< len(term):
        pdf.cell(13)
        if len(xxs)!=0:
            if l==0:
                pdf.cell(23, 10, xxs[l], 1, 0)
            else:
                pdf.cell(23, 10, xxs[int(l/2)], 1, 0)
        pdf.cell(23, 10, term[l], 1, 0)
        pdf.cell(23, 10, intf[l], 1, 0)
        pdf.cell(23, 10, ips[l], 1, 0)
        if(l+1!=len(term)):
            pdf.cell(23, 10, term[l+1], 1, 0)
            pdf.cell(23, 10, intf[l+1], 1, 0)
            pdf.cell(23, 10, ips[l+1], 1, 1)
        l=l+2
    pdf.output("Ex3.pdf")
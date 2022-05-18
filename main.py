from bs4 import BeautifulSoup as bs

import requests
import glob

mot1 = "couper"
mot2 = "pain"
relation = "r_patient"


filepath = glob.glob("**/"+mot1+mot2+".txt", recursive=True)
if (len(filepath) )>0:
    print(filepath)
    print ("fichier trouve")
    f = open(mot1+mot2+".txt", "r+", encoding='utf8')
else:
    print("fichier doesn't exist")
    fic = mot1+mot2+".txt"
    f = open(fic, "w+", encoding='utf8')

    f = open(fic, "r+", encoding='utf8')
    url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + mot1 + "&rel="
    response = requests.get(url)
    if response.status_code != 200: print("Erreur dans l'ortographe du mot 1")
    html = response.content
    soup = bs(html, "lxml")

    f.write(soup.getText())

    url2 = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + mot2 + "&rel="
    response2 = requests.get(url2)
    if response2.status_code != 200: print("Erreur dans l'ortographe du mot 2")
    html2 = response2.content
    soup2 = bs(html2, "lxml")

    f.write(soup2.getText())


lignes = f.readlines()



ida = ""
idr = ""
idb = ""
c = 0

def getidnode(lignes, mot):
    for ligne in lignes:
        if 'e;' in ligne:
            e = ligne.split(';')
            if (str(e[2]) == ("\'""" + mot + "\'""")):
                id = e[1]
                return id

def getmotnode(lignes, id):
    for ligne in lignes:
        if 'e;' in ligne:
            e = ligne.split(';')
            if (str(e[1]) ==  str(id)):
                mot = e[2]
                return mot
#print("la fonction getmotnode"+ getmotnode(lignes,48510) )
def getidrelation(lignes,mot):
    for ligne in lignes:
        if 'rt;' in ligne:
            rt = ligne.split(';')
            if (str(rt[2]) == ("\'""" + mot + "\'""")):
                id = rt[1]
                return id
def getmotrelation(lignes, id):
    for ligne in lignes:
        if 'rt;' in ligne:
            rt = ligne.split(';')
            if (str(rt[1]) ==  str(id)):
                mot = rt[2]
                return mot

#Retrouver les identifiants
idb = getidnode(lignes, mot1)
ida = getidnode(lignes, mot2)
idr = getidrelation(lignes, relation)

print("l'identifiant du premier mot"+mot1+"est"+idb)
print("l'identifiant du second mot"+mot2+"est"+ida)
print("l'identifiant de la relation"+relation+"est"+idr)

listeaded=["r_associated", "r_isa","r_agent-1", "r_associated", "r_lieu", "r_sentiment", "r_patient", "r_instr", "r_associated", "r_lieu"]
listebded=["r_patient","r_agent-1", "r_instr", "r_agent-1", "r_domain", "r_family", "r_instr", "r_patient", "r_has_part", "r_lieu"]

listeaind =["r_hypo", "r_syn", "r_locution", "r_family", "r_successeur-time", "r_syn","r_locution", "r_make_use_of", 'r_lemma']
listebind =["r_agent-1", "r_patient","r_patient", "r_patient", "r_patient", "r_agent-1","r_agent-1", "r_agent-1", 'r_lieu']



#rechercher l'inférence
trouve =False
for ligne in lignes:
    if 'r;' in ligne:
        r = ligne.split(';')
        if (r[4] == idr):
            if (r[2] == idb):
                if (r[3] == ida):
                  print("relation existante!")
                  trouve = True
                  for j in range(len(lignes) - 1):
                      if 'r;' in lignes[j]:
                          for m in range(len(lignes) - 2):
                              if 'r;' in lignes[m]:
                                  elementc = lignes[m].split(';')
                                  elementb = lignes[j].split(';')
                                  if (r[2] == elementb[2] and elementc[2] == elementb[3] and r[3] == elementc[3]
                                          and r[4] == elementc[4] and str(r[5])>str(0) and str(elementc[5])> str(0) and str(elementb[5])>str(0)
                                        and r[2]!= r[3] and elementc[2]!=elementc[3]and elementb[2]!=elementb[3]):
                                      for q in range(len(listeaind)):
                                          if (str(elementb[4]) == str(getidrelation(lignes, listeaind[q]))):
                                              if (str(elementc[4]) == str(getidrelation(lignes, listebind[q]))):
                                                  print("oui par induction des elements car" + getmotnode(lignes,
                                                                                                          elementb[
                                                                                                              2]) + getmotrelation(
                                                      lignes, elementb[
                                                          4]) + getmotnode(lignes, elementb[3]) + "et" +
                                                        getmotnode(lignes, elementc[2]) + getmotrelation(lignes,
                                                                                                         elementc[
                                                                                                             4]) + getmotnode(
                                                      lignes, elementc[3]))
                                      for p in range(len(listeaded)):
                                          if (str(elementb[4]) == str(getidrelation(lignes, listeaded[p]))):

                                              if (str(elementc[4]) == str(getidrelation(lignes, listebded[p]))):
                                                  #print("node a"+ elementb[2]+"relation"+ elementb[4]+ "nodeb"+ elementb[3] + "et"+ "node a"+elementc[2]+"relation"+ elementc[4] + "nodeb"+elementc[3])

                                                  print("oui par deduction des elements car" + getmotnode(lignes,
                                                                                                          elementb[
                                                                                                              2]) + getmotrelation(
                                                      lignes, elementb[
                                                          4]) + getmotnode(lignes, elementb[3]) + "et" +
                                                        getmotnode(lignes, elementc[2]) + getmotrelation(lignes,
                                                                                                         elementc[
                                                                                                             4]) + getmotnode(
                                                      lignes, elementc[3]))
                                      if (r[4] == elementb[4]):



                                          print("oui par transitivite des elements car" + getmotnode(lignes, elementb[
                                              2]) + getmotrelation(lignes, elementb[
                                              4]) + getmotnode(lignes, elementb[3]) + "et" +
                                                getmotnode(lignes, elementc[2]) + getmotrelation(lignes,
                                                                                                 elementc[
                                                                                                     4]) + getmotnode(
                                              lignes, elementc[3]))




f.close()


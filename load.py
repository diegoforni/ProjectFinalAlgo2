#EL PATH ES UN INPUT Y VA CON DOBLE BARRA INVERTIDA

import PyPDF2
import trie
import pdfFunctions
import pickle
import os    
import cleanText

#crea una lista con los nombres de los pdfs, cada uno le va a tener que cambiar el path
def namesPDFs(pathPDFs):
    listNamesPDFs = []
    listNamesPDFs = os.listdir(pathPDFs) #hay que cambiar el path por un imput
    return listNamesPDFs

#convierte los pdfs a texto y los guarda en una lista
def convertPDFs(listPDFs, base_path):#hay que pasarle el path de la carpeta donde estan los pdfs
    # Inicializamos una lista vacía para almacenar los textos extraídos de los PDFs
    listTexts = []
    
    # Iteramos sobre cada PDF en la lista de PDFs
    for i in range(len(listPDFs)):
        # Construimos el path completo al archivo PDF
        pdf_path = base_path +"\\"+ listPDFs[i]
        
        # Abrimos el archivo PDF en modo lectura binaria
        with open(pdf_path, 'rb') as file:
            # Creamos un objeto PdfReader para leer el archivo PDF
            reader = PyPDF2.PdfReader(file)
            
            # Inicializamos una cadena vacía para almacenar el texto extraído
            text = ''
            
            # Iteramos sobre cada página en el archivo PDF
            for page in reader.pages:
                # Extraemos el texto de la página y lo agregamos a la cadena de texto
                text += page.extract_text()
            
            # Agregamos el texto extraído a la lista de textos
            listTexts.append(text)
    
    # Devolvemos la lista de textos extraídos
    return listTexts

def loadInTrie(pathPDFs): #esta es la funcion que hay que llamar para cargar los archivos al trie
    
    listPDFs = namesPDFs(pathPDFs)  #lista de nombres de los pdfs
    listTexts = convertPDFs(listPDFs,pathPDFs) #lista de textos de los pdfs como strings
    #limpio todos los textos
    for i in range(len(listPDFs)):
        listTexts[i] = cleanText.cleanText(listTexts[i])

    #creo una lista con los IDs de los pdfs
    idToPdf, pdfToID = pdfFunctions.createPdfID(listPDFs)
    ids = []
    for i in range(len(listPDFs)):
        ids.append(pdfFunctions.getIDFromPdf(listPDFs[i],pdfToID))
        
    #inserto en el trie
    t = trie.Trie()
    for i in range(len(listTexts)):    
        trie.insertMainTrie(t,listTexts[i],ids[i])
    return t

def saveTrie(trie): #esta funcion guarda el trie en un archivo
    with open("trieDocument", "wb") as f:
        pickle.dump(trie, f)
        
def loadTrie(): #esta funcion carga el trie desde un archivo
    with open("trieDocument", "rb") as f:
        trie = pickle.load(f)
    return trie   
      
#EL PATH ES UN INPUT
path = '/Users/Rocio/Documents/GitHub/finalProjectAlgo2/pdfs'

#GUARDO LOS PDFS EN EL TRIE
T = loadInTrie(path)

#GUARDO EL TRIE EN UN ARCHIVO
saveTrie(T)

#ME TRAIGO EL TRIE DESDE EL ARCHIVO Y LO GUARDO EN UNA VARIABLE
R = loadTrie()

#trie.printTrie(R.root,1)

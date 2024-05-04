import os
import PyPDF2
import PySimpleGUI as sg
import fitz  # Importa la biblioteca PyMuPDF

def buscar_texto_en_pdf(pdf_file, texto):
    texto_encontrado = False
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if texto in page_text:
                texto_encontrado = True
                break
    return texto_encontrado

# Definir el diseño de la interfaz gráfica
layout = [
    [sg.Text('Ingrese el texto a buscar:'), sg.InputText(key='-TEXTO-')],
    [sg.Text('Seleccione un archivo PDF:'), sg.InputText(key='-ARCHIVO-'), sg.FileBrowse()],
    [sg.Button('Buscar'), sg.Button('Cerrar')]
]

window = sg.Window('Buscador de Texto en PDF', layout, icon='icono.ico')  # Reemplaza 'icono.ico' con la ruta de tu archivo de icono

# Event Loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cerrar'):
        break
    if event == 'Buscar':
        texto_a_buscar = values['-TEXTO-']
        pdf_file = values['-ARCHIVO-']
        if pdf_file:
            pdf_file_name = os.path.basename(pdf_file)
            if buscar_texto_en_pdf(pdf_file, texto_a_buscar):
                sg.popup('Abriendo PDF...', auto_close=True, auto_close_duration=2)
                doc = fitz.open(pdf_file)
                pdf_viewer = sg.Window(pdf_file_name, [[sg.Image(data=page.get_pixmap()) for page in doc.pages]])
                pdf_viewer.read(close=True)
                doc.close()
            else:
                sg.popup(f"El texto '{texto_a_buscar}' no fue encontrado en el archivo '{pdf_file_name}'.")

window.close()

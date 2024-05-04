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
    return texto_encontrado, page_num, texto

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
            texto_encontrado, page_num, texto = buscar_texto_en_pdf(pdf_file, texto_a_buscar)
            if texto_encontrado:
                sg.popup(f"El texto '{texto}' fue encontrado en el archivo:", title="Resultado de la búsqueda", custom_text=f'{pdf_file_name}', text_color='blue', font=('Helvetica', 12), keep_on_top=True)

                # Abrir el PDF y resaltar la palabra buscada
                doc = fitz.open(pdf_file)
                page = doc[page_num]
                text_instances = page.search_for(texto)
                for inst in text_instances:
                    page.add_highlight_annot(inst)

                # Guardar el PDF con los cambios
                pdf_output_file = f'{os.path.splitext(pdf_file)[0]}_marcado.pdf'
                doc.save(pdf_output_file)
                doc.close()

                # Abrir el PDF marcado
                os.startfile(pdf_output_file)
            else:
                sg.popup(f"El texto '{texto_a_buscar}' no fue encontrado en el archivo '{pdf_file_name}'.")

window.close()

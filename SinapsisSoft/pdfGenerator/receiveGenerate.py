import pdfkit
import jinja2

def crearPDF():
    my_name = "SinapsisSoft"
    my_address = "Calle 123"
    my_city = "Bogota"
    my_state = "Colombia"
    my_zip = "12345"
    my_phone = "123-456-7890"

    context = {'my_name': my_name,'my_address': my_address}

    templateLoader = jinja2.FileSystemLoader('./')
    templateEnv=jinja2.Environment(loader=templateLoader)

    html_template= 'SinapsisSoft/pdfGenerator/template.html'
    template = templateEnv.get_template(html_template)
    outputText=template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    output_pdf = 'RecibodePagoSInapsis'+my_zip+'.pdf'
    pdfkit.from_string(outputText, output_pdf, configuration=config, css='SinapsisSoft/pdfGenerator/styles.css')

if __name__ == '__main__':
    crearPDF()
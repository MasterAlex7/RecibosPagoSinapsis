import pdfkit
import jinja2

def crearPDF():
    client_name = "Sinapsis Software"
    num_contrato = "365098"
    today_date = "12/12/2020"
    id_recibo = "12"
    mensualidad_num = "9"
    abono = "2000"
    saldo_ant = "3000"
    descuento = "0"
    saldo_actual = "1000"
    nom_acreedor = "Sinapsis Software"

    context = {'client_name': client_name, 'num_contrato': num_contrato, 'today_date': today_date,
            'id_recibo': id_recibo, 'mensualidad_num': mensualidad_num, 'abono': abono, 
            'saldo_ant': saldo_ant, 'descuento': descuento, 'saldo_actual': saldo_actual,'nom_acreedor':nom_acreedor}

    templateLoader = jinja2.FileSystemLoader('./')
    templateEnv=jinja2.Environment(loader=templateLoader)

    html_template= 'SinapsisSoft/pdfGenerator/template.html'
    template = templateEnv.get_template(html_template)
    outputText=template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    output_pdf = 'RecibodePagoSInapsis'+id_recibo+'.pdf'
    pdfkit.from_string(outputText, output_pdf, configuration=config, css='SinapsisSoft/pdfGenerator/styles.css')

if __name__ == '__main__':
    crearPDF()
import pdfkit
import jinja2

def crearPDF(response,tipoRecibo):
    client_name = response[0]['nombre_cliente']
    num_contrato = response[0]['num_contrato']
    today_date = response[0]['fecha']
    id_recibo = response[0]['idPago']
    mensualidad_num = response[0]['mensualidad_recibida']
    abono = response[0]['abono']
    saldo_ant = response[0]['saldo_anterior']
    descuento = response[0]['descuento']
    saldo_actual = response[0]['saldo_actual']
    if tipoRecibo == 'Sinapsis':
        img = "https://raw.githubusercontent.com/MasterAlex7/assetsProyects/main/assetsSinapsis/LogoSinapsis.jpeg"
    else:
        img = "https://raw.githubusercontent.com/MasterAlex7/assetsProyects/main/assetsSinapsis/LogoSpeakers.jpeg"

    context = {'imgRecibo': img,'client_name': client_name, 'num_contrato': num_contrato, 'today_date': today_date,
            'id_recibo': id_recibo, 'mensualidad_num': mensualidad_num, 'abono': abono, 
            'saldo_ant': saldo_ant, 'descuento': descuento, 'saldo_actual': saldo_actual}

    templateLoader = jinja2.FileSystemLoader('./')
    templateEnv=jinja2.Environment(loader=templateLoader)

    html_template= 'SinapsisSoft/pdfGenerator/template.html'
    template = templateEnv.get_template(html_template)
    outputText=template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    output_pdf = 'RecibodePagoSInapsis'+str(client_name)+str(id_recibo)+'.pdf'
    pdfkit.from_string(outputText, output_pdf, configuration=config, css='SinapsisSoft/pdfGenerator/styles.css')

if __name__ == '__main__':
    crearPDF()
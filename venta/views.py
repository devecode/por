from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import requires_csrf_token
import json
from django.core import serializers
from django.contrib.auth.models import User
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .models import VentaGeneral, VentaProducto
from inv import models as modelsInv
from cliente import models as modelsCliente

from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table,Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, elevenSeventeen, inch 
from io import BytesIO
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import mm
from pos import settings


class VentaG(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = VentaGeneral
    permission_required='venta.view_ventageneral'
    template_name = 'venta/ventageneral_list.html'
    context_object_name = 'obj'


class VentaGeneralList(LoginRequiredMixin, generic.ListView):
    login_url = "contabilidad:login"
    model = VentaGeneral
    permission_required='venta.view_ventageneral'
    template_name = 'venta/venta_new.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = modelsInv.Producto.objects.all
        clientes = modelsCliente.Cliente.objects.all
        context['productos'] = productos
        context['clientes'] = clientes
        return context


def CodigoBarrasSearch(request, bar_id):
    response = modelsInv.Producto.objects.filter(codigo_barra=bar_id)
    if response:
        data = serializers.serialize('json', response)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponseBadRequest()

@requires_csrf_token
def apliacionVenta(request):
    if request.method == 'POST':
        post = json.loads(request.body)
        print(request.body)
        try:
            import datetime
            now = datetime.datetime.now()
            user = User.objects.get(username=post["user"])
            metodo = ''
            if float(post["efectivo"]) != 0 and float(post["tarjeta"]) != 0:
                metodo = 'MIXTO'
            elif (float(post["efectivo"]) == 0):
                metodo = 'TARJETA'
            else:
                metodo = 'EFECTIVO'
            try:
                clienteSearch = modelsCliente.Cliente.objects.get(id=int(post["cliente"]))
                venta = VentaGeneral(metodo_pago=metodo,vendedor=user, total_efectivo=float(post["efectivo"]), total_tarjeta=float(post["tarjeta"]))
                venta.cliente = clienteSearch
                venta.save()
            except:
               
                return HttpResponseBadRequest()
               # venta = VentaGeneral(metodo_pago=metodo,vendedor=user, total_efectivo=float(post["efectivo"]), total_tarjeta=float(post["tarjeta"]))

        except Exception as inst:
            return HttpResponseBadRequest(inst)

        try:
            for product in post["productos"]:
                #print(product["producto"])
                prod = modelsInv.Producto.objects.get(codigo_barra=product["producto"])
                #borrar el venta.pk y poner venta para que jale
                ventaProd = VentaProducto(cantidad=float(product["cantidad"]), producto=prod, num_venta=venta)
                ventaProd.save()
        except :
            #Para borra el registro si algo sale mal
            VentaGeneral.objects.filter(id=venta.pk).delete()

            #Error, ocurrió un problema
            return HttpResponseBadRequest()
            #return HttpResponse("400", content_type="text/plain")

        #Venta correctamente registrada
        return HttpResponse(venta.pk, content_type="text/plain")
    else:
        return HttpResponseBadRequest()

def get_ticket(request, pk):
    
    venta = VentaGeneral.objects.get(id=pk)
    vendedor = venta.vendedor.username
    productos = VentaProducto.objects.filter(num_venta=venta.pk)

    response = HttpResponse(content_type='application/pdf')
    name = 'Ticket Venta' + pk  
    pdf_name = name +'.pdf'  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    

    #1 pulgada = 2.54 cm
    #5.5cm = 2.16535 pulgadas
    #2.16535 pulgadas + 72DPI = 160.2359px
    #El título + fecha + vendedor llegan hasta los 110px y cada artículo mide 17px aproximadamente
    #por lo que por cada producto se deberá aumentar ese tamaño para que el ticket salga adecuadamente
    alto = 110
    ancho = 146
    pagesize = (ancho,alto)


    doc = SimpleDocTemplate(buff, 
                            pagesize=pagesize,
                            rightMargin=0,
                            leftMargin=0,
                            topMargin=0,
                            bottomMargin=5,
                            )
    

    art = []
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='Titulo_CENTER',
                                      parent=styles['Normal'],
                                      fontName='Helvetica',
                                      wordWrap='LTR',
                                      alignment=TA_CENTER,
                                      leading = 6,
                                      fontSize=12,
                                      ))

    styles.add(ParagraphStyle(name='Texto_CENTER',
                                      parent=styles['Normal'],
                                      fontName='Helvetica',
                                      wordWrap='LTR',
                                      alignment=TA_CENTER,
                                      leading = 6,
                                      fontSize=8,
                                      ))
    
    styles.add(ParagraphStyle(name='Texto_CENTERR',
                                      parent=styles['Normal'],
                                      fontName='Helvetica',
                                      wordWrap='LTR',
                                      alignment=TA_CENTER,
                                      fontSize=5,
                                      leading = 6,
                                      justifyBreaks = 1,
                                      ))

    styles.add(ParagraphStyle(name='Desglose_derecha',
                                      parent=styles['Normal'],
                                      fontName='Helvetica',
                                      wordWrap='LTR',
                                      alignment=TA_RIGHT,
                                      fontSize=5,
                                      rightIndent=9,
                                      leading = 6,
                                      justifyBreaks = 1,
                                      ))
    styles.add(ParagraphStyle(name='Desglose_izquierda',
                                      parent=styles['Normal'],
                                      fontName='Helvetica',
                                      wordWrap='LTR',
                                      alignment=TA_LEFT,
                                      fontSize=5,
                                      rightIndent=9,
                                      leading = 6,
                                      justifyBreaks = 1,
                                      ))

    
    header = Paragraph('', styles['Heading1'])
    art.append(header)
    art.append(header)
    imagen = Image(settings.PATH_MEDIA+'FS.jpg')
    imagen.drawHeight = 0.5*inch
    imagen.drawWidth = 0.6*inch
    imagen.hAlign='CENTER'
    art.append(imagen)
    header = Paragraph('', styles['Heading1'])
    art.append(header)
    art.append(header)

    header = Paragraph('DIRECCIÓN: XXX XXX #XXX, COL. CENTRO TICKET: #'+ pk + '\n', styles['Desglose_izquierda'])
    art.append(header)
    header = Paragraph('TELÉFONO: XXX XXX XXX '+ '' + '\n', styles['Desglose_izquierda'])
    art.append(header)
    header = Paragraph('****************************************************************'+ '' + '\n', styles['Desglose_izquierda'])
    art.append(header)
    header = Paragraph('ANTENDIÓ: '+ vendedor + '\n', styles['Desglose_izquierda'])
    art.append(header)

    header = Paragraph('FECHA: '+venta.fc.strftime("%d/%m/%Y")+ '\n', styles['Desglose_izquierda'])
    art.append(header)
    header = Paragraph('HORA: '+venta.fc.strftime("%H:%M")+ '\n', styles['Desglose_izquierda'])
    art.append(header)
    header = Paragraph('****************************************************************'+ '' + '\n', styles['Desglose_izquierda'])
    art.append(header)
    


    headings = ('CANT','ARTÍCULO','PRECIO','IMPORTE')
    alto += 25
    allfields = [] 
    aux = []
    for p in productos:
        
        aux.append(p.cantidad)
        produc = p.producto.nombre
        texto = ''
        cont=0
        for letra in list(produc):
            texto += letra
            cont+=1
            if cont%15==0:
                texto += '\n'
                alto += 13
                cont=0
            

        aux.append(texto)
        aux.append(str(format(p.venta,".2f")))
        aux.append(str(format(p.importe,".2f")))
        allfields.append(aux)
        aux = []
        alto += 25
   
    gris = colors.Color( 0, 0, 0, alpha=0.05)
    
    tProductos = Table([headings] + allfields ,hAlign='CENTER')
    tProductos.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('LINEBELOW', (-1, -1), (0, 0), 2, colors.white ),
            ('BOX', (0,0), (6,-2), 0.40, colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 5),       
            ('ALIGN',(2,1),(20,20),'CENTER'),
            ('VALIGN',(2,1),(20,20),'MIDDLE'),     
            ('ALIGN',(0,0),(0,20),'CENTER'),
            ('VALIGN',(0,0),(0,20),'MIDDLE'),
            #('BACKGROUND', (2, 1), (20, 20), gris), #Este pone un fondo gris a los encabezados

        ]
    ))
    art.append(tProductos)

    

    #Representando el totales en forma de tabla (más difíciles de manipular)
    '''
    alto += 120
    allfields = [['Subtotal',venta.sub_total],['Descuento',venta.descuento],['IVA',format((venta.total/29)*4,".1f")],
                ['Efectivo',format(venta.total_efectivo,".2f")],
                ['Tarjeta',format(venta.total_tarjeta,".2f")],
                ['Total',format(venta.total,".1f")]
                 ] 
                
               
    gris = colors.Color( 0, 0, 0, alpha=0.05)
                
    tTotales = Table(allfields,hAlign='RIGHT')
    tTotales.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('LINEBELOW', (-1, -1), (0, 0), 2, colors.white ),
            ('BOX', (0,0), (6,-2), 0.40, colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 5),   

            #('BACKGROUND', (0, 0), (4, 0), gris), #Este pone un fondo gris a los encabezados

        ]
    ))
    tTotales.alignment = TA_RIGHT
    art.append(tTotales)
    '''



    #Esta es una forma de presentarlos
    alto += 53
    header = Paragraph('=========================================='+ '' + '\n', styles['Desglose_izquierda'])
    art.append(header)
    header = Paragraph('SUBTOTAL.....$'+ str(format(venta.sub_total,".2f")) + '\n', styles['Desglose_derecha'])
    art.append(header)
    header = Paragraph('DESCUENTO.....$'+ str(format(venta.descuento,".2f")) + '\n', styles['Desglose_derecha'])
    art.append(header)
    header = Paragraph('TOTAL.....$'+ str(format(venta.total,".2f")) + '\n', styles['Desglose_derecha'])
    art.append(header)
    if (venta.total_efectivo > 0 ):
        header = Paragraph('EFECTIVO.....$'+ str(format(venta.total_efectivo,".2f")) + '\n', styles['Desglose_derecha'])
        art.append(header)
        alto += 13
    
    if (venta.total_tarjeta > 0  ):
        header = Paragraph('TARJETA.....$'+ str(format(venta.total_tarjeta,".2f")) + '\n', styles['Desglose_derecha'])
        art.append(header)
        alto += 13
    
    


    doc.pagesize = (ancho,alto)
    doc.build(art)
    response.write(buff.getvalue())
    buff.close()
    return response

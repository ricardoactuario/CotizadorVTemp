from django.shortcuts import render
from .forms import C_Intermediario2, form_CotizadorTAR
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import locale
import os
from .models import TR1
from decimal import Decimal
import base64
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import HttpResponse
# Create your views here.

def CotizadorTemp(request):
    if request.method == 'GET':
        return render(request, 'S_Temporal.html', {
            'form_intermediario2': C_Intermediario2(),
            'form_CotizadorTAR': form_CotizadorTAR(),
        })
    else:
        buffer = BytesIO()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        # Crear un objeto PDF
        pdf = canvas.Canvas(buffer)
        #Estilo de Letra
        pdf.setFont("Helvetica", 9)
        #Trabajo con Variables
        Nom = request.POST.get('Nombre', None)
        In = request.POST.get('Int', None)
        Te = request.POST.get('Tel', None)
        Cor = request.POST.get('Correo', None)
        Identificacion = request.POST.get('Id', None)
        Solicitante = request.POST.get('Sol', None)
        Nacimiento = request.POST.get('Nac', None)
        Genero = request.POST.get('Gen', None)
        Tem = request.POST.get('Temporal', None)
        Suma = request.POST.get('Sum', 0)
        BeneficioA = request.POST.get('Ben2', None)
        BeneficioITP = request.POST.get('Ben1', None)
        TipoR = request.POST.get('Fum', None)
        TipoP = request.POST.get('Temp', None)

        Mails = request.POST.get('Mail', None)
        Cellphones = request.POST.get('Cellphone', None)

        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        image_path = os.path.join('cotizadort', 'static', 'atlanv.png')

        # Agregando contenido al PDF
        pdf.drawString(460, 790, fecha_actual)
            
        pdf.drawImage(image_path, x=50, y=730, width=100, height=40)
            
        pdf.setFont("Helvetica-Bold", 9)
            
        pdf.drawString(240, 740, "OFERTA DE SEGURO TEMPORAL DE VIDA INDIVIDUAL")
            
        pdf.setFont("Helvetica", 9)
            
        pdf.drawString(60, 710, "Presentamos nuestra oferta de Seguro Temporal de Vida Individual, la cual cuenta con las siguientes características:")
        altura_solicitante = 685
        altura_suma = 672
        altura_nacimiento = 659
        altura_edad = 646
        altura_genero = 633
        altura_TipoR = 620
        altura_plazo = 607
        
        altura_cobertura = 582
        altura_fallecimiento = 569
        altura_gastos = 556
        altura_accidental = 543
        altura_ITP = 517
        altura_total = 491
        pdf.drawString(50, altura_solicitante, "SOLICITANTE:")
        pdf.drawString(50, altura_suma, "SUMA ASEGURADA:")
        pdf.drawString(50, altura_nacimiento, "FECHA DE NACIMIENTO:")
        pdf.drawString(50, altura_edad, "EDAD:")
        pdf.drawString(50, altura_genero, "GÉNERO:")
        pdf.drawString(50, altura_TipoR, "TIPO DE RIESGO:")
        pdf.drawString(50, altura_plazo, "PLAZO DEL SEGURO:")
        pdf.drawString(50, altura_cobertura, "COBERTURAS:")
        pdf.drawString(50, altura_fallecimiento, "SUMA ASEGURADA BÁSICA:")
        pdf.drawString(50, altura_gastos, "GASTOS FUNERARIOS:")
        pdf.drawString(50, altura_accidental, "DOBLE INDEMNIZACIÓN POR MUERTE")
        pdf.drawString(50, altura_accidental-13, "ACCIDENTAL:")
        pdf.drawString(50, altura_ITP, "PAGO ANTICIPADO POR INVALIDEZ TOTAL")
        pdf.drawString(50, altura_ITP-13, "Y PERMANENTE:")
        pdf.drawString(50, altura_total, "TOTAL:")
        #REQUISITOS DE ASEGURABILIDAD
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 469, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(230, 473, "REQUISITOS DE ASEGURABILIDAD")
        pdf.setFont("Helvetica", 9)
        #SOLICITANTE
        ancho_texto1 = pdf.stringWidth(Solicitante, "Helvetica-Bold", 9)
        x_centro1 = 280 + (270 - ancho_texto1)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, 685, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x_centro1, altura_solicitante+3, Solicitante)
        pdf.setFont("Helvetica", 9)
        #SUMA ASEGURADA
        SumaAsegurada = "{:,.2f}".format(float(Suma))
        ancho_texto2 = pdf.stringWidth(SumaAsegurada, "Helvetica", 9)
        x_centro2 = 280 + (270 - ancho_texto2)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_suma, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro2, altura_suma+2, "$" + SumaAsegurada)
        #FECHA DE NACIMIENTO
        ancho_texto3 = pdf.stringWidth(Nacimiento, "Helvetica", 9)
        x_centro3 = 280 + (270 - ancho_texto3)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_nacimiento, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro3, altura_nacimiento+3, Nacimiento)
        #EDAD
        fecha_nacimiento = datetime.strptime(Nacimiento, "%Y/%m/%d")
        fechaActual = datetime.now()
        edad = fechaActual.year - fecha_nacimiento.year - ((fechaActual.month, fechaActual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        ancho_texto4 = pdf.stringWidth(str(edad), "Helvetica", 9)
        x_centro4 = 280 + (270 - ancho_texto4)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_edad, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro4-10, altura_edad+2, str(edad) + " años")
        #GÉNERO
        ancho_text1 = pdf.stringWidth(Genero, "Helvetica", 9)
        x_center1 = 280 + (270 - ancho_text1)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_genero, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_center1, altura_genero+3, Genero)
        #TIPO DE RIESGO
        ancho_text2 = pdf.stringWidth(TipoR, "Helvetica", 9)
        x_center2 = 280 + (270 - ancho_text2)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_TipoR, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_center2, altura_TipoR+3, TipoR)
        #PLAZO
        ancho_text3 = pdf.stringWidth(Tem, "Helvetica", 9)
        x_center3 = 280 + (270 - ancho_text3)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_plazo, 270, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_center3, altura_plazo+3, Tem)
        #COBERTURAS
        pdf.setFont("Helvetica-Bold", 9)
        ancho_texto6 = pdf.stringWidth("SUMA ASEGURADA", "Helvetica", 9)
        x_centro6 = 280 + (270 - ancho_texto6)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_cobertura, 120, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro6-76, altura_cobertura+3, "SUMA ASEGURADA:")

        ancho_texto7 = pdf.stringWidth("PRIMA", "Helvetica", 9)
        x_centro7 = 280 + (270 - ancho_texto7)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(450, altura_cobertura, 100, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro7+85, altura_cobertura+3, "PRIMA:")
        #SUMA ASEGURADA BÁSICA
        Suma1 = "{:,.2f}".format(float(Suma))
        pdf.setFont("Helvetica", 9)
        ancho_texto8 = pdf.stringWidth("$"+ Suma1, "Helvetica", 9)
        x_centro8 = 280 + (120 - ancho_texto8)/2
        pdf.drawString(x_centro8, altura_fallecimiento, "$" + Suma1)
        edadP = int(edad)
        SumaP = float(Suma)

        if Tem == '10 años' and Genero == 'Hombre':
            tr_value = TR1.objects.get(Age=edadP).t10
        elif Tem == '15 años' and Genero == 'Hombre':
            tr_value = TR1.objects.get(Age=edadP).t15
        elif Tem == '20 años' and Genero == 'Hombre':
            tr_value = TR1.objects.get(Age=edadP).t20
        elif Tem == '25 años' and Genero == 'Hombre':
            tr_value = TR1.objects.get(Age=edadP).t25
        elif Tem == '30 años' and Genero == 'Hombre':
            tr_value = TR1.objects.get(Age=edadP).t30

        elif Tem == '10 años' and Genero == 'Mujer':
            tr_value = TR1.objects.get(Age=edadP-3).t10
        elif Tem == '15 años' and Genero == 'Mujer':
            tr_value = TR1.objects.get(Age=edadP-3).t15
        elif Tem == '20 años' and Genero == 'Mujer':
            tr_value = TR1.objects.get(Age=edadP-3).t20
        elif Tem == '25 años' and Genero == 'Mujer':
            tr_value = TR1.objects.get(Age=edadP-3).t25
        elif Tem == '30 años' and Genero == 'Mujer':
            tr_value = TR1.objects.get(Age=edadP-3).t30

        tr_decimal = Decimal(tr_value)
        PrimaP = tr_decimal * Decimal(SumaP)
        PrimaPrincipal = PrimaP
        if TipoR == "Fumador":
            PrimaP = float(PrimaP) * 1.15
        else:
            PrimaP = float(PrimaP)
        
        PrimaP1 = "{:,.2f}".format(float(PrimaP))
        ancho_texto9 = pdf.stringWidth("$" + str(PrimaP1), "Helvetica", 9)
        x_centro9 = 450 + (100 - ancho_texto9)/2
        pdf.drawString(x_centro9, altura_fallecimiento, "$" + str(PrimaP1))
        #GASTOS FUNERARIOS
        if (0.10 * SumaP) <= 2000:
            Suma_g = 0.10 * float(SumaP)
        else:
            Suma_g = 2000
        Suma_g1 = "{:,.2f}".format(float(Suma_g))
        ancho_texto10 = pdf.stringWidth("$" + str(Suma_g1), "Helvetica", 9)
        x_centro10 = 280 + (120 - ancho_texto10)/2
        pdf.drawString(x_centro10, altura_gastos, "$" + str(Suma_g1))

        ancho_texto11 = pdf.stringWidth("GRATIS", "Helvetica", 9)
        x_centro11 = 450 + (100 - ancho_texto11)/2
        pdf.drawString(x_centro11, altura_gastos, "GRATIS")
        #DOBLE INDEMNIZACIÓN
        if BeneficioA == 'Si':
            ancho_texto12 = pdf.stringWidth("$" + Suma1, "Helvetica", 9)
            x_centro12 = 280 + (120 - ancho_texto12)/2
            pdf.drawString(x_centro12, altura_accidental, "$" + str(Suma1))
        else:
            ancho_texto12 = pdf.stringWidth("", "Helvetica", 9)
            x_centro12 = 280 + (120 - ancho_texto12)/2
            pdf.drawString(x_centro12, altura_accidental, "")
        PrimaB = 0
        if BeneficioA == 'Si':
            PrimaB = 0.10 * float(PrimaPrincipal)
            PrimaB1 = "{:,.2f}".format(float(PrimaB))
            ancho_texto13 = pdf.stringWidth("$" + str(PrimaB1), "Helvetica", 9)
            x_centro13 = 450 + (100 - ancho_texto13)/2
            pdf.drawString(x_centro13, altura_accidental, "$" + str(PrimaB1))
        else:
            PrimaB1 = 0
            ancho_texto13 = pdf.stringWidth("", "Helvetica", 9)
            x_centro13 = 450 + (100 - ancho_texto13)/2
            pdf.drawString(x_centro13, altura_accidental, "")
        #ITP
        if BeneficioITP == 'Si':
            ancho_texto14 = pdf.stringWidth("$" +  str(Suma1), "Helvetica", 9)
            x_centro14 = 280 + (120 - ancho_texto14)/2
            pdf.drawString(x_centro14, altura_ITP-10, "$" + str(Suma1))
        else:
            ancho_texto14 = pdf.stringWidth("", "Helvetica", 9)
            x_centro14 = 280 + (120 - ancho_texto14)/2
            pdf.drawString(x_centro14, altura_ITP, "")
        PrimaITP = 0
        if BeneficioITP == 'Si':
            PrimaITP = 0.25 * float(PrimaP)
            PrimaITP1 = "{:,.2f}".format(float(PrimaITP))
            ancho_texto15 = pdf.stringWidth("$" + str(PrimaITP1), "Helvetica", 9)
            x_centro15 = 450 + (100 - ancho_texto15)/2
            pdf.drawString(x_centro15, altura_ITP-10, "$" + str(PrimaITP1))
        else:
            PrimaITP1 = "{:,.2f}".format(float(PrimaITP))
            ancho_texto15 = pdf.stringWidth("", "Helvetica", 9)
            x_centro15 = 450 + (100 - ancho_texto15)/2
            pdf.drawString(x_centro15, altura_ITP+1, "")
        #TOTAL
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(280, altura_total, 120, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)

        PrimaTotal = float(PrimaP) + float(PrimaB) + float(PrimaITP)
        PrimaTotal1 = "{:,.2f}".format(float(PrimaTotal))
        ancho_texto16 = pdf.stringWidth("$" + str(PrimaTotal1), "Helvetica", 9)
        x_centro16 = 450 + (100 - ancho_texto16)/2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(450, altura_total, 100, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x_centro16, altura_total+3, "$" + str(PrimaTotal1))
        pdf.setFont("Helvetica", 9)
        #PARAMETRO DE REQUISITOS DE ASEGURABILIDAD
        SumaM = float(Suma)
        edadM = int(edad)
        if edadM <= 39 and SumaM <= 75000:
            parametro = "Declaración de Salud"
        elif edadM <= 39 and 75000 < SumaM <= 150000:
            parametro = "Declaración de Salud y Análisis de Orina"
        elif edadM <= 39 and 150000 < SumaM <= 300000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de orina, ECG reposo y HIV"
        elif edadM <= 39 and 300000 < SumaM <= 750000:
            parametro = "Declaración de Salud, Exámen médico, Análisis de orina, ECG reposo, HIV y LAB 1"
        elif edadM <= 39 and SumaM > 750000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de Orina, ECG reposo, HIV, LAB 2 y Rx tórax"
        elif 40 <= edadM <= 49 and SumaM <= 75000:
            parametro = "Declaración de Salud"
        elif 40 <= edadM <= 49 and 75000 < SumaM <= 150000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de Orina y HIV"
        elif 40 <= edadM <= 49 and 150000 < SumaM <= 300000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de orina, ECG reposo, HIV y LAB 1"
        elif 40 <= edadM <= 49 and 300000 < SumaM <= 750000:
            parametro = "Declaración de Salud, Exámen médico, Análisis de orina, Prueba de esfuerzo, HIV, LAB 1 y Rx tórax"
        elif 40 <= edadM <= 49 and SumaM > 750000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de Orina, Prueba de esfuerzo, HIV, LAB 2 y Rx tórax"
        elif 50 <= edadM <= 59 and SumaM <= 75000:
                parametro = "Declaración de Salud, Exámen Médico y Análisis de orina"
        elif 50 <= edadM <= 59 and 75000 < SumaM <= 150000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de Orina, ECG reposo, HIV y LAB 1"
        elif 50 <= edadM <= 59 and 150000 < SumaM <= 300000:
            parametro = "Exámen Médico, Análisis de orina, ECG reposo, HIV, LAB 1 y Rx tórax"
        elif 50 <= edadM <= 59 and 300000 < SumaM <= 750000:
            parametro = "Declaración de Salud, Exámen médico, Análisis de orina, Prueba de esfuerzo, HIV, LAB 2 y Rx tórax"
        elif 50 <= edadM <= 59 and SumaM > 750000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de Orina, Prueba de esfuerzo, HIV, LAB 2 y Rx tórax"
        elif edadM >= 60 and SumaM <= 75000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de orina y ECG reposo"
        elif edadM >= 60 and 75000 < SumaM <= 150000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de Orina, ECG reposo, HIV y LAB 2"
        elif edadM >= 60 and 150000 < SumaM <= 300000:
            parametro = "Exámen Médico, Análisis de orina, Prueba de esfuerzo, HIV, LAB 2 y Rx tórax"
        elif edadM >= 60 and 300000 < SumaM <= 750000:
            parametro = "Declaración de Salud, Exámen médico, Análisis de orina, Prueba de esfuerzo, HIV, LAB 2 y Rx tórax"
        elif edadM >= 60 and SumaM > 750000:
            parametro = "Declaración de Salud, Exámen Médico, Análisis de Orina, Prueba de esfuerzo, HIV, LAB 2 y Rx tórax"
        ancho_texto17 = pdf.stringWidth(parametro, "Helvetica", 9)
        x_centro17 = 50 + (497 - ancho_texto17)/2
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 459, 497, 10, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(x_centro17, 459, parametro)
        #FORMA DE PAGO
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 441, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(270, 445, "FORMA DE PAGO:")
        pdf.setFont("Helvetica", 9)
        #ANUAL
        pdf.drawString(120, 429, "ANUAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(170, 426, 15, 12, fill=False, stroke=True)
        #SEMESTRAL
        pdf.drawString(200, 429, "SEMESTRAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(270, 426, 15, 12, fill=False, stroke=True)
        #TRIMESTRAL
        pdf.drawString(300, 429, "TRIMESTRAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(370, 426, 15, 12, fill=False, stroke=True)
        #MENSUAL
        pdf.drawString(400, 429, "MENSUAL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(460, 426, 15, 12, fill=False, stroke=True)
        #FORMA DE PAGO2
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 407, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(210, 413, "FORMA DE PAGO (Incluye gastos e impuestos)")
        pdf.setFont("Helvetica", 9)
        #PARÁMETROS DE FORMAS DE PAGO2
        #ANUAL
        parametro1 = "ANUAL:          1 cuota anual de $" + str(PrimaTotal1) + " al suscribir el Seguro." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 399, 497, 11, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 400, parametro1)
        #SEMESTRAL
        PrimaTotalSemestral = (float(PrimaTotal) * 1.04)/2
        PrimaTotalSemestral = "{:,.2f}".format(float(PrimaTotalSemestral))
        parametro2 = "SEMESTRAL: 1 cuota de $" + str(PrimaTotalSemestral) + " al suscribir el Seguro y $" + str(PrimaTotalSemestral) + " el semestre siguiente." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 387, 497, 12, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 387, parametro2)
        #TRIMESTRAL
        PrimaTotalTrimestral = (float(PrimaTotal) * 1.06)/4
        PrimaTotalTrimestral = "{:,.2f}".format(float(PrimaTotalTrimestral))
        parametro3 = "TRIMESTRAL:1 cuota de $" + str(PrimaTotalTrimestral) + " al suscribir el Seguro y $" + str(PrimaTotalTrimestral) + " cada uno de los trimestres siguientes." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 375, 497, 11, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 375, parametro3)
        #MENSUAL
        PrimaTotalMensual = (float(PrimaTotal) * 1.07)/12
        PrimaTotalMensual = "{:,.2f}".format(float(PrimaTotalMensual))
        parametro4 = "MENSUAL:     1 cuota de $" + str(PrimaTotalMensual) + " al suscribir el Seguro y $" + str(PrimaTotalMensual) + " cada uno de los meses siguientes." 
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 362, 497, 12, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 362, parametro4)
        #TEXTO DE PRIMA SUJETA A VERIFICACIÓN
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(170, 351, "Prima sujeta a verificación de exámen médico y análisis de suscripción")
        pdf.setFont("Helvetica", 9)
        #CESIÓN DE DERECHOS
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 333, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(260, 337, "CESIÓN DE DERECHOS")
        pdf.setFont("Helvetica", 9)
        #TEXTO DEBAJO DE CESION
        pdf.drawString(50, 309, "A favor de __________________________________________________ por valor de $____________________")
        pdf.drawString(50, 283, "Si usted acepta la presente cotización, favor devolver los siguientes documentos completos y firmados:")
        pdf.drawString(50, 268, "1. Solicitud de seguro y declaración de salud.")
        pdf.drawString(50, 256, "2. Ficha Integral.")
        pdf.drawString(50, 244, "3. Declaración Jurada.")
        pdf.drawString(50, 232, "4. Documento de Identidad, Pasaporte o Carnet de Residente.")
        pdf.drawString(50, 202, "Oferta válida 30 días a partir de la fecha de su emisión:")
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(275, 202, fecha_actual)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(50, 190, "Suicidio cubierto después de dos años de vigencia. Muerte Presunta cubierta según ley.")
        pdf.drawString(50, 178, "La prima cotizada puede cambiar si en la fecha de emisión de la póliza la edad para el seguro fuere otra.")
        #FIRMAS
        pdf.drawString(100, 128, "__________________________")
        pdf.drawString(110, 116, "Firma de aceptación cliente")
        pdf.drawString(360, 128, "__________________________")
        pdf.drawString(380, 116, "Fecha de aceptación")
        pdf.drawString(100, 76, "__________________________")
        pdf.drawString(116, 64, "Firma de intermediario")
        #Pie de página
        if Nom == "" and In == "":
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 40, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 42, "Intermediario, Empresa: Oficina Principal, Atlántida Vida S.A. Seguro de Personas")
            pdf.drawString(500, 42, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 27, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 29, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 29, "Teléfono: " + str(Te))
        else:
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 40, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 42, "Intermediario, Empresa: " + str(In) + ", " + str(Nom))
            pdf.drawString(500, 42, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 27, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 29, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 29, "Teléfono: " + str(Te))
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 14, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 16, "Atención al cliente: (503)2283-0800")
        pdf.drawString(332, 16, "Correo electrónico: aseguradoatlantida@seatlan.sv")
        # Guardar el PDF en el buffer
        pdf.showPage()
        pdf.setTitle('OFERTA_DE_STEMPORAL_INDIVIDUAL.pdf')
        pdf.save()

        # Obtener el contenido del buffer y devolverlo como una respuesta HTTP
        #buffer.seek(0)

        pdf_bytes = buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        #response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'inline; filename="Oferta_TemporalRenovable.pdf"'
        #response.write(buffer.read())

        correos = [correo for correo in [Cor, Mails] if correo]  # Filtrar correos válidos

        # Si hay correos válidos, enviar el correo
        if correos:
            enviar_correo(correos, Solicitante, Cellphones, edad, pdf_bytes)
        
        return render(request, 'Oferta_Temp.html', 
            {'pdf_base64': pdf_base64,
             'Solicitante': Solicitante,
             })
    
def enviar_correo(correos, Solicitante, Cellphones, edad, pdf_bytes):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = 'henriquezricardo459@gmail.com'
    password = 'omou bfpf amij afcw'  # Recuerda almacenar la contraseña de manera segura
    
    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(correos)
    msg['Subject'] = 'Oferta de Seguro Temporal Individual'

    cuerpo_mensaje = f"""Información del cliente:

- Nombre: {Solicitante}
- Edad: {edad}
-Teléfono: {Cellphones}

Es un placer saludarle. Adjuntamos la oferta del Seguro Temporal Individual, así cómo los documentos adicionales necesarios en caso de que acepte nuestra cotización.

Cualquier consulta, no dude en responder a este correo o comunicarse con nosotros al 2283-0000. Quedamos a su disposición para cualquier consulta adicional.

Saludos cordiales

Atentamente,

Seguros Atlántida S.A., de C.V.
    """
    msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
    # Adjuntar el PDF generado
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_bytes)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='Oferta de Seguro Temporal Individual.pdf')
    msg.attach(attachment)

    # Adjuntar otros archivos PDF
    for documento in ['Declaracion_Jurada_Persona_Natural.pdf', 'Solicitud_VidaIndividual.pdf', 'Hoja_de_Vinculacion_Persona_Natural.pdf']:
        with open(os.path.join('cotizadort/static', documento), 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=documento)
            msg.attach(attachment)

    # Iniciar la conexión SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)


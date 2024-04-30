from django import forms

Opciones = [
    ('Si', 'Si'),
    ('No', 'No'),
]
Opciones2 = [
    ('Mensual', 'Mensual'),
    ('Trimestral', 'Trimestral'),
    ('Semestral', 'Semestral'),
    ('Anual', 'Anual'),
]
Opcion = [
    ('No Fumador', 'No Fumador'),
    ('Fumador', 'Fumador'),
]
Opcion1 = [
    ('Hombre', 'Hombre'),
    ('Mujer', 'Mujer'),
]
Opcion3 = [
    ('10 años', '10 años'),
    ('15 años', '15 años'),
    ('20 años', '20 años'),
    ('25 años', '25 años'),
    ('30 años', '30 años'),
]
class C_Intermediario2(forms.Form):
    Nombre = forms.CharField(label="Nombre de Empresa:", max_length=200, required=False)
    Int = forms.CharField(label="Intermediario:", max_length=200, required=False)
    Tel = forms.CharField(label="Teléfono:", max_length=200, required=False)
    Correo = forms.CharField(label="Correo electrónico:", max_length=200, required=False)
    Id = forms.CharField(label="IVD o CVD:", max_length=200, required=False) 
    
class form_CotizadorTAR(forms.Form):
    Sol = forms.CharField(label="Solicitante:", max_length=200)
    Nac = forms.CharField(label="Fecha de Nacimiento (AAAA/MM/DD):", max_length=200)
    Gen = forms.ChoiceField(label="Género:", choices=Opcion1, widget=forms.Select(attrs={'id':'gen'}))
    Temporal = forms.ChoiceField(label='Temporalidad del Seguro', choices=Opcion3, widget=forms.Select(attrs={'id':'temporal'}))
    Sum = forms.CharField(label="Suma Asegurada (Entre $10,000 - $10,000,000):", max_length=200)
    Mail = forms.CharField(label="Correo Electrónico", max_length=200, required=False)
    Cellphone = forms.CharField(label="Celular:", max_length=200)
    Fum = forms.ChoiceField(label="Tipo de Riesgo", choices=Opcion, widget=forms.Select(attrs={'id':'fum'}))
    Titulo = forms.CharField(label="", initial="Coberturas Opcionales:", widget=forms.Textarea(attrs={'readonly':'readonly', 'class': 'Coberturas'})) 
    Ben1 = forms.ChoiceField(label="Beneficio de Invalidez Total y Permanente", choices=Opciones, widget=forms.Select(attrs={'id':'ben1'}))
    Ben2 = forms.ChoiceField(label="Beneficio de Muerte Accidental y Desmembramiento", choices=Opciones, widget=forms.Select(attrs={'id':'ben2'}))
    
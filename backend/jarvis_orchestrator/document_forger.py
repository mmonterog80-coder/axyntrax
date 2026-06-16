import os
from fpdf import FPDF, XPos, YPos
from datetime import datetime

class CotizacionPDF(FPDF):
    def header(self):
        # Logo Axyntrax
        logo_path = r"C:\Users\YARVIS\axyntrax-jarvis-complete\public\axyntrax-logo.png"
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 33)
        
        self.set_font('helvetica', 'B', 15)
        self.set_x(50)
        self.cell(0, 10, 'AXYNTRAX AUTOMATION', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        
        self.set_font('helvetica', 'I', 10)
        self.set_x(50)
        self.cell(0, 10, 'Innovacion en Arquitecturas de Inteligencia Artificial', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def generar_cotizacion_pdf(cliente_nombre: str, rubro: str, detalles_arquitectura: list, precio_total: float) -> str:
    pdf = CotizacionPDF()
    pdf.add_page()
    
    # Metadatos del Documento
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Propuesta Arquitectonica Oficial de IA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 12)
    fecha = datetime.now().strftime("%d de %B, %Y")
    pdf.cell(0, 10, f"Fecha: {fecha}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Cliente: {cliente_nombre}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Rubro de Operaciones: {rubro}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    # Cuerpo / Arquitectura
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Detalle de Arquitectura de Inteligencia Artificial a Implementar:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("helvetica", "", 11)
    for detalle in detalles_arquitectura:
        pdf.multi_cell(w=0, h=8, text=f"- {detalle}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    
    # Precio Total
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"Inversion Total Sugerida: S/ {precio_total:,.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
    pdf.ln(10)
    
    # Firma / Cierre
    pdf.set_font("helvetica", "I", 10)
    texto_cierre = ("Este documento fue generado por la Inteligencia Artificial NOVA. La arquitectura "
                    "descrita está diseñada específicamente para optimizar y automatizar los flujos de "
                    "trabajo de su corporación, brindando ventajas competitivas absolutas.")
    pdf.multi_cell(w=0, h=8, text=texto_cierre, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                         
    # Directorio de salida
    salida_dir = os.path.join(os.path.dirname(__file__), "..", "..", "workspace", "documentos_oficiales")
    os.makedirs(salida_dir, exist_ok=True)
    
    nombre_archivo = f"AXYNTRAX_Cotizacion_{cliente_nombre.replace(' ', '_')}_{int(datetime.now().timestamp())}.pdf"
    ruta_completa = os.path.join(salida_dir, nombre_archivo)
    
    pdf.output(ruta_completa)
    return ruta_completa

if __name__ == "__main__":
    ruta = generar_cotizacion_pdf(
        cliente_nombre="Empresa de Prestamos Ejemplo SAC",
        rubro="Préstamos y Finanzas",
        detalles_arquitectura=[
            "Agente Scoring: Evalúa el riesgo del prestatario en tiempo real.",
            "Agente Cobranza: Recordatorios automáticos por WhatsApp con voz y texto.",
            "Dashboard Administrativo (Axyntrax OS)."
        ],
        precio_total=1250.00
    )
    print(f"Cotizacion de prueba generada en: {ruta}")

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_chemistry_pdf():
    pdf_filename = "chemistry_formulas.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, spaceAfter=12, textColor='#0b0f19')
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, spaceBefore=8, spaceAfter=4, textColor='#1e293b')
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, spaceAfter=4)

    content = [Paragraph("Master Chemistry Formula Sheet & Constants for NEET/JEE", title_style), Spacer(1, 10)]

    formula_data = [
        ("Physical Chemistry - Mole Concept", ["n = mass/molar mass", "N = n * NA", "Mole fraction: χ = moles / total moles"]),
        ("Physical Chemistry - Gas Laws", ["PV = nRT", "P₁V₁/T₁ = P₂V₂/T₂", "Graham's Law: r₁/r₂ = √(M₂/M₁)"]),
        ("Physical Chemistry - Atomic Structure", ["E = -13.6 / n² eV", "De Broglie wavelength: λ = h / mv"]),
        ("Physical Chemistry - Thermodynamics", ["ΔU = q + w", "w = -PΔV", "ΔH = ΔU + ΔnRT", "ΔG = ΔH - TΔS"]),
        ("Physical Chemistry - Equilibrium", ["Kc = Products / Reactants", "Kw = [H⁺][OH⁻]", "pH = -log[H⁺]", "pOH = -log[OH⁻]", "pH + pOH = 14"]),
        ("Physical Chemistry - Ionic Equilibrium", ["Ka = [H⁺][A⁻] / [HA]", "Kb = [BH⁺][OH⁻] / [B]", "Ka * Kb = Kw"]),
        ("Physical Chemistry - Electrochemistry", ["Ecell = Ecathode - Eanode", "ΔG = -nFE", "Nernst Equation: E = E° - (0.0591/n)logQ"]),
        ("Physical Chemistry - Chemical Kinetics", ["Rate = k[A]^m[B]^n", "First order: k = (2.303/t)log(a / (a-x))", "t½ = 0.693 / k"]),
        ("Physical Chemistry - Surface Chemistry", ["Freundlich Adsorption Isotherm: x/m = kP^(1/n)"]),
        ("Inorganic Chemistry", ["Coordination Compounds - EAN = Z - oxidation state + electrons donated", "Metallurgy - % Purity = (pure metal / sample mass) * 100"]),
        ("Organic Chemistry - Homologous Series", ["Alkanes: CnH2n+2", "Alkenes: CnH2n", "Alkynes: CnH2n-2", "Cycloalkanes: CnH2n", "Alcohols: ROH", "Aldehydes: RCHO", "Ketones: RCOR", "Carboxylic Acids: RCOOH", "Amines: RNH₂", "Ethers: ROR", "Esters: RCOOR"]),
        ("Important Universal Constants", ["g = 9.8 m/s²", "R = 8.314 J mol⁻¹ K⁻¹", "NA = 6.022 × 10²³ mol⁻¹", "h = 6.626 × 10⁻³⁴ Js", "c = 3 × 10⁸ m/s", "e = 1.602 × 10⁻¹⁹ C", "F = 96500 C mol⁻¹", "ε₀ = 8.854 × 10⁻¹² F/m", "G = 6.67 × 10⁻¹¹ N m²/kg²"])
    ]

    for section_title, formulas in formula_data:
        content.append(Paragraph(section_title, heading_style))
        for formula in formulas:
            content.append(Paragraph(f"• {formula}", body_style))
        content.append(Spacer(1, 4))

    doc.build(content)
    print("Chemistry PDF generated successfully!")

if __name__ == "__main__":
    create_chemistry_pdf()
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_formula_pdf():
    pdf_filename = "physics_formulas.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, spaceAfter=12, textColor='#0b0f19')
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, spaceBefore=8, spaceAfter=4, textColor='#1e293b')
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, spaceAfter=4)

    content = [Paragraph("Master Physics Formula Sheet for NEET/JEE", title_style), Spacer(1, 10)]

    formula_data = [
        ("1. Units & Dimensions", ["Density = m/V", "Relative density = Density of substance / Density of water"]),
        ("2. Motion in One Dimension", ["v = u + at", "s = ut + ½at²", "v² = u² + 2as", "s = (u+v)t/2"]),
        ("3. Projectile Motion", ["Time of flight: T = 2u sinθ/g", "Maximum height: H = u²sin²θ/2g", "Range: R = u²sin2θ/g"]),
        ("4. Newton's Laws", ["F = ma", "Weight = mg", "Friction: Fs ≤ μsN, Fk = μkN"]),
        ("5. Work, Energy & Power", ["Work = Fs cosθ", "KE = ½mv²", "PE = mgh", "Spring PE = ½kx²", "Power = W/t = Fv"]),
        ("6. Circular Motion", ["Fc = mv²/r", "ac = v²/r = ω²r", "v = rω"]),
        ("7. Gravitation", ["F = GMm/r²", "g = GM/r²", "PE = -GMm/r", "Escape velocity = √(2GM/R)", "Orbital velocity = √(GM/R)"]),
        ("8. Fluid Mechanics", ["Pressure = F/A", "P = hρg", "Buoyant force = ρVg", "Continuity: A₁v₁ = A₂v₂", "Bernoulli: P + ½ρv² + ρgh = constant"]),
        ("9. SHM", ["a = -ω²x", "ω = 2π/T", "T = 2π√(m/k)", "T(pendulum) = 2π√(L/g)"]),
        ("10. Waves", ["v = νλ", "Frequency = 1/T", "Doppler: ν' = ν[(v±vo)/(v∓vs)]"]),
        ("11. Heat & Thermodynamics", ["Q = mcΔT", "Q = mL", "PV = nRT", "ΔU = Q - W", "Cp - Cv = R", "γ = Cp/Cv"]),
        ("12. Kinetic Theory", ["PV = ⅓Nmvrms²", "vrms = √(3RT/M)"]),
        ("13. Electrostatics", ["F = kq₁q₂/r²", "E = kq/r²", "V = kq/r", "U = kq₁q₂/r", "C = Q/V"]),
        ("14. Capacitors", ["Parallel: C = C₁ + C₂ + ...", "Series: 1/C = 1/C₁ + 1/C₂ + ...", "Energy = ½CV²"]),
        ("15. Current Electricity", ["V = IR", "R = ρL/A", "P = VI = I²R = V²/R", "Cells: E = IR + Ir"]),
        ("16. Magnetic Effects", ["F = q(v×B)", "F = BIL sinθ", "B = μ₀I/2πr", "B(center of coil) = μ₀NI/2R"]),
        ("17. Electromagnetic Induction", ["ε = -dΦ/dt", "Φ = BA cosθ", "Self inductance: ε = -L(dI/dt)"]),
        ("18. Alternating Current", ["Irms = I₀/√2", "Vrms = V₀/√2", "XL = ωL", "XC = 1/ωC", "Z = √(R² + (XL-XC)²)"]),
        ("19. Ray Optics", ["Mirror: 1/f = 1/v + 1/u", "Lens: 1/f = 1/v - 1/u", "Magnification: m = h₂/h₁ = v/u"]),
        ("20. Wave Optics", ["Young's: β = λD/d", "Diffraction: a sinθ = nλ"]),
        ("21. Modern Physics", ["E = hν", "λ = h/p", "Einstein: E = mc²", "Photoelectric: hν = φ + KEmax"]),
        ("22. Nuclear Physics", ["N = N₀e^(-λt)", "T½ = 0.693/λ", "Activity: A = λN"])
    ]

    for section_title, formulas in formula_data:
        content.append(Paragraph(section_title, heading_style))
        for formula in formulas:
            content.append(Paragraph(f"• {formula}", body_style))
        content.append(Spacer(1, 4))

    doc.build(content)
    print("Physics PDF generated successfully!")

if __name__ == "__main__":
    create_formula_pdf()
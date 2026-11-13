# -*- coding: utf-8 -*-
"""Contenido del currículum de Luis Ricardo Garrido Mendoza, en español e inglés.

Fuente única para el PDF y para el Word. TODO sale del currículum que entregó
(CV_RICARDO_MENDOZA_2026.docx): no se añadió ni un dato, ni una cifra, ni un
logro. Lo que cambia es la forma: verbos en vez de sustantivos («Elaboro y
reviso…» por «Elaboración y revisión de…»), viñetas que decían lo mismo
fundidas en una, y las diez competencias agrupadas en cuatro renglones
«rótulo: valores» para que un lector automático no pierda qué va con qué.
"""

DATOS = {
    "nombre": "Luis Ricardo Garrido Mendoza",
    "tel": "+52 442 775 7307",
    "tel_href": "tel:+524427757307",
    "correo": "luis.mendoza97@outlook.com",
    "linkedin": "linkedin.com/in/ricardo-mendoza-211947259",
    "linkedin_href": "https://www.linkedin.com/in/ricardo-mendoza-211947259/",
    "cedula": "15649339",
}

ES = {
    "lang": "es",
    "titulo": "Abogado",
    "bajada": "Derecho mercantil · Contratos · Asuntos corporativos",
    "cedula_r": "Cédula Profesional",
    "h_perfil": "Perfil profesional",
    "perfil": ("Abogado con más de cinco años de experiencia en asuntos civiles, mercantiles y notariales. "
               "Elaboro y reviso contratos e instrumentos jurídicos, llevo litigio civil y mercantil, redacto demandas "
               "y promociones, y analizo expedientes. Mi práctica en despacho, sector público y notaría me da una visión "
               "integral del manejo preventivo y contencioso de los asuntos. Busco incorporarme a una empresa o despacho "
               "en Ciudad de México para desarrollarme en derecho corporativo y mercantil, contratación y asesoría jurídica."),
    "h_comp": "Competencias",
    "comp": [
        ("Corporativo y contratos", "Derecho mercantil · Contratos y documentación jurídica · Protocolización de actas de asamblea"),
        ("Litigio", "Litigio civil y mercantil · Juicio de amparo · Elaboración de escritos jurídicos"),
        ("Notarial", "Actos e instrumentos notariales: escrituras públicas, poderes y testamentos"),
        ("Análisis y servicio", "Revisión y análisis documental · Investigación jurídica · Atención y asesoría a clientes"),
    ],
    "h_exp": "Experiencia profesional",
    "exp": [
        {"puesto": "Abogado, Área Notarial", "empresa": "Notaría Pública No. 1", "fechas": "Jul 2023 – Actualidad", "puntos": [
            "Elaboro y reviso escrituras públicas, poderes, testamentos y otros instrumentos jurídicos.",
            "Participo en operaciones de compraventa, créditos hipotecarios y cancelaciones de hipoteca.",
            "Protocolizo actas de asamblea y preparo la documentación correspondiente.",
            "Reviso e integro expedientes y documentación para la formalización de actos jurídicos.",
            "Atiendo y oriento a clientes, y doy seguimiento a trámites ante autoridades administrativas y registrales.",
        ]},
        {"puesto": "Abogado Litigante", "empresa": "JURIDEX, S.C.", "fechas": "Feb 2023 – Jun 2024", "puntos": [
            "Llevé asuntos en materia civil y mercantil ante autoridades y tribunales.",
            "Redacté demandas, contestaciones, promociones, recursos y demás escritos jurídicos.",
            "Analicé expedientes y documentación para preparar estrategias jurídicas.",
            "Asesoré a clientes sobre el desarrollo de sus asuntos y participé en asuntos de juicio de amparo.",
        ]},
        {"puesto": "Auxiliar Jurídico", "empresa": "HM Abogados", "fechas": "Jul 2022 – Feb 2023", "puntos": [
            "Integré y di seguimiento a expedientes judiciales y extrajudiciales, y a diligencias ante autoridades.",
            "Revisé contratos y documentación jurídica.",
            "Investigué y revisé la legislación aplicable; apoyé en la elaboración de escritos y análisis jurídicos.",
        ]},
        {"puesto": "Abogado Pasante", "empresa": "Despacho Jurídico MR", "fechas": "Mar 2022 – Jul 2022", "puntos": [
            "Elaboré escritos jurídicos y documentos bajo supervisión; apoyé en la elaboración y revisión de contratos.",
            "Investigué y analicé la legislación aplicable; di atención inicial y seguimiento a asuntos de clientes.",
        ]},
        {"puesto": "Auxiliar de Ministerio Público Federal", "empresa": "Fiscalía General de la República", "fechas": "Oct 2020 – Nov 2021", "puntos": [
            "Apoyé en la integración y seguimiento de carpetas de investigación.",
            "Elaboré escritos, determinaciones y oficios de carácter jurídico.",
            "Di seguimiento a diligencias y coordiné con policías de investigación y peritos.",
        ]},
    ],
    "h_edu": "Formación académica",
    "edu": [
        ("Maestría en Juicios Orales", "Universidad Interamericana para el Desarrollo", "2024 – 2025"),
        ("Licenciatura en Derecho y Ciencias Jurídicas", "Universidad Interamericana para el Desarrollo", "2021"),
    ],
    "h_idi": "Idiomas",
    "idi": [("Español", "Nativo"), ("Inglés", "B2 – Intermedio avanzado")],
}

EN = {
    "lang": "en",
    "titulo": "Attorney",
    "bajada": "Commercial law · Contracts · Corporate matters",
    "cedula_r": "Professional Licence (Cédula Profesional)",
    "h_perfil": "Professional profile",
    "perfil": ("Attorney with more than five years of experience in civil, commercial and notarial matters. "
               "I draft and review contracts and legal instruments, handle civil and commercial litigation, prepare claims "
               "and motions, and analyse case files. My practice in private firms, the public sector and a notary office gives "
               "me a full view of both the preventive and the contentious side of legal matters. I am looking to join a company "
               "or law firm in Mexico City to grow in corporate and commercial law, contracts and legal advisory."),
    "h_comp": "Core competencies",
    "comp": [
        ("Corporate & contracts", "Commercial law · Contracts and legal documents · Notarisation of shareholders’ meeting minutes"),
        ("Litigation", "Civil and commercial litigation · Amparo proceedings · Drafting of legal briefs"),
        ("Notarial", "Notarial acts and instruments: public deeds, powers of attorney and wills"),
        ("Analysis & service", "Document review and analysis · Legal research · Client service and counsel"),
    ],
    "h_exp": "Professional experience",
    "exp": [
        {"puesto": "Attorney, Notarial Practice", "empresa": "Notaría Pública No. 1 (Notary Office)", "fechas": "Jul 2023 – Present", "puntos": [
            "Draft and review public deeds, powers of attorney, wills and other legal instruments.",
            "Take part in sale transactions, mortgage loans and mortgage releases.",
            "Notarise shareholders’ meeting minutes and prepare the supporting documentation.",
            "Review and assemble files and documentation to formalise legal acts.",
            "Advise clients and follow up on filings before administrative and registry authorities.",
        ]},
        {"puesto": "Litigation Attorney", "empresa": "JURIDEX, S.C.", "fechas": "Feb 2023 – Jun 2024", "puntos": [
            "Handled civil and commercial matters before authorities and courts.",
            "Drafted claims, answers, motions, appeals and other legal briefs.",
            "Analysed case files and documentation to prepare legal strategies.",
            "Advised clients on the progress of their matters and took part in amparo proceedings.",
        ]},
        {"puesto": "Legal Assistant", "empresa": "HM Abogados", "fechas": "Jul 2022 – Feb 2023", "puntos": [
            "Assembled and followed up judicial and out-of-court case files, and proceedings before authorities.",
            "Reviewed contracts and legal documents.",
            "Researched and reviewed the applicable legislation; supported the drafting of briefs and legal analyses.",
        ]},
        {"puesto": "Trainee Attorney", "empresa": "Despacho Jurídico MR", "fechas": "Mar 2022 – Jul 2022", "puntos": [
            "Drafted legal briefs and documents under supervision; supported the drafting and review of contracts.",
            "Researched and analysed the applicable legislation; handled first contact and follow-up of client matters.",
        ]},
        {"puesto": "Assistant to the Federal Public Prosecutor", "empresa": "Fiscalía General de la República (FGR)", "fechas": "Oct 2020 – Nov 2021", "puntos": [
            "Supported the assembly and follow-up of investigation files.",
            "Drafted legal briefs, determinations and official letters.",
            "Followed up proceedings and coordinated with investigative police and expert witnesses.",
        ]},
    ],
    "h_edu": "Education",
    "edu": [
        ("Master’s Degree in Oral Trials (Maestría)", "Universidad Interamericana para el Desarrollo", "2024 – 2025"),
        ("Bachelor’s Degree in Law and Legal Sciences (Licenciatura)", "Universidad Interamericana para el Desarrollo", "2021"),
    ],
    "h_idi": "Languages",
    "idi": [("Spanish", "Native"), ("English", "B2 – Upper-intermediate")],
}

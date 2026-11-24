UK_TAX = (
    "HMRC 2026/27 rates",
    "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027",
)
UK_ALLOWANCE = ("HMRC Personal Allowance", "https://www.gov.uk/income-tax-rates")
UK_GROSS_UP = (
    "HMRC gross-up guidance",
    "https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye72028",
)
TAX_EQUALISATION = (
    "HMRC tax equalisation",
    "https://www.gov.uk/government/publications/tax-equalisation-hs212-self-assessment-helpsheet/tax-equalisation-2026-hs212",
)
UK_HOUSING = (
    "HMRC accommodation valuation",
    "https://www.gov.uk/guidance/company-provided-living-accommodation-480-chapter-21",
)
UK_WORKPLACE_RELIEF = (
    "HMRC secondments",
    "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim77010",
)
UK_RELOCATION_CAP = (
    "HMRC relocation exemption",
    "https://www.gov.uk/expenses-and-benefits-relocation/whats-exempt",
)
UK_CASH_ALLOWANCE = (
    "HMRC flat allowances",
    "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03139",
)
UK_TEMPORARY_HOUSING = (
    "HMRC temporary housing",
    "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03117",
)
UK_NIC = (
    "HMRC certificate of coverage",
    "https://www.gov.uk/guidance/social-security-contributions-for-workers-coming-to-the-uk-from-the-eea-or-switzerland#coming-to-work-in-the-uk--from-gibraltar-iceland-liechtenstein-norway-or-switzerland",
)
SWISS_POSTING = (
    "UK–Swiss convention, Article 14",
    "https://assets.publishing.service.gov.uk/media/6697bfdaa3c2a28abb50d14e/TS_47.2024_UK_Switzerland_Convention_Social_Security_Coordination_with_corrections.pdf#page=14",
)
SWISS_FEDERAL_TAX = (
    "FTA 2026 tariff",
    "https://www.estv.admin.ch/dam/de/sd-web/vFK3ntWLQ4s4/2-215-D-2025-d.pdf",
)
ZURICH_TARIFF = (
    "Zurich 2026 basic tariff",
    "https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/steuern-finanzen/steuern/vertreter/steuerbuch/zstb-nr-48-1/zstb-nr-48-1.pdf",
)
ZURICH_CANTON = (
    "Zurich cantonal multiplier",
    "https://www.zh.ch/de/steuern-finanzen/steuern/steuerstatistiken/aktuelle-gemeinde-steuerfuesse.html",
)
ZURICH_CITY = (
    "Zurich city multiplier",
    "https://www.stadt-zuerich.ch/de/lebenslagen/steuern/natuerliche-personen/steuerberechnung.html",
)
ZURICH_DEDUCTIONS = (
    "Zurich 2026 tax guide",
    "https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/steuern-finanzen/steuern/natuerlichepersonen/2026/est-wegleitungen-uj/305%20Wegleitung%20ZH%202026%20UJ%20bf.pdf",
)
SWISS_CALCULATOR = (
    "FTA tax calculator",
    "https://swisstaxcalculator.estv.admin.ch/#/calculator/income-wealth-tax",
)
SWISS_CONTRIBUTIONS = (
    "SVA Zürich contribution rates",
    "https://svazurich.ch/lohn",
)
SWISS_ADMIN = (
    "SVA Zürich fee schedule",
    "https://svazurich.ch/content/dam/sva-dokumente/2000_ak/2800_vb/2800_vb1_verwaltungskostenbeitraege_ab_2026.pdf",
)
SWISS_WAGE = (
    "FSIO assessable-pay guidance",
    "https://sozialversicherungen.admin.ch/de/d/6944/download?version=22",
)

GBM_RULES = (
    "Global Business Mobility rules",
    "https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-global-business-mobility-routes",
)
SPONSOR_LICENCE = (
    "Sponsor licence application",
    "https://www.gov.uk/uk-visa-sponsorship-employers/apply-for-your-licence",
)
SPONSOR_CERTIFICATE = (
    "Certificate of Sponsorship",
    "https://www.gov.uk/uk-visa-sponsorship-employers/certificates-of-sponsorship",
)
VISA_FEES = (
    "Work visa fees and maintenance",
    "https://www.gov.uk/senior-specialist-worker-visa/how-much-it-costs",
)
VISA_ELIGIBILITY = (
    "Work visa eligibility",
    "https://www.gov.uk/senior-specialist-worker-visa/eligibility",
)
ETA_APPLICATION = ("ETA application", "https://www.gov.uk/eta/apply")

IMMIGRATION_GUIDANCE = {
    "route": (
        (
            "Senior or Specialist Worker visa",
            "https://www.gov.uk/senior-specialist-worker-visa",
        ),
        (
            "Home Office guide for GBM sponsors",
            "https://www.gov.uk/government/publications/sponsor-a-global-business-mobility-worker/workers-and-temporary-workers-sponsor-a-global-business-mobility-worker-accessible",
        ),
    ),
    "eligibility": (
        VISA_ELIGIBILITY,
        (
            "Occupation codes and going rates",
            "https://www.gov.uk/government/publications/global-business-mobility-going-rates-for-eligible-occupations/global-business-mobility-going-rates-for-eligible-occupations",
        ),
        GBM_RULES,
    ),
    "overseas_service": (VISA_ELIGIBILITY,),
    "visa_fees": (VISA_FEES,),
    "visit": (
        (
            "UK visits for Swiss citizens",
            "https://www.gov.uk/guidance/visiting-the-uk-as-an-eu-eea-or-swiss-citizen",
        ),
        ("Who needs an ETA", "https://www.gov.uk/eta"),
        ETA_APPLICATION,
    ),
    "visit_activities": (
        (
            "Permitted business activities",
            "https://www.gov.uk/standard-visitor/visit-on-business",
        ),
        (
            "Switching to a work visa",
            "https://www.gov.uk/senior-specialist-worker-visa/switch-to-this-visa",
        ),
    ),
    "passport": (
        (
            "Passport and border documents",
            "https://www.gov.uk/uk-border-control/before-you-leave-for-the-uk",
        ),
        ETA_APPLICATION,
    ),
    "work_documents": (
        (
            "Work visa documents",
            "https://www.gov.uk/senior-specialist-worker-visa/documents-you-need-to-apply",
        ),
        (
            "Passport details in your UKVI account",
            "https://www.gov.uk/evisa/update-ukvi-account",
        ),
        (
            "Travelling with an eVisa",
            "https://www.gov.uk/guidance/confirm-your-immigration-status-to-your-carrier-before-travelling-to-the-uk",
        ),
    ),
    "licence": (SPONSOR_LICENCE,),
    "certificate": (SPONSOR_CERTIFICATE,),
    "skills_charge": (
        (
            "Immigration Skills Charge",
            "https://www.gov.uk/uk-visa-sponsorship-employers/immigration-skills-charge",
        ),
    ),
    "health_surcharge": (
        (
            "Health surcharge calculation",
            "https://www.gov.uk/government/publications/immigration-health-surcharge-caseworker-guidance/immigration-health-surcharge-caseworker-guidance-accessible",
        ),
        GBM_RULES,
    ),
    "health_refund": (
        (
            "Health surcharge refunds",
            "https://www.gov.uk/healthcare-immigration-application/refunds",
        ),
    ),
    "visa_timing": (
        (
            "Applying from outside the UK",
            "https://www.gov.uk/senior-specialist-worker-visa/apply-from-outside-the-uk",
        ),
        (
            "Priority visa decisions",
            "https://www.gov.uk/faster-decision-visa-settlement",
        ),
    ),
    "right_to_work": (
        (
            "Right-to-work checks",
            "https://www.gov.uk/check-job-applicant-right-to-work",
        ),
        (
            "Sponsor responsibilities",
            "https://www.gov.uk/uk-visa-sponsorship-employers/your-responsibilities",
        ),
    ),
}

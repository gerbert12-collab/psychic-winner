"""
Compound database for the radial stammbaum dashboard.

DATA INTEGRITY WARNING
----------------------
half_life and legal_status_germany below are PLACEHOLDERS unless explicitly
sourced. Values marked "VERIFY" have NOT been confirmed. Do not present this
to end users as factual harm-reduction information until each row is checked
against:
  - German BtMG Anlagen I-III (scheduled substances)
  - NpSG Stoffgruppen definitions (group bans on phenethylamine /
    cathinone core structures, in force since 2016 with later amendments)
  - EMCDDA / published pharmacokinetic literature for half_life

Schema per entry:
  name                 : str, unique, used as graph node id and edge target
  family               : str, used for angular sector + global filter
  parent               : str | None, name of the compound this derives from
                         (None marks a family root, structural_distance 0)
  half_life            : str, free text so ranges and "VERIFY" are allowed
  legal_status_germany : str, one of the LEGAL_* categories below or "VERIFY"
  structural_distance  : int 0-5, modifications away from the family root
  notes                : str, shown in the sidebar

TO ADD A NEW COMPOUND:
  Append a dict to COMPOUNDS. Ensure `parent` matches an existing `name`
  exactly, set `structural_distance` = parent's distance + 1 (or 0 for a
  new root), and assign a `family`. New families automatically receive their
  own angular sector and a checkbox in the global filter. No other code
  changes are required.
"""

# Legal status category constants (display strings).
LEGAL_BTMG = "BtMG (scheduled substance)"
LEGAL_NPSG = "NpSG (covered by group ban)"
LEGAL_UNCLEAR = "Status unclear / uncontrolled"
LEGAL_VERIFY = "VERIFY"

COMPOUNDS = [

     {"name": "Phenethylamine", "family": "Backbone", "parent": "Phenethylamine",
     "half_life": "Short", "legal_status_germany": "Uncontrolled",
     "structural_distance": 0, "notes": "Universal phenethylamine backbone."},

    # ---- Amphetamines -----------------------------------------------------
    {"name": "Amphetamine", "family": "Amphetamines", "parent": "Phenethylamine",
     "half_life": "~10-13 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Family root."},
    {"name": "Methamphetamine", "family": "Amphetamines", "parent": "Amphetamine",
     "half_life": "~9-12 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "N-methyl analogue."},
    {"name": "2-FA", "family": "Amphetamines", "parent": "Amphetamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 1, "notes": "Ring-fluorinated."},
    {"name": "3-FA", "family": "Amphetamines", "parent": "Amphetamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 1, "notes": "Ring-fluorinated."},
    {"name": "4-FA", "family": "Amphetamines", "parent": "Amphetamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 1, "notes": "Ring-fluorinated."},
    {"name": "4-MA", "family": "Amphetamines", "parent": "Amphetamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 1, "notes": "4-methyl analogue."},
    {"name": "2-FMA", "family": "Amphetamines", "parent": "Methamphetamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Fluorinated methamphetamine."},
    {"name": "4-FMA", "family": "Amphetamines", "parent": "Methamphetamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Fluorinated methamphetamine."},
    {"name": "PMA", "family": "Amphetamines", "parent": "Amphetamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "High toxicity, slow onset."},
    {"name": "PMMA", "family": "Amphetamines", "parent": "PMA",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 3, "notes": "N-methyl PMA, high toxicity."},

    # ---- Entactogens (MDxx) ----------------------------------------------
    {"name": "MDA", "family": "Entactogens", "parent": "Phenethylamine",
     "half_life": "~6-10 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Family root (methylenedioxy)."},
    {"name": "MDMA", "family": "Entactogens", "parent": "MDA",
     "half_life": "~7-9 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "N-methyl MDA."},
    {"name": "MDEA", "family": "Entactogens", "parent": "MDA",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "N-ethyl analogue."},
    {"name": "MBDB", "family": "Entactogens", "parent": "MDMA",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Alpha-ethyl homologue."},
    {"name": "6-APB", "family": "Entactogens", "parent": "MDA",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Benzofuran analogue."},
    {"name": "5-APB", "family": "Entactogens", "parent": "MDA",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Benzofuran analogue."},
    {"name": "5-MAPB", "family": "Entactogens", "parent": "5-APB",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 3, "notes": "N-methyl benzofuran."},

    # ---- Cathinones -------------------------------------------------------
    {"name": "Cathinone", "family": "Cathinones", "parent": "Phenethylamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Family root (beta-keto)."},
    {"name": "Methcathinone", "family": "Cathinones", "parent": "Cathinone",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "N-methyl cathinone."},
    {"name": "4-MMC (Mephedrone)", "family": "Cathinones", "parent": "Methcathinone",
     "half_life": "~1-2 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "4-methyl methcathinone."},
    {"name": "3-MMC", "family": "Cathinones", "parent": "Methcathinone",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "3-methyl positional isomer."},
    {"name": "4-CMC", "family": "Cathinones", "parent": "4-MMC (Mephedrone)",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 3, "notes": "4-chloro analogue."},
    {"name": "3-CMC", "family": "Cathinones", "parent": "3-MMC",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 3, "notes": "3-chloro analogue."},
    {"name": "4-MEC", "family": "Cathinones", "parent": "4-MMC (Mephedrone)",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 3, "notes": "N-ethyl analogue."},
    {"name": "Methylone (bk-MDMA)", "family": "Cathinones", "parent": "Methcathinone",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "Beta-keto MDMA."},
    {"name": "Ethylone", "family": "Cathinones", "parent": "Methylone (bk-MDMA)",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 3, "notes": "N-ethyl methylone."},
    {"name": "Butylone", "family": "Cathinones", "parent": "Methylone (bk-MDMA)",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 3, "notes": "Alpha-ethyl homologue."},
    {"name": "Pentylone", "family": "Cathinones", "parent": "Butylone",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 4, "notes": "Alpha-propyl homologue."},

    # ---- Pyrrolidinophenones (cathinone sub-branch) -----------------------
    {"name": "Pyrovalerone", "family": "Pyrrolidinophenones", "parent": "Phenethylamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Family root (pyrrolidine + keto)."},
    {"name": "alpha-PVP", "family": "Pyrrolidinophenones", "parent": "Pyrovalerone",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "Des-methyl pyrovalerone."},
    {"name": "alpha-PHP", "family": "Pyrrolidinophenones", "parent": "alpha-PVP",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Higher homologue of alpha-PVP."},
    {"name": "MDPV", "family": "Pyrrolidinophenones", "parent": "alpha-PVP",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "Methylenedioxy pyrovalerone."},

    # ---- 2C / NBOMe (psychedelic phenethylamines) ------------------------
    {"name": "2C-B", "family": "2C / NBOMe", "parent": "Phenethylamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Family root."},
    {"name": "2C-I", "family": "2C / NBOMe", "parent": "2C-B",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 1, "notes": "Iodo analogue."},
    {"name": "2C-E", "family": "2C / NBOMe", "parent": "2C-B",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 1, "notes": "Ethyl analogue."},
    {"name": "2C-C", "family": "2C / NBOMe", "parent": "2C-B",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 1, "notes": "Chloro analogue."},
    {"name": "DOB", "family": "2C / NBOMe", "parent": "2C-B",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Alpha-methyl, very potent."},
    {"name": "DOI", "family": "2C / NBOMe", "parent": "2C-I",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Alpha-methyl iodo."},
    {"name": "DOM", "family": "2C / NBOMe", "parent": "2C-B",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Alpha-methyl methyl."},
    {"name": "25B-NBOMe", "family": "2C / NBOMe", "parent": "2C-B",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "N-benzyl, active at low doses."},
    {"name": "25I-NBOMe", "family": "2C / NBOMe", "parent": "2C-I",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "N-benzyl, active at low doses."},
    {"name": "25C-NBOMe", "family": "2C / NBOMe", "parent": "2C-C",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "N-benzyl, active at low doses."},

	    # ---- Tryptamines ------------------------------------------------------
    # NOTE: indolealkylamine backbone — chemically distinct from the
    # phenethylamine core. Rooted on "Phenethylamine" only to keep the
    # radial graph connected to the central backbone node.
    {"name": "Tryptamine", "family": "Tryptamines", "parent": "Phenethylamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_UNCLEAR,
     "structural_distance": 0, "notes": "Family root (indole-3-ethylamine)."},
    {"name": "DMT", "family": "Tryptamines", "parent": "Tryptamine",
     "half_life": "~0.2 h (very short)", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "N,N-dimethyltryptamine."},
    {"name": "5-MeO-DMT", "family": "Tryptamines", "parent": "DMT",
     "half_life": "VERIFY (short)", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "5-methoxy analogue."},
    {"name": "Bufotenin (5-HO-DMT)", "family": "Tryptamines", "parent": "DMT",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "5-hydroxy analogue."},
    {"name": "DET", "family": "Tryptamines", "parent": "DMT",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "N,N-diethyl homologue."},
    {"name": "DPT", "family": "Tryptamines", "parent": "DMT",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 2, "notes": "N,N-dipropyl homologue."},
    {"name": "DiPT", "family": "Tryptamines", "parent": "DMT",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 2, "notes": "N,N-diisopropyl; auditory-distorting."},
    {"name": "MiPT", "family": "Tryptamines", "parent": "Tryptamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "N-methyl-N-isopropyl."},
    {"name": "5-MeO-MiPT", "family": "Tryptamines", "parent": "MiPT",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 2, "notes": "5-methoxy MiPT."},
    {"name": "5-MeO-DiPT", "family": "Tryptamines", "parent": "DiPT",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 3, "notes": "5-methoxy DiPT."},
    {"name": "Psilocin (4-HO-DMT)", "family": "Tryptamines", "parent": "DMT",
     "half_life": "~1.5-3 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 2, "notes": "4-hydroxy analogue; active metabolite."},
    {"name": "Psilocybin (4-PO-DMT)", "family": "Tryptamines", "parent": "Psilocin (4-HO-DMT)",
     "half_life": "prodrug (see psilocin)", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 3, "notes": "Phosphate-ester prodrug of psilocin."},
    {"name": "4-AcO-DMT", "family": "Tryptamines", "parent": "Psilocin (4-HO-DMT)",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 3, "notes": "Acetate-ester prodrug of psilocin."},
    {"name": "4-HO-MET", "family": "Tryptamines", "parent": "Psilocin (4-HO-DMT)",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 3, "notes": "4-hydroxy N-methyl-N-ethyl."},
    {"name": "4-HO-MiPT", "family": "Tryptamines", "parent": "Psilocin (4-HO-DMT)",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 3, "notes": "4-hydroxy N-methyl-N-isopropyl."},

    # ---- Lysergamides (ergolines) ----------------------------------------
    # NOTE: tetracyclic ergoline backbone — distinct chemistry. Rooted on
    # "Phenethylamine" only as a graph-connection convention.
    {"name": "LSD", "family": "Lysergamides", "parent": "Phenethylamine",
     "half_life": "~3-5 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Family root; lysergic acid diethylamide."},
    {"name": "1P-LSD", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "1-propionyl prodrug."},
    {"name": "1cP-LSD", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "1-cyclopropanoyl prodrug."},
    {"name": "1B-LSD", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "1-butanoyl prodrug."},
    {"name": "ALD-52 (1A-LSD)", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "1-acetyl prodrug."},
    {"name": "AL-LAD", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "6-allyl-6-nor analogue."},
    {"name": "ETH-LAD", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "6-ethyl-6-nor analogue."},
    {"name": "LSZ", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "Azetidide amide variant."},
    {"name": "LSA (Ergine)", "family": "Lysergamides", "parent": "LSD",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "Lysergic acid amide; naturally occurring."},

    # ---- Scalines (mescaline series) -------------------------------------
    {"name": "Mescaline", "family": "Scalines", "parent": "Phenethylamine",
     "half_life": "~6 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Family root; 3,4,5-trimethoxyphenethylamine."},
    {"name": "Escaline", "family": "Scalines", "parent": "Mescaline",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "3-ethoxy analogue."},
    {"name": "Proscaline", "family": "Scalines", "parent": "Mescaline",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "3-propoxy analogue."},
    {"name": "Allylescaline", "family": "Scalines", "parent": "Mescaline",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "3-allyloxy analogue."},
    {"name": "Methallylescaline", "family": "Scalines", "parent": "Mescaline",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_VERIFY,
     "structural_distance": 1, "notes": "3-methallyloxy analogue."},

# ---- Arylcyclohexylamines ----------------------------------------------
    {"name": "Arylcyclohexylamines", "family": "Dissociatives", "parent": None,
     "half_life": "N/A", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 0, "notes": "Root scaffold for dissociatives."},
    
    {"name": "PCP", "family": "Dissociatives", "parent": "Arylcyclohexylamines",
     "half_life": "7-16 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "Phenylcyclohexylpiperidine. Potent NMDA antagonist."},
    
    {"name": "Ketamine", "family": "Dissociatives", "parent": "Arylcyclohexylamines",
     "half_life": "2-4 h", "legal_status_germany": LEGAL_BTMG,
     "structural_distance": 1, "notes": "2-(2-chlorophenyl)-2-(methylamino)cyclohexan-1-one."},
    
    {"name": "2-FDCK", "family": "Dissociatives", "parent": "Ketamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Fluorinated ketamine analogue."},
    
    {"name": "MXE", "family": "Dissociatives", "parent": "Ketamine",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Methoxetamine. Highly potent analogue."},
    
    {"name": "3-MeO-PCP", "family": "Dissociatives", "parent": "PCP",
     "half_life": "VERIFY", "legal_status_germany": LEGAL_NPSG,
     "structural_distance": 2, "notes": "Methoxy derivative of PCP."},

    {"name": "Benzimidazole", "family": "Nitazenes", "structural_distance": 0, "parent": None, "half_life": "N/A", "legal_status_germany": "Legal"},
    {"name": "Etonitazene", "family": "Nitazenes", "structural_distance": 1, "parent": "Benzimidazole", "half_life": "2-3h", "legal_status_germany": "Illegal"},
    {"name": "Isotonitazene", "family": "Nitazenes", "structural_distance": 1, "parent": "Benzimidazole", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Protonitazene", "family": "Nitazenes", "structural_distance": 1, "parent": "Benzimidazole", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Metonitazene", "family": "Nitazenes", "structural_distance": 1, "parent": "Benzimidazole", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Butonitazene", "family": "Nitazenes", "structural_distance": 1, "parent": "Benzimidazole", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Etodesnitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Etonitazene", "half_life": "Short", "legal_status_germany": "Illegal"},
    {"name": "Flunitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Etonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Nitazepyne", "family": "Nitazenes", "structural_distance": 2, "parent": "Isotonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "N-Desethylisotonitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Isotonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "N-Pyrrolidino-etonitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Etonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "N-Piperidino-etonitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Etonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Fluonitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Protonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Metodesnitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Metonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    {"name": "Clobenitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Isotonitazene", "half_life": "Variable", "legal_status_germany": "Illegal"},
    
    
    {"name": "Anilino-piperidine", "family": "Fentanyl", "structural_distance": 0, "parent": "Phenethylamine"},
    {"name": "Fentanyl", "family": "Fentanyl", "structural_distance": 2, "parent": "Anilino-piperidine"},
    {"name": "Acetylfentanyl", "family": "Fentanyl", "structural_distance": 3, "parent": "Fentanyl"},
    {"name": "Butyrfentanyl", "family": "Fentanyl", "structural_distance": 3, "parent": "Fentanyl"},
    {"name": "Acrylofentanyl", "family": "Fentanyl", "structural_distance": 3, "parent": "Fentanyl"},
    {"name": "Furanylfentanyl", "family": "Fentanyl", "structural_distance": 3, "parent": "Fentanyl"},
    {"name": "Fluorofentanyl", "family": "Fentanyl", "structural_distance": 3, "parent": "Fentanyl"},
    {"name": "Methoxyacetylfentanyl", "family": "Fentanyl", "structural_distance": 4, "parent": "Fluorofentanyl"},
    {"name": "Carfentanil", "family": "Fentanyl", "structural_distance": 4, "parent": "Fentanyl"},
    {"name": "Remifentanil", "family": "Fentanyl", "structural_distance": 4, "parent": "Fentanyl"},

    # --- Extended Nitazene Chain ---
    {"name": "Benzimidazole", "family": "Nitazenes", "structural_distance": 0, "parent": None},
    {"name": "Etonitazene", "family": "Nitazenes", "structural_distance": 1, "parent": "Benzimidazole"},
    {"name": "Isotonitazene", "family": "Nitazenes", "structural_distance": 1, "parent": "Benzimidazole"},
    {"name": "N-Desethylisotonitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Isotonitazene"},
    {"name": "N-Desethylprotonitazene", "family": "Nitazenes", "structural_distance": 2, "parent": "Protonitazene"},
    {"name": "N-Pyrrolidino-isotonitazene", "family": "Nitazenes", "structural_distance": 3, "parent": "N-Desethylisotonitazene"},
    {"name": "N-Piperidino-isotonitazene", "family": "Nitazenes", "structural_distance": 3, "parent": "N-Desethylisotonitazene"},


{"name": "Indole Scaffold", "family": "Synthetic Cannabinoids", "structural_distance": 0, "parent": None},
    {"name": "JWH-018", "family": "Synthetic Cannabinoids", "structural_distance": 1, "parent": "Indole Scaffold"},
    {"name": "AM-2201", "family": "Synthetic Cannabinoids", "structural_distance": 2, "parent": "JWH-018"},
    
    {"name": "Indazole Scaffold", "family": "Synthetic Cannabinoids", "structural_distance": 0, "parent": None},
    {"name": "AB-CHMINACA", "family": "Synthetic Cannabinoids", "structural_distance": 1, "parent": "Indazole Scaffold"},
    {"name": "5F-ADB", "family": "Synthetic Cannabinoids", "structural_distance": 2, "parent": "AB-CHMINACA"},
    {"name": "MDMB-CHMICA", "family": "Synthetic Cannabinoids", "structural_distance": 2, "parent": "AB-CHMINACA"},

    # --- Phytocannabinoid & Semi-Synthetic THC Alternatives ---
    {"name": "Cannabinoid Backbone", "family": "Cannabinoids", "structural_distance": 0, "parent": None},
    {"name": "THC", "family": "Cannabinoids", "structural_distance": 1, "parent": "Cannabinoid Backbone"},
    {"name": "CBD", "family": "Cannabinoids", "structural_distance": 1, "parent": "Cannabinoid Backbone"},
    {"name": "HHC", "family": "Cannabinoids", "structural_distance": 2, "parent": "THC"},
    {"name": "THCP", "family": "Cannabinoids", "structural_distance": 2, "parent": "THC"},
    {"name": "HHC-P", "family": "Cannabinoids", "structural_distance": 3, "parent": "HHC"},
    {"name": "Delta-8-THC", "family": "Cannabinoids", "structural_distance": 2, "parent": "THC"},
    {"name": "THC-O-Acetate", "family": "Cannabinoids", "structural_distance": 2, "parent": "THC"},

]




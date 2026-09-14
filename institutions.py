"""
institutions.py - Comprehensive directory and intelligent search service for
educational institutions, engineering colleges, universities, and polytechnics.
Includes detailed data for AKTU/Delhi-NCR colleges (such as ABESIT, ABES EC, AKGEC, KIET),
top national institutes (IITs, NITs, IIITs, BITS), and world universities.
"""

INSTITUTIONS_CATALOG = [
    # --- AKTU & Delhi-NCR Engineering Colleges ---
    {
        "name": "ABES Institute of Technology (ABESIT)",
        "short": "ABESIT",
        "location": "Ghaziabad, Uttar Pradesh",
        "affiliation": "AKTU / Dr. APJ Abdul Kalam Technical University",
        "tags": "abesit abes it abes institute of technology aktu ghaziabad engineering btech cse"
    },
    {
        "name": "ABES Engineering College (ABES EC)",
        "short": "ABES EC",
        "location": "Ghaziabad, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "abes ec abes engineering college aktu ghaziabad"
    },
    {
        "name": "Ajay Kumar Garg Engineering College (AKGEC)",
        "short": "AKGEC",
        "location": "Ghaziabad, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "akgec ajay kumar garg engineering college ghaziabad aktu"
    },
    {
        "name": "KIET Group of Institutions (KIET)",
        "short": "KIET",
        "location": "Ghaziabad, Uttar Pradesh",
        "affiliation": "AKTU / Deemed",
        "tags": "kiet krishna institute of engineering and technology ghaziabad aktu"
    },
    {
        "name": "JSS Academy of Technical Education (JSSATE)",
        "short": "JSSATE",
        "location": "Noida, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "jss jssate jss academy of technical education noida aktu"
    },
    {
        "name": "GL Bajaj Institute of Technology and Management",
        "short": "GL Bajaj",
        "location": "Greater Noida, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "gl bajaj glbitm greater noida aktu"
    },
    {
        "name": "Galgotias College of Engineering and Technology (GCET)",
        "short": "Galgotias College",
        "location": "Greater Noida, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "galgotias gcet galgotias college of engineering greater noida"
    },
    {
        "name": "Galgotias University",
        "short": "GU",
        "location": "Greater Noida, Uttar Pradesh",
        "affiliation": "Private University",
        "tags": "galgotias university gu greater noida"
    },
    {
        "name": "IMS Engineering College (IMSEC)",
        "short": "IMSEC",
        "location": "Ghaziabad, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "ims imsec ims engineering college ghaziabad aktu"
    },
    {
        "name": "Raj Kumar Goel Institute of Technology (RKGIT)",
        "short": "RKGIT",
        "location": "Ghaziabad, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "rkgit raj kumar goel institute of technology ghaziabad aktu"
    },
    {
        "name": "Noida Institute of Engineering and Technology (NIET)",
        "short": "NIET",
        "location": "Greater Noida, Uttar Pradesh",
        "affiliation": "Autonomous / AKTU",
        "tags": "niet noida institute of engineering and technology greater noida"
    },
    {
        "name": "Jaypee Institute of Information Technology (JIIT)",
        "short": "JIIT",
        "location": "Noida, Uttar Pradesh",
        "affiliation": "Deemed University",
        "tags": "jiit jaypee noida sector 62 sector 128 deemed"
    },
    {
        "name": "Inderprastha Engineering College (IPEC)",
        "short": "IPEC",
        "location": "Ghaziabad, Uttar Pradesh",
        "affiliation": "AKTU",
        "tags": "ipec inderprastha engineering college ghaziabad"
    },
    {
        "name": "Dr. A.P.J. Abdul Kalam Technical University (AKTU)",
        "short": "AKTU",
        "location": "Lucknow, Uttar Pradesh",
        "affiliation": "State Technical University",
        "tags": "aktu uptu abdul kalam technical university lucknow uttar pradesh"
    },
    {
        "name": "Harcourt Butler Technical University (HBTU)",
        "short": "HBTU",
        "location": "Kanpur, Uttar Pradesh",
        "affiliation": "State University",
        "tags": "hbtu hbti harcourt butler technical university kanpur"
    },
    {
        "name": "Madan Mohan Malaviya University of Technology (MMMUT)",
        "short": "MMMUT",
        "location": "Gorakhpur, Uttar Pradesh",
        "affiliation": "State University",
        "tags": "mmmut mmec gorakhpur malaviya"
    },

    # --- Delhi Technical Universities & Colleges ---
    {
        "name": "Delhi Technological University (DTU / DCE)",
        "short": "DTU",
        "location": "New Delhi, Delhi",
        "affiliation": "State University",
        "tags": "dtu dce delhi technological university delhi college of engineering"
    },
    {
        "name": "Netaji Subhas University of Technology (NSUT / NSIT)",
        "short": "NSUT",
        "location": "New Delhi, Delhi",
        "affiliation": "State University",
        "tags": "nsut nsit netaji subhas university of technology dwarka delhi"
    },
    {
        "name": "Indraprastha Institute of Information Technology Delhi (IIIT-Delhi)",
        "short": "IIIT Delhi",
        "location": "New Delhi, Delhi",
        "affiliation": "State University",
        "tags": "iiit delhi iiitd okhla phase 3"
    },
    {
        "name": "Indira Gandhi Delhi Technical University for Women (IGDTUW)",
        "short": "IGDTUW",
        "location": "New Delhi, Delhi",
        "affiliation": "State University",
        "tags": "igdtuw igit kashmere gate women delhi"
    },
    {
        "name": "Guru Gobind Singh Indraprastha University (GGSIPU)",
        "short": "IP University",
        "location": "New Delhi, Delhi",
        "affiliation": "State University",
        "tags": "ipu ggsipu guru gobind singh indraprastha university dwarka delhi"
    },
    {
        "name": "Maharaja Agrasen Institute of Technology (MAIT)",
        "short": "MAIT",
        "location": "Rohini, New Delhi",
        "affiliation": "GGSIPU",
        "tags": "mait maharaja agrasen institute of technology rohini ipu"
    },
    {
        "name": "Maharaja Surajmal Institute of Technology (MSIT)",
        "short": "MSIT",
        "location": "Janakpuri, New Delhi",
        "affiliation": "GGSIPU",
        "tags": "msit maharaja surajmal institute of technology janakpuri ipu"
    },
    {
        "name": "Bharati Vidyapeeth's College of Engineering (BVCOE)",
        "short": "BVCOE Delhi",
        "location": "Paschim Vihar, New Delhi",
        "affiliation": "GGSIPU",
        "tags": "bvcoe bharati vidyapeeth paschim vihar ipu"
    },
    {
        "name": "Bhagwan Parshuram Institute of Technology (BPIT)",
        "short": "BPIT",
        "location": "Rohini, New Delhi",
        "affiliation": "GGSIPU",
        "tags": "bpit bhagwan parshuram rohini ipu"
    },
    {
        "name": "University of Delhi (DU)",
        "short": "DU",
        "location": "New Delhi, Delhi",
        "affiliation": "Central University",
        "tags": "du delhi university north campus south campus cic dduc hansraj hindu st stephens"
    },
    {
        "name": "Jawaharlal Nehru University (JNU)",
        "short": "JNU",
        "location": "New Delhi, Delhi",
        "affiliation": "Central University",
        "tags": "jnu jawaharlal nehru university delhi scss"
    },
    {
        "name": "Jamia Millia Islamia (JMI)",
        "short": "JMI",
        "location": "New Delhi, Delhi",
        "affiliation": "Central University",
        "tags": "jmi jamia millia islamia okhla delhi engineering fet"
    },

    # --- Private Universities in NCR ---
    {
        "name": "Amity University Uttar Pradesh",
        "short": "Amity Noida",
        "location": "Noida, Uttar Pradesh",
        "affiliation": "Private University",
        "tags": "amity university noida auup"
    },
    {
        "name": "Shiv Nadar University (SNU)",
        "short": "SNU",
        "location": "Greater Noida, Uttar Pradesh",
        "affiliation": "Private University / Institute of Eminence",
        "tags": "snu shiv nadar university dadri greater noida"
    },
    {
        "name": "Bennett University",
        "short": "Bennett",
        "location": "Greater Noida, Uttar Pradesh",
        "affiliation": "Times Group / Private University",
        "tags": "bennett university greater noida times group"
    },
    {
        "name": "Sharda University",
        "short": "Sharda",
        "location": "Greater Noida, Uttar Pradesh",
        "affiliation": "Private University",
        "tags": "sharda university knowledge park greater noida"
    },

    # --- Indian Institutes of Technology (IITs) ---
    {
        "name": "Indian Institute of Technology Delhi (IIT Delhi)",
        "short": "IITD",
        "location": "Hauz Khas, New Delhi",
        "affiliation": "Institute of National Importance",
        "tags": "iit delhi iitd hauz khas"
    },
    {
        "name": "Indian Institute of Technology Bombay (IIT Bombay)",
        "short": "IITB",
        "location": "Powai, Mumbai, Maharashtra",
        "affiliation": "Institute of National Importance",
        "tags": "iit bombay iitb powai mumbai"
    },
    {
        "name": "Indian Institute of Technology Kanpur (IIT Kanpur)",
        "short": "IITK",
        "location": "Kanpur, Uttar Pradesh",
        "affiliation": "Institute of National Importance",
        "tags": "iit kanpur iitk kalyanpur uttar pradesh"
    },
    {
        "name": "Indian Institute of Technology Madras (IIT Madras)",
        "short": "IITM",
        "location": "Chennai, Tamil Nadu",
        "affiliation": "Institute of National Importance",
        "tags": "iit madras iitm chennai adyar"
    },
    {
        "name": "Indian Institute of Technology Kharagpur (IIT Kharagpur)",
        "short": "IITKGP",
        "location": "Kharagpur, West Bengal",
        "affiliation": "Institute of National Importance",
        "tags": "iit kharagpur iitkgp kgp"
    },
    {
        "name": "Indian Institute of Technology Roorkee (IIT Roorkee)",
        "short": "IITR",
        "location": "Roorkee, Uttarakhand",
        "affiliation": "Institute of National Importance",
        "tags": "iit roorkee iitr thomason college"
    },
    {
        "name": "Indian Institute of Technology Guwahati (IIT Guwahati)",
        "short": "IITG",
        "location": "Guwahati, Assam",
        "affiliation": "Institute of National Importance",
        "tags": "iit guwahati iitg"
    },
    {
        "name": "Indian Institute of Technology (BHU) Varanasi",
        "short": "IIT BHU",
        "location": "Varanasi, Uttar Pradesh",
        "affiliation": "Institute of National Importance",
        "tags": "iit bhu bhu varanasi it bhu"
    },
    {
        "name": "Indian Institute of Technology Hyderabad (IIT Hyderabad)",
        "short": "IITH",
        "location": "Kandi, Sangareddy, Telangana",
        "affiliation": "Institute of National Importance",
        "tags": "iit hyderabad iith kandi"
    },
    {
        "name": "Indian Institute of Technology Indore (IIT Indore)",
        "short": "IITI",
        "location": "Indore, Madhya Pradesh",
        "affiliation": "Institute of National Importance",
        "tags": "iit indore iiti simrol"
    },
    {
        "name": "Indian Institute of Technology Gandhinagar (IITGN)",
        "short": "IITGN",
        "location": "Gandhinagar, Gujarat",
        "affiliation": "Institute of National Importance",
        "tags": "iit gandhinagar iitgn palaj"
    },

    # --- National Institutes of Technology (NITs) ---
    {
        "name": "National Institute of Technology Tiruchirappalli (NIT Trichy)",
        "short": "NITT",
        "location": "Tiruchirappalli, Tamil Nadu",
        "affiliation": "Institute of National Importance",
        "tags": "nit trichy nitt nit tiruchirappalli"
    },
    {
        "name": "National Institute of Technology Karnataka (NITK Surathkal)",
        "short": "NITK",
        "location": "Surathkal, Mangalore, Karnataka",
        "affiliation": "Institute of National Importance",
        "tags": "nitk surathkal nit karnataka mangalore"
    },
    {
        "name": "National Institute of Technology Rourkela (NIT Rourkela)",
        "short": "NITR",
        "location": "Rourkela, Odisha",
        "affiliation": "Institute of National Importance",
        "tags": "nit rourkela nitr odisha"
    },
    {
        "name": "National Institute of Technology Warangal (NIT Warangal)",
        "short": "NITW",
        "location": "Warangal, Telangana",
        "affiliation": "Institute of National Importance",
        "tags": "nit warangal nitw rec warangal"
    },
    {
        "name": "Motilal Nehru National Institute of Technology Allahabad (MNNIT)",
        "short": "MNNIT",
        "location": "Prayagraj / Allahabad, Uttar Pradesh",
        "affiliation": "Institute of National Importance",
        "tags": "mnnit allahabad mnnit prayagraj nit allahabad mnrec"
    },
    {
        "name": "National Institute of Technology Calicut (NITC)",
        "short": "NITC",
        "location": "Kozhikode, Kerala",
        "affiliation": "Institute of National Importance",
        "tags": "nit calicut nitc kerala"
    },
    {
        "name": "Visvesvaraya National Institute of Technology (VNIT Nagpur)",
        "short": "VNIT",
        "location": "Nagpur, Maharashtra",
        "affiliation": "Institute of National Importance",
        "tags": "vnit nagpur nit nagpur"
    },
    {
        "name": "Malaviya National Institute of Technology Jaipur (MNIT Jaipur)",
        "short": "MNIT",
        "location": "Jaipur, Rajasthan",
        "affiliation": "Institute of National Importance",
        "tags": "mnit jaipur nit jaipur"
    },
    {
        "name": "Maulana Azad National Institute of Technology (MANIT Bhopal)",
        "short": "MANIT",
        "location": "Bhopal, Madhya Pradesh",
        "affiliation": "Institute of National Importance",
        "tags": "manit bhopal nit bhopal"
    },
    {
        "name": "National Institute of Technology Kurukshetra (NIT Kurukshetra)",
        "short": "NITKKR",
        "location": "Kurukshetra, Haryana",
        "affiliation": "Institute of National Importance",
        "tags": "nit kkr nit kurukshetra haryana"
    },
    {
        "name": "Dr. B R Ambedkar National Institute of Technology Jalandhar (NITJ)",
        "short": "NIT Jalandhar",
        "location": "Jalandhar, Punjab",
        "affiliation": "Institute of National Importance",
        "tags": "nit jalandhar nitj punjab"
    },

    # --- IIITs & BITS ---
    {
        "name": "BITS Pilani (Birla Institute of Technology and Science)",
        "short": "BITS Pilani",
        "location": "Pilani, Rajasthan",
        "affiliation": "Deemed University / IoE",
        "tags": "bits pilani birla institute pilani rajasthan"
    },
    {
        "name": "BITS Pilani, K. K. Birla Goa Campus",
        "short": "BITS Goa",
        "location": "Zuarinagar, Goa",
        "affiliation": "Deemed University",
        "tags": "bits goa bits pilani goa zuarinagar"
    },
    {
        "name": "BITS Pilani, Hyderabad Campus",
        "short": "BITS Hyderabad",
        "location": "Jawahar Nagar, Hyderabad, Telangana",
        "affiliation": "Deemed University",
        "tags": "bits hyderabad bphc bits pilani hyderabad"
    },
    {
        "name": "Indian Institute of Information Technology Allahabad (IIIT Allahabad)",
        "short": "IIITA",
        "location": "Prayagraj, Uttar Pradesh",
        "affiliation": "Institute of National Importance",
        "tags": "iiit allahabad iiita jhalwa prayagraj"
    },
    {
        "name": "International Institute of Information Technology Hyderabad (IIIT-H)",
        "short": "IIIT Hyderabad",
        "location": "Gachibowli, Hyderabad, Telangana",
        "affiliation": "Autonomous University",
        "tags": "iiit hyderabad iiith gachibowli cse research"
    },
    {
        "name": "International Institute of Information Technology Bangalore (IIIT-B)",
        "short": "IIIT Bangalore",
        "location": "Electronic City, Bangalore, Karnataka",
        "affiliation": "Deemed University",
        "tags": "iiit bangalore iiitb electronic city"
    },

    # --- Top Private & State Tech Colleges Across India ---
    {
        "name": "Vellore Institute of Technology (VIT Vellore)",
        "short": "VIT",
        "location": "Vellore, Tamil Nadu",
        "affiliation": "Deemed University",
        "tags": "vit vellore vellore institute of technology vit chennai vit ap vit bhopal"
    },
    {
        "name": "SRM Institute of Science and Technology (SRMIST)",
        "short": "SRM",
        "location": "Kattankulathur, Chennai, Tamil Nadu",
        "affiliation": "Deemed University",
        "tags": "srm srmist kattankulathur ramapuram srm university"
    },
    {
        "name": "Thapar Institute of Engineering and Technology (TIET)",
        "short": "Thapar",
        "location": "Patiala, Punjab",
        "affiliation": "Deemed University",
        "tags": "thapar tiet patiala thapar university punjab"
    },
    {
        "name": "Manipal Academy of Higher Education (MAHE / MIT Manipal)",
        "short": "Manipal",
        "location": "Manipal, Karnataka",
        "affiliation": "Deemed University",
        "tags": "manipal mit manipal mahe karnataka"
    },
    {
        "name": "Kalinga Institute of Industrial Technology (KIIT)",
        "short": "KIIT University",
        "location": "Bhubaneswar, Odisha",
        "affiliation": "Deemed University",
        "tags": "kiit university bhubaneswar odisha"
    },
    {
        "name": "Chandigarh University (CU)",
        "short": "Chandigarh University",
        "location": "Mohali, Punjab",
        "affiliation": "Private University",
        "tags": "chandigarh university cu mohali punjab gharuan"
    },
    {
        "name": "Lovely Professional University (LPU)",
        "short": "LPU",
        "location": "Phagwara, Punjab",
        "affiliation": "Private University",
        "tags": "lpu lovely professional university jalandhar phagwara"
    },
    {
        "name": "College of Engineering, Pune (COEP)",
        "short": "COEP",
        "location": "Shivajinagar, Pune, Maharashtra",
        "affiliation": "Autonomous University",
        "tags": "coep college of engineering pune shivajinagar maharashtra"
    },
    {
        "name": "Veermata Jijabai Technological Institute (VJTI)",
        "short": "VJTI",
        "location": "Matunga, Mumbai, Maharashtra",
        "affiliation": "Autonomous / Mumbai University",
        "tags": "vjti veermata jijabai matunga mumbai"
    },
    {
        "name": "RV College of Engineering (RVCE)",
        "short": "RVCE",
        "location": "Bangalore, Karnataka",
        "affiliation": "Autonomous / VTU",
        "tags": "rvce rv college of engineering bangalore vtu"
    },
    {
        "name": "BMS College of Engineering (BMSCE)",
        "short": "BMSCE",
        "location": "Basavanagudi, Bangalore, Karnataka",
        "affiliation": "Autonomous / VTU",
        "tags": "bmsce bms college of engineering bangalore"
    },
    {
        "name": "M. S. Ramaiah Institute of Technology (MSRIT)",
        "short": "Ramaiah",
        "location": "Bangalore, Karnataka",
        "affiliation": "Autonomous / VTU",
        "tags": "msrit ramaiah institute of technology bangalore"
    },
    {
        "name": "PSG College of Technology",
        "short": "PSG Tech",
        "location": "Coimbatore, Tamil Nadu",
        "affiliation": "Autonomous / Anna University",
        "tags": "psg psg tech coimbatore tamil nadu"
    },
    {
        "name": "Anna University (CEG Guindy)",
        "short": "Anna University",
        "location": "Guindy, Chennai, Tamil Nadu",
        "affiliation": "State University",
        "tags": "anna university ceg college of engineering guindy chennai"
    },
    {
        "name": "Jadavpur University (Faculty of Engineering)",
        "short": "Jadavpur",
        "location": "Kolkata, West Bengal",
        "affiliation": "State University",
        "tags": "jadavpur university ju kolkata west bengal"
    },

    # --- Top Global Universities ---
    {
        "name": "Massachusetts Institute of Technology (MIT)",
        "short": "MIT",
        "location": "Cambridge, Massachusetts, USA",
        "affiliation": "Private Research University",
        "tags": "mit massachusetts institute of technology usa boston"
    },
    {
        "name": "Stanford University",
        "short": "Stanford",
        "location": "Stanford, California, USA",
        "affiliation": "Private Research University",
        "tags": "stanford university silicon valley california usa"
    },
    {
        "name": "Harvard University",
        "short": "Harvard",
        "location": "Cambridge, Massachusetts, USA",
        "affiliation": "Ivy League",
        "tags": "harvard university ivy league cambridge usa"
    },
    {
        "name": "University of California, Berkeley (UC Berkeley)",
        "short": "UC Berkeley",
        "location": "Berkeley, California, USA",
        "affiliation": "Public Research University",
        "tags": "uc berkeley cal california berkeley usa"
    },
    {
        "name": "Carnegie Mellon University (CMU)",
        "short": "CMU",
        "location": "Pittsburgh, Pennsylvania, USA",
        "affiliation": "Private Research University",
        "tags": "cmu carnegie mellon computer science pittsburgh usa"
    },
    {
        "name": "University of Oxford",
        "short": "Oxford",
        "location": "Oxford, Oxfordshire, United Kingdom",
        "affiliation": "Collegiate Research University",
        "tags": "oxford university of oxford uk england"
    },
    {
        "name": "University of Cambridge",
        "short": "Cambridge",
        "location": "Cambridge, Cambridgeshire, United Kingdom",
        "affiliation": "Collegiate Research University",
        "tags": "cambridge university of cambridge uk england"
    },
    {
        "name": "National University of Singapore (NUS)",
        "short": "NUS",
        "location": "Singapore",
        "affiliation": "Autonomous Research University",
        "tags": "nus national university of singapore asia"
    },
    {
        "name": "University of Toronto",
        "short": "U of T",
        "location": "Toronto, Ontario, Canada",
        "affiliation": "Public Research University",
        "tags": "utoronto university of toronto canada ontario"
    }
]

def search_institutions(query: str, limit: int = 12):
    if not query or not query.strip():
        return INSTITUTIONS_CATALOG[:limit]

    q = query.strip().lower()
    exact_matches = []
    prefix_matches = []
    sub_matches = []
    tag_matches = []

    for inst in INSTITUTIONS_CATALOG:
        name_lower = inst["name"].lower()
        short_lower = inst["short"].lower()
        tags_lower = inst.get("tags", "").lower()

        if short_lower == q or name_lower == q:
            exact_matches.append(inst)
        elif short_lower.startswith(q) or name_lower.startswith(q):
            prefix_matches.append(inst)
        elif q in short_lower or q in name_lower:
            sub_matches.append(inst)
        elif q in tags_lower or q in inst["location"].lower() or q in inst.get("affiliation", "").lower():
            tag_matches.append(inst)

    combined = exact_matches + prefix_matches + sub_matches + tag_matches
    seen = set()
    results = []
    for item in combined:
        if item["name"] not in seen:
            seen.add(item["name"])
            results.append(item)
            if len(results) >= limit:
                break

    return results

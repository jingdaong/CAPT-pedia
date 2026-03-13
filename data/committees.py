"""
CAPT (College of Alice & Peter Tan) committee data.

Each committee entry contains:
- name:        Display name of the committee
- short_name:  Short identifier used in callback data
- overview:    Brief description of what the committee does
- ig_handle:   Instagram handle (empty string if not available)
- tele_handle: Telegram channel/group handle (empty string if not available)
- website:     Website URL (empty string if not available)
- directors:   List of {name, tele_handle} dicts for current directors/ExCo leads
- faqs:        List of {question, answer} dicts of frequently asked questions
"""

COMMITTEES: list[dict] = [
    {
        "name": "Student Executive Committee (SExC)",
        "short_name": "sexc",
        "overview": (
            "The Student Executive Committee (SExC) is the main student governance body "
            "of CAPT. It oversees all other sub-committees and represents the student "
            "body in liaising with college management. SExC organises college-wide events "
            "and is the go-to committee for general administrative matters."
        ),
        "ig_handle": "@capt.sexc",
        "tele_handle": "@captSExC",
        "website": "https://capt.nus.edu.sg",
        "directors": [
            {"name": "President", "tele_handle": "@capt_president"},
            {"name": "Vice-President (Internal)", "tele_handle": "@capt_vpi"},
            {"name": "Vice-President (External)", "tele_handle": "@capt_vpe"},
        ],
        "faqs": [
            {
                "question": "How do I join SExC?",
                "answer": (
                    "Recruitment for SExC takes place at the start of each academic year. "
                    "Look out for open recruitment posts on the CAPT SExC Instagram page "
                    "or Telegram channel. You can also reach out directly to any of the "
                    "directors listed above."
                ),
            },
            {
                "question": "What events does SExC organise?",
                "answer": (
                    "SExC organises major college-wide events such as CAPT Day, Freshmen "
                    "Orientation Camp (FOC), Inter-College Games (ICG) and town halls. "
                    "It also coordinates activities with other Residential Colleges."
                ),
            },
            {
                "question": "How can I raise a feedback or suggestion?",
                "answer": (
                    "You can approach any SExC member directly or submit feedback "
                    "through our anonymous feedback form linked in our Instagram bio. "
                    "You can also use the 'Ask a Question' feature in this bot to send "
                    "an anonymous message to SExC."
                ),
            },
        ],
    },
    {
        "name": "Academic Committee (AcaCom)",
        "short_name": "acacom",
        "overview": (
            "AcaCom promotes academic excellence and a culture of learning within CAPT. "
            "It organises study sessions, peer tutoring, academic workshops, and connects "
            "residents with academic resources. AcaCom also coordinates with NUS faculty "
            "for college-level academic talks and seminars."
        ),
        "ig_handle": "@capt.acacom",
        "tele_handle": "@captAcaCom",
        "website": "",
        "directors": [
            {"name": "AcaCom Director", "tele_handle": "@capt_acadir"},
        ],
        "faqs": [
            {
                "question": "Does AcaCom offer tutoring or study groups?",
                "answer": (
                    "Yes! AcaCom organises peer tutoring matching and module-specific "
                    "study groups each semester. Check our Telegram channel for the "
                    "latest sign-up links."
                ),
            },
            {
                "question": "What academic workshops does AcaCom run?",
                "answer": (
                    "AcaCom runs workshops on academic writing, research skills, time "
                    "management, and exam preparation throughout the year. Dates are "
                    "announced on our Instagram page."
                ),
            },
            {
                "question": "Can I suggest a workshop topic?",
                "answer": (
                    "Absolutely! DM our Instagram page or use the 'Ask a Question' "
                    "feature in this bot to send your suggestion to the AcaCom team."
                ),
            },
        ],
    },
    {
        "name": "Arts Committee (ArtsCom)",
        "short_name": "artscom",
        "overview": (
            "ArtsCom nurtures the creative and artistic spirit of CAPT residents. "
            "It organises concerts, art exhibitions, drama productions, open-mic nights, "
            "and collaborations with external arts groups. ArtsCom welcomes residents of "
            "all artistic backgrounds and skill levels."
        ),
        "ig_handle": "@capt.artscom",
        "tele_handle": "@captArtsCom",
        "website": "",
        "directors": [
            {"name": "ArtsCom Director", "tele_handle": "@capt_artsdir"},
        ],
        "faqs": [
            {
                "question": "Do I need prior experience to join ArtsCom?",
                "answer": (
                    "Not at all! ArtsCom welcomes everyone regardless of experience. "
                    "Whether you are a seasoned performer or a curious beginner, there "
                    "is a place for you."
                ),
            },
            {
                "question": "What kind of performances does ArtsCom organise?",
                "answer": (
                    "ArtsCom organises a variety of events including musical concerts, "
                    "theatre productions, art exhibitions, open-mic nights, and creative "
                    "writing showcases."
                ),
            },
        ],
    },
    {
        "name": "Sports Committee (SportsCom)",
        "short_name": "sportscom",
        "overview": (
            "SportsCom promotes a healthy and active lifestyle among CAPT residents. "
            "It manages CAPT's sports facilities booking, organises intra-college sports "
            "events, and represents CAPT in inter-college competitions such as ICG "
            "(Inter-College Games). SportsCom also runs regular fitness sessions and "
            "recreational sporting activities."
        ),
        "ig_handle": "@capt.sportscom",
        "tele_handle": "@captSportsCom",
        "website": "",
        "directors": [
            {"name": "SportsCom Director", "tele_handle": "@capt_sportsdir"},
        ],
        "faqs": [
            {
                "question": "How do I sign up for ICG (Inter-College Games)?",
                "answer": (
                    "ICG sign-ups are usually announced on our Instagram and Telegram "
                    "channel at the start of each semester. Keep an eye out for "
                    "registration links!"
                ),
            },
            {
                "question": "How do I book sports facilities?",
                "answer": (
                    "Facility bookings are managed through the NUS OSA booking portal. "
                    "SportsCom also organises block bookings for popular time slots — "
                    "check our Telegram channel for shared booking slots."
                ),
            },
            {
                "question": "What sports does CAPT compete in for ICG?",
                "answer": (
                    "CAPT participates in a wide range of ICG sports including football, "
                    "basketball, volleyball, badminton, swimming, frisbee, and more. "
                    "The full list varies each year."
                ),
            },
        ],
    },
    {
        "name": "Welfare Committee (WelfareCom)",
        "short_name": "welfarecom",
        "overview": (
            "WelfareCom looks after the well-being of all CAPT residents. It organises "
            "welfare drives, distributes care packs during exam periods, runs mental "
            "health awareness initiatives, and ensures residents feel supported and "
            "valued throughout their stay."
        ),
        "ig_handle": "@capt.welfarecom",
        "tele_handle": "@captWelfareCom",
        "website": "",
        "directors": [
            {"name": "WelfareCom Director", "tele_handle": "@capt_welfaredir"},
        ],
        "faqs": [
            {
                "question": "Does WelfareCom provide care packs during exams?",
                "answer": (
                    "Yes! WelfareCom distributes care packs to residents before major "
                    "examination periods (mid-terms and finals). Look out for "
                    "announcements on our Instagram page."
                ),
            },
            {
                "question": "What mental health resources are available?",
                "answer": (
                    "WelfareCom works with NUS Counselling & Psychological Services "
                    "(CPS) and organises regular wellness activities. If you need "
                    "immediate support, please reach out to NUS CPS at "
                    "https://nus.edu.sg/alc/cps or call 6516-2376."
                ),
            },
            {
                "question": "How can I suggest a welfare initiative?",
                "answer": (
                    "DM our Instagram or use the 'Ask a Question' feature in this bot "
                    "to share your idea with the WelfareCom team!"
                ),
            },
        ],
    },
    {
        "name": "Publicity Committee (PubCom)",
        "short_name": "pubcom",
        "overview": (
            "PubCom is the creative arm of CAPT, responsible for producing all visual "
            "and media content for the college. From event posters to photography and "
            "videography, PubCom tells the story of life at CAPT through design and media."
        ),
        "ig_handle": "@capt.pubcom",
        "tele_handle": "@captPubCom",
        "website": "",
        "directors": [
            {"name": "PubCom Director", "tele_handle": "@capt_pubdir"},
        ],
        "faqs": [
            {
                "question": "What skills do I need to join PubCom?",
                "answer": (
                    "PubCom welcomes graphic designers, photographers, videographers, "
                    "and copywriters. Experience with Adobe Photoshop, Illustrator, "
                    "Premiere Pro or Canva is helpful but not required — we provide "
                    "training!"
                ),
            },
            {
                "question": "Can I request PubCom to cover my event?",
                "answer": (
                    "Yes! Reach out to our Director via Telegram or DM our Instagram "
                    "page at least 1 week in advance so we can schedule a photographer "
                    "or videographer for your event."
                ),
            },
        ],
    },
    {
        "name": "Environment Committee (EnvCom)",
        "short_name": "envcom",
        "overview": (
            "EnvCom champions sustainability and environmental consciousness within CAPT "
            "and the wider NUS community. It organises eco-friendly initiatives, "
            "upcycling workshops, community gardens, and collaborates with NUS "
            "Sustainability to make CAPT a greener place to live."
        ),
        "ig_handle": "@capt.envcom",
        "tele_handle": "@captEnvCom",
        "website": "",
        "directors": [
            {"name": "EnvCom Director", "tele_handle": "@capt_envdir"},
        ],
        "faqs": [
            {
                "question": "How can I get involved in EnvCom initiatives?",
                "answer": (
                    "Follow our Instagram page for updates on upcoming activities like "
                    "community gardening sessions, recycling drives, and sustainability "
                    "workshops. You can join as a member or just participate in events!"
                ),
            },
            {
                "question": "Does CAPT have recycling facilities?",
                "answer": (
                    "Yes! CAPT has designated recycling points for paper, plastic, and "
                    "e-waste. EnvCom also organises periodic clothing swap and upcycling "
                    "events. Check our Instagram for locations and schedules."
                ),
            },
        ],
    },
    {
        "name": "Dialogue Committee (DiaCom)",
        "short_name": "diacom",
        "overview": (
            "DiaCom fosters meaningful conversations and community cohesion at CAPT. "
            "It organises town halls, inter-cultural dialogues, discussion forums, and "
            "facilitated conversations on topics that matter to residents. DiaCom is "
            "the voice of civil discourse within the college."
        ),
        "ig_handle": "@capt.diacom",
        "tele_handle": "@captDiaCom",
        "website": "",
        "directors": [
            {"name": "DiaCom Director", "tele_handle": "@capt_diadir"},
        ],
        "faqs": [
            {
                "question": "How do DiaCom town halls work?",
                "answer": (
                    "Town halls are open forums where residents can raise issues, give "
                    "feedback, and discuss college life with SExC and college management. "
                    "DiaCom facilitates these sessions and ensures all voices are heard."
                ),
            },
            {
                "question": "Can I propose a dialogue topic?",
                "answer": (
                    "Definitely! DM our Instagram or use the 'Ask a Question' feature "
                    "in this bot to suggest a topic for a future dialogue session."
                ),
            },
        ],
    },
]

# Build a lookup dictionary keyed by short_name for fast access
COMMITTEES_BY_KEY: dict[str, dict] = {c["short_name"]: c for c in COMMITTEES}

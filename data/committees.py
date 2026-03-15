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

Source: CAPT 14th CSC Mass Rec Catalogue AY25/26
"""

COMMITTEES: list[dict] = [
    {
        "name": "CSC Secretariat",
        "short_name": "csc_secretariat",
        "overview": (
            "The CSC Secretariat is a subsidiary of the Standing Committee and "
            "is responsible for administrative and finance matters across CSC "
            "committees. It maintains high standards in PDPA and treasury "
            "management while streamlining workflows to support the student body."
        ),
        "ig_handle": "@capt_csc_secretariat",
        "tele_handle": "@capt_csc_secretariat",
        "website": "",
        "directors": [{"name": "John Doe", "tele_handle": "@john_doe"},
                      {"name": "Jane Smith", "tele_handle": "@jane_smith"}],
        "faqs": [],
    },
    {
        "name": "Active Community Engagement (ACE)",
        "short_name": "ace",
        "overview": (
            "ACE provides CAPTains with sustained platforms to engage and build "
            "relationships with community partners through meaningful, long-term "
            "interaction. The wing focuses on mutual learning, empathy, and "
            "empowerment across diverse communities."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "External Affairs Committee (EXA)",
        "short_name": "exa",
        "overview": (
            "EXA engages CAPT alumni through events and supports graduating "
            "CAPTains in transitioning into alumni life. It is also the main "
            "liaison between CAPT and other residential colleges, organizing "
            "inter-college initiatives to strengthen community ties."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Social Innovation (SI)",
        "short_name": "si",
        "overview": (
            "The Social Innovation wing addresses social problems by empathizing "
            "with community needs and testing human-centered solutions. Guided by "
            "innovation frameworks, SI aims to create sustainable long-term impact."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Clubs & Societies (ClubSocs)",
        "short_name": "clubsocs",
        "overview": (
            "ClubSocs is the heart of CAPT's arts and culture scene. It supports "
            "interest groups such as CAPTunes, CAPTinSYNC, CAPT Coffee, CAPT "
            "Baking, and CAPT Cooking, while organizing college-wide arts events."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Publicity Committee",
        "short_name": "pubcom",
        "overview": (
            "Publicity drives CAPT storytelling and creative communications, from "
            "content and copywriting to design, social coverage, and web presence. "
            "The committee supports CAPT's identity across digital and physical media."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Sports Committee",
        "short_name": "sportscom",
        "overview": (
            "Sports Committee plans and executes CAPT sports events and outreach, "
            "including major inter-house and college-wide sports initiatives. It "
            "builds participation, bonding, and a strong active culture in CAPT."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Student Affairs Committee (SAC)",
        "short_name": "sac",
        "overview": (
            "SAC builds a vibrant and inclusive CAPT community through student "
            "life and welfare events across the academic year. Signature efforts "
            "include Inter-Neighbourhood Shield, welfare initiatives, and bonding "
            "activities that strengthen house connections."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Freshman Orientation Camp (FOC)",
        "short_name": "foc",
        "overview": (
            "FOC plans and runs CAPT's freshman orientation experience. The team "
            "designs a meaningful and engaging onboarding journey for incoming "
            "students while building a strong, supportive batch culture."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPT Ambassadors",
        "short_name": "capt_ambassadors",
        "overview": (
            "CAPT Ambassadors represent the college to guests and visitors through "
            "tours and outreach events such as Family Night and Open House. The "
            "committee develops communication and hosting skills while sharing CAPT "
            "stories with the wider community."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPTSLAM Queensway",
        "short_name": "captslam_queensway",
        "overview": (
            "CAPTSLAM Queensway is a leadership mentoring program for Secondary 3 "
            "student leaders from Queensway Secondary School. It includes team "
            "activities, reflection sessions, mentorship, and an overseas component."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPTSLAM Townsquare",
        "short_name": "captslam_townsquare",
        "overview": (
            "CAPTSLAM Townsquare mentors Secondary 2 student leaders from New "
            "Town Secondary School through value-driven engagement and leadership "
            "development, culminating in an overseas service-learning experience."
        ),
        "ig_handle": "@captslam.townsquare",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPT Kamal",
        "short_name": "capt_kamal",
        "overview": (
            "CAPT Kamal is a year-long committee that plans and runs a two-week "
            "overseas program for communities from socio-economically disadvantaged "
            "backgrounds, with a focus on empowerment and mutual growth."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPT Support",
        "short_name": "capt_support",
        "overview": (
            "CAPT Support raises awareness of mental health and well-being through "
            "training, workshops, campaigns, and peer support initiatives. The "
            "committee equips CAPTains to care for themselves and others while "
            "fostering a culture of empathy and support."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPT In Prayer",
        "short_name": "capt_in_prayer",
        "overview": (
            "CAPT In Prayer builds a Christian support community in CAPT through "
            "worship, prayer, fellowship, outreach, and bible study initiatives. "
            "It focuses on shepherding leaders and creating safe spaces for faith "
            "conversations in college life."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Tech Comm",
        "short_name": "tech_comm",
        "overview": (
            "Tech Comm develops and maintains digital solutions to improve student "
            "life in CAPT. It brings together product, innovation, and development "
            "workstreams to solve pain points across committees."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Roc House Committee",
        "short_name": "roc_hc",
        "overview": (
            "Roc House Committee fosters a lively and inclusive house culture "
            "through sports, music, social activities, welfare, and community "
            "bonding, with the goal of making Roc one big family."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Dragon House Committee",
        "short_name": "dragon_hc",
        "overview": (
            "Dragon House Committee plans house activities, creates social content, "
            "and drives welfare initiatives to keep the house welcoming, vibrant, "
            "and closely knit."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Garuda House Committee",
        "short_name": "garuda_hc",
        "overview": (
            "Garuda House Committee builds house spirit through programs, publicity, "
            "admin support, and innovative initiatives, creating a warm and energetic "
            "community experience for Garudians."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Phoenix House Committee",
        "short_name": "phoenix_hc",
        "overview": (
            "Phoenix House Committee fosters community and camaraderie through "
            "programming, welfare, publicity, and design initiatives. Its mission "
            "is to create a warm, inclusive home for all Firebirds."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Tulpar House Committee",
        "short_name": "tulpar_hc",
        "overview": (
            "Tulpar House Committee cultivates friendship, support, and belonging "
            "among Tulpies through house events, publicity, and welfare initiatives "
            "throughout the year."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
]


ACE_SUBCOMMITTEES: list[dict] = [
    {
        "name": "CAPT in Silence",
        "short_name": "ace_silence",
        "overview": (
            "CAPT in Silence engages the Deaf community and builds communication "
            "understanding so CAPTains can form meaningful long-term relationships."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPT in the Dark",
        "short_name": "ace_dark",
        "overview": (
            "CAPT in the Dark seeks to challenge perceptions of the visually "
            "impaired community while building confidence and strengths among "
            "participating students."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPTSpark",
        "short_name": "ace_captspark",
        "overview": (
            "CAPTSpark organizes activities for special needs children while "
            "equipping CAPTains with meaningful learning experiences in the "
            "special needs space."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Constellations",
        "short_name": "ace_constellations",
        "overview": (
            "Constellations empowers boys to discover their potential through "
            "different development mediums, with music as a key avenue."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "ACE Elderly",
        "short_name": "ace_elderly",
        "overview": (
            "ACE Elderly connects CAPTains with the elderly community to promote "
            "mutual empowerment, understanding, and meaningful interaction."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "ACE Homes",
        "short_name": "ace_homes",
        "overview": (
            "ACE Homes explores different forms of homelessness through "
            "befriending rough sleepers and creating intentional opportunities "
            "for interaction."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Kindle",
        "short_name": "ace_kindle",
        "overview": (
            "Through one-to-one mentoring, Kindle helps mentors nurture confidence "
            "and social-emotional growth in mentees."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Kindle+",
        "short_name": "ace_kindle_plus",
        "overview": (
            "Kindle+ focuses on meaningful values formation and growth among "
            "foster youths through sustained engagement."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "ACE Migrants",
        "short_name": "ace_migrants",
        "overview": (
            "ACE Migrants creates a platform for bonds within migrant communities "
            "while fostering mutual learning and empathy between CAPTains and migrants."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "PACE",
        "short_name": "ace_pace",
        "overview": (
            "PACE gives volunteers insight into the world of stray animals and "
            "caretakers, enabling hands-on impact for vulnerable pets and communities."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "Stella",
        "short_name": "ace_stella",
        "overview": (
            "Stella centers on mentor-mentee empowerment and creates a caring, "
            "growth-oriented environment through shared activities and relationships."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
    {
        "name": "CAPT Renew",
        "short_name": "ace_renew",
        "overview": (
            "CAPT Renew supports and empowers halfway house residents on their "
            "reintegration journeys through intentional conversations and activities."
        ),
        "ig_handle": "",
        "tele_handle": "",
        "website": "",
        "directors": [],
        "faqs": [],
    },
]


# Build lookup dictionaries keyed by short_name for fast access.
COMMITTEES_BY_KEY: dict[str, dict] = {c["short_name"]: c for c in COMMITTEES}
ACE_SUBCOMMITTEES_BY_KEY: dict[str, dict] = {
    c["short_name"]: c for c in ACE_SUBCOMMITTEES
}

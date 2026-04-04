# ============================================================
# utils/listening_content.py
# All IELTS listening scripts and questions
# Used by practice, diagnostic, challenge and mock test
# ============================================================

LISTENING_SECTIONS = {

    "Section 1 — Conversation": {
        "script": """
Good morning. Riverside Sports Centre, how can I help you?

Hi, I'd like to find out about your swimming classes, please.

Of course. We have classes for all levels. Can I ask, is this for an adult or a child?

It's for me — I'm 28. I haven't swum in years, so I'd say I'm a beginner.

No problem at all. We have a beginner adult class on Monday evenings at 7pm and Saturday mornings at 9am. Each session is 45 minutes long.

How much does it cost?

It's 12 pounds per session, or you can buy a block of 8 sessions for 80 pounds, which saves you 16 pounds.

That's good value. And where exactly is the pool?

We're at 14 Kensington Road, just opposite the post office. The nearest bus stop is Market Street, about a 5-minute walk.

Do I need to bring anything?

Yes, you'll need a swimming cap — these are mandatory in our pool. You can purchase one at reception for 3 pounds if you don't have one. Towels are available to hire for 1 pound each.

Great. How do I register?

You can register online at our website — that's riversporthub.co.uk — or come to reception and we'll sort it out for you. If you register online, please use the code SWIM10 for a 10 percent discount on your first block booking.

Wonderful, thank you so much.

You're welcome. See you soon!
""",
        "questions": [
            "How old is the caller?",
            "What time is the Monday beginner class?",
            "How long is each session in minutes?",
            "How much does a single session cost in pounds?",
            "How many sessions are in the block booking?",
            "What street is the sports centre on?",
            "What is mandatory in the pool?",
            "How much does a towel hire cost in pounds?",
            "What is the website address?",
            "What discount code gives 10 percent off?",
        ],
        "answers": [
            "28", "7pm", "45", "12", "8",
            "kensington road", "swimming cap", "1",
            "riversporthub.co.uk", "swim10"
        ]
    },

    "Section 2 — Monologue": {
        "script": """
Welcome to the Greenfield Community Garden orientation. I'm Janet, your volunteer coordinator.

The garden was established in 2015 and covers an area of approximately 2 hectares. We currently have 120 registered members, and we're always looking for new volunteers.

Let me tell you about our facilities. We have 6 greenhouse buildings — 4 for vegetables and 2 for tropical plants. The main tool storage shed is located at the north entrance. Please always return tools after use and report any damage to the tool manager, whose contact number is on the shed door.

Our composting area is in the southeast corner. We produce about 3 tonnes of compost per year, which is distributed free to all members. If you'd like extra compost for personal use, you can purchase bags at 4 pounds each from the main office.

We ask all volunteers to complete a health and safety induction before their first session. These run every Thursday at 10am in the meeting room. The induction lasts approximately 2 hours. Please bring photo ID and wear closed-toe shoes to your induction.

Our community café opens from Tuesday to Sunday, 8am to 4pm. Hot meals are served until 2pm. The café accepts card payments only — we no longer accept cash.

Finally, our annual garden festival takes place on the second weekend of July each year. Last year we welcomed over 800 visitors. If you'd like to help organise this year's festival, please speak to me after this session.

Thank you for joining us. Let's go and take a tour of the grounds.
""",
        "questions": [
            "In what year was the garden established?",
            "How many registered members does the garden have?",
            "How many greenhouse buildings are used for vegetables?",
            "Where is the main tool storage shed located?",
            "How many tonnes of compost are produced per year?",
            "How much does a bag of extra compost cost in pounds?",
            "What day do health and safety inductions run?",
            "How long does the induction last in hours?",
            "What days is the community café open?",
            "How many visitors attended last year's festival?",
        ],
        "answers": [
            "2015", "120", "4", "north entrance", "3",
            "4", "thursday", "2", "tuesday to sunday", "800"
        ]
    },

    "Section 3 — Academic discussion": {
        "script": """
Tutor: So, Sarah and James, let's discuss your research proposal on urban food systems. Sarah, would you like to start?

Sarah: Sure. Our proposal focuses on the impact of urban farming initiatives on food security in mid-sized cities. We've been looking at three case studies — one in Rotterdam, one in Singapore, and one in Detroit.

Tutor: Interesting selection. What drew you to Detroit specifically?

James: Detroit is particularly compelling because it's gone through significant deindustrialisation. By 2010, there were over 100,000 vacant plots in the city. Community organisations started converting these into urban farms, and now Detroit has one of the highest densities of urban farms in the United States.

Tutor: And what methodology are you planning to use?

Sarah: We're combining quantitative and qualitative methods. For quantitative data, we'll analyse crop yield statistics and food bank usage rates over a 10-year period. For qualitative data, we'll conduct semi-structured interviews with farm coordinators and local residents.

Tutor: How many interviews are you planning?

James: We're aiming for 30 interviews — 10 per city. We've already made contact with organisations in Rotterdam and Singapore, but we're still working on Detroit.

Tutor: What's the main argument you're trying to make?

Sarah: We want to challenge the assumption that urban farming is primarily a lifestyle choice for wealthy urban residents. Our preliminary data suggests that in lower-income areas, urban farms provide between 15 and 20 percent of residents' fresh vegetable intake.

Tutor: That's a significant finding. Make sure your literature review addresses the criticism that urban farming can never produce enough food to be meaningful at scale.

James: We've actually found a 2022 study by Professor Kim at Seoul National University that directly addresses this. It suggests that with vertical farming techniques, urban areas could theoretically supply up to 40 percent of their own vegetable needs.

Tutor: Excellent. Make sure you include that. Now, regarding your timeline...
""",
        "questions": [
            "How many case studies does the proposal focus on?",
            "How many vacant plots were in Detroit by 2010?",
            "How many years of crop yield statistics will they analyse?",
            "How many total interviews are they planning?",
            "How many interviews per city are planned?",
            "What percentage of fresh vegetables do urban farms provide in lower-income areas?",
            "What year was the study by Professor Kim published?",
            "Which university is Professor Kim from?",
            "What percentage of vegetable needs could vertical farming supply?",
            "Which city are they still trying to make contact with?",
        ],
        "answers": [
            "3", "100,000", "10", "30", "10",
            "15 to 20", "2022", "seoul national university", "40", "detroit"
        ]
    },

    "Section 4 — Academic lecture": {
        "script": """
Good morning everyone. Today I want to talk about a phenomenon that's received increasing attention in cognitive psychology over the past two decades — the concept of cognitive load and its implications for learning and education.

Cognitive load theory was first proposed by John Sweller in 1988. The theory is based on the idea that our working memory has a limited capacity. Sweller identified three types of cognitive load. The first is intrinsic load, which refers to the inherent complexity of the material being learned. The second is extraneous load, which comes from the way information is presented — poorly designed materials can increase this unnecessarily. The third is germane load, which refers to the mental effort used to create and store new knowledge structures, or what psychologists call schemas.

Research has consistently shown that when total cognitive load exceeds working memory capacity, learning is significantly impaired. A landmark study published in the Journal of Educational Psychology in 2001 found that students who received instruction designed to reduce extraneous load scored 34 percent higher on subsequent tests compared to a control group.

These findings have profound implications for instructional design. For example, split-attention effect occurs when learners must mentally integrate information from multiple sources. Studies show this increases extraneous load by up to 28 percent. The solution is to physically integrate related information — for example, placing labels directly on a diagram rather than in a separate legend.

Another application is the worked example effect. Research shows that beginners learn more effectively from studying worked examples than from solving problems independently. However, as learners gain expertise, this effect reverses — a phenomenon known as the expertise reversal effect, first documented by Kalyuga and colleagues in 2003.

The practical takeaway for educators is clear: instructional materials should be designed with cognitive architecture in mind. Reducing unnecessary complexity, integrating related information, and matching task difficulty to learner expertise level are all evidence-based strategies for improving learning outcomes.
""",
        "questions": [
            "In what year did John Sweller propose cognitive load theory?",
            "What is the first type of cognitive load called?",
            "What do psychologists call new knowledge structures?",
            "In what journal was the 2001 landmark study published?",
            "By what percentage did students score higher after reduced extraneous load instruction?",
            "By what percentage does split-attention effect increase extraneous load?",
            "What is the solution to the split-attention effect mentioned?",
            "What effect describes beginners learning better from examples than problems?",
            "What is it called when this effect reverses for experts?",
            "In what year was the expertise reversal effect first documented?",
        ],
        "answers": [
            "1988", "intrinsic load", "schemas",
            "journal of educational psychology", "34", "28",
            "physically integrate related information",
            "worked example effect", "expertise reversal effect", "2003"
        ]
    },
}


# ── DIAGNOSTIC TEST LISTENING ──
DIAGNOSTIC_LISTENING = {
    "script": """
Good morning students. I have some important announcements about next week's schedule.

On Monday, the library will open at 8am instead of the usual 9am, due to a special study session for final year students.

The science lab on the third floor will be closed for maintenance on Tuesday and Wednesday. Students who need lab access should use the alternative lab on the first floor.

The cafeteria will introduce a new menu starting Thursday, with vegetarian options now available every day.

Finally, the sports hall booking system has changed. You must now book at least 24 hours in advance using the new online portal. Walk-in bookings will no longer be accepted.

If you have any questions, please contact the student office at extension 204.
""",
    "questions": [
        "What time will the library open on Monday?",
        "Which floor is the science lab that will be closed?",
        "On which two days will the science lab be closed?",
        "What is new about the cafeteria starting Thursday?",
        "How many hours in advance must students book the sports hall?",
    ],
    "answers": ["8am", "third", "tuesday and wednesday", "vegetarian options", "24"]
}


# ── MOCK TEST FINAL LISTENING ──
MOCK_TEST_LISTENING = {
    "script": """
Good morning everyone. Welcome to the Riverside Community Centre orientation. My name is Sandra, and I'll be your guide today.

The centre was established in 1998 and has been serving the local community for over 25 years. We have three main areas: the sports complex, the learning hub, and the arts studio.

The sports complex opens at 6:30 in the morning and closes at 10 at night on weekdays. On weekends, the hours are 8am to 8pm. The annual membership fee is 240 pounds for adults and 120 pounds for students with a valid ID.

In the learning hub, we offer over 50 different courses ranging from language classes to computer skills. The most popular course is our digital photography class, which runs every Tuesday evening. Registration for new courses opens on the first Monday of each month.

The arts studio on the third floor has recently been renovated and now includes a professional recording studio. It is available for community groups at a subsidised rate of 15 pounds per hour. Private bookings cost 35 pounds per hour.

Finally, I'd like to mention our volunteer programme. We currently need volunteers for three roles: reception support, sports coaching, and event organisation. If you're interested, please speak to the coordinator, whose office is located next to the main entrance, room number 104.
""",
    "questions": [
        "In what year was the community centre established?",
        "What time does the sports complex open on weekdays?",
        "What is the annual adult membership fee in pounds?",
        "How many courses does the learning hub offer?",
        "On which day does the photography class run?",
        "When does registration for new courses open each month?",
        "On which floor is the arts studio?",
        "What is the subsidised hourly rate for community groups in pounds?",
        "How many volunteer roles are currently available?",
        "What is the volunteer coordinator's room number?",
    ],
    "answers": [
        "1998", "6:30", "240", "50", "tuesday",
        "first monday", "third", "15", "three", "104"
    ]
}

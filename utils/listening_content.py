# ============================================================
# utils/listening_content.py
# All IELTS listening scripts - single speaker, clear audio
# ============================================================

LISTENING_SECTIONS = {

    "Section 1 — Conversation": {
        "script": """
Good morning and thank you for calling Riverside Sports Centre.
You have reached our automated information line.

We are currently offering beginner swimming classes for adults.
Classes are held on Monday evenings at seven pm, and Saturday mornings at nine am.
Each session lasts forty-five minutes.

The cost is twelve pounds per session.
Alternatively, you can purchase a block of eight sessions for eighty pounds,
saving you sixteen pounds in total.

Our centre is located at fourteen Kensington Road,
directly opposite the post office.
The nearest bus stop is Market Street, approximately a five minute walk away.

Please note that swimming caps are mandatory in our pool.
You may purchase one at reception for three pounds.
Towel hire is available for one pound per visit.

To register, please visit our website at riversporthub dot co dot uk.
First-time members who register online may use the code SWIM10
for a ten percent discount on their first block booking.

Thank you for calling Riverside Sports Centre.
We look forward to welcoming you soon.
""",
        "questions": [
            "What time is the Monday evening swimming class?",
            "How long is each session in minutes?",
            "How much does a single session cost in pounds?",
            "How much does the block of 8 sessions cost in pounds?",
            "What street is the sports centre located on?",
            "What is the nearest bus stop?",
            "What item is mandatory in the pool?",
            "How much does towel hire cost in pounds?",
            "What is the website address?",
            "What discount code gives 10 percent off?",
        ],
        "answers": [
            "7pm", "45", "12", "80",
            "kensington road", "market street",
            "swimming cap", "1",
            "riversporthub.co.uk", "swim10"
        ]
    },

    "Section 2 — Monologue": {
        "script": """
Welcome to the Greenfield Community Garden orientation recording.
My name is Janet, and I am the volunteer coordinator.

The garden was established in two thousand and fifteen,
and covers an area of approximately two hectares.
We currently have one hundred and twenty registered members.

Regarding our facilities:
We have six greenhouse buildings in total —
four are used for vegetables, and two for tropical plants.
The main tool storage shed is located at the north entrance.
Please always return tools after use.

Our composting area is in the southeast corner of the garden.
We produce approximately three tonnes of compost per year,
which is distributed free of charge to all members.
Additional bags of compost may be purchased at four pounds each
from the main office.

All new volunteers must complete a health and safety induction
before their first working session.
Inductions are held every Thursday at ten in the morning,
in the meeting room.
Each induction lasts approximately two hours.
Please bring photo identification and wear closed-toe shoes.

Our community café is open Tuesday to Sunday,
from eight in the morning until four in the afternoon.
Hot meals are served until two pm.
Please note the café accepts card payments only.
Cash is no longer accepted.

Our annual garden festival takes place on the second weekend of July.
Last year, the festival welcomed over eight hundred visitors.

Thank you for joining the Greenfield Community Garden.
We hope you enjoy your time with us.
""",
        "questions": [
            "In what year was the garden established?",
            "How many registered members does the garden have?",
            "How many greenhouses are used for vegetables?",
            "Where is the main tool storage shed?",
            "How many tonnes of compost are produced per year?",
            "How much does a bag of extra compost cost in pounds?",
            "What day do health and safety inductions run?",
            "How long does the induction last in hours?",
            "What payment method does the café accept?",
            "How many visitors attended last year's festival?",
        ],
        "answers": [
            "2015", "120", "4", "north entrance", "3",
            "4", "thursday", "2", "card", "800"
        ]
    },

    "Section 3 — Academic discussion": {
        "script": """
This is a recorded summary of a research proposal discussion
from the Department of Urban Studies.

The research project focuses on the impact of urban farming initiatives
on food security in mid-sized cities.
Three case studies have been selected for analysis:
one in Rotterdam, one in Singapore, and one in Detroit.

Detroit was selected because of its significant deindustrialisation.
By two thousand and ten, there were over one hundred thousand vacant plots in the city.
Community organisations began converting these plots into urban farms.
Detroit now has one of the highest densities of urban farms in the United States.

The research methodology combines both quantitative and qualitative approaches.
For quantitative data, the team will analyse crop yield statistics
and food bank usage rates over a ten-year period.
For qualitative data, thirty semi-structured interviews will be conducted —
ten interviews per city.

The central argument of the research challenges the assumption
that urban farming is primarily a lifestyle choice for wealthy residents.
Preliminary data suggests that in lower-income areas,
urban farms provide between fifteen and twenty percent
of residents' fresh vegetable intake.

A significant supporting study was published in two thousand and twenty-two
by Professor Kim at Seoul National University.
This study suggests that with vertical farming techniques,
urban areas could theoretically supply up to forty percent
of their own vegetable requirements.

The research team is currently finalising contact arrangements
with organisations in Detroit, having already established connections
in Rotterdam and Singapore.
""",
        "questions": [
            "How many case studies does the research include?",
            "How many vacant plots were in Detroit by 2010?",
            "How many years of crop statistics will be analysed?",
            "How many interviews will be conducted in total?",
            "How many interviews will be conducted per city?",
            "What percentage of vegetables do urban farms provide in lower-income areas?",
            "What year was Professor Kim's study published?",
            "Which university is Professor Kim from?",
            "What percentage of vegetables could vertical farming supply?",
            "Which city are they still finalising contact with?",
        ],
        "answers": [
            "3", "100,000", "10", "30", "10",
            "15 to 20", "2022", "seoul national university",
            "40", "detroit"
        ]
    },

    "Section 4 — Academic lecture": {
        "script": """
Welcome to today's lecture on cognitive load theory
and its implications for learning and education.

Cognitive load theory was first proposed by John Sweller in nineteen eighty-eight.
The theory is based on the principle that our working memory has a limited capacity.

Sweller identified three types of cognitive load.

The first type is called intrinsic load.
This refers to the inherent complexity of the material being learned.
Some subjects are naturally more complex than others,
and this creates a higher intrinsic cognitive load for the learner.

The second type is called extraneous load.
This refers to the mental effort caused by the way information is presented.
Poorly designed instructional materials can increase extraneous load unnecessarily,
leaving less mental capacity available for actual learning.

The third type is called germane load.
This refers to the mental effort used to create and store new knowledge structures,
which psychologists call schemas.

Research has consistently shown that when total cognitive load
exceeds working memory capacity, learning is significantly impaired.

A landmark study published in the Journal of Educational Psychology in two thousand and one
found that students who received instruction designed to reduce extraneous load
scored thirty-four percent higher on subsequent tests
compared to a control group.

One practical application of this theory is addressing the split-attention effect.
This occurs when learners must mentally integrate information from multiple sources.
Studies show this increases extraneous load by up to twenty-eight percent.
The recommended solution is to physically integrate related information —
for example, placing labels directly on a diagram
rather than in a separate legend.

Another important application is the worked example effect.
Research shows that beginners learn more effectively
from studying worked examples than from solving problems independently.

However, as learners gain expertise, this effect reverses.
This phenomenon is known as the expertise reversal effect,
first documented by Kalyuga and colleagues in two thousand and three.

The key takeaway for educators is this:
instructional materials should always be designed
with the learner's cognitive architecture in mind.
""",
        "questions": [
            "In what year did Sweller propose cognitive load theory?",
            "What is the first type of cognitive load called?",
            "What term describes new knowledge structures?",
            "In which journal was the 2001 study published?",
            "By what percentage did scores improve after reducing extraneous load?",
            "By what percentage does split-attention effect increase extraneous load?",
            "What is the solution to the split-attention effect?",
            "What effect describes beginners learning better from examples?",
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


# ── DIAGNOSTIC LISTENING ──
DIAGNOSTIC_LISTENING = {
    "script": """
Good morning students. This is an important announcement regarding next week's schedule.

Please listen carefully as this message will not be repeated.

On Monday, the library will open at eight in the morning,
instead of the usual nine am opening time.
This change is due to a special study session for final year students.

The science lab on the third floor will be closed for maintenance
on Tuesday and Wednesday of next week.
Students who require laboratory access during this period
should use the alternative facility located on the first floor.

From Thursday onwards, the cafeteria will introduce a new menu.
Vegetarian options will now be available every day of the week.

Finally, please be aware that the sports hall booking system has changed.
You must now book your session at least twenty-four hours in advance
using the new online portal.
Walk-in bookings will no longer be accepted under any circumstances.

If you have any questions regarding these announcements,
please contact the student office at extension two zero four.

Thank you for your attention.
""",
    "questions": [
        "What time will the library open on Monday?",
        "Which floor is the science lab that will be closed?",
        "On which two days will the science lab be closed?",
        "What is new about the cafeteria from Thursday?",
        "How many hours in advance must students book the sports hall?",
    ],
    "answers": [
        "8am", "third", "tuesday and wednesday",
        "vegetarian options", "24"
    ]
}


# ── MOCK TEST FINAL LISTENING ──
MOCK_TEST_LISTENING = {
    "script": """
Good morning everyone, and welcome to the Riverside Community Centre.
This is your orientation recording. Please listen carefully.

The centre was established in nineteen ninety-eight
and has been proudly serving the local community for over twenty-five years.
We offer three main areas of service:
the sports complex, the learning hub, and the arts studio.

The sports complex is open on weekdays from six thirty in the morning
until ten o'clock at night.
Weekend hours are eight in the morning until eight in the evening.
Annual membership costs two hundred and forty pounds for adults,
and one hundred and twenty pounds for students with valid identification.

The learning hub offers over fifty different courses,
ranging from language classes to computer skills training.
Our most popular course is the digital photography class,
which runs every Tuesday evening.
Registration for all new courses opens on the first Monday of each month.

The arts studio is located on the third floor.
It has recently been renovated and now includes a professional recording studio.
Community groups may book the studio at a subsidised rate of fifteen pounds per hour.
Private bookings are available at thirty-five pounds per hour.

Finally, we are currently seeking volunteers for three roles:
reception support, sports coaching, and event organisation.
If you are interested in volunteering,
please visit the coordinator's office, which is located
next to the main entrance in room one zero four.

Thank you for choosing the Riverside Community Centre.
We hope you enjoy everything we have to offer.
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

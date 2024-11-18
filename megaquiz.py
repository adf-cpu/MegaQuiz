import streamlit as st
import pandas as pd
from datetime import datetime
import random
import cloudinary
import cloudinary.uploader
import os
st.markdown(
    """
    <style>
    .st-emotion-cache-1huvf7z {
        display: none; /* Hides the button */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Hide the avatar image
st.markdown(
    """
    <style>
    ._profileImage_1yi6l_74 {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use Streamlit's image function to show the image on the left side
col1, col2 = st.columns([1, 3])  # Create 2 columns with ratios (left narrower than right)

with col1:  # Left column
    st.image("Huawei.jpg", width=80)

cloudinary.config(
    cloud_name="drpkmvcdb",  # Replace with your Cloudinary cloud name
    api_key="421723639371647",        # Replace with your Cloudinary API key
    api_secret="AWpJzomMBrw-5DHNqujft5scUbM"   # Replace with your Cloudinary API secret
)

def upload_to_cloudinary(file_path, public_id):
    try:
        response = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",
            public_id=public_id,
            overwrite=True,  # Allow overwriting
            invalidate=True,  # Invalidate cached versions on CDN
            unique_filename=False,  # Do not generate a unique filename
            use_filename=True  # Use the file's original filename
        )
        return response['secure_url']
    except cloudinary.exceptions.Error as e:
        st.error(f"Cloudinary upload failed: {str(e)}")
        return None

# Function to save results to Excel
def save_results(username, total_attempted, correct_answers, wrong_answers, total_score, time_taken, details):   
    try:
        df = pd.read_excel("quiz_results_megaquiz.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Username", "Date", "Total Attempted", "Correct Answers", "Wrong Answers", "Total Score", "Time Taken", "Details"])

    new_data = pd.DataFrame([[username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_attempted, correct_answers, wrong_answers, total_score, time_taken, details]],
                            columns=["Username", "Date", "Total Attempted", "Correct Answers", "Wrong Answers", "Total Score", "Time Taken", "Details"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel("quiz_results_megaquiz.xlsx", index=False)
       # Upload the file to Cloudinary
    uploaded_url = upload_to_cloudinary("quiz_results_megaquiz.xlsx", "quiz_results_megaquiz")
    if uploaded_url:
        st.success(f"Quiz results uploaded successfully!")
        # st.markdown(f"Access your file here: [quiz_results.xlsx]({uploaded_url})")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'flattened_questions' not in st.session_state:
    st.session_state.flattened_questions = []
# List of allowed usernames
allowed_usernames = {
    "Farrukh.Hussain",
    "HIC_ISB_TrainingTeam_01.",
    "HIC_ISB_TrainingTeam_02",
    "HIC_ISB_TrainingTeam_03",
    "HIC_ISB_TrainingTeam_04",
    "HIC_ISB_TrainingTeam_05",
    "pc_kamran02",
    "pt_saqibali",
    "ies_mobeen01",
    "ies_khalid01",
    "ies_shoaib01",
    "ies_hamza01",
    "tt_bilal01"
}
# Define your questions
megaquiz= {
"true_false": [
       {"question": "Electrical tilt antenna has remote control function, can control the downtilt angle, azimuth angle remotely.", "answer": "False"},
    {"question": "When the outdoor feeders enter the indoor system, they need to be connected to the surge protector to protect the BTS equipment against damages from lightning.", "answer": "False"},
    {"question": "4G has no BSC/RNC.", "answer": "True"},
    {"question": "The vertical deviation of cabinets and the clearance between combined cabinets should be less than 3 mm.", "answer": "True"},
    {"question": "The labels of communication cables, feeder cables and jumper should be stuck and tied according to specifications.", "answer": "True"},
    {"question": "If someone needs to enter an unsafe working area, a job safety analysis must be performed and control measures must be implemented.", "answer": "True"},
    {"question": "When hazards cannot be eliminated, all possible steps must be taken to minimize risks.", "answer": "True"},
    {"question": "Two ground cables can be connected to the same grounding hole on grounding busbar.", "answer": "False"},
    {"question": "Antenna's main beam is determined by the array’s element distribution.", "answer": "True"},
    {"question": "The power cable and grounding cable must be made of copper core materials, and there can be connectors in the middle.", "answer": "True"},
    {"question": "Insulation, lockout, and tag-out must be implemented for hazardous electrical work.", "answer": "True"},
    {"question": "Only qualified first aiders are allowed to use first aid to rescue casualties.", "answer": "True"},
    {"question": "Small Cell can enhance indoor coverage.", "answer": "True"},
    {"question": "If a driver drives the car very slowly, there is no need to fasten the seatbelt.", "answer": "False"},
    {"question": "Safety measures are often not seen as an impediment to productivity.", "answer": "True"},
    {"question": "Jumper is quite soft, its common specification is 1/2” and can be used for long distance connection.", "answer": "False"},
    {"question": "All employees must comply with safety regulations at all times.", "answer": "True"},
    {"question": "The company should have a clear safety policy that is communicated to all employees.", "answer": "True"},
    {"question": "Hazards identification in advance is a must even if you are certified on EHS.", "answer": "True"},
    {"question": "Exposed live parts such as diesel generator, transformer and distribution cabinet shall be insulated or isolated.", "answer": "True"},
    {"question": "It's acceptable to modify safety protocols for expediency.", "answer": "False"},
    {"question": "Accidents are a natural part of working life and should be accepted.", "answer": "False"},
    {"question": "When the project is finished, we can leave everything as it is without any cleaning.", "answer": "False"},
    {"question": "Emergency exits must be clearly marked and accessible.", "answer": "True"},
    {"question": "Only accidents that cause injury must be reported.", "answer": "False"},
    {"question": "Site Engineers are responsible for engineering quality, with no need to audit EHS.", "answer": "False"},
    {"question": "All safety-related incidents should be documented.", "answer": "True"},
    {"question": "Personal protective equipment must be maintained in good condition.", "answer": "True"},
    {"question": "If the firefighting system is not available on-site, we can still carry out our activities.", "answer": "False"},
    {"question": "Safety protocols should be reviewed regularly to ensure effectiveness.", "answer": "True"},
    {"question": "Employees must receive appropriate safety training before starting work.", "answer": "True"},
    {"question": "Casual shoes, sandals, or slippers are NOT allowed in the worksite.", "answer": "True"},
    {"question": "Staff are responsible for complying with established procedures and instructions.", "answer": "True"},
    {"question": "In 2G Base station is connected to RNC.", "answer": "False"},
    {"question": "Accidents only happen because workers are careless.", "answer": "False"},
    {"question": "Safety is a shared responsibility among all team members.", "answer": "True"},
    {"question": "Safety audits are unnecessary once the project is underway.", "answer": "False"},
    {"question": "Personal protective equipment should be used only when necessary.", "answer": "True"},
    {"question": "The effectiveness of safety training should be evaluated after delivery.", "answer": "True"},
    {"question": "Reporting near misses is not important.", "answer": "False"},
    {"question": "The safety culture of an organization can improve over time.", "answer": "True"},
    {"question": "The project team should have regular safety meetings to discuss issues and improvements.", "answer": "True"},
    {"question": "Safety equipment must be used only if it is convenient.", "answer": "False"},
    {"question": "Employees should not bring personal protective equipment from home.", "answer": "False"},
    {"question": "The project team can request not to follow project EHS absolute rules when local resources are limited.", "answer": "False"},
    {"question": "Drivers should practice enough to use a hand-held phone while driving.", "answer": "False"},
    {"question": "Safety inspections should be conducted regularly to identify hazards.", "answer": "True"},
    {"question": "If no internet is working on-site, there is no need to get approval from a supervisor.", "answer": "False"},
    {"question": "All employees should receive recognition for following safety procedures.", "answer": "True"},
    {"question": "First aid kits must be regularly checked and restocked.", "answer": "True"},
    {"question": "In 3G Base station, the RNC connects to the core network.", "answer": "True"},
    {"question": "4G supports VoLTE and CSFB.", "answer": "True"},
    {"question": "All employees should participate in safety initiatives.", "answer": "True"},
    {"question": "It is important to provide safety training for temporary workers.", "answer": "True"},
    {"question": "Safety performance should be a consideration in promotions.", "answer": "True"},
    {"question": "Only workers who have been trained and are competent can carry out safety work.", "answer": "True"},
    {"question": "All 5G spectrum is above 6GHz.", "answer": "False"},
    {"question": "Only management has the responsibility for Safety.", "answer": "False"},
    {"question": "Safety performance should be evaluated regularly to improve processes.", "answer": "True"},
    {"question": "The installation position of antennas in the same site shall follow the principle of the higher is better.", "answer": "True"},
    {"question": "The bolt installed in the following photo are correct.", "answer": "False"},
    {"question": "Better EHS management with a higher total cost reduces the project profit.", "answer": "False"},
    {"question": "4G cannot support voice service.", "answer": "False"},
    {"question": "All employees must understand the emergency evacuation plan.", "answer": "True"},
    {"question": "It is not necessary to provide safety information to employees if they are already familiar with the procedures.", "answer": "False"},
    {"question": "Employees should feel comfortable reporting safety concerns without fear of retaliation.", "answer": "True"},
    {"question": "Site hazard identification must be done only at the beginning of the project.", "answer": "False"},
    {"question": "The company should promote a culture of safety throughout the organization.", "answer": "True"},
    {"question": "Job hazard analysis must be done only at the beginning of the project.", "answer": "False"},
    {"question": "If hazards are not eliminated, it is acceptable to use personal protective equipment as the only means of protection.", "answer": "False"}
],

    "single_choice": [
    {
        "question": "The height of DCDU is:",
        "options": ["A) 1 U", "B) 2 U", "C) 3 U", "D) 4 U"],
        "answer": "A) 1 U"  # Correct answer
    },
    {
        "question": "What is the maximum temperature for working at height?",
        "options": ["A) 34°C", "B) 40°C", "C) 44°C", "D) 45°C"],
        "answer": "D) 45°C"  # Correct answer
    },
    {
        "question": "Which cabinet is always used indoor?",
        "options": ["A) BTS3900", "B) BTS3900A", "C) APM30", "D) BTS3902E"],
        "answer": "A) BTS3900"  # Correct answer
    },
    {
        "question": "Which of the following statements about bending radius is wrong?",
        "options": [
            "A) 7/8\" feeder above 250mm, 5/4\" feeder above 380mm.",
            "B) 1/4\" jumper above 35mm, 1/2\" jumper (super flexible) above 50mm, 1/2\" jumper (normal) above 127mm.",
            "C) The bending radius of power/grounding cable no less than 3-5 times of its diameter.",
            "D) Bending radius of signal cable no less than twice of its diameter."
        ],
        "answer": "D) Bending radius of signal cable no less than twice of its diameter."  # Correct answer
    },
    {
        "question": "In Swap sites the transmission equipment will get power from:",
        "options": ["A) DCDU_BLVD", "B) DCDU_LLVD", "C) DC PDB", "D) AC PDB"],
        "answer": "A) DCDU_BLVD"  # Correct answer
    },
    {
        "question": "The purpose of keeping the work site clear and tidy is:",
        "options": [
            "A) Comfortable for work",
            "B) Any protruding nails can wound workers or bend them over",
            "C) Meeting the requirements of EHS laws",
            "D) None of the above"
        ],
        "answer": "B) Any protruding nails can wound workers or bend them over"  # Correct answer
    },
    {
        "question": "The jumper cable’s size of RRU commonly is:",
        "options": ["A) 1/4 inch", "B) 1/2 inch", "C) 5/4 inch", "D) 7/8 inch"],
        "answer": "B) 1/2 inch"  # Correct answer
    },
    {
        "question": "The radius of the load drop zone equals ( ) the height of the load:",
        "options": ["A) 0.1", "B) 0.3", "C) 0.5", "D) 0.8"],
        "answer": "C) 0.5"  # Correct answer
    },
    {
        "question": "For wireless hardware installation, the wrong explanation is:",
        "options": [
            "A) After punching at cement floor for fixing cabinet foundation, vacuum sweeper is used to clean the dust.",
            "B) Electrostatic prevention hand ring should be worn as operating to pluck or insert the board in cabinet.",
            "C) The white ribbon should be used indoors.",
            "D) The hammer can be used for OT terminal fixing."
        ],
        "answer": "D) The hammer can be used for OT terminal fixing."  # Correct answer
    },
    {
        "question": "Job Hazard Analysis been completed on First Aid Kit and Tower Rescue Kit includes:",
        "options": [
            "A) Emergency services phone numbers, location, and map",
            "B) Home address",
            "C) Office location",
            "D) None of the above"
        ],
        "answer": "A) Emergency services phone numbers, location, and map"  # Correct answer
    },
    {
        "question": "Height of BBU3900 is:",
        "options": ["A) 1 U", "B) 2 U", "C) 3 U", "D) 4 U"],
        "answer": "B) 2 U"  # Correct answer
    },
    {
        "question": "Which description is wrong as below?",
        "options": [
            "A) The jumper connectors must be protected before hoisting.",
            "B) The antenna and jumper cable can’t be hoisted together.",
            "C) Before hoisting the antenna, the hoisting rope bind on the upper antenna bracket, the steering rope bind on the lower antenna bracket.",
            "D) When hoisting the antenna, one group of people pulls the hoisting rope down, while another group pulls the steering rope away from the tower, preventing the antenna from hitting the tower."
        ],
        "answer": "B) The antenna and jumper cable can’t be hoisted together."  # Correct answer
    },
    {
        "question": "For working at height (unsafe zone):",
        "options": [
            "A) Allow worker to walk underneath",
            "B) Allow worker to walk underneath if another watchman reminds of danger",
            "C) Never allow worker to walk underneath",
            "D) All of the above are wrong"
        ],
        "answer": "C) Never allow worker to walk underneath"  # Correct answer
    },
    {
        "question": "Making the OT terminal of the 16mm² grounding cable, the terminal’s type is:",
        "options": ["A) 12", "B) 14", "C) 15", "D) 16"],
        "answer": "B) 14"  # Correct answer
    },
    {
        "question": "Which of the following protective actions is wrong?",
        "options": [
            "A) Paste insulation tape at the incision.",
            "B) Protect action is needed where fiber goes out of the cabinet, to prevent from squeeze and bite.",
            "C) Tie the fiber terminal when lifting and installing the RRU.",
            "D) Clear define the specification of using fiber tube."
        ],
        "answer": "C) Tie the fiber terminal when lifting and installing the RRU."  # Correct answer
    },
    {
        "question": "What is the distance between each feeder cable clip?",
        "options": ["A) 1.5~2M", "B) 2~2.5M", "C) 2.5~3M", "D) 2~2.5M"],
        "answer": "A) 1.5~2M"  # Correct answer
    },
    {
        "question": "Manual lifting: Pulling strength shall be:",
        "options": [
            "A) Not allow sudden pull, sudden stop",
            "B) Allow sudden pull, sudden stop",
            "C) If pulling strength is enough, allow sudden pull, sudden stop",
            "D) None of the above"
        ],
        "answer": "A) Not allow sudden pull, sudden stop"  # Correct answer
    },
    {
        "question": "Which cable will be connected first as the cabinet is installed?",
        "options": ["A) Power cable", "B) Signal line", "C) Transmission cable", "D) Grounding cable"],
        "answer": "D) Grounding cable"  # Correct answer
    },
    {
        "question": "The wrong explanation about jumping and IF cable:",
        "options": [
            "A) Jumping cable that is used for different sectors is connected with the main or standby channel correctly, and laid out tidily.",
            "B) Jumping cable for main channel is marked by double color ring, the one for standby is marked by single.",
            "C) 0–5 sector marking color order: red, orange, yellow, blue, purple, green.",
            "D) For minimum bending radius of jumping cable, the requirement that smaller is better is wrong."
        ],
        "answer": "C) 0–5 sector marking color order: red, orange, yellow, blue, purple, green."  # Correct answer
    },
    {
        "question": "The most important activity for EHS management is:",
        "options": [
            "A) Prevention",
            "B) Corrective actions",
            "C) Quick reactions",
            "D) No response to accidents or incidents"
        ],
        "answer": "A) Prevention"  # Correct answer
    },
    {
        "question": "RRU has how many grounding points?",
        "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
        "answer": "B) 2"  # Correct answer
    },
    {
        "question": "25 mm² grounding cable is made for OT terminal, which type of it can be selected?",
        "options": ["A) 20", "B) 22", "C) 24", "D) 25"],
        "answer": "B) 22"  # Correct answer
    },
        {
        "question": "What is a common renewable energy source used in telecom power systems?",
        "options": ["A) Wind", "B) Hydroelectric", "C) Geothermal", "D) Solar"],
        "answer": "D) Solar"
    },
    {
        "question": "Which type of battery is commonly used for telecom backup power?",
        "options": ["A) Lithium-ion", "B) Nickel-Cadmium", "C) Lead-acid", "D) Alkaline"],
        "answer": "C) Lead-acid"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) XMC-5D ODU have two IF ports & called 1T1R", "B) XMC-5D ODU have two IF ports & called 2T2R", "C) XMC-5D ODU have Four IF ports & called 4T4R", "D) XMC-5D ODU have three IF ports & called 3T3R"],
        "answer": "B) XMC-5D ODU have two IF ports & called 2T2R"
    },
    {
        "question": "EHS Accident investigations begin:",
        "options": [
            "A) The moment an accident occurred",
            "B) Within 1 day when an accident occurred",
            "C) Within 3 days when an accident occurred",
            "D) Within 7 days when an accident occurred"
        ],
        "answer": "A) The moment an accident occurred"
    },
    {
        "question": "Purpose of Grounding in electrical System:",
        "options": ["A) Improve Energy efficiency", "B) Prevent Electric Shock and ensure safety", "C) Increase Voltage of System", "D) For better Transmission Speed"],
        "answer": "B) Prevent Electric Shock and ensure safety"
    },
    {
        "question": "Which MW is Full outdoor.",
        "options": ["A) RTN380", "B) RTN950A", "C) RTN950A", "D) RTN10A"],
        "answer": "A) RTN380"
    },
    {
        "question": "How many types of BBU Used in Wireless?",
        "options": ["A) 4", "B) 2", "C) 1", "D) 3"],
        "answer": "D) 3"
    },
    {
        "question": "What is the typical output voltage of telecom DC power systems?",
        "options": ["A) 5V", "B) 48V", "C) 220V", "D) 12V"],
        "answer": "B) 48V"
    },
    {
        "question": "What is the purpose of grounding in telecom power systems?",
        "options": ["A) To reduce power consumption", "B) To protect against lightning", "C) To increase efficiency", "D) To provide backup power"],
        "answer": "B) To protect against lightning"
    },
    {
        "question": "How many antennas required for 1+1 XPIC Configurations.",
        "options": ["A) 2", "B) 4", "C) None of the above"],
        "answer": "A) 2"
    },
    {
        "question": "Input voltage of RTN950A are as follow.",
        "options": ["A) –48 V DC power inputs with 20A fuse capacity", "B) –40 V DC power inputs with 10A fuse capacity", "C) –80 V DC power inputs with 40A fuse capacity", "D) –20 V DC power inputs with 20A fuse capacity"],
        "answer": "A) –48 V DC power inputs with 20A fuse capacity"
    },
    {
        "question": "Purpose of a Type 2 SPD?",
        "options": ["A) Protect against Lightning Strike", "B) Protect against overvoltage from electrical network", "C) Provide Grounding for electrical System", "D) To filter out electromagnetic interference"],
        "answer": "B) Protect against overvoltage from electrical network"
    },
    {
        "question": "How many supporting rods are required for 1.8M MW Antenna.",
        "options": ["A) 1", "B) 3", "C) 2", "D) 4"],
        "answer": "C) 2"
    },
    {
        "question": "Which Control Board related with RTN 950A.",
        "options": ["A) CSHN", "B) CSH", "C) CSHNU", "D) CSHO"],
        "answer": "D) CSHO"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) We can use 38GHz ODU with 6GHz Antennae", "B) We can use 38GHz ODU with 38GHz Antennae", "C) We can use 23GHz ODU with 8GHz Antennae", "D) We can use 13GHz ODU with 80GHz Antennae"],
        "answer": "B) We can use 38GHz ODU with 38GHz Antennae"
    },
    {
        "question": "Lifting a product to height, the product shall be:",
        "options": [
            "A) Tied tightly and locked with a safety facility",
            "B) Tied loosely for easy unjointing",
            "C) Tied and don’t unlock",
            "D) All of the above are wrong"
        ],
        "answer": "A) Tied tightly and locked with a safety facility"
    },
    {
        "question": "When carrying heavy objects by hand, you need to keep your head:",
        "options": ["A) Looking down on the ground", "B) Looking straight", "C) Looking at the heavy objects", "D) None of the above"],
        "answer": "B) Looking straight"
    },
    {
        "question": "RTN905-2F can easily use at (   ) layers.",
        "options": ["A) Three sites dependent HUB site", "B) Access layer", "C) Aggregation layers", "D) Fiber Nodes"],
        "answer": "B) Access layer"
    },
    {
        "question": "After how long a time of driving must the driver stop the vehicle?",
        "options": ["A) 2.5 hours", "B) 4 hours", "C) 3 hours", "D) 3.5 hours"],
        "answer": "C) 3 hours"
    },
    {
        "question": "No of IF ports of XMC-3E ODU is (  ).",
        "options": ["A) one port", "B) Three ports", "C) Five ports", "D) Two Ports"],
        "answer": "A) one port"
    },
    {
        "question": "Which IF card have 10G Port.",
        "options": ["A) ISM6", "B) ISV3", "C) ISX2", "D) ISM8"],
        "answer": "D) ISM8"
    },
    {
        "question": "Which service boards are related with RTN980.",
        "options": ["A) EM6X", "B) CSH", "C) CSHNA", "D) CSHNU"],
        "answer": "A) EM6X"
    },
    {
        "question": "Which RRU stands for?",
        "options": ["A) Radio frequency unit", "B) Radio Resource Unit", "C) Remote Radio Unit", "D) Radio Frequency Unit"],
        "answer": "C) Remote Radio Unit"
    },
    {
        "question": "Can we download & use any Third Party Software from internet websites?",
        "options": ["A) Yes", "B) No"],
        "answer": "B) No"
    },
   {
        "question": "What is the Name of Controller used in ICC710?",
        "options": ["A) SMU01B", "B) SMU03A", "C) SMU02B", "D) UIMC01"],
        "answer": "C) SMU02B"
    },
    {
        "question": "Which module is used to convert AC input voltage into -48V DC voltage?",
        "options": ["A) BBU", "B) SPLU", "C) PSU", "D) RFU"],
        "answer": "C) PSU"
    },
    {
        "question": "What does the abbreviation 'UPS' stand for?",
        "options": ["A) Universal Power Supply", "B) Uninterrupted Power Supply", "C) Uninterrupted Power Source", "D) Utility Power System"],
        "answer": "B) Uninterrupted Power Supply"
    },
    {
        "question": "What is the primary function of a Power Distribution Unit (PDU) in a data center?",
        "options": ["A) Backup power", "B) Cooling", "C) Distribute power", "D) Manage network traffic"],
        "answer": "C) Distribute power"
    },
    {
        "question": "Batteries within the Power should be proper spacing on----mm?",
        "options": ["A) 10mm", "B) 5mm", "C) 15mm", "D) 20mm"],
        "answer": "A) 10mm"
    },
    {
        "question": "In hybrid telecom power systems, which of the following is used alongside solar power?",
        "options": ["A) Capacitor", "B) Generator", "C) Inverter", "D) Resistor"],
        "answer": "B) Generator"
    },
    {
        "question": "What is the typical voltage used for power distribution to servers in data centers?",
        "options": ["A) 120V", "B) 220V", "C) 48V", "D) 400V"],
        "answer": "B) 220V"
    },
    {
        "question": "When On Site status is 'COM NOK', which tool can be used to confirm Ping from Site to NetEco?",
        "options": ["A) Putty", "B) FileZilla", "C) Lan Tester", "D) Web Browser"],
        "answer": "A) Putty"
    },
    {
        "question": "Grounding BUS Bar is available on Tower, where should be the RRU Grounded?",
        "options": ["A) Tower Leg", "B) Grounding BUS Bar", "C) Grounding is not required", "D) Ground later"],
        "answer": "A) Tower Leg"
    },
    {
        "question": "What is the role of a Power Distribution Unit (PDU) in telecom towers?",
        "options": ["A) Store energy", "B) Distribute power", "C) Regulate voltage", "D) Convert DC to AC"],
        "answer": "B) Distribute power"
    },
    {
        "question": "What is the purpose of Power Usage Effectiveness (PUE) in a data center?",
        "options": ["A) Measure energy efficiency", "B) Manage cooling systems", "C) Improve network performance", "D) Ensure data security"],
        "answer": "A) Measure energy efficiency"
    },
    {
        "question": "What is a common source of power redundancy in data centers?",
        "options": ["A) Multiple PDUs", "B) Battery banks", "C) Dual power feeds", "D) Cooling systems"],
        "answer": "C) Dual power feeds"
    },
    {
        "question": "Packing of Rectifier and Batteries should be removed when Equipment is on-------?",
        "options": ["A) On Site", "B) WH", "C) Outside WH", "D) Supplier WH"],
        "answer": "A) On Site"
    },
    {
        "question": "Which of the following is a common fuel source for data center backup generators?",
        "options": ["A) Natural Gas", "B) Coal", "C) Diesel", "D) Wind"],
        "answer": "C) Diesel"
    },
    {
        "question": "What is the main function of UPS in data centers?",
        "options": ["A) Provide long-term power storage", "B) Provide short-term power during an outage", "C) Convert AC to DC", "D) Distribute power to servers"],
        "answer": "B) Provide short-term power during an outage"
    },
    {
        "question": "Which of the following power distribution methods is commonly used in data centers?",
        "options": ["A) Radial", "B) Ring", "C) Mesh", "D) Grid"],
        "answer": "A) Radial"
    },
    {
        "question": "Batteries can be transported to site in -----packing?",
        "options": ["A) Wooden Packing", "B) Polythen packing", "C) No Packing", "D) Any Packing"],
        "answer": "A) Wooden Packing"
    },
    {
        "question": "Which type of power is commonly used to operate servers in data centers?",
        "options": ["A) AC", "B) DC", "C) Solar", "D) Wind"],
        "answer": "A) AC"
    },
    {
        "question": "What is a common cooling solution for data centers?",
        "options": ["A) Liquid immersion cooling", "B) Air-cooled radiators", "C) Fans", "D) Heat sinks"],
        "answer": "A) Liquid immersion cooling"
    },
    {
        "question": "RRU are situated at",
        "options": ["A) Near the Antenna", "B) Foot of the tower", "C) In BTS cabinet", "D) Near Generator"],
        "answer": "A) Near the Antenna"
    },
    {
        "question": "What is the login Browser IP of Power Cube 1CC710-ICC500 (     )?",
        "options": ["A) 192.168.10.1", "B) 192.168.0.10", "C) 192.168.1.1", "D) 192.168.10.1"],
        "answer": "B) 192.168.0.10"
    },
    {
        "question": "For tightening Battery Terminal and Rawal Bolts how much N.M for Torque Wrench Torque Required?",
        "options": ["A) 17N.m & 46 N.m", "B) 17N.m & 45 N.m", "C) 40 N.M & 70 N.M", "D) 40 N.m & 60 N.m"],
        "answer": "B) 17N.m & 45 N.m"
    },
    {
        "question": "Which of the following is NOT a component of telecom power systems?",
        "options": ["A) Rectifier", "B) Transformer", "C) Battery", "D) Firewall"],
        "answer": "D) Firewall"
    },
    {
        "question": "Star Connections is used when",
        "options": ["A) Neutral and 2 separate voltages are Needed", "B) Neutral and 3 separate voltages are Needed", "C) Only 2 Separate Voltages are needed", "D) None of the above"],
        "answer": "A) Neutral and 2 separate voltages are Needed"
    },
    {
        "question": "Which of the following is a power efficiency metric used in data centers?",
        "options": ["A) RPM", "B) PUE", "C) MVA", "D) UPS"],
        "answer": "B) PUE"
    },
    {
        "question": "Which voltage is standard for single-phase supply?",
        "options": ["A) 215V", "B) 230V", "C) 415V", "D) 430V"],
        "answer": "B) 230V"
    },
    {
        "question": "Where to patch AC SPD alarm in ICC710 (     )?",
        "options": ["A) DIN6", "B) DIN4", "C) DIN8", "D) DIN3"],
        "answer": "A) DIN6"
    }

    

        
    ],
    "multiple_choice": [
       {
            "question": "What are the impacts of level-1 VSWR alarm?",
            "options": ["A) Service interrupt", "B) The RF emissive power reduces", "C) The amplifier of RF unit is shut down", "D) Shrink the cell coverage"],
            "answer": ["B) The RF emissive power reduces", "D) Shrink the cell coverage"]  # Correct answers
        },
        {
        "question": "What are the impacts of level-1 VSWR alarm?",
        "options": [
            "A) Service interrupt",
            "B) The RF emissive power reduces",
            "C) The amplifier of RF unit is shut down",
            "D) Shrink the cell coverage"
        ],
        "answer": ["B) The RF emissive power reduces", "D) Shrink the cell coverage"]
    },
    {
        "question": "Which type of the transmission can be supported by WMPT board?",
        "options": [
            "A) E1/T1",
            "B) Electronic IP",
            "C) Optical IP",
            "D) Microwave"
        ],
        "answer": ["A) E1/T1", "B) Electronic IP", "C) Optical IP"]
    },
    {
        "question": "BBU3900’s functions include",
        "options": [
            "A) interactive communication between BTS and BSC",
            "B) provide the system clock",
            "C) BTS Centralized Management",
            "D) provide the maintenance channel with LMT(or M2000)"
        ],
        "answer": ["A) interactive communication between BTS and BSC", "B) provide the system clock", "C) BTS Centralized Management", "D) provide the maintenance channel with LMT(or M2000)"]
    },
    {
        "question": "Option board of BBU3900 includes",
        "options": [
            "A) power module UPEU",
            "B) E1 surge protector UELP",
            "C) Universal clock unit USCU",
            "D) Environment monitor interface board UEIU"
        ],
        "answer": ["B) E1 surge protector UELP", "C) Universal clock unit USCU", "D) Environment monitor interface board UEIU"]
    },
    {
        "question": "The typical installation of BTS3900 includes",
        "options": [
            "A) concrete floor",
            "B) stub fixed",
            "C) ESD floor",
            "D) sand ground installation"
        ],
        "answer": ["A) concrete floor", "C) ESD floor"]
    },
    
    {
        "question": "Which of the following statements of grounding is correct?",
        "options": [
            "A) First connect grounding cables when installation; unmount grounding cables at the end when Un-deployment",
            "B) Destroy grounding conductor is prohibit",
            "C) Operate device before installing grounding conductor is prohibit",
            "D) Device should ground with reliability"
        ],
        "answer": ["A) First connect grounding cables when installation; unmount grounding cables at the end when Un-deployment", "C) Operate device before installing grounding conductor is prohibit", "D) Device should ground with reliability"]
    },
    {
        "question": "Which of the following statements of GPS installation is correct?",
        "options": [
            "A) GPS antenna should install at the protect area of lighting rod(45 degree below the lighting rod top)",
            "B) Keep metal base horizon, use washer when need",
            "C) Fixing the GPS firmly, nothing block the vertical 90 degree area of the antenna",
            "D) Waterproof is needed at the connector between GPS antenna and feeder"
        ],
        "answer": ["A) GPS antenna should install at the protect area of lighting rod(45 degree below the lighting rod top)", "B) Keep metal base horizon, use washer when need", "C) Fixing the GPS firmly, nothing block the vertical 90 degree area of the antenna", "D) Waterproof is needed at the connector between GPS antenna and feeder"]
    },
    {
        "question": "Which of the following statements about PRRU installation is incorrect?",
        "options": [
            "A) Keep the equipment away from the room where there is water leaking or dripping.",
            "B) Do not install PRRU next to strong heat source equipment.",
            "C) The pRRU should be installed at least 50 cm away from heat sources or temperature-sensitive devices.",
            "D) The installation position, specifications, models, and supports of the antenna must meet the engineering design requirements."
        ],
        "answer": ["D) The installation position, specifications, models, and supports of the antenna must meet the engineering design requirements."]
    },
    
    {
        "question": "The cross-sectional area of the PGND cable of the FOIS300 outdoor cabinet is () The cross-sectional area of the AC power cable is not less than (A).",
        "options": [
            "A) 25mm2, 4mm2",
            "B) 25mm2, 6mm2",
            "C) 16mm2, 4mm2"
        ],
        "answer": ["A) 25mm2, 4mm2"]
    },
    {
        "question": "After unpacking a cabinet or BBU, you must power on the cabinet or BBU within (B) days.",
        "options": [
            "A) 1 day",
            "B) 7 days",
            "C) 14 days",
            "D) NA"
        ],
        "answer": ["B) 7 days"]
    },
    {
        "question": "The installation path ground cable should be ()",
        "options": [
            "A) As short as possible",
            "B) As long as possible",
            "C) No turning",
            "D) At least one turn"
        ],
        "answer": ["A) As short as possible"]
    },
    {
        "question": "Cables should be connected () to avoid water entering the junction box.",
        "options": [
            "A) Down to the top",
            "B) Up to the bottom",
            "C) Both sides",
            "D) Back"
        ],
        "answer": ["A) Down to the top"]
    },
    {
        "question": "Cables inside the cabinet must be routed according to the rules. () cables must be bundled to the cabinet.",
        "options": [
            "A) Left cabling",
            "B) Right cabling",
            "C) Far cabling",
            "D) Separate cabling on both sides of the cabinet"
        ],
        "answer": ["D) Separate cabling on both sides of the cabinet"]
    },
    {
        "question": "After excavation of foundation pit, the main content of trench inspection is to check ()",
        "options": [
            "A) Foundation Substrate soil",
            "B) Concrete cushion",
            "C) Construction safety",
            "D) Ambient environment"
        ],
        "answer": ["A) Foundation Substrate soil"]
    },
    {
        "question": "Which statements about the sealing of cable holes in the cabinet is unreasonable?",
        "options": [
            "A) All cable inlets and outlet holes of the cabinet must be closed.",
            "B) The cable openings of plastic parts must be properly cut.",
            "C) The cable openings of plastic parts must be neat and insulated.",
            "D) The cable holes on the cabinet can be properly closed to ensure ventilation of the cabinet."
        ],
        "answer": ["D) The cable holes on the cabinet can be properly closed to ensure ventilation of the cabinet."]
    },
    {
        "question": "The cable holes at the bottom of the outdoor cabinet need to be sealed with sealing materials. Which of the following is not a common sealing material?",
        "options": [
            "A) Silicone",
            "B) Oil sludge",
            "C) Cement"
        ],
        "answer": ["C) Cement"]
    },
    {
        "question": "Which of the following statements are correct about waterproofing the 3+3 connector of the RRU RF jumper?",
        "options": [
            "A) Step 1: Wrap three layers of waterproof tape on the connector.",
            "B) Step 2: Wrap three layers of PVC insulation tape.",
            "C) Step 3: Start binding cable ties to the cable at a position.",
            "D) All of the above are correct."
        ],
        "answer": ["A) Step 1: Wrap three layers of waterproof tape on the connector.", "B) Step 2: Wrap three layers of PVC insulation tape.", "C) Step 3: Start binding cable ties to the cable at a position."]
    },
    {
        "question": "Which statements about the removal of old equipment are correct?",
        "options": [
            "A) The old equipment must be intact.",
            "B) Use waterproof and dustproof materials to protect the ports.",
            "C) Old cables must be coiled and bundled separately.",
            "D) Old devices can be thrown away without recycling."
        ],
        "answer": ["A) The old equipment must be intact.", "B) Use waterproof and dustproof materials to protect the ports.", "C) Old cables must be coiled and bundled separately."]
    },
    
        {
            "question": "Which type of the transmission can be supported by WMPT board?",
            "options": ["A) E1/T1", "B) Electronic IP", "C) Optical IP", "D) Microwave"],
            "answer": ["A) E1/T1", "B) Electronic IP", "C) Optical IP"]  # Correct answers
        },
        
        {
            "question": "BBU3900’s functions include:",
            "options": [
                "A) Interactive communication between BTS and BSC", 
                "B) Provide the system clock", 
                "C) BTS Centralized Management", 
                "D) Provide the maintenance channel with LMT (or M2000)"
            ],
            "answer": ["A) Interactive communication between BTS and BSC", "B) Provide the system clock", "C) BTS Centralized Management", "D) Provide the maintenance channel with LMT (or M2000)"]  # All options are correct
        },
        {
            "question": "Option board of BBU3900 include:",
            "options": [
                "A) Power module UPEU", 
                "B) E1 surge protector UELP", 
                "C) Universal clock unit USCU", 
                "D) Environment monitor interface board UEIU"
            ],
            "answer": ["B) E1 surge protector UELP", "C) Universal clock unit USCU", "D) Environment monitor interface board UEIU"]  # Correct answers
        },
        {
            "question": "The typical installation of BTS3900 include:",
            "options": ["A) Concrete floor", "B) Stub fixed", "C) ESD floor", "D) Sand ground installation"],
            "answer": ["A) Concrete floor", "C) ESD floor"]  # Correct answers
        },
        {
            "question": "Which of the following statements of grounding is correct?",
            "options": [
                "A) First connect grounding cables when installation; unmount grounding cables at the end when Un-deployment", 
                "B) Destroy grounding conductor is prohibit", 
                "C) Operate device before installing grounding conductor is prohibit", 
                "D) Device should ground with reliability"
            ],
            "answer": ["A) First connect grounding cables when installation; unmount grounding cables at the end when Un-deployment", "C) Operate device before installing grounding conductor is prohibit", "D) Device should ground with reliability"]  # Correct answers
        },
        {
            "question": "Which of following statements of GPS installation is correct?",
            "options": [
                "A) GPS antenna should install at the protect area of lighting rod (45 degree below the lighting rod top)", 
                "B) Keep metal base horizon, use washer when need", 
                "C) Fixing the GPS firmly, nothing block the vertical 90 degree area of the antenna", 
                "D) Waterproof is needed at the connector between GPS antenna and feeder"
            ],
            "answer": ["A) GPS antenna should install at the protect area of lighting rod (45 degree below the lighting rod top)", "B) Keep metal base horizon, use washer when need", "C) Fixing the GPS firmly, nothing block the vertical 90 degree area of the antenna", "D) Waterproof is needed at the connector between GPS antenna and feeder"]  # All options are correct
        },
       {
            "question": "The key tasks for Site Supervisor are:",
            "options": [
                "A) Carry out an onsite risk assessment",
                "B) Ensure the rescue kit is on site and is suitable",
                "C) All PPE and equipment is fit for purpose and used",
                "D) Any exclusion zones (drop zones) are suitable"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "All work at height requires planning. A risk assessment must be carried out to identify:",
            "options": [
                "A) The significant rated hazards",
                "B) The medium rated hazards",
                "C) The low rated hazards",
                "D) No hazards"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "RF safety needs to be minded following:",
            "options": [
                "A) All RF related working need competent and certified person",
                "B) Ensure to understand the safety area of antenna before approaching to antenna",
                "C) Need to shut down power if must work in unsafe area of RF",
                "D) Must not remove RF cable and connectors when they are running in order to avoid RF burst"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "The project EHS management requirement comes from:",
            "options": [
                "A) Local EHS-related laws and regulations, international standards",
                "B) EHS-related clauses in the contract with the customer, customer’s requirements and expectations for EHS management",
                "C) Huawei minimum safety standards and EHS management absolute rules",
                "D) None of the above"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "EHS 3P Self-Management includes:",
            "options": [
                "A) Prepare to work safely",
                "B) Pre-Task Check",
                "C) Performing Check",
                "D) PPE Check"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "Working at height, PPE shall include:",
            "options": [
                "A) Head protection",
                "B) Foot protection",
                "C) Full body harness",
                "D) Eye protection"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "Working at the tower safely:",
            "options": [
                "A) Not allow one rigger to work on tower, a watchman must standby",
                "B) Must check PPE and wear PPE per requirements",
                "C) Ensure lanyard is fixed at 2 different points",
                "D) Carried tools shall be kept in a bag to avoid being dropped down"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "Field working:",
            "options": [
                "A) Need to prepare enough food as it is not convenient for food outside",
                "B) Normally need 2 or more workers to go to avoid being robbed or hurt by wild animals, take protection facility when needed, and avoid working late",
                "C) Need to wear anti-skidding shoes and clothes fit to the body",
                "D) None of the above"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "Working safety needs consideration of local weather patterns, such as:",
            "options": [
                "A) Wind speeds",
                "B) Temperature and temperature changes",
                "C) Humidity levels",
                "D) Snow/ice formation and type/frequency of rainfall"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "Before work, need to analyze the risk source and take necessary actions for prevention with PPE for:",
            "options": [
                "A) Getting an electric shock",
                "B) Dropping from height",
                "C) Being hit by dropping product",
                "D) Traffic accidents"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "Unsafe acts that cause accidents and incidents include:",
            "options": [
                "A) Working without authority",
                "B) Failure to warn others of danger",
                "C) Using dangerous or wrong equipment",
                "D) Horseplay"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "EHS objectives are:",
            "options": [
                "A) Zero Fatalities",
                "B) Zero Injuries",
                "C) Zero Accidents",
                "D) Zero defects in the product"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "Safety areas of engineering construction must have:",
            "options": [
                "A) Alert signs and fence facilities",
                "B) Workers in unsafe areas need related protection (e.g., helmet, gloves, vest, eye protection glasses, and safety shoes) and necessary safety facilities and tools",
                "C) Dangerous operations must be equipped with emergency response and safety protection approaches for worker safety",
                "D) None of the above"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "Risks to health and safety that may arise from radio frequency (RF) fields include:",
            "options": [
                "A) Interaction of RF fields with the human body",
                "B) Interference with medical equipment",
                "C) Interference with safety-related electronics",
                "D) Fuel and flammable atmospheres"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "Managing EHS Risk includes:",
            "options": [
                "A) EHS Risk recognition",
                "B) EHS Risk evaluation",
                "C) EHS Risk control",
                "D) EHS Risk monitoring"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
        {
            "question": "Safety Signs should include but not be limited to the following:",
            "options": [
                "A) No access to unauthorized persons",
                "B) Safety Helmets must be worn",
                "C) Working at height",
                "D) None of the above"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "EHS Check in project delivery includes:",
            "options": [
                "A) Subcontractor Self-check",
                "B) Random Spot-check",
                "C) No check",
                "D) Leadership Safety Tour"
            ],
            "answer": ["A", "B", "D"]  # Correct answers
        },
        {
            "question": "For electrical safety:",
            "options": [
                "A) Power cables are not allowed to be put on the ground",
                "B) Overload for power cable is not allowed",
                "C) Damaged components of power must be replaced in time",
                "D) None of the above"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "For vehicle seat belts, the correct answers are:",
            "options": [
                "A) All company vehicles fitted with seat belts",
                "B) Seat belts checked as part of routine maintenance",
                "C) Driver training includes the use of seat belts",
                "D) None of the above"
            ],
            "answer": ["A", "B", "C"]  # Correct answers
        },
        {
            "question": "Fitness to drive can be affected by a number of issues:",
            "options": [
                "A) Illness",
                "B) Drug use",
                "C) Alcohol consumption",
                "D) Age"
            ],
            "answer": ["A", "B", "C", "D"]  # Correct answers
        },
       {
        "question": "Antenna Types include",
        "options": ["A) Single band", "B) Dual Band", "C) Tri-Band", "D) Quad band", "E) Penta band"],
        "answer": ["A) Single band", "B) Dual Band", "C) Tri-Band", "D) Quad band", "E) Penta band"]
    },
    {
        "question": "UBBP Board can be installed in BBU at",
        "options": ["A) Slot 7", "B) Slot 1", "C) Slot 4", "D) Slot 3", "E) Slot 5", "F) Slot 2"],
        "answer": ["B) Slot 1", "C) Slot 4", "D) Slot 3", "E) Slot 5", "F) Slot 2"]
    },
    {
        "question": "UPEU Board can be installed in BBU at",
        "options": ["A) Slot 18", "B) Slot 1", "C) Slot 4", "D) Slot 19", "E) Slot 5", "F) Slot 2"],
        "answer": ["A) Slot 18", "D) Slot 19"]
    },
    {
        "question": "DBS3900/5900 system consists of",
        "options": ["A) BBU", "B) RRU", "C) Antenna", "D) RCU (Optional)"],
        "answer": ["A) BBU", "B) RRU", "C) Antenna", "D) RCU (Optional)"]
    },
    {
        "question": "HUAWEI Main Base Station",
        "options": ["A) Indoor eNodeB BTS3900", "B) Outdoor eNodeB BTS3900", "C) Distributed eNodeB DBS3900"],
        "answer": ["A) Indoor eNodeB BTS3900", "B) Outdoor eNodeB BTS3900", "C) Distributed eNodeB DBS3900"]
    },
    {
        "question": "What are UBBP boards types",
        "options": ["A) UBBPd5", "B) UBBPe2", "C) UBBPg", "D) UBBPj"],
        "answer": ["A) UBBPd5", "B) UBBPe2", "C) UBBPg", "D) UBBPj"]
    },
    {
        "question": "Below are BBU Boards",
        "options": ["A) RRU", "B) UBBP", "C) UPEU", "D) UMPT"],
        "answer": ["B) UBBP", "C) UPEU", "D) UMPT"]
    },
    {
        "question": "BBU Installation scenarios",
        "options": ["A) Indoor", "B) Outdoor", "C) Indoor on the wall"],
        "answer": ["A) Indoor", "B) Outdoor", "C) Indoor on the wall"]
    },
{
        "question": "RTN905-2F supports (   ) IF ports.",
        "options": ["A) One IF port", "B) Three IF ports", "C) Five IF ports", "D) Two IF Ports"],
        "answer": "D) Two IF Ports"
    },
    {
        "question": "RTN905-2F can easily use at (   ) layers.",
        "options": ["A) Three sites dependent HUB site", "B) Access layer", "C) Aggregation layers", "D) Fiber Nodes"],
        "answer": "B) Access layer"
    },
    {
        "question": "In case of New link installation, must confirm before MW link installation (   ).",
        "options": ["A) Check the delivered equipment on site with Huawei provided link budget in detail", "B) Check security guard's uniform", "C) Check the fuel tank of Generator", "D) Check the Wapda transformer on site"],
        "answer": "A) Check the delivered equipment on site with Huawei provided link budget in detail"
    },
    {
        "question": "SDB MW link have combination of two freq bands, which are (   ).",
        "options": ["A) 23GHz & 38GHz", "B) 18GHz & 6GHz", "C) 13GHz & 80GHz", "D) 11GHz & 15GHz", "E) 6GHz & 7GHz"],
        "answer": "C) 13GHz & 80GHz"
    },
    {
        "question": "Control card CSHOF have total 10G(o) ports.",
        "options": ["A) one port", "B) Three ports", "C) Five ports", "D) Two Ports"],
        "answer": "D) Two Ports"
    },
    {
        "question": "Input voltage of RTN950A are as follow.",
        "options": ["A) –48 V DC power inputs with 20A fuse capacity", "B) –40 V DC power inputs with 10A fuse capacity", "C) –80 V DC power inputs with 40A fuse capacity", "D) –20 V DC power inputs with 20A fuse capacity"],
        "answer": "A) –48 V DC power inputs with 20A fuse capacity"
    },
    {
        "question": "No of IF ports of XMC-3E ODU is (  ).",
        "options": ["A) one port", "B) Three ports", "C) Five ports", "D) Two Ports"],
        "answer": "A) one port"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) XMC-5D ODU have two IF ports & called 1T1R", "B) XMC-5D ODU have two IF ports & called 2T2R", "C) XMC-5D ODU have Four IF ports & called 4T4R", "D) XMC-5D ODU have three IF ports & called 3T3R"],
        "answer": "B) XMC-5D ODU have two IF ports & called 2T2R"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) RTN6900 -ISM10 have 1 sub board slot used for only EBBsa", "B) RTN6900 -ISM10 have 1 sub board slot used for only ISMsa", "C) RTN6900 -ISM10 have 1 sub board slot used for only ISM8", "D) RTN6900 -ISM10 have 1 sub board slot used for ISMsa & EBBsa"],
        "answer": "D) RTN6900 -ISM10 have 1 sub board slot used for ISMsa & EBBsa"
    },
    {
        "question": "Single Polarized antennae can only used for.",
        "options": ["A) 13G_1+0 XPIC link", "B) 23G_2+0 XPIC link", "C) 1+0 link", "D) SDB Microwave link"],
        "answer": "C) 1+0 link"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) We can use 38GHz ODU with 6GHz Antennae", "B) We can use 38GHz ODU with 38GHz Antennae", "C) We can use 23GHz ODU with 8GHz Antennae", "D) We can use 13GHz ODU with 80GHz Antennae"],
        "answer": "B) We can use 38GHz ODU with 38GHz Antennae"
    },
    {
        "question": "Which MW is Full outdoor.",
        "options": ["A) RTN380", "B) RTN950A", "C) RTN950A", "D) RTN10A"],
        "answer": "A) RTN380"
    },
    {
        "question": "Which Control Board related with RTN 950A.",
        "options": ["A) CSHN", "B) CSH", "C) CSHNU", "D) CSHO"],
        "answer": "D) CSHO"
    },
    {
        "question": "Which Service Boards are related with RTN980.",
        "options": ["A) EM6X", "B) CSH", "C) CSHNA", "D) CSHNU"],
        "answer": "A) EM6X"
    },
    {
        "question": "If Critical incident found the incident must report with in () minutes.",
        "options": ["A) 60", "B) 30", "C) 15", "D) 5"],
        "answer": "D) 5"
    },
    {
        "question": "Can we download & use any Third Party Software from internet websites.",
        "options": ["A) Yes", "B) No"],
        "answer": "B) No"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) Antennae with 18GHz freq can support 23GHz & 38GHz freq ODU", "B) Antennae with 18GHz freq can support 18GHz & 38GHz freq ODU", "C) Antennae with 18GHz freq can support 13GHz & 38GHz freq ODU", "D) Antennae with 18GHz freq can support only 18GHz freq ODU"],
        "answer": "C) Antennae with 18GHz freq can support 13GHz & 38GHz freq ODU"
    },
    {
        "question": "Which RTN IF boards have Dual port of IF.",
        "options": ["A) ISV3", "B) ISU2", "C) ISM6", "D) IF1A"],
        "answer": "C) ISM6"
    },
    {
        "question": "Which IF card have 10G Port.",
        "options": ["A) ISM6", "B) ISV3", "C) ISX2", "D) ISM8"],
        "answer": "D) ISM8"
    },
    {
        "question": "Which RTN900 ODU have Dual IF port.",
        "options": ["A) 13G XMC-3", "B) 23G-XMC-2", "C) 15G-XMC-3", "D) 15G-XMC5D"],
        "answer": "D) 15G-XMC5D"
    },
    {
        "question": "When installing the IF board, E1 board and EHT board, what need to use.",
        "options": ["Screw Driver", "Antistatic Wrist strap", "Label Printer"],
        "answer": "B) Antistatic Wrist strap"
    },
    {
        "question": "Default polarization of MW antenna is.",
        "options": ["A) Vertical", "B) Horizontal", "C) None of the above"],
        "answer": "A) Vertical"
    },
    {
        "question": "How many supporting rods are required for 1.8M MW Antenna.",
        "options": ["A) 1", "B) 3", "C) 2", "D) 4"],
        "answer": "C) 2"
    },
    {
        "question": "Pair slots in RTN980 are.",
        "options": ["A) 7,9", "B) 6,8", "C) 3,5", "D) 2,4"],
        "answer": "C) 3,5"
    },
    {
        "question": "ISM10 Board can be installed in.",
        "options": ["A) RTN950A", "B) RTN6900", "C) RTN980"],
        "answer": "B) RTN6900"
    },
    {
        "question": "ISMsa is sub board of.",
        "options": ["A) ISM10", "B) ISM8", "C) ISM6", "D) ISV3"],
        "answer": "A) ISM10"
    },
    {
        "question": "RTN6900 Supports which type of ODU.",
        "options": ["A) XMC-2", "B) XMC-3", "C) XMC-5D", "D) XMC-5D Pro"],
        "answer": "D) XMC-5D Pro"
    },
    {
        "question": "Running mode supported by ISM8 card.",
        "options": ["A) IS3", "B) IS8", "C) IS6", "D) All of the above"],
        "answer": "D) All of the above"
    },
    {
        "question": "How many antennas required for 1+1 XPIC Configurations.",
        "options": ["A) 2", "B) 4", "C) None of the above"],
        "answer": "A) 2"
    },
    {
        "question": "While working on Ufone network must consider the (   ).",
        "options": ["A) Huawei Engineers have allowed to access or connect with other vendor equipment", "B) Prohibit to operate/login in any other vendor equipment", "C) After completing the activity leave the site without NOC confirmation for services alarms", "D) ignore the interference coming from other Ufone's MW link"],
        "answer": "B) Prohibit to operate/login in any other vendor equipment"
    },
    {
        "question": "ODU grounding is (   ).",
        "options": ["A) Necessary", "B) Not Necessary"],
        "answer": "A) Necessary"
    },
    {
        "question": "IDU grounding is (   ).",
        "options": ["A) Necessary", "B) Not Necessary"],
        "answer": "A) Necessary"
    },
    {
        "question": "IF grounding, Nito & self bonding are (   ).",
        "options": ["A) Necessary", "B) Not Necessary"],
        "answer": "A) Necessary"
    },
{
        "question": "The Network Communication Modes include (   ).",
        "options": [
            "A) Simplex",
            "B) Half Duplex",
            "C) Full Duplex",
            "D) Microwave",
            "E) Simplex+Half Duplex+Full Duplex"
        ],
        "answer": ["A) Simplex", "B) Half Duplex", "C) Full Duplex"]
    },
    {
        "question": "OSI Model Network Layers Include (   ).",
        "options": [
            "A) Transport Layer",
            "B) Control Layer",
            "C) Physical Layer",
            "D) Protocol Layer",
            "E) Transport Layer + Physical Layer"
        ],
        "answer": ["A) Transport Layer", "C) Physical Layer"]
    },
    {
        "question": "Types of Diode Include (   ).",
        "options": [
            "A) Laser Diode",
            "B) Zener Diode",
            "C) Light Emitting Diode",
            "D) PN junction Diode",
            "E) Laser Diode+Zener Diode+Light Emitting Diode"
        ],
        "answer": ["A) Laser Diode", "B) Zener Diode", "C) Light Emitting Diode"]
    },
    {
        "question": "Lithium battery: ESM-48100A6 can be used for cabinets (   ).",
        "options": [
            "A) ICC330-HA1-C11",
            "B) ICC330-HD1-C6",
            "C) ICC360-HA1-C2",
            "D) ICC800-A1-C2",
            "E) ICC330-HA1-C11 + ICC360-HA1-C2 + ICC330-HD1-C6 + ICC800-A1-C2"
        ],
        "answer": ["A) ICC330-HA1-C11", "B) ICC330-HD1-C6", "C) ICC360-HA1-C2", "D) ICC800-A1-C2"]
    },
    {
        "question": "Lithium Ion Cells are used in applications like (   ).",
        "options": [
            "A) Smartphones",
            "B) Medical devices",
            "C) Power tools",
            "D) Vehicles",
            "E) Smartphone+Medical devices+Power tools"
        ],
        "answer": ["A) Smartphones", "B) Medical devices", "C) Power tools"]
    },
    {
        "question": "The Major types of UPS system configurations are (   ).",
        "options": [
            "A) Online double conversion",
            "B) Battery back up",
            "C) Line interactive",
            "D) Single Conversion",
            "E) Online double conversion+Battery back up+Line interactive"
        ],
        "answer": ["A) Online double conversion", "B) Battery back up", "C) Line interactive"]
    },
    {
        "question": "Which of the following components are typically used in telecom power systems? (   ).",
        "options": [
            "A) Rectifier",
            "B) Inverter",
            "C) Battery",
            "D) Firewall",
            "E) Rectifier+Inverter+Battery"
        ],
        "answer": ["A) Rectifier", "B) Inverter", "C) Battery"]
    },
    {
        "question": "What Sensors does a cabinet contain (   ).",
        "options": [
            "A) Smoke",
            "B) Water",
            "C) Dust",
            "D) GPS",
            "E) Smoke+Dust+Water+GPS"
        ],
        "answer": ["A) Smoke", "B) Water", "C) Dust", "D) GPS"]
    },
    {
        "question": "What are the benefits of using DC power in telecom systems (   ).",
        "options": [
            "A) Lower energy losses",
            "B) Higher efficiency",
            "C) Simple power conversion",
            "D) Higher voltage",
            "E) Lower energy losses+Higher efficiency+Simple power conversion"
        ],
        "answer": ["A) Lower energy losses", "B) Higher efficiency", "C) Simple power conversion"]
    },
    {
        "question": "Which of the following are power sources for telecom towers? (   ).",
        "options": [
            "A) Diesel generators",
            "B) Solar panels",
            "C) Wind turbines",
            "D) Battery banks",
            "E) Diesel generators+Solar panels+Wind turbines+Battery banks"
        ],
        "answer": ["A) Diesel generators", "B) Solar panels", "C) Wind turbines"]
    },
    {
        "question": "Telecom backup power systems typically include (   ).",
        "options": [
            "A) Generators",
            "B) Rectifiers",
            "C) Batteries",
            "D) PDUs",
            "E) Generators+Rectifiers+Batteries"
        ],
        "answer": ["A) Generators", "B) Rectifiers", "C) Batteries"]
    },
    {
        "question": "Hybrid telecom power systems may use (   ).",
        "options": [
            "A) Solar power",
            "B) Wind power",
            "C) Diesel generators",
            "D) UPS systems",
            "E) Solar power+Wind power+Diesel generators+UPS systems"
        ],
        "answer": ["A) Solar power", "B) Wind power", "C) Diesel generators"]
    },
    {
        "question": "Data Center Power Scenario (   ).",
        "options": [
            "A) UPS systems",
            "B) Power Distribution Units (PDUs)",
            "C) Cooling systems",
            "D) Network switches",
            "E) UPS systems+Power Distribution Units (PDUs)+Cooling systems"
        ],
        "answer": ["A) UPS systems", "B) Power Distribution Units (PDUs)", "C) Cooling systems"]
    },
    {
        "question": "Which of the following are used to ensure power redundancy in data centers? (   ).",
        "options": [
            "A) Backup generators",
            "B) Multiple UPS systems",
            "C) Dual power supplies",
            "D) Battery banks",
            "E) Backup generators+Multiple UPS systems+Dual power supplies+Battery banks"
        ],
        "answer": ["A) Backup generators", "B) Multiple UPS systems", "C) Dual power supplies"]
    },
    {
        "question": "Power usage in a data center can be optimized by (   ).",
        "options": [
            "A) Using high-efficiency PDUs",
            "B) Reducing cooling power consumption",
            "C) Implementing power monitoring",
            "D) Increasing server density",
            "E) Using high-efficiency PDUs+Reducing cooling power consumption+Implementing power monitoring"
        ],
        "answer": ["A) Using high-efficiency PDUs", "B) Reducing cooling power consumption", "C) Implementing power monitoring"]
    },
    {
        "question": "Which of the following metrics are used to measure data center power efficiency? (   ).",
        "options": [
            "A) PUE (Power Usage Effectiveness)",
            "B) UPS runtime",
            "C) Load balancing",
            "D) Cooling energy efficiency",
            "E) PUE (Power Usage Effectiveness)"
        ],
        "answer": ["A) PUE (Power Usage Effectiveness)"]
    },
    {
        "question": "Data center power management includes (   ).",
        "options": [
            "A) Load distribution",
            "B) Energy efficiency monitoring",
            "C) Generator maintenance",
            "D) Heat dissipation management",
            "E) Load distribution+Energy efficiency monitoring+Generator maintenance"
        ],
        "answer": ["A) Load distribution", "B) Energy efficiency monitoring", "C) Generator maintenance"]
    },
    {
        "question": "Which of the following are common voltage levels used in telecom power systems (   ).",
        "options": [
            "A) 24V",
            "B) 48V",
            "C) 110V",
            "D) 220V",
            "E) 24V+48V+110V"
        ],
        "answer": ["A) 24V", "B) 48V", "C) 110V"]
    },
    {
        "question": "Which components are essential for converting AC to DC in telecom systems (   ).",
        "options": [
            "A) Rectifier",
            "B) Transformer",
            "C) Inverter",
            "D) UPS",
            "E) Rectifier"
        ],
        "answer": ["A) Rectifier"]
    },
    {
        "question": "What types of batteries are commonly used in telecom power systems (   ).",
        "options": [
            "A) Lead-acid",
            "B) Lithium-ion",
            "C) Nickel-Cadmium",
            "D) Alkaline",
            "E) Lead-acid+Lithium-ion+Nickel-Cadmium"
        ],
        "answer": ["A) Lead-acid", "B) Lithium-ion", "C) Nickel-Cadmium"]
    },
    {
        "question": "Which of the following are benefits of using DC power in telecom networks (   ).",
        "options": [
            "A) Lower energy losses",
            "B) Simpler design",
            "C) Reduced cooling needs",
            "D) Enhanced signal quality",
            "E) Lower energy losses+Simpler design"
        ],
        "answer": ["A) Lower energy losses", "B) Simpler design"]
    },
    {
        "question": "What types of backup power sources can be found in telecom sites (   ).",
        "options": [
            "A) Batteries",
            "B) Solar panels",
            "C) Diesel generators",
            "D) Fuel cells",
            "E) Batteries+Solar panels+Diesel generators"
        ],
        "answer": ["A) Batteries", "B) Solar panels", "C) Diesel generators"]
    },
    {
        "question": "Which of the following devices are used to protect telecom equipment from voltage spikes (   ).",
        "options": [
            "A) Circuit Breaker",
            "B) SPD (Surge Protection Device)",
            "C) Transformer",
            "D) Inverter",
            "E) SPD (Surge Protection Device)"
        ],
        "answer": ["B) SPD (Surge Protection Device)"]
    },
    {
        "question": "Which renewable energy sources are integrated into telecom power systems (   ).",
        "options": [
            "A) Wind power",
            "B) Solar power",
            "C) Hydroelectric power",
            "D) Geothermal power",
            "E) Wind power+Solar power"
        ],
        "answer": ["A) Wind power", "B) Solar power"]
    },
    {
        "question": "Which components can be found in a telecom power distribution unit (   ).",
        "options": [
            "A) Circuit breakers",
            "B) Meters",
            "C) UPS",
            "D) Transformers",
            "E) Circuit breakers+Meters+Transformers"
        ],
        "answer": ["A) Circuit breakers", "B) Meters", "D) Transformers"]
    },
    {
        "question": "What are the main functions of a Battery Management System (BMS) (   ).",
        "options": [
            "A) Monitor battery health",
            "B) Regulate voltage",
            "C) Optimize charging",
            "D) Distribute power",
            "E) Monitor battery health+Regulate voltage+Optimize charging"
        ],
        "answer": ["A) Monitor battery health", "B) Regulate voltage", "C) Optimize charging"]
    },
    {
        "question": "Which of the following issues can affect telecom power systems (   ).",
        "options": [
            "A) Overvoltage",
            "B) Under-voltage",
            "C) Power surges",
            "D) Network congestion",
            "E) Overvoltage+Under-voltage+Power surges"
        ],
        "answer": ["A) Overvoltage", "B) Under-voltage", "C) Power surges"]
    },
    {
        "question": "Which types of energy sources are increasingly being used in hybrid telecom power systems (   ).",
        "options": [
            "A) Diesel generators",
            "B) Solar panels",
            "C) Wind turbines",
            "D) Biomass",
            "E) Solar panels+Wind turbines"
        ],
        "answer": ["B) Solar panels", "C) Wind turbines"]
    },
    {
        "question": "What are the advantages of using a UPS in telecom applications (   ).",
        "options": [
            "A) Provides immediate backup",
            "B) Stabilizes voltage",
            "C) Reduces energy costs",
            "D) Increases system complexity",
            "E) Provides immediate backup+Stabilizes voltage"
        ],
        "answer": ["A) Provides immediate backup", "B) Stabilizes voltage"]
    },
    {
        "question": "Which components are commonly used for voltage regulation in telecom systems (   ).",
        "options": [
            "A) Voltage regulators",
            "B) Transformers",
            "C) Capacitors",
            "D) Inductors",
            "E) Voltage regulators+Transformers"
        ],
        "answer": ["A) Voltage regulators", "B) Transformers"]
    },
    {
        "question": "What are common maintenance practices for telecom power systems (   ).",
        "options": [
            "A) Regular battery checks",
            "B) Inspection of power distribution",
            "C) Cleaning of solar panels",
            "D) Software updates",
            "E) Regular battery checks+Inspection of power distribution+Cleaning of solar panels"
        ],
        "answer": ["A) Regular battery checks", "B) Inspection of power distribution", "C) Cleaning of solar panels"]
    },
    {
        "question": "Which safety measures are critical in telecom power installations (   ).",
        "options": [
            "A) Proper grounding",
            "B) Use of fuses",
            "C) Circuit breakers",
            "D) Fire suppression systems",
            "E) Proper grounding+Use of fuses+Circuit breakers"
        ],
        "answer": ["A) Proper grounding", "B) Use of fuses", "C) Circuit breakers"]
    },
    {
        "question": "What are the key components of a solar power system used in telecom (   ).",
        "options": [
            "A) Solar panels",
            "B) Inverters",
            "C) Battery storage",
            "D) Charge controllers",
            "E) Solar panels+Inverters+Battery storage"
        ],
        "answer": ["A) Solar panels", "B) Inverters", "C) Battery storage"]
    },
    {
        "question": "Which of the following are indicators of good power quality in telecom systems (   ).",
        "options": [
            "A) Low total harmonic distortion (THD)",
            "B) Stable voltage levels",
            "C) Minimal power interruptions",
            "D) High energy consumption",
            "E) Low total harmonic distortion (THD)+Stable voltage levels+Minimal power interruptions"
        ],
        "answer": ["A) Low total harmonic distortion (THD)", "B) Stable voltage levels", "C) Minimal power interruptions"]
    },
    {
        "question": "What types of communication networks commonly use DC power (   ).",
        "options": [
            "A) Mobile networks",
            "B) Fiber optic networks",
            "C) Fixed-line networks",
            "D) Satellite networks",
            "E) Mobile networks+Fixed-line networks"
        ],
        "answer": ["A) Mobile networks", "C) Fixed-line networks"]
    },
    {
        "question": "Which types of electrical connections are used in telecom power systems (   ).",
        "options": [
            "A) Star connection",
            "B) Delta connection",
            "C) Series connection",
            "D) Parallel connection",
            "E) Star connection+Delta connection+Parallel connection"
        ],
        "answer": ["A) Star connection", "B) Delta connection", "D) Parallel connection"]
    },
    {
        "question": "What are typical energy-saving technologies used in telecom systems (   ).",
        "options": [
            "A) Energy-efficient batteries",
            "B) Power factor correction devices",
            "C) Smart grids",
            "D) High-voltage transmission lines",
            "E) Energy-efficient batteries+Power factor correction devices+Smart grids"
        ],
        "answer": ["A) Energy-efficient batteries", "B) Power factor correction devices"]
    },
    {
        "question": "Which of the following are common types of UPS systems used in data centers (   ).",
        "options": [
            "A) Offline UPS",
            "B) Line-interactive UPS",
            "C) Online UPS",
            "D) Hybrid UPS",
            "E) Offline UPS+Line-interactive UPS+Online UPS"
        ],
        "answer": ["A) Offline UPS", "B) Line-interactive UPS", "C) Online UPS"]
    },
    {
        "question": "What are the typical cooling methods employed in data centers (   ).",
        "options": [
            "A) Air cooling",
            "B) Liquid cooling",
            "C) Evaporative cooling",
            "D) Solar cooling",
            "E) Air cooling+Liquid cooling+Evaporative cooling"
        ],
        "answer": ["A) Air cooling", "B) Liquid cooling", "C) Evaporative cooling"]
    },
    {
        "question": "Which power metrics are commonly used to assess data center efficiency (   ).",
        "options": [
            "A) PUE (Power Usage Effectiveness)",
            "B) DCiE (Data Center Infrastructure Efficiency)",
            "C) TCO (Total Cost of Ownership)",
            "D) CAPEX (Capital Expenditure)",
            "E) PUE (Power Usage Effectiveness)+DCiE (Data Center Infrastructure Efficiency)"
        ],
        "answer": ["A) PUE (Power Usage Effectiveness)", "B) DCiE (Data Center Infrastructure Efficiency)"]
    },
    {
        "question": "What types of energy sources can be integrated into data centers (   ).",
        "options": [
            "A) Diesel generators",
            "B) Natural gas",
            "C) Solar panels",
            "D) Wind turbines",
            "E) Diesel generators+Solar panels+Wind turbines"
        ],
        "answer": ["A) Diesel generators", "C) Solar panels", "D) Wind turbines"]
    },
    {
        "question": "Which of the following devices can be used for power monitoring in data centers (   ).",
        "options": [
            "A) Smart PDUs",
            "B) Energy meters",
            "C) Circuit breakers",
            "D) Transformers",
            "E) Smart PDUs+Energy meters"
        ],
        "answer": ["A) Smart PDUs", "B) Energy meters"]
    },
    {
        "question": "What factors can impact the reliability of power systems in data centers (   ).",
        "options": [
            "A) Redundant power supplies",
            "B) UPS configuration",
            "C) Cooling efficiency",
            "D) Power distribution architecture",
            "E) Redundant power supplies+UPS configuration"
        ],
        "answer": ["A) Redundant power supplies", "B) UPS configuration", "D) Power distribution architecture"]
    },
    {
        "question": "Which components are typically included in a data center power distribution system (   ).",
        "options": [
            "A) Transformers",
            "B) Circuit breakers",
            "C) PDUs",
            "D) Servers",
            "E) Transformers+Circuit breakers+PDUs"
        ],
        "answer": ["A) Transformers", "B) Circuit breakers", "C) PDUs"]
    },
    {
        "question": "What strategies can be employed to reduce energy consumption in data centers (   ).",
        "options": [
            "A) Efficient cooling systems",
            "B) Virtualization of servers",
            "C) Energy-efficient lighting",
            "D) Increased server count",
            "E) Efficient cooling systems+Virtualization of servers+Energy-efficient lighting"
        ],
        "answer": ["A) Efficient cooling systems", "B) Virtualization of servers", "C) Energy-efficient lighting"]
    },
    {
        "question": "Which factors should be considered when selecting a UPS for a data center (   ).",
        "options": [
            "A) Load capacity",
            "B) Runtime requirements",
            "C) Battery technology",
            "D) Cost",
            "E) Load capacity+Runtime requirements+Battery technology"
        ],
        "answer": ["A) Load capacity", "B) Runtime requirements", "C) Battery technology"]
    },
    {
        "question": "What is the purpose of redundancy in data center power systems (   ).",
        "options": [
            "A) Improve performance",
            "B) Ensure continuous operation during failures",
            "C) Reduce costs",
            "D) Increase cooling efficiency",
            "E) Ensure continuous operation during failures"
        ],
        "answer": ["B) Ensure continuous operation during failures"]
    },
    {
        "question": "What are some common causes of power interruptions in data centers (   ).",
        "options": [
            "A) Weather conditions",
            "B) Utility outages",
            "C) Equipment failures",
            "D) Maintenance activities",
            "E) Weather conditions+Utility outages+Equipment failures+Maintenance activities"
        ],
        "answer": ["A) Weather conditions", "B) Utility outages", "C) Equipment failures"]
    },
    {
        "question": "There should be ---- engineers from Suppliers for any major activity includes Huawei (   ).",
        "options": [
            "A) 2 Subon +1 Huawei",
            "B) 2 Subon +2 Huawei",
            "C) 1 Subon +0 Huawei",
            "D) 1 Subon +1 Huawei",
            "E) 2 Subon +1 Huawei & 1 Subcon + 1 Huawei"
        ],
        "answer": ["A) 2 Subon +1 Huawei", "E) 2 Subon +1 Huawei & 1 Subcon + 1 Huawei"]
    },
    {
        "question": "Core Site Activity which prerequisites Required in Core Room implemented by customer (   ).",
        "options": [
            "A) Proper EHS + Insulated Tools",
            "B) No EHS + Proper Tools",
            "C) Customer Regulations Follow",
            "D) No Need any Rules",
            "E) Proper EHS + Insulated Tools & Customer Regulations Follow"
        ],
        "answer": ["A) Proper EHS + Insulated Tools", "E) Proper EHS + Insulated Tools & Customer Regulations Follow"]
    },
    {
        "question": "BBU and RRU should be connected to which type of breakers (   ).",
        "options": [
            "A) 63 Amps LLVD",
            "B) 63 Amps BLVD",
            "C) 32Amps LLVD",
            "D) 32Amps BLVD",
            "E) 63 Amps LLVD & 32Amps BLVD"
        ],
        "answer": ["A) 63 Amps LLVD", "E) 63 Amps LLVD & 32Amps BLVD"]
    },
    {
        "question": "During Battery Installation, AC Power Should be Switched ---- while Battery Breaker should be switched---- (   ).",
        "options": [
            "A) ON/ON",
            "B) OFF/OFF",
            "C) ON/OFF",
            "D) OFF/ON",
            "E) OFF/OFF"
        ],
        "answer": ["B) OFF/OFF"]
    },
    {
        "question": "ICC710 can be used with following batteries back up (   ).",
        "options": [
            "A) ACB",
            "B) FCB",
            "C) TCB",
            "D) Narada",
            "E) ACB, FCB, TCB"
        ],
        "answer": ["E) ACB, FCB, TCB"]
    },
    {
        "question": "On Site SMU NetEco Port and UPEU/UEIU Card ports name are (   ).",
        "options": [
            "A) FE & ALM",
            "B) MON1 & RS485/232",
            "C) MON0 & RS485/232",
            "D) MON0 & FE",
            "E) MON1 & RS485/232 + MON0 & RS485/232"
        ],
        "answer": ["E) MON1 & RS485/232 + MON0 & RS485/232"]
    },
    {
        "question": "On Site LAN Cable's can be made with which Tools and Tested with which Meter (   ).",
        "options": [
            "A) Digonal Plier",
            "B) Cripping tool",
            "C) LAN Cable Tester",
            "D) DMM",
            "E) Cripping tool & LAN Cable Tester"
        ],
        "answer": ["E) Cripping tool & LAN Cable Tester"]
    },
    {
        "question": "240mm2 DC Cable Thimble can be made with-----and straight with------- (   ).",
        "options": [
            "A) Nose Plier",
            "B) Thimble Presser",
            "C) Hammer",
            "D) Screw Driver",
            "E) Thimble presser and Hammer"
        ],
        "answer": ["B) Thimble Presser", "C) Hammer"]
    }

    ]
}
# Flatten questions for navigation
if not st.session_state.flattened_questions:
    flattened_questions = []

    for category, qs in megaquiz.items():
        for q in qs:
            q['type'] = category  # Set the type for each question
            flattened_questions.append(q)

    # Shuffle questions within each type
    random.shuffle(flattened_questions)

    true_false_questions = [q for q in flattened_questions if q['type'] == 'true_false']
    single_choice_questions = [q for q in flattened_questions if q['type'] == 'single_choice']
    mcq_questions = [q for q in flattened_questions if q['type'] == 'multiple_choice']

    # Combine the questions in the desired order
    all_questions = (
    true_false_questions[:25] + 
    single_choice_questions[:25] + 
    mcq_questions[:20]
)

    # Limit to the first 200 questions
    st.session_state.flattened_questions = all_questions[:70]

# Initialize answers
if len(st.session_state.answers) != len(st.session_state.flattened_questions):
    st.session_state.answers = [None] * len(st.session_state.flattened_questions)


# Login form
if not st.session_state.logged_in:
    st.header("Welcome to Huawei Quiz Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")  # You might want to handle password validation separately

    if st.button("Login"):
        if username in allowed_usernames and password:  # Add password validation as needed
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.start_time = datetime.now()  # Track start time on login
            st.success("Logged in successfully!")
            st.session_state.logged_in = True
            st.experimental_set_query_params()  # Ensures the state is saved and reloaded without rerunning the entire script
              
        else:
            st.error("Please enter a valid username and password.")
else:
    st.sidebar.markdown(f"## Welcome **{st.session_state.username}** For The Mega Quiz ")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_question = 0  # Reset current question
        st.session_state.answers = [None] * len(st.session_state.flattened_questions)  # Reset answers
        st.session_state.username = ""
        st.session_state.quiz_submitted = False  # Reset quiz submission status
        st.session_state.flattened_questions = []  # Reset questions
        st.success("You have been logged out.")
        # st.experimental_rerun()  # Refresh the page to reflect the new state

    # Quiz Page
    st.header(f"Welcome {st.session_state.username} For The Mega Quiz")
    
    # Navigation buttons
    col1, col2 = st.columns(2)

    # Only show navigation buttons if the quiz hasn't been submitted
    if not st.session_state.quiz_submitted:
        if st.session_state.current_question > 0:
            with col1:
                if st.button("Previous", key="prev"):
                    st.session_state.current_question -= 1

    if st.session_state.current_question < len(st.session_state.flattened_questions) - 1:  # Show "Next" button if not on the last question
        with col2:
            if st.button("Next", key="next"):
                st.session_state.current_question += 1

    if st.session_state.current_question == len(st.session_state.flattened_questions) - 1 and not st.session_state.quiz_submitted:
        if st.button("Submit", key="submit"):
            if not st.session_state.quiz_submitted:  # Only process if not already submitted
                total_score = 0
                questions_attempted = 0
                correct_answers = 0
                wrong_answers = 0
                result_details = []

                for idx, question_detail in enumerate(st.session_state.flattened_questions):
                    user_answer = st.session_state.answers[idx]
                    if user_answer is not None:
                        questions_attempted += 1
                        
                        if question_detail["type"] == "true_false":
                            
                            score = 2
                            if user_answer == question_detail["answer"]:
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))
                        elif question_detail["type"] == "single_choice":
                            score = 2
                            if sorted(user_answer) == sorted(question_detail["answer"]):
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))
                        elif question_detail["type"] == "multiple_choice":
                            score = 5
                            if user_answer == question_detail["answer"]:
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))

                end_time = datetime.now()
                time_taken = end_time - st.session_state.start_time
                
                save_results(st.session_state.username, questions_attempted, correct_answers, wrong_answers, total_score, str(time_taken), str(result_details))
                st.success("Quiz submitted successfully!")
                st.session_state.quiz_submitted = True

                total_marks = 200  # Total marks for the quiz
                percentage = (total_score / total_marks) * 100
                result_message = "<h1 style='color: green;'>Congratulations! You passed the Test!</h1>" if percentage >= 70 else "<h1 style='color: red;'>Sorry You Have Failed The Test!.</h1>"

                # Display results in a card
                st.markdown("<div class='card'><h3>Quiz Results</h3>", unsafe_allow_html=True)
                st.markdown(result_message, unsafe_allow_html=True)
                st.write(f"**Total Questions Attempted:** {questions_attempted}")
                st.write(f"**Correct Answers:** {correct_answers}")
                st.write(f"**Wrong Answers:** {wrong_answers}")
                st.write(f"**Total Score:** {total_score}")
                st.write(f"**Percentage:** {percentage:.2f}%")
                st.markdown("</div>", unsafe_allow_html=True)

    # CSS for enhanced design
    st.markdown("""<style>
        .card {
            background-color: #ffcccc; /* Light background */
            border: 1px solid #ddd; /* Subtle border */
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .question-card {
            background-color: #ffcccc; /* Light red color for questions */
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>""", unsafe_allow_html=True)

    # Display current question if quiz is not submitted
    if not st.session_state.quiz_submitted and st.session_state.current_question < len(st.session_state.flattened_questions):
        current_question = st.session_state.flattened_questions[st.session_state.current_question]
        total_questions = 70
        question_number = st.session_state.current_question + 1 
        progress_percentage = question_number / total_questions
        st.write(f"**Question {question_number} of {total_questions}**")  # Question count
        st.progress(progress_percentage)
        
        st.markdown(f"<div class='question-card'><h4>Question {question_number}: {current_question['question']}</h4></div>", unsafe_allow_html=True)

        # Display options based on question type
        if current_question["type"] == "multiple_choice":
            st.header('Multiple Choice Questions')
            st.session_state.answers[st.session_state.current_question] =  st.multiselect("Choose Multiple Choice option:", current_question["options"], key=f"mc_{st.session_state.current_question}")
        elif current_question["type"] == "true_false":
            st.header('True False')
         
            st.session_state.answers[st.session_state.current_question] =st.radio("Choose an  option:", ["True", "False"], key=f"tf_{st.session_state.current_question}")
        elif current_question["type"] == "single_choice":
            st.header('Single Choice Questions')
           
            st.session_state.answers[st.session_state.current_question] =st.radio("Choose Single Choice options:", current_question["options"], key=f"cc_{st.session_state.current_question}")

# Add a footer
st.markdown("<footer style='text-align: center; margin-top: 20px;'>© 2024 Huawei Training Portal. All Rights Reserved.</footer>", unsafe_allow_html=True)

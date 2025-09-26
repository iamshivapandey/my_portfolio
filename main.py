import streamlit.components.v1 as components
import streamlit as st
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime, timedelta
import requests, os, json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# ---- Page Config ----
st.set_page_config(page_title="Shiva Pandey | Portfolio", page_icon="💼", layout="centered")

uri = st.secrets["uri"]

@st.cache_resource
def init_connection():
    """Initializes and caches the MongoDB client connection."""
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB and cached the connection!")
        
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

client = init_connection()

if client:
    db = client['streamlit_portfolio']
    visitors_collection = db['visitors_info']

    print(f"Connected to database '{db.name}' and collection '{visitors_collection.name}'.")
else:
    print("Could not connect to the database. Please check your URI and network.")

def log_new_visitor(ip_address, visitor_document):
    """
    Inserts a new document for a first-time visitor.
    """

    visitor_document['ip_address'] = ip_address
    visitor_document['first_visit'] = datetime.now()
    visitor_document['last_visit'] = datetime.now()
    visitor_document['visit_count'] = 1


    try:
        result = visitors_collection.insert_one(visitor_document)
        print(f"New visitor logged with document ID: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Error inserting new visitor: {e}")
        return False

def update_existing_visitor(ip_address):
    """
    Finds and updates a document for a repeat visitor.
    Increments the visit count and updates the last_visit timestamp.
    """
    # The filter to find the specific document
    filter_query = {"ip_address": ip_address}

    # The update operation to increment the count and set the last_visit
    update_operation = {
        "$set": {"last_visit": datetime.now()},
        "$inc": {"visit_count": 1}
    }

    try:
        result = visitors_collection.update_one(filter_query, update_operation)
        if result.modified_count > 0:
            print(f"Updated record for visitor: {ip_address}")
            return True
        else:
            print(f"Visitor record for {ip_address} not found. No update performed.")
            return False
    except Exception as e:
        print(f"Error updating visitor record: {e}")
        return False

def find_visitor_by_ip(ip_address):
    """
    Retrieves a document for a specific IP address.
    """
    # The find_one() method returns the first document that matches the filter, or None.
    document = visitors_collection.find_one({"ip_address": ip_address})
    return document

def capture_visitor_info():
    """
    Logs visitor information to the MongoDB Atlas database.
    """
    try:
        # Get public IP
        ip = streamlit_js_eval(
            js_expressions="fetch('https://api.ipify.org?format=json').then(res => res.json()).then(data => data.ip)",
            key='get_ip', 
            want_output=True,
        )

        if ip is None:
            return {"message": "Waiting for IP address to be fetched..."}

        # Check if the visitor already exists in the database
        existing_visitor = find_visitor_by_ip(ip)

        if existing_visitor:
            last_visit_time = existing_visitor['last_visit']
            time_since_last_visit = datetime.now() - last_visit_time

            # Check if enough time has passed since the last visit (more than 4 hours)
            if time_since_last_visit > timedelta(hours=4):
                update_existing_visitor(ip)
                return {"message": "Updated existing visitor log.", "ip": ip}
            else:
                return {"message": "Skipping log update (already logged in the last 4 hours).", "ip": ip}

        else:
            # Get geolocation info for a new visitor
            geo_data = requests.get(f"https://ipapi.co/{ip}/json/").json()

            geo_keys = ['city','region','country','latitude','longitude']
            final_geo_data = dict((k, geo_data[k]) for k in geo_keys if k in geo_data)

            # Log the new visitor
            log_new_visitor(ip, final_geo_data)
            
            return {"message": "New visitor logged successfully.", "ip": ip}

    except Exception as e:
        return {"error": str(e)}

# ---- Load Image & Resume ----
profile_img = Image.open("shiva.jpg")  # Your profile image
resume_file = "Shiva_new_resume.pdf"       # Your resume PDF

# ---- Custom CSS ----
st.markdown("""
    <style>
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        60% {
            opacity: 1;
            transform: translateY(-10px);
        }
        80% {
            transform: translateY(5px);
        }
        100% {
            transform: translateY(0);
        }
    }

    @keyframes zoomInGlow {
    0% {
        opacity: 0;
        transform: scale(0.5);
        text-shadow: 0 0 5px rgba(106, 13, 173, 0.8);  /* Royal Purple Glow */
    }
    100% {
        opacity: 1;
        transform: scale(1);
        text-shadow: 0 0 10px rgba(106, 13, 173, 1);  /* Strong Royal Purple Glow */
    }
}

    @keyframes pulseGlow {
        0% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.6;
            transform: scale(1.1);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }

    body, .stApp {
        background-color: #0e1117;
        color: white;
    }
    .title-text {
        font-size: 2.5em;
        font-weight: bold;
        color: #6A0DAD;
        margin-bottom: -10px;
        animation: zoomInGlow 1.5s ease-out;
    }
    .subheader {
        font-size: 1.2em;
        color: #cccccc;
        margin-bottom: 15px;
    }
    .section-header {
        font-size: 1.5em;
        color: #F5B041;
        font-weight: bold;
        border-bottom: 1px solid #444;
        margin-top: 40px;
        margin-bottom: 10px;
        animation: bounceIn 2s ease-out;

    }
    </style>
""", unsafe_allow_html=True)

# ---- Header ----
col1, col2 = st.columns([1, 3])
with col1:
    st.image(profile_img, width=150)
with col2:
    st.markdown("<div class='title-text'>Shiva Pandey</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>Data Engineer | Big Data | Cloud | Python</div>", unsafe_allow_html=True)
    with open(resume_file, "rb") as pdf_file:
        st.download_button(label="📄 Download Resume", data=pdf_file, file_name="Shiva_Pandey_Resume.pdf", mime="application/pdf")
    st.markdown("📧 [pandey.shiva623@gmail.com](mailto:pandey.shiva623@gmail.com) &nbsp; | &nbsp; [LinkedIn](https://www.linkedin.com/in/shivaapandey/) &nbsp; | &nbsp; [GitHub](https://github.com/iamshivapandey) | &nbsp; [Certifications](#certifications-section)", unsafe_allow_html=True)

# ---- Profile Summary ----
st.markdown("<div class='section-header'>👨‍💻 Profile Summary</div>", unsafe_allow_html=True)
st.markdown("""
Data Engineer with 2+ years of experience in building and optimizing big data pipelines using **Python, PySpark, AWS, Databricks, Kafka, Delta Lake and Iceberg**. Skilled in databases, ETL processes, data lakehouse, data warehousing, migration, and SQL. Experienced in designing scalable, cloud-native solutions to process large volumes of structured and semi-structured data.
""")

# ---- Skills ----
st.markdown("<div class='section-header'>🧠 Skills</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **Languages:** Python, Java, SQL, C  
    - **Big Data & Cloud:** Databricks, PySpark, Kafka, Airflow, Glue, EMR, Lambda, ECS, Fargate  
    - **Databases:** MySQL, PostgreSQL, Snowflake, ClickHouse  
    """)
with col2:
    st.markdown("""
    - **Tools:** Git, Docker, Bitbucket, Linux  
    - **Visualization:** Power BI, Tableau  
    - **Concepts:** Delta Lake, Iceberg, Data Warehousing, Data Lakehouse, ETL, ELT, Migration  
    """)


# CSS for anchor offset
st.markdown("""
    <style>
    .anchor {
        display: block;
        position: relative;
        top: -200px; /* adjust offset */
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# 📜 Certifications Section (anchor + header together)
st.markdown(
    '<span id="certifications-section" class="anchor"></span><div class="section-header">📜 Certifications</div>',
    unsafe_allow_html=True
)

certifications = {
    "Databricks Certified Data Engineer Associate": "https://credentials.databricks.com/6d2895e7-8358-4f7f-846d-d5b758c471bb",
    "Databricks Lakehouse Fundamentals": "https://credentials.databricks.com/dbf32d2f-7e53-4ebe-b239-cf80ac7eb6f8",
    "NPTEL Cloud Computing": "https://archive.nptel.ac.in/noc/Ecertificate/?q=NPTEL21CS62S2358036903173368",
    "Databricks Certified Data Engineer Associate Preparation": "https://www.udemy.com/certificate/UC-5f85d300-97ae-49b0-b4bc-2a4e245cfdb1/",
    "HackerRank SQL Advanced": "https://www.hackerrank.com/certificates/5782df7ce739"
    }

with st.expander("Click to view"):
    for name, link in certifications.items():
        st.markdown(f"- [{name}]({link})")

# ---- Work History ----
st.markdown("<div class='section-header'>💼 Work History</div>", unsafe_allow_html=True)

st.markdown("""
    <style>
        .job-title {
            font-size: 20px;
            font-weight: bold;
            color: #00FFFF;    /* Cyan */
            font-family: 'Arial', sans-serif;
            margin-bottom: 0px;
        }
        .job-time {
            font-size: 14px;
            font-weight: 600;
            color: #DC143C;    /* Light Blue */
            font-family: 'Arial', sans-serif;
            font-style: italic;
            margin-top: -5px;
            margin-bottom: -2px;
            margin-left: 30px;
        }
    </style>

    <div class="job-title">🔧 Data Engineer | Velotio Technologies</div>
    <div class="job-time">Apr 2025 – Present</div>
""", unsafe_allow_html=True)




st.markdown("""
- Doing a POC on tools like **Risingwave** streaming database and **Spline**, **DataHub** for tracking Spark job lineage
- Migrating Data from SAS into **Databricks** Data Lakehouse (Delta Lake)
- Building streaming and batch pipelines for databricks tables by replacing SAS
""")

# st.markdown("##### 🔧 Data Engineer | Demandhelm (Neiron India)")
# st.markdown("<span style='color: white; font-size: 14px; margin-left: 30px;'>**Oct 2023 – Mar 2025**</span>", unsafe_allow_html=True)

st.markdown("""
    <div class="job-title">🔧 Data Engineer | Demandhelm (Neiron India)</div>
    <div class="job-time">Oct 2023 – Mar 2025</div>
""", unsafe_allow_html=True)

st.markdown("""
- Built scalable big data pipeline with AWS Glue, PySpark, Iceberg, and Snowflake  
- Migrated 350+ ETL jobs from Pandas to PySpark, improving efficiency by 80%  
- Led database migration to Apache Iceberg from MySQL/PostgreSQL  
- Deployed workloads using AWS ECS Fargate, reducing costs by 70%  
- Created marketing pipelines using AMC + Lambda for real-time analytics  
- Automated workflows with Airflow on EC2  
""")



# ---- Projects (Interactive) ----
st.markdown("<div class='section-header'>🛠️ Projects</div>", unsafe_allow_html=True)

with st.expander("♟️ Chess pieces detection and moves prediction"):
    st.write("""
    🔧 **Tech:** Pytorch, Python, OpenCV, Stockfish  
    - A self-trained ResNet18 model detects chess pieces and their positions from the board
    - The board state is converted into a FEN (Forsyth–Edwards Notation) string
    - The FEN is passed to the Stockfish engine, which suggests the best move
    """)
    st.markdown("[🔗 GitHub Repo](https://github.com/iamshivapandey/chess_player)")

with st.expander("🌤️ Real-Time Weather Data Pipeline"):
    st.write("""
    🔧 **Tech:** Kafka, PySpark, APIs, MySQL, S3, Linux  
    - Developed a weather data pipeline that fetches live data via RapidAPI  
    - Streamed data to Kafka, processed with PySpark for cleaning & validation  
    - Loaded clean data into MySQL for analytics dashboards  
    - Deployed to S3 with versioned archives for traceability  
    """)
    st.markdown("[🔗 GitHub Repo](https://github.com/iamshivapandey/live-weather-data-streaming-pipeline)")

with st.expander("🫁 Pneumonia Detection Web App"):
    st.write("""
    🔧 **Tech:** Streamlit, TensorFlow, AWS EC2  
    - Trained a convolutional neural network to classify X-ray images  
    - Built a clean Streamlit frontend for real-time diagnosis  
    - Deployed on AWS EC2 with live demo and user input support  
    """)
    st.markdown("[🔗 GitHub Repo](https://github.com/iamshivapandey/Pneumonia-detection-in-chest-X-ray-images)")

with st.expander("🐳 Dockerized Spark Setup"):
    st.write("""
    🔧 **Tech:** Docker, Spark, Python, Jupyter  
    - Created a fully containerized Spark environment for local dev  
    - Integrated Python, Spark and Jupyter Notebook inside Docker  
    - Image published to Docker Hub for easy reuse across teams  
    """)
    st.markdown("[🔗 GitHub Repo](https://github.com/iamshivapandey/pyspark_using_docker)")

with st.expander("📈 Crypto Twitter Bot"):
    st.write("""
    🔧 **Tech:** Selenium, Pillow, Twitter API, GitHub Actions  
    - Scraped real-time crypto data and posted daily updates on Twitter  
    - Auto-generated visual summaries using Pillow  
    - Scheduled using GitHub Actions & Cron without needing servers  
    """)
    st.markdown("[🔗 GitHub Repo](https://github.com/iamshivapandey/twitter_bot)")


# ---- Contact Form ----
st.markdown("<div class='section-header'>📫 Contact Me</div>", unsafe_allow_html=True)

# Get the email token from Streamlit secrets
email_token = st.secrets["email_token"]

# Now we embed the form using the email_token variable
components.html(f"""
<style>
  .form-container {{
    width: 100%;
    max-width: 600px;
    font-family: 'Segoe UI', sans-serif;
    color: white;
    background-color: #0e1117;
    padding: 20px 0;
    margin-left: -5px;
  }}

  .form-container input,
  .form-container textarea {{
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    margin-bottom: 16px;
    border: 1px solid #444;
    background-color: #1c1e23;
    color: white;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.2s ease;
  }}

  .form-container input:focus,
  .form-container textarea:focus {{
    border-color: #4f8bf9;
    outline: none;
  }}

  .form-container button {{
    background-color: #4f8bf9;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }}

  .form-container button:hover {{
    background-color: #397de5;
  }}
</style>

<div class="form-container">
  <form action="{email_token}" method="POST" id="contact-form"
    onsubmit="setTimeout(() => document.getElementById('contact-form').reset(), 100);">
    
    <label for="Name">Your Name</label>
    <input type="text" name="name" placeholder="Enter your name" required>

    <label for="Email">Your Email</label>
    <input type="email" name="email" placeholder="Enter your email" required>

    <label for="Message">Your Message</label>
    <textarea name="message" rows="6" placeholder="Type your message here..." required></textarea>

    <button type="submit">Send Message</button>
  </form>
</div>
""", height=600)


# ---- Footer ----
st.markdown("---")
st.markdown("*Last updated September 2025*")


print(capture_visitor_info())
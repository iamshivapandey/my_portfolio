import streamlit.components.v1 as components
import streamlit as st
from PIL import Image

# ---- Page Config ----
st.set_page_config(page_title="Shiva Pandey | Portfolio", page_icon="💼", layout="centered")

# ---- Load Image & Resume ----
profile_img = Image.open("shiva.jpg")  # Your profile image
resume_file = "Shiva_Resume.pdf"       # Your resume PDF

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
    st.markdown("📧 [pandey.shiva623@gmail.com](mailto:pandey.shiva623@gmail.com) &nbsp; | &nbsp; [LinkedIn](https://www.linkedin.com/in/shivaapandey/) &nbsp; | &nbsp; [GitHub](https://github.com/iamshivapandey)", unsafe_allow_html=True)

# ---- Profile Summary ----
st.markdown("<div class='section-header'>👨‍💻 Profile Summary</div>", unsafe_allow_html=True)
st.markdown("""
Data Engineer with almost 2 years of experience in building and optimizing big data pipelines using **Python, PySpark, AWS, Databricks, Kafka, and Iceberg**.  
Skilled in databases, ETL processes, data lakes, data warehousing, migration, and SQL.  
Experienced in designing scalable, cloud-native solutions to process large volumes of structured and semi-structured data.
""")

# ---- Skills ----
st.markdown("<div class='section-header'>🧠 Skills</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **Languages:** Python, Java, SQL, C  
    - **Big Data & Cloud:** PySpark, Kafka, Airflow, Glue, EMR, Lambda, ECS, Fargate  
    - **Databases:** MySQL, PostgreSQL, Snowflake, ClickHouse  
    """)
with col2:
    st.markdown("""
    - **Tools:** Git, Docker, Bitbucket, Linux  
    - **Visualization:** Power BI, Tableau  
    - **Concepts:** Data Lakes, Iceberg, Data Warehousing, ETL, ELT, Migration  
    """)

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
- Doing a POC on tools like **Spline**, **DataHub** for tracking Spark job lineage
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
st.markdown("*Last updated April 2025*")

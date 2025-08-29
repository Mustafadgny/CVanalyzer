# CV Analyzer

This project is a web application designed to help users analyze and get feedback on their resumes (CVs) using a set of powerful tools. Built with Python and HTML, it provides a seamless experience for uploading, analyzing, and discussing CVs with an AI assistant.

# CV Analyzer Interface

<img width="1127" height="865" alt="Ekran görüntüsü 2025-08-29 125551" src="https://github.com/user-attachments/assets/e5daf277-345a-4df6-aeba-567a0a425272" />
<img width="1897" height="867" alt="Ekran görüntüsü 2025-08-29 125637" src="https://github.com/user-attachments/assets/cd0d5746-427a-49d1-9333-eda1804a2ca6" />
<img width="1907" height="584" alt="Ekran görüntüsü 2025-08-29 125744" src="https://github.com/user-attachments/assets/e5db2fda-9673-44cb-a000-0114ff995a23" />

---

### **Key Features**

The application is structured into three main sections, each serving a distinct purpose:

1.  **CV Uploader:** This is the entry point of the application. It provides a simple and clean interface for users to upload their CVs in PDF format.
    * **Functionality:** Users can select and upload a PDF file directly from their local machine.

2.  **CV List & Analysis:** After uploading, the CVs are listed for detailed analysis. This section offers an in-depth look into the content of each CV.
    * **Functionality:** Users can view a list of all uploaded CVs. By selecting a CV, a detailed analysis is displayed, including key insights and a comprehensive breakdown of the document's content.

3.  **AI Chatbot:** This feature allows for an interactive conversation about the uploaded CVs. The AI assistant provides personalized feedback and suggestions.
    * **Functionality:** Users can engage with a chatbot to ask specific questions about their CV, get suggestions for improvement, or discuss their career goals and how to better highlight them on their resume.

---

### **Project Structure & Technologies**

This project was developed using the following core technologies:

* **Python:** The backend logic for file uploads, data processing, analysis, and the AI chatbot is handled by Python.
* **HTML:** The user interface, including the three main pages, is built using HTML to ensure a clean and responsive design.

### **How to Run the Project Locally**

To run this application on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Mustafadgny/CVanalyzer.git](https://github.com/Mustafadgny/CVanalyzer.git)
    cd CVanalyzer
    ```
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    * Make sure you have a `requirements.txt` file listing all necessary Python libraries (e.g., Django/Flask, pdf-parser, AI libraries, etc.).
    * Run the following command to install them:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Application:**
    * Use the appropriate command for your framework (e.g., `python manage.py runserver` for Django or a similar command for Flask).

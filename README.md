# AI Lost & Found Management System

## Overview

AI Lost & Found Management System is a web-based application developed using Flask and SQLite to simplify the process of reporting and locating lost items. Users can report lost or found belongings, upload images, and search for items through a simple interface.

The application also includes an AI-based matching feature that compares the descriptions of lost and found items using Natural Language Processing (TF-IDF Vectorization and Cosine Similarity) to identify potential matches.

---

## Features

- Report Lost Items
- Report Found Items
- Upload Item Images
- Search Lost and Found Records
- AI-Based Description Matching
- Responsive User Interface
- Admin Dashboard
- SQLite Database Integration

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Bootstrap 5
- JavaScript
- Scikit-learn (TF-IDF & Cosine Similarity)

---

## AI Matching

The application uses TF-IDF Vectorization and Cosine Similarity to compare the descriptions of lost and found items. When a similarity score exceeds the predefined threshold, the system identifies it as a potential match and displays the confidence percentage.

---

## Project Structure

```
LostFoundProject/
│
├── app.py
├── requirements.txt
├── database.db
├── static/
│   ├── style.css
│   ├── script.js
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── lost.html
│   ├── found.html
│   ├── search.html
│   └── admin.html
│
└── README.md
```

---

## How to Run

1. Clone the repository.

```
git clone <repository-url>
```

2. Navigate to the project folder.

```
cd LostFoundProject
```

3. Create a virtual environment.

```
python3 -m venv venv
```

4. Activate the virtual environment.

```
source venv/bin/activate
```

5. Install dependencies.

```
pip install -r requirements.txt
```

6. Run the application.

```
python app.py
```

7. Open the browser.

```
http://127.0.0.1:5000
```

---

## Future Enhancements

- OCR-based image recognition
- Email notifications
- User authentication
- Cloud database integration
- Mobile application support

---

## Author

Sreya Sudevan

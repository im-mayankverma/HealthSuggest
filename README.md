# HealthSuggest – Symptom-Based Health Suggestion System

HealthSuggest is a **Django-based web application** that gives **basic health suggestions** based on user-selected symptoms, duration, and self-rated severity.

It uses a **rule-based scoring system** on top of a structured dataset of symptoms and conditions stored inside the project (via Django fixtures), so it can run easily on any machine after cloning.

> **Important:** This is an educational project.  
> It is **not** a medical diagnosis tool and must **not** be used for real medical decisions.

---

## Features

- Searchable list of symptoms grouped by body part (e.g., head, chest, stomach, skin, mind, etc.)
- Select **multiple symptoms** via checkboxes
- Input for:
  - Duration of symptoms (in days)
  - User’s perceived severity (Mild / Moderate / Severe)
- Suggestion engine:
  - Calculates a **score** for each condition based on symptom weights
  - Shows **best-matched condition**
  - Lists **other possible conditions** with match percentages
  - Displays **severity**, **advice**, **home_remedies**, and **when_to_see_doctor**
- Clean and responsive UI:
  - Selected symptoms shown as “chips”
  - Colored cards/labels for severity and risk
  - **Print / Save** button on results page
- Initial data stored as a **fixture** (`initial_data.json`) so all symptoms and conditions travel with the project in Git.

---

## Technology Stack

- **Language:** Python 3.x  
- **Framework:** Django (MVT architecture)  
- **Database (Recommended):** SQLite (default Django DB)  
- **Frontend:** HTML, CSS, vanilla JavaScript, Django templates  
- **Version Control:** Git & GitHub (`im-mayankverma/HealthSuggest`)  
- **Environment:** Python virtual environment (`venv`)

---

## Project Structure (simplified)

```text
manage.py
healthsuggest/              # Django project settings & URLs
    __init__.py             # (optional) project init
    settings.py             # DATABASES, INSTALLED_APPS, templates, etc.
    urls.py
    asgi.py / wsgi.py

symptoms/                   # Main app
    models.py               # Symptom, Condition, ConditionSymptom
    views.py                # home, get_suggestions logic
    urls.py                 # app-level URLs (if used)
    templates/
        symptoms/
            base.html       # Common layout
            home.html       # Symptom selection form
            results.html    # Suggestions and risk view
    fixtures/
        initial_data.json   # Initial symptoms & conditions data

static/
    css/
        style.css           # Main CSS styling
docs/
    home-page.png           # Screenshot: home page
    results-page.png        # Screenshot: result page
README.md
requirements.txt
```

---

## Screenshots

### Home page – Select symptoms

![Home page](docs/home-page.png)

### Results page – Suggestions and risk level

![Results page](docs/results-page.png)

---

## How the Suggestion Logic Works

1. User selects symptoms, duration, and perceived severity.
2. For each condition:
   - The app finds all matching `ConditionSymptom` records for the selected symptoms.
   - It sums the **weight** values to get a score.
3. The condition with the **highest score** is the **best match**.
4. Other conditions with non-zero scores are listed as **“other possible conditions”**.
5. A simple **risk level** (Low / Medium / High) can be derived from:
   - Match score
   - Stored severity of the condition (mild / moderate / severe)
   - User’s reported severity

This is a **transparent, rule-based** system (no black-box machine learning).

---

## Setup Instructions (Windows / any new PC)

### 1. Clone the repository

```bash
git clone https://github.com/im-mayankverma/HealthSuggest.git
cd HealthSuggest
```

### 2. Create and activate a virtual environment

On Windows (Command Prompt / PowerShell):

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If you are only using SQLite (recommended for local/dev), there is **no need** to install MySQL drivers.

### 4. Configure database (SQLite recommended)

In `healthsuggest/settings.py`, ensure your `DATABASES` section looks like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

SQLite is file-based and works out of the box; no extra server install needed.

### 5. Apply migrations

```bash
python manage.py migrate
```

This creates the required tables in `db.sqlite3`.

### 6. Load initial data (symptoms + conditions)

The project includes a fixture file `symptoms/fixtures/initial_data.json`
containing multiple symptoms, conditions, and weighted links between them.

Load it with:

```bash
python manage.py loaddata initial_data
```

You should see something like:

```text
Installed XX object(s) from 1 fixture(s)
```

(XX is the number of objects in the fixture.)

### 7. Run the development server

```bash
python manage.py runserver
```

Open your browser and go to:

- http://127.0.0.1:8000/

You should now see:

- Home page with a list of symptoms.
- Ability to select symptoms and see suggested conditions.

---

## Development Notes

- **Fixtures:**  
  - All starter data lives in `symptoms/fixtures/initial_data.json`.  
  - If you change/add symptoms or conditions in the admin or shell and want to update the fixture:

    ```bash
    python manage.py dumpdata symptoms.Symptom symptoms.Condition symptoms.ConditionSymptom --indent 2 > symptoms/fixtures/initial_data.json
    ```

    Commit and push this file so new machines get the updated dataset.

- **Models:**
  - `Symptom` — basic symptom info.
  - `Condition` — name, description, severity, advice, home_remedies, when_to_see_doctor.
  - `ConditionSymptom` — many-to-many bridge with a `weight` field.

- **Views & Templates:**
  - `home` view + `home.html` — form to collect user input.
  - `get_suggestions` view + `results.html` — calculation and results display.

---

## Limitations

- Rule-based with a manually defined dataset; not a real clinical decision system.
- No real-time medical database or AI/ML integration.
- Not validated by healthcare professionals.
- Not meant for emergency use or serious medical decisions.

---

## Future Enhancements (Ideas)

- Add many more conditions and refine symptom weights.
- User accounts and history of previous suggestions.
- Export results as PDF.
- More detailed risk scoring and visualization.
- Optional integration with an authenticated medical API (for educational exploration only).

---

## Disclaimer

This project is for **learning and demonstration purposes** only.

- It does **not** provide medical diagnosis.
- It does **not** replace a doctor or emergency services.
- Always consult a qualified healthcare professional for any health concerns, especially in emergencies.

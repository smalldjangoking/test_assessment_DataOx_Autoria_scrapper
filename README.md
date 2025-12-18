# 🚗 AutoRia Scraper & Scheduler

Data collection system for the AutoRia platform.
This project includes PostgreSQL integration, Playwright-based web scraping, Pydantic for data validation and normalization, automated daily database backups, and containerized scheduling.

---

### ⚠️ Important Notes (Read First!)

* **Ukrainian IP**: To ensure stable operation and avoid access restrictions, it is highly recommended to use a clean **Ukrainian IP address**.
* **Scheduling**: Cron task intervals are managed in the `compose.yaml` file. You can easily switch to a test frequency (every 15 minutes) by following the comments in the `labels` section of the scheduler service.
* **Local Execution**: If you intend to run the script outside of Docker, ensure you have the `postgresql-client` package installed on your system so the `make_db_dump()` function can access `pg_dump`. Otherwise, simply comment out the dump function call in `main.py`.

---

### 🛠 Installation & Setup

Follow these steps to get the project up and running:

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/smalldjangoking/test_assessment_DataOx_Autoria_scrapper.git](https://github.com/smalldjangoking/test_assessment_DataOx_Autoria_scrapper.git)
    cd test_assessment_DataOx_Autoria_scrapper
    ```

2.  **Environment Configuration**: Create a `.env` file in the root directory and fill in your credentials:
    ```env
    DB_USER=your_user
    DB_PASSWORD=your_password
    DB_NAME=autoria
    DB_HOST=auto_ria_db
    DB_PORT=5432
    ```

3.  **Launch via Docker**: Execute the following command in your terminal:
    ```bash
    docker compose up -d --build
    ```

---

### ⚙️ How It Works
** Scraps the first page of cars to collect URLs.
** Scraps each URL and extracts the following fields:
- url (string)
- title
- price_usd
- odometer
- username (string)
- phone_number
- image_url
- images_count
- car_number
- car_vin
- 
** After scraping, all fields are validated and normalized using **Pydantic**
** If the data matches the requirements, it is added to the database  
   If the record already exists, it is skipped

* **Initial Run**  
  Immediately after the containers start, the `app` service performs an initial "test" scraping run to populate the database and verify dump functionality

* **Automated Scheduling**  
  After the initial run, the **Ofelia** scheduler takes over and triggers the scraper daily at exactly **12:00 PM**

* **Data Persistence**
  * Collected data is stored in a **PostgreSQL** database
  * Database backup files (`.sql`) are automatically generated and saved to the `./dumps` directory

---

### 📂 Project Structure

* `/app` – Main scraper logic powered by playwright.
* `/database` – SQLAlchemy models and database connection setup.
* `/dumps` – Storage directory for automated database backups.
* `compose.yaml` – Orchestration for the App, Database, and Scheduler services.
* `Dockerfile` – Environment setup for the Python application.

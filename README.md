# Supply Chain Dashboard

A Data Analyst project visualizing supply chain metrics using Streamlit, Python, and MySQL.

Deployed webpage version can be accessed from here https://supply-chain-data-dashboarding-with-mysql-cloud-backend.streamlit.app/

## Features
- **KPIs**: Total Revenue, Average Lead Time, Total Products Sold.
- **Visualizations**:
    - Revenue & Lead Time by Transportation Mode.
    - Revenue by Product Type & Demographics.
    - Location Analysis.
- **Data Export**: Download raw data as CSV.
- **Database Integration**: Connects to a local MySQL database.

## Setup

1.  **Prerequisites**:
    -   Python 3.8+
    -   MySQL Server
    -   Database `startersql` with `supply_chain` table.

2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Configuration**:
    -   Update `db_utils.py` with your MySQL credentials if they differ from the default:
        -   User: `root`
        -   Password: `admin1234`
        -   Database: `startersql`

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## Project Structure
- `app.py`: Main application file.
- `db_utils.py`: Database connection and data fetching logic.
- `requirements.txt`: Python dependencies.

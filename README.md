# Gmail Activity Analytics Dashboard

This project fetches emails from a Gmail account, processes them using **DLT**, stores them in **BigQuery**, and visualizes the data using **Apache Superset**


## Features

- Fetch emails from Gmail using Python (`gmail_source.py`)
- Extract and clean metadata (From, To, Subject, Date, Labels, etc.)
- Parse date into structured fields (day, hour, weekday) for analytics
- Exclude unwanted emails (e.g., emails containing "***")
- Store data in **BigQuery** via a DLT pipeline
- Visualize emails in **Superset** with:
  - Pie chart: Emails by Sender
  - Table: All Gmail messages
  - Heat map: Email activity by day and hour, AND much more
- Apply filters for Sender and Labels in Superset dashboards


## Data Details

- In `gmail_source.py`, we wrote code to fetch **up to 100 emails** from Gmail
- In the DLT pipeline, emails were added to **BigQuery**
- Out of the fetched emails, only **60 were initially added**, and **5 were excluded** due to sender filtering (e.g., containing "***")
- The **final 55 emails** were used in the **Gmail Activity Analytics Dashboard** to render and display charts and tables


## Project Structure


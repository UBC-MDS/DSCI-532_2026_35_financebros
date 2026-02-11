# Proposal Examples

These examples are provided to help you understand the expected depth and style of your proposal. You do not need to follow them exactly, but your sections should cover similar ground. Use the lecture materials to better motivate your proposal.

## Section 1: Motivation and Purpose

> **Our role:** Data scientist consultancy firm
> **Target audience:** Health care administrators
>
> Missed medical appointments cost the healthcare system a lot of money and affects the quality of care. If we could understand which factors lead to missed appointments it may be possible to reduce their frequency and use the saved resources to improve patient outcomes. To address this challenge, we propose building a data visualization app that allows health care administrators to visually explore a dataset of missed appointments to identify common factors. Our app will show the distribution of factors contributing to appointment show/no show and allow users to explore different aspects of this data by filtering and re-ordering on different variables in order to compare factors that contribute to absence.

## Section 2: Description of the Data

> We will be visualizing a dataset of approximately 300,000 missed patient appointments. Each appointment has 15 associated variables that describe the following characteristics, which we hypothesize could be helpful in determining why patient's miss their appointments:
>
> - Patient demographics (`patient_id`, `gender`, `age`, etc)
> - The health status of the patient (`general_health_status`, `existing_conditions` e.g. "Hypertension", "Physical disability")
> - Information about the appointment itself (`appointment_id`, `appointment_date`)
>
> Using this data we will also derive new variables, such as the time since the patient's last appointment (`days_since_last_appointment`) and which weekday the appointment was on (`appointment_weekday`), as it would be interesting to explore if these could be linked to the patient missing their appointment.

## Section 3: Research Questions & Usage Scenarios

### Usage Scenario
> Mary is a policy maker with the Canadian Ministry of Health and she wants to understand what factors lead to missed appointments in order to devise an intervention that improves attendance numbers. She wants to be able to [explore] a dataset in order to [compare] the effect of different variables on absenteeism and [identify] the most relevant variables around which to frame her intervention policy.
>
> When Mary logs on to our "Missed Appointments app", she will see an overview of all the available variables in her dataset, according to the number of people that did or did not show up to their medical appointment. She can filter out variables for head-to-head comparisons, and explore which variables are most important in determining whether a patient will show up to their appointment. When she does so, Mary may e.g. notice that "physical disability" appears to be a strong predictor missing appointments, and in fact patients with a physical disability also have the largest number of missed appointments.
>
> Based on her findings from using our app, Mary hypothesizes that patients with a physical disability could be having a hard time finding transportation to their appointments, and decides she needs to conduct a follow-on study since transportation information is not captured in her current dataset.

### User Stories
*You can choose to frame your detailed requirements as User Stories...*

> **User Story 1:**
> As a **policy maker**, I want to **filter appointments by specific demographics (e.g., age, gender)** in order to **determine if specific population groups are disproportionately missing appointments**.
>
> **User Story 2:**
> As a **policy maker**, I want to **compare no-show rates between patients with and without specific conditions (e.g., hypertension)** in order to **identify if medical conditions are high-risk factors**.
>
> **User Story 3:**
> As a **policy maker**, I want to **visualize no-shows across days of the week** in order to **decide if specific days need scheduling interventions**.

### Jobs to Be Done
*...or as Jobs to Be Done:*

> **JTBD 1:**
> **Situation:** When I am reviewing monthly attendance reports...
> **Motivation:** ...I want to separate routine absences from systemic issues...
> **Outcome:** ...so I can allocate intervention budget to the right patient groups.
>
> **JTBD 2:**
> **Situation:** When investigating a spike in no-shows...
> **Motivation:** ...I want to see if specific physical disabilities correlate with absenteeism...
> **Outcome:** ...so I can propose targeted transportation support services.
>
> **JTBD 3:**
> **Situation:** When planning clinic hours...
> **Motivation:** ...I want to see if appointments on Mondays or Fridays are missed more often...
> **Outcome:** ...so I can optimize the scheduling grid.

## Section 4: Exploratory Data Analysis

> *To address User Story 1 (Demographics), we analyzed the no-show rate across different age groups.*
>
> **Analysis:** The bar chart in `notebooks/eda_analysis.ipynb` reveals that patients in the 20-30 age bracket have a 15% higher no-show rate than the average.
>
> **Reflection:** This finding supports the need for a targeted filter in the dashboard. By allowing the policy maker to isolate "Young Adults," they can investigate if this high trend holds true across different clinic locations, helping them decide if age-specific text message reminders are needed.

## Section 5: App Sketch & Description

![Dashboard](sketch.png "App Sketch")

> The app contains a landing page that shows the distribution (depending on data type, bar chart, density chart etc) of dataset factors (hypertension, physical disabilities etc.) colored coded according to whether patients showed up or didn't show up for an appointment. From a dropdown list, users can filter out variables from the distribution display, by patient demographics (i.e. only show female patients), by appointment data (i.e. if SMS was sent), and finally by the date range of appointments. A different dropdown menu will allow users to re-order variables according to the probability of patients being a no-show or in alphabetical order to co-morbidities. Users can compare the distribution of co-morbidities by scrolling down through the app interface.
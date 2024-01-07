# Grade-Calc

## Introduction
This tool allows you to upload CSVs directly from blackboard and calculate all student's grades

## Prerequisites
Before you begin, ensure you have met the following requirements:
- **Python**: This project is built using Python. If you do not have Python installed, download and install it from [python.org](https://www.python.org/downloads/).
- **Pipenv**: This project uses Pipenv for managing dependencies. Make sure you have Pipenv installed. If not, you can install it using pip:
  ```bash
  pip install pipenv
  ```

## Installation and Setup
1. **Enter Project**:
   ```bash
   cd grade-calc 
   ```

2. **Install Dependencies**:
   ```bash
   pipenv install
   ```

3. **Activate the Pipenv Shell**:
   ```bash
   pipenv shell
   ```

## Usage Instructions
1. **Prepare Your CSV File**:
   - The CSV file should be a comma-delimited file exported from Blackboard.
   - Place your CSV file in the `load_files` folder.

2. **Run the Application**:
   ```bash
   python [your_script_name].py
   ```
   - The program will process the CSV file and categorize assignments based on your configuration.

3. **Configure Grading Categories**:
   - Create categories for your grading configuration. Each category represents a part of the weighted grade.
   - For instance, you can create a category named `Exams` and assign it a weight, e.g., 0.45 (45%).

4. **Add Tags to Categories**:
   - Tags help the application classify each assignment in the CSV file.
   - Assign tags to each category based on how you want to categorize the assignments from Blackboard.

5. **Handling Category Matches**:
   - If an assignment matches multiple categories, or fits no category, you will be prompted to address these cases.

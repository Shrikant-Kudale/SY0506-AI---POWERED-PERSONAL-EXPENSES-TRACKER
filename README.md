AI-Powered Expense Tracker with GUI
This is a user-friendly desktop application for managing personal expenses. Built using Python, Tkinter, SQLite3, and RandomForestRegressor, this app allows users to record, visualize, and predict their spending behavior.

The application provides a graphical interface to add, edit, and delete expense records across categories such as Food, Bills, Transport, Entertainment, and others. It includes category-wise bar charts to visualize spending trends, and uses a trained Random Forest model to forecast future expenses based on past data.

The app uses an SQLite database to store data locally and offers simple sentence-based summaries for added insights. It also includes category-based analysis and alerts to help users stay within their budget.

To run the project, ensure you have Python installed and run the following command to install the required libraries:
pip install tkcalendar pandas matplotlib scikit-learn

Then launch the application using:
python main.py

This will start the GUI and allow expense management through the visual interface.


The project structure includes:

main.py: The main script containing the GUI and core logic

Expense Tracker.db: The local SQLite database (auto-generated when you run the app)

README.md: This project documentation file

The machine learning component uses Random Forest Regressor from scikit-learn to estimate monthly expenses based on user data. The model compares predictions with average past values and last month's totals to offer personalized insights.

Technologies used include Tkinter for the GUI, SQLite3 for the backend database, scikit-learn for the AI model, and Matplotlib for data visualization.

This project was developed as part of an academic submission under the guidance of Prof. Jayashree Prasad.


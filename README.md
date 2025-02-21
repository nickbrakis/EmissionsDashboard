# Streamlit Dashboard App

This project is a Streamlit application that allows users to select files and plots to display in a dashboard format. The application is designed to provide an interactive experience for visualizing data.

## Project Structure

```
streamlit-dashboard-app
├── src
│   ├── app.py                # Main entry point of the Streamlit application
│   ├── components            # Directory for reusable components
│   │   └── __init__.py       # Initialization file for components
│   ├── data                  # Directory for data files
│   │   └── sample_data.csv    # Sample data used for plotting
│   └── utils                 # Directory for utility functions
│       └── __init__.py       # Initialization file for utilities
├── requirements.txt          # File listing project dependencies
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/streamlit-dashboard-app.git
   cd streamlit-dashboard-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit application, execute the following command in your terminal:
```
streamlit run src/app.py
```

Once the application is running, you can interact with the dashboard by selecting different files and plots to visualize the data.

## Docker Instructions

To run the application using Docker, follow these steps:

1. Build the Docker image:
```
docker build -t streamlit-dashboard-app .

```
2. Run the Docker container:
```
docker run -p 8501:8501 streamlit-dashboard-app

```
This will start the Streamlit application inside a Docker container, and you can access it by navigating to `http://localhost:8501` in your web browser.

## Deployment

The application is deployed and can be accessed at the following URL:
[https://emissionsdashboard.streamlit.app/](https://emissionsdashboard.streamlit.app/)


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
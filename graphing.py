import pandas as pd  # Analyze data
import matplotlib.pyplot as plt  # Plot stuff
import glob  # For finding CSV files

def load_data():
    files = glob.glob('borderData.csv')
    data_frames = []
    
    # Finds the data from the CSV and puts it into a list, then concatenates
    for file in files:
        df = pd.read_csv(file)
        data_frames.append(df)

    # Concatenate all data into a single DataFrame
    all_data = pd.concat(data_frames, ignore_index=True)
    return all_data

def preprocess_data(data):

    # Replace 'Midnight' and 'Noon' with '12:00 AM' and '12:00 PM'
    data['Time'] = data['Time'].replace({'Midnight': '12:00 AM', 'Noon': '12:00 PM'})
    
    # Convert 'Time' to datetime
    data['Time'] = pd.to_datetime(data['Time'], format='%I:%M %p', errors='coerce')

    return data    # Return the processed data

def filter_data_by_day(data, day):
    # Filter data for a specific day
    return data[data['Date'] == day]

def filter_data_by_week(data, start_date, end_date):
    # Filter data for a specific week
    mask = (data['Date'] >= start_date) & (data['Date'] <= end_date)
    return data[mask]

def analyze_best_worst_times(data):
  
    data['Hour'] = data['Time'].dt.hour
    best_time = data.groupby('Hour')['Average (min)'].mean().idxmin()
    worst_time = data.groupby('Hour')['Average (min)'].mean().idxmax()

    return best_time, worst_time

def analyze_best_day(data):
    # Calculate average wait time by day of the week
    data['Day'] = pd.to_datetime(data['Date']).dt.day_name()
    best_day = data.groupby('Day')['Average (min)'].mean().idxmin()
    worst_day = data.groupby('Day')['Average (min)'].mean().idxmax()

    return best_day, worst_day

def plot_trends(data):
    # Group by date to visualize trends
    daily_average = data.groupby('Date')['Average (min)'].mean()
    plt.figure(figsize=(12, 6))
    plt.plot(daily_average.index, daily_average, marker='o', label='Daily Average Wait Time', color='orange')
    plt.title('Daily Average Wait Time Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Wait Time (min)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_data(data):
    # Combine 'Date' and 'Time' into a new DateTime column
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'].dt.strftime('%I:%M %p'), 
                                       format='%Y-%m-%d %I:%M %p', errors='coerce')    

    # Set the new DateTime as the index
    data.set_index('DateTime', inplace=True)

    # Clean and prepare the data
    data['Today (min)'] = pd.to_numeric(data['Today (min)'], errors='coerce')
    data['Average (min)'] = pd.to_numeric(data['Average (min)'], errors='coerce')

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Bar plot for 'Average (min)'
    plt.bar(data.index, data['Average (min)'], width=0.02, label='Average (min)', color='green', alpha=0.7)

    # Line plot for 'Today (min)'
    plt.plot(data.index, data['Today (min)'], marker='o', label='Today (min)', color='blue')

    # Adding titles and labels
    plt.title('Average Wait Time and Today (min) Over Time')
    plt.xlabel('Time')
    plt.ylabel('Minutes')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    data = load_data()
    data = preprocess_data(data)

    # Example: Select a specific day or week to check
    user_choice = input("Would you like to filter by day or week? (day/week): ").strip().lower()

    if user_choice == 'day':
        day = input("Enter the date (YYYY-MM-DD) you want to analyze: ")
        filtered_data = filter_data_by_day(data, day)
        plot_data(filtered_data)

        best_time, worst_time = analyze_best_worst_times(filtered_data)
        print(f"Best time to go: {best_time}:00")
        print(f"Worst time to go: {worst_time}:00")

    elif user_choice == 'week':
        start_date = input("Enter the start date of the week (YYYY-MM-DD): ")
        end_date = input("Enter the end date of the week (YYYY-MM-DD): ")
        filtered_data = filter_data_by_week(data, start_date, end_date)
        plot_data(filtered_data)

        # Analyze best and worst times
        best_time, worst_time = analyze_best_worst_times(filtered_data)
        print(f"Best time to go: {best_time}:00")
        print(f"Worst time to go: {worst_time}:00")

        # Analyze best and worst days
        best_day, worst_day = analyze_best_day(filtered_data)
        print(f"Best day to go: {best_day}")
        print(f"Worst day to go: {worst_day}")

        # Plot trends over time
        plot_trends(filtered_data)

    else:
        print("Invalid choice. Please enter 'day' or 'week'.")

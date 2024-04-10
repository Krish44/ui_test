import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# Function to read CSV data
def read_csv_data():
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_csv(file_path, parse_dates=[0], infer_datetime_format=True)
        return df
    else:
        return None

# Function to update the graphs
def update_graphs(window, canvas, axs, file_path):
    df = pd.read_csv(file_path, parse_dates=[0], infer_datetime_format=True)
    for i, ax in enumerate(axs):
        ax.clear()  # Clear the previous plot
        if i < len(df.columns) - 1:
            ax.plot(df.iloc[:, 0], df.iloc[:, i+1])
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            ax.set_title(df.columns[i+1])
            ax.grid(True)
    canvas.draw()
    window.after(10000, update_graphs, window, canvas, axs, file_path)  # Schedule next update

# Function to plot initial graphs
def plot_graphs(df, file_path):
    # Create a window
    window = tk.Tk()
    window.title("CSV Data Graphs")

    # Determine the number of graphs
    num_graphs = len(df.columns) - 1
    num_rows = (num_graphs + 2) // 3

    # Create a figure for the plots
    fig, axs = plt.subplots(num_rows, 3, figsize=(15, 5 * num_rows))
    axs = axs.flatten()

    # Plot each column against the datetime
    for i, column in enumerate(df.columns[1:], start=0):
        axs[i].plot(df.iloc[:, 0], df[column])
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        axs[i].set_title(column)
        axs[i].grid(True)

    # Adjust layout
    plt.tight_layout()

    # Embed the plots into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Schedule the first update
    window.after(10000, update_graphs, window, canvas, axs, file_path)

    # Run the application
    window.mainloop()

# Main function
def main():
    df = read_csv_data()
    if df is not None:
        file_path = filedialog.askopenfilename()  # Get the file path again for updates
        plot_graphs(df, file_path)

if __name__ == "__main__":
    main()

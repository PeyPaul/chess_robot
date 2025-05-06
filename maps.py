from motor_control import test, theta10, theta20
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import tkinter as tk
from tkinter import messagebox
import os

def load_map(filename="map.txt"):
    points = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                x, y, status = line.strip().split(',')
                points.append((float(x), float(y), status))
    return points
def save_point(x, y, status, filename="map.txt"):
    with open(filename, "a") as f:
        f.write(f"{x},{y},{status}\n")


def main():
    points = load_map()
    
    fig, ax = plt.subplots()
    ax.set_xlim(-100, 500)
    ax.set_ylim(-100, 500)
    ax.set_title("click to test points")

    for x, y, status in points:
        color = 'green' if status == 'yes' else 'red'
        ax.plot(x, y, 'o', color=color)

    def on_click(event):
        if event.button is MouseButton.LEFT:
            x_click, y_click = event.xdata, event.ydata
            if x_click is None or y_click is None:
                return 
            
            print(f"Test launched for : ({x_click}, {y_click})")
            test(x_click, y_click)
            
            root = tk.Tk()
            root.withdraw() 
            result = messagebox.askquestion("Confirmation", "Position reached ?")
            root.destroy()

            status = "yes" if result == 'yes' else "no"
            color = 'green' if status == 'yes' else 'red'
            ax.plot(x_click, y_click, 'o', color=color)
            save_point(x_click, y_click, status)
            fig.canvas.draw()

    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
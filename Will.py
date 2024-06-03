import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_graph(v, k, s, q):
    """
    This function generates and displays a graph representing the total cost curve
    based on annual demand (v), ordering cost (k), holding cost (s), and order quantity (q).

    Args:
        v (float): Annual demand for fuel.
        k (float): Ordering cost per delivery.
        s (float): Holding cost per liter per unit time.
        q (float): Order quantity.
    """
    # Create a sequence of order quantity values for the x-axis.
    start = q * 0.5
    le = 100
    step = 1 / le

    x = []
    for i in range(le):  # Adjust the range for x-axis values
        x.append(start + step * q * i)
    y = [(k * v / q + s * q / 2) for q in x]

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=11, sticky="nsew")  # Place the canvas in the grid
    ax.set_xlabel("quantity")
    ax.set_ylabel("total cost")
    ax.set_title("Total cost in relation to order quantity")
    ax.plot(x, y, label="L(q)=k * v / q + s * q / 2")
    ax.plot(q, k * v / q + s * q / 2, marker='o', markersize=10, markerfacecolor="red", markeredgewidth=2,
            markeredgecolor="blue", label=f"min({q},{k * v / q + s * q / 2})")  # Customize marker style
    ax.legend()
    canvas.draw()  # Draw the plot on the canvas


def calculate_quantity():
    """
    This function retrieves user input, calculates the optimal order quantity using the Wilson EOQ formula,
    and displays the results along with the total cost curve.
    """
    # Get values from the entry boxes
    try:
        demand_for_year = float(entry1.get())
        shipping_cost = float(entry2.get())
        holding_cost = float(entry3.get())
    except ValueError:
        # Handle non-numeric input
        result_label.config(text="Please enter valid numbers!", fg="red")
        result_label1.config(text="", fg="red")
        result_label2.config(text="", fg="red")
        return
    optimal_order_quantity = (2 * shipping_cost * demand_for_year / holding_cost) ** 0.5
    optimal_time = optimal_order_quantity / demand_for_year
    periodic_cost = holding_cost * optimal_order_quantity

    # Update the result label with styling
    result_label.config(text=f"Optimal order quantity is: {optimal_order_quantity}", fg="green")
    result_label1.config(text=f"cycle: {optimal_time} in years(units time)", fg="green")
    result_label2.config(text=f"Yore periodic cost is: {periodic_cost}", fg="green")
    plot_graph(demand_for_year,
               shipping_cost,
               holding_cost,
               optimal_order_quantity
               )

# Create the main application window
window = tk.Tk()
# Set the title of the window
window.title("Wilson Calculator")

# Window background color
window.configure(bg="#f0f0f0", pady=20)

# Font for labels and buttons
font_style = ("Arial", 12)

label1 = tk.Label(window, text="מחשבון מודל כלכלי של ווילסון", font=("Arial", 22))
label1.grid(row=0, column=0, pady=5, padx=80)
label1 = tk.Label(window, text="לבעלים של תחנת דלק", font=font_style)
label1.grid(row=1, column=0, pady=5, padx=10)

# Create labels for each input with styling
label1 = tk.Label(window, text="How much fuel do you sell per year (in liters)?", font=font_style)
label1.grid(row=2, column=0, pady=5, padx=10)

label2 = tk.Label(window, text="How much does it cost to order a refill?:", font=font_style)
label2.grid(row=4, column=0, pady=5)

# This text block explains the Wilson economic model and its application to gas stations.
label3 = tk.Label(window, text="How much does it cost to store a liter of fuel per year?", font=font_style)
label3.grid(row=6, column=0, pady=5)

entry1 = tk.Entry(window, width=15, borderwidth=2)
entry1.grid(row=3, column=0, padx=5)

entry2 = tk.Entry(window, width=15, borderwidth=2)
entry2.grid(row=5, column=0, padx=5)

entry3 = tk.Entry(window, width=15, borderwidth=2)
entry3.grid(row=7, column=0, padx=5)

# Create a button for calculation with styling (using relief)
calculate_button = tk.Button(window, text="Calculate Quantity", command=calculate_quantity, relief="raised")
calculate_button.grid(row=8, column=0, pady=20)
window.bind('<Return>', lambda event: calculate_quantity())

# Create a label to display the result with styling
result_label = tk.Label(window, text="", fg="black")  # Initial color for result
result_label.grid(row=9, column=0)
result_label1 = tk.Label(window, text="", fg="black")  # Initial color for result
result_label1.grid(row=10, column=0)
result_label2 = tk.Label(window, text="", fg="black")  # Initial color for result
result_label2.grid(row=11, column=0)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=0, column=1, rowspan=11, sticky="nsew")  # Place the canvas in the grid
ax.set_xlabel("quantity")
ax.set_ylabel("total cost ")
ax.set_title("Total cost in relation to order quantity")
label1 = tk.Label(window, text="Wilson economic model calculator", font=("Arial", 22))
# label1.grid(row=0, column=0, pady=5, padx=80)
label1.grid(row=12, columnspan=2, sticky="nsew", pady=3)

# Create a label explaining the Wilson economic model
labele_xplaining = tk.Label(window, text="Finding the Optimal Order Quantity for a Gas Station\n\
The gas station owner's goal is to minimize the total cost per year, which includes:\n\
Cost per liter of fuel: This includes the purchase price (X1) and any transportation costs not dependent on quantity.\n\
We will ignore this price in this model because the profit per liter does not change in relation to the quantity\
Additionally\n\
Delivery cost: This is a fixed cost (K) charged per truck delivery regardless of the amount delivered.\n\
Holding cost: This cost is proportional to the amount of fuel stored and the time it's stored. We can represent it as Q/2 x S, where:\n\
S is the holding cost per liter per unit time (e.g., per year).\n\
Q/2 is the average number of liters in storage.\n\
We need to find the order quantity (Q) that minimizes the total cost per year.", font=font_style)
labele_xplaining.grid(row=13, columnspan=2, sticky="nsew", pady=15)

window.mainloop()

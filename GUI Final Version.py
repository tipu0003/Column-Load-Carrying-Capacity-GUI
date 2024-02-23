import pickle
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from sklearn.ensemble import RandomForestRegressor

# Load the dataset
data = pd.read_excel("dataset.xlsx")
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Initialize the Random Forest Regressor
rf_regressor = RandomForestRegressor()

# Fit the model on the training data
rf_regressor.fit(X, y)

# Save the trained model
with open('rf_model.pkl', 'wb') as model_file:
    pickle.dump(rf_regressor, model_file)


# tkinter GUI
root = tk.Tk()
root.title("Load Carrying Capacity Prediction")

canvas1 = tk.Canvas(root, width=550, height=550)
canvas1.configure(background='#e9ecef')
canvas1.pack()

label0 = tk.Label(root, text='Developed by Mr. Rupesh Kumar Tipu', font=('Times New Roman', 15, 'bold'), bg='#e9ecef')
canvas1.create_window(20, 20, anchor="w", window=label0)

label_phd = tk.Label(root, text='K. R. Mangalam University, India.\nEmail: tipu0003@gmail.com',
                     font=('Futura Md Bt', 12), bg='#e9ecef')

canvas1.create_window(20, 50, anchor="w", window=label_phd)

label_input = tk.Label(root, text='Input Variables', font=('Times New Roman', 12, 'bold', 'italic', 'underline'),
                       bg='#e9ecef')
canvas1.create_window(20, 90, anchor="w", window=label_input)

# Labels and entry boxes
# labels = ['Area of concrete section  (mm\u00b2)', 'Concrete strength of unconfined concrete  (MPa)',
#           'Total thickness of FRP wraps  (mm)', 'Elastic modulus of FRP  (MPa)',
#           'Area of steel tubes  (mm\u00b2)', 'Yield strength of internal steel tubes  (MPa)']
# # Labels for user input features based on provided feature names
features = [
    "Concrete strength  (MPa)", "Height of column  (mm)", "Diameter of outer steel tube (from outer to outer) (mm)",
    "Diameter of outer steel tube (from inner to inner) (mm)", "Yield strength of outer steel tube  (MPa)", "Yield "
                                                                                                            "strength"
                                                                                                            " of "
                                                                                                            "longitudinal reinforcing rebars  (MPa)", "Ratio of longitudinal reinforcing rebars",
    "Volumetric ratio of circular/spiral reinforcing rebars", "Yield strength of circular/spiral reinforcing rebars  "
                                                              "(MPa)", "Total area of internal reinforcing steel "
                                                                       "section  (mm\u00b2)", "Yield strength of "
                                                                                              "internal reinforcing "
                                                                                              "steel section  (MPa)",
    "Eccentricity (mm)"
]
entry_boxes = []
for i, feature_name in enumerate(features):
    label = tk.Label(root, text=feature_name, font=('Times New Roman', 12, 'italic'), bg='#e9ecef', pady=5)
    canvas1.create_window(20, 120 + i * 30, anchor="w", window=label)

    entry = tk.Entry(root)
    canvas1.create_window(480, 120 + i * 30, window=entry)
    entry_boxes.append(entry)


label_output = tk.Label(root, text='Load carrying capacity', font=('Times New Roman', 18,'bold'),
                        bg='#e9ecef')
canvas1.create_window(20, 520, anchor="w", window=label_output)




def predict_capacity():
    input_values = []
    for entry_box in entry_boxes:
        value = entry_box.get().strip()
        if value:
            try:
                input_values.append(float(value))
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")
                return
        else:
            messagebox.showerror("Error", "Please fill in all the input fields.")
            return

    input_data = pd.DataFrame([input_values], columns=X.columns)

    # Load the trained RandomForestRegressor model
    with open('rf_model.pkl', 'rb') as model_file:
        rf_loaded = pickle.load(model_file)

    # Predict using the loaded model
    prediction_result = rf_loaded.predict(input_data)
    prediction_result = round(prediction_result[0], 2)

    # Display the prediction on the GUI
    label_prediction = tk.Label(root, text=f'{str(prediction_result)} kN', font=('Times New Roman', 20, 'bold'), bg='white')
    canvas1.create_window(270, 520, anchor="w", window=label_prediction)


button_predict = tk.Button(root, text='Predict', command=predict_capacity, bg='#4285f4', fg='white', font=('Times New Roman', 20, 'bold'), bd=3, relief='ridge')
canvas1.create_window(420, 520, anchor="w", window=button_predict)

root.mainloop()
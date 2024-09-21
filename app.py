from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculate():
    # Inicializamos variables
    z_score = None
    percentile = None
    gestational_age = ''
    fetal_sex = ''
    maternal_height = ''
    pre_pregnancy_weight = ''
    observed_fetal_weight = ''
    
    if request.method == "POST":
        # Capturamos los valores ingresados por el usuario y los mantenemos
        gestational_age = float(request.form.get("gestational_age"))
        fetal_sex = int(request.form.get("fetal_sex"))
        maternal_height = float(request.form.get("maternal_height"))
        pre_pregnancy_weight = float(request.form.get("pre_pregnancy_weight"))
        observed_fetal_weight = float(request.form.get("observed_fetal_weight"))
        
        # Cálculos intermedios
        w1 = 2.991 - (0.3185 * gestational_age) + (gestational_age ** 2 * 0.01094) - (gestational_age ** 3 * 0.0001055)
        w2 = w1 * 0.86
        w3 = 1496.202 + (64.3479 * fetal_sex) + (831.362 * maternal_height) + (9.567 * pre_pregnancy_weight)
        w4 = w1 * w3
        w5 = w2 * w3
        w6 = (w4 - w5) / 1.28
        
        # Cálculo del z-score con 2 decimales
        z_score = round((observed_fetal_weight - w4) / w6, 2)
        
        # Cálculo del percentil con 1 decimal
        from scipy.stats import norm
        percentile = round(norm.cdf(z_score) * 100, 1)
        
    return render_template("index.html", z_score=z_score, percentile=percentile,
                           gestational_age=gestational_age, fetal_sex=fetal_sex,
                           maternal_height=maternal_height, pre_pregnancy_weight=pre_pregnancy_weight,
                           observed_fetal_weight=observed_fetal_weight)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Excel faylning aniq yo‘li
EXCEL_FILE = os.path.join(os.getcwd(), "TIME_CONTAINER.xlsx")

def read_excel():
    try:
        if not os.path.exists(EXCEL_FILE):
            return {"error": "Excel fayli topilmadi!"}

        df = pd.read_excel(EXCEL_FILE)

        # Ustunlarni tekshirish
        expected_columns = ["#", "NAME", "START", "END", "TIME", "STATUS"]  # '#' ustuni qo'shildi
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            return {"error": f"Excel faylida quyidagi ustunlar yetishmaydi: {', '.join(missing_columns)}"}

        # NaN qiymatlarni bo'sh stringga almashtirish
        df = df.fillna("")

        # JSON formatga o‘tkazish
        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(read_excel())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

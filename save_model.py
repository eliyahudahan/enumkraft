import joblib
import os

# צור תיקייה
os.makedirs('models', exist_ok=True)

# שמור מודל (תחליף את lgb_model2 בשם המשתנה שלך)
# joblib.dump(lgb_model2, 'models/lightgbm_model.pkl')
print("✅ Model saved")

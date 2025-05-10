# Placeholder for macro calculation utility
def calculate_macros(calories, protein_ratio=0.3, fat_ratio=0.3, carb_ratio=0.4):
    protein = calories * protein_ratio / 4
    fat = calories * fat_ratio / 9
    carbs = calories * carb_ratio / 4
    return {"protein": round(protein), "fat": round(fat), "carbs": round(carbs)}

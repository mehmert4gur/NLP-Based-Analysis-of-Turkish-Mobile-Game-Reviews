import subprocess
import sys

steps = [
    "src/preprocess_reviews.py",
    "src/analyze_categories.py",
    "src/visualize_results.py",
]

for step in steps:
    print(f"\nÇalıştırılıyor: {step}")
    result = subprocess.run([sys.executable, step])

    if result.returncode != 0:
        print(f"\nHata oluştu: {step}")
        sys.exit(result.returncode)

print("\nAnaliz başarıyla tamamlandı.")
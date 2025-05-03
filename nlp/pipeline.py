import pandas as pd
import os
import sys

# Ensure History_documents folder is in path
sys.path.append(r"C:\Users\15614\Documents\History_documents")

from chronicling_america import load_chronicling_articles_all_states
from wikipedia_loader import load_ancient_articles
#from wikisource_loader import load_wikisource_articles
from gutenburg_loader import load_gutenberg_european_history
#from medieval_sourcebook_loader import load_medieval_articles  # NEW!

def run_pipeline():
    output_dir = r"C:\Users\15614\Documents\History_documents"
    os.makedirs(output_dir, exist_ok=True)

    # === Load Chronicling America ===
    print(" Loading Chronicling America data...")
    chronicling_data = load_chronicling_articles_all_states(
        date1="1776", date2="1945",
        rows_per_state=20,
        delay_between_states=2
    )
    df_chronicling = pd.DataFrame(chronicling_data)
    chronicling_path = os.path.join(output_dir, "chronicling_dataset.csv")
    df_chronicling.to_csv(chronicling_path, index=False)
    print(f" Chronicling America dataset saved to: {chronicling_path}")

    # === Load Wikipedia Ancient History ===
    print("\n Loading Wikipedia ancient history data...")
    wikipedia_data = load_ancient_articles(keyword="ancient", limit=30)
    df_wikipedia = pd.DataFrame(wikipedia_data)
    wikipedia_path = os.path.join(output_dir, "wikipedia_ancient_history_dataset.csv")
    df_wikipedia.to_csv(wikipedia_path, index=False)
    print(f" Wikipedia dataset saved to: {wikipedia_path}")

    # === Load Medieval Sourcebook ===
    # print("\n Loading Internet Medieval Sourcebook data...")
    # medieval_data = load_medieval_articles(limit=20)
    # df_medieval = pd.DataFrame(medieval_data)
    # medieval_path = os.path.join(output_dir, "medieval_dataset.csv")
    # df_medieval.to_csv(medieval_path, index=False)
    # print(f" Medieval dataset saved to: {medieval_path}")

    # === Load Project Gutenberg European History ===
    print("\n Loading Project Gutenberg European History data...")
    gutenberg_data = load_gutenberg_european_history(limit=50)
    df_gutenberg = pd.DataFrame(gutenberg_data)
    gutenberg_path = os.path.join(output_dir, "gutenberg_european_history_dataset.csv")
    df_gutenberg.to_csv(gutenberg_path, index=False)
    print(f" Project Gutenberg dataset saved to: {gutenberg_path}")

    # === Merge Datasets ===
    print("\n Combining all datasets...")
    df_combined = pd.concat([df_chronicling, df_wikipedia], ignore_index=True)
    combined_path = os.path.join(output_dir, "combined_history_dataset.csv")
    df_combined.to_csv(combined_path, index=False)
    print(f" Combined dataset saved to: {combined_path}")

if __name__ == "__main__":
    run_pipeline()

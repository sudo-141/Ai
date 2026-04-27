# Medical Expert System using Rule-Based Approach

def diagnose(symptoms):
    rules = {
        "Flu": ["fever", "cough", "body ache"],
        "Common Cold": ["cough", "sneezing", "runny nose"],
        "Malaria": ["fever", "chills", "sweating"],
        "COVID-19": ["fever", "cough", "loss of taste"],
        "Dengue": ["fever", "rash", "joint pain"]
    }

    results = []

    for disease, disease_symptoms in rules.items():
        # Using set intersection for a more 'Pythonic' match count
        match_count = len(set(symptoms) & set(disease_symptoms))

        if match_count >= 2:  # threshold
            results.append(disease)

    return results


def main():
    print("=== Medical Expert System ===")
    print("Enter symptoms (comma-separated, e.g., fever, cough): ")
    
    user_input = input(">> ").lower()
    # Ensure we don't pass empty strings if the user adds trailing commas
    symptoms = [s.strip() for s in user_input.split(",") if s.strip()]

    if not symptoms:
        print("No symptoms entered.")
        return

    diagnosis = diagnose(symptoms)

    if diagnosis:
        print("\nPossible Diseases:")
        for d in diagnosis:
            print(f"- {d}")
    else:
        print("\nNo matching disease found based on the current rules. Consult a doctor.")


if __name__ == "__main__":
    main()
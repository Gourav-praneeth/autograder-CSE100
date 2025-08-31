#include <iostream>
using namespace std;

int main() {
    // 1. Declare variables
    int feet, inches, totalInchesOver5;
    int idealFemale, idealMale;

    // 2. Print welcome message
    cout << "\tWelcome to Ideal Weight Calculation Program\n" << endl;

    // 3. Get input from the user
    cout << "Please enter your height, feet followed by inches (eg; 5 3): ";
    cin >> feet >> inches;

    // 4. Convert to inches over 5 feet
    totalInchesOver5 = (feet - 5) * 12 + inches;

    // Ensure no subtraction if height is less than 5 feet
    if (totalInchesOver5 < 0) {
        totalInchesOver5 = 0;
    }

    // 5. Compute ideal weights
    idealFemale = 100 + (5.1 * totalInchesOver5);
    idealMale = 106 + (6 * totalInchesOver5);

    // 6. Print results
    cout << "\nIf you are a male, your ideal weight should be " << idealMale << " pounds." << endl;
    cout << "\nIf you are a female, your ideal weight should be " << idealFemale << " pounds." << endl;

    return 0;
}

#include <iostream>
#include <string> 
using namespace std;

int main() {
    int feet, inches, inchesOverFive, idealWeight;
    string gender;

    cout << "\t Welcome to Ideal Weight Calculation Program" << endl;
    cout << "Please enter your height, feet followed by inches (eg; 5 3): ";
    cin >> feet >> inches;

    if (feet < 0 || inches < 0) {
	cout << "Invalid height!\n";
	return 0;
    } 

    inchesOverFive = (feet - 5) * 12 + inches;
    
    /*if (inchesOverFive < 0) {
        inchesOverFive = 0;
    }*/

    cout << "Enter your gender: ";
    cin >> gender;

    for (int i = 0; i < gender.length(); i++) {
        gender[i] = tolower(gender[i]);
    }

    if (gender == "female") {
        idealWeight = 100 + (5 * inchesOverFive);
    } 
    else if (gender == "male") {
        idealWeight = 106 + (6 * inchesOverFive);
    } 
    else {
        cout << "Invalid gender entered." << endl;
        return 0;
    }
    cout << "Your ideal weight should be " << idealWeight << " pounds." << endl;
    return 0;
}

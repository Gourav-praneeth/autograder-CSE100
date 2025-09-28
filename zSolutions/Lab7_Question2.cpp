#include <iostream>
#include <iomanip>
#include <limits>
using namespace std;

// Function prototypes
void printDescription();
void getInput(float &rate, int &hours);
void computePaycheck(float rate, int hours, float &gross, float &net);
void displayOutput(float gross, float net);

const int MAX_ATTEMPTS = 3;

int main() {
    float rate, gross, net;
    int hours;

    printDescription();
    getInput(rate, hours);
    computePaycheck(rate, hours, gross, net);
    displayOutput(gross, net);

    return 0;
}

// Displays standard payroll system message
void printDescription() {
    cout << "Welcome to the Payroll System\n";
    cout << "-----------------------------\n\n";
}

// Gets input with validation (at most 3 attempts for each)
void getInput(float &rate, int &hours) {
    int attempts = 0;

    // Pay rate
    while (true) {
        cout << "Enter hourly pay rate: ";
        if (cin >> rate && rate > 0) break;

        cout << "Invalid input. Pay rate must be positive.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (++attempts >= MAX_ATTEMPTS) {
            cout << "Too many invalid attempts!\n";
            exit(0);
        }
    }

    attempts = 0; // reset for hours

    // Hours worked
    while (true) {
        cout << "Enter hours worked: ";
        if (cin >> hours && hours > 0 && hours <= 80) break;

        cout << "Invalid input. Hours must be between 1 and 80.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (++attempts >= MAX_ATTEMPTS) {
            cout << "Too many invalid attempts!\n";
            exit(0);
        }
    }
}

// Computes gross and net pay (tax = 15% of gross)
void computePaycheck(float rate, int hours, float &gross, float &net) {
    gross = rate * hours;
    net = gross - (0.15f * gross);
}

// Displays gross and net pay
void displayOutput(float gross, float net) {
    cout << fixed << setprecision(2);
    cout << "\nGross Pay: $" << gross << endl;
    cout << "Net Pay:   $" << net << endl;
}

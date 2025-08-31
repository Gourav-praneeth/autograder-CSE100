
#include <iostream>
#include <cctype>   // for isupper, islower, isdigit

using namespace std;

double calculateRegularBill(int minutes, double &stage1, double &stage2) {
    const double base = 29.99;
    stage1 = 0.0;
    stage2 = 0.0;
    if (minutes > 200) {
        int extra = minutes - 200;
        if (extra <= 250) {
            stage1 = extra * 0.55;
        } else {
            stage1 = 250 * 0.55;
            stage2 = (extra - 250) * 0.88;
        }
    }
    return base + stage1 + stage2;
}

// Function to calculate Business customer bill
double calculateBusinessBill(int minutes, double &stage1, double &stage2) {
    const double base = 99.99;
    stage1 = 0.0;
    stage2 = 0.0;
    if (minutes > 600) {
        int extra = minutes - 600;
        if (extra <= 100) {
            stage1 = extra * 0.45;
        } else {
            stage1 = 100 * 0.45;
            stage2 = (extra - 100) * 0.99;
        }
    }
    return base + stage1 + stage2;
}


// Function to display the bill
void displayBill(string phone, int minutes, double base, double stage1, double stage2, double total) {
    cout << "\n\tPhone Bill for: " << phone << endl;
    cout << "\t============================" << endl;
    cout << "Total Minutes Used: " << minutes << endl;
    cout << "Monthly Base Payment: $" << base << endl;
    cout << "Stage 1 Cost: $" << stage1 << endl;
    cout << "Stage 2 Cost: $" << stage2 << endl;
    cout << "---------------------------------" << endl;
    cout << "Total Cost: $" << total << endl;
}

int main() {
    cout << "==========================================" << endl;
    cout << "\tPhone Bill Generation Software" << endl;
    cout << "==========================================" << endl;

    char more = 'Y';
    while (more == 'Y' || more == 'y') {
        string phone;
        char type;
        int minutes;
        int attempts = 0;

        // Customer type input
        while (true) {
            cout << "\nPlease Enter the Customer Type (R for Regular, B for Business): ";
            cin >> type;
            if (type == 'R' || type == 'r' || type == 'B' || type == 'b') break;
            cout << "Invalid customer type! Please enter R/r or B/b." << endl;
            if (++attempts == 3) return 0;
        }

        // Phone number input
        cout << "Please Enter the Customer Phone Number: ";
        cin >> phone;

        // Minutes input
        attempts = 0;
        while (true) {
            cout << "Enter the phone usage in minutes: ";
            cin >> minutes;
            if (minutes >= 0) break;
            cout << "Invalid phone usage! Minutes must be non-negative." << endl;
            if (++attempts == 3) return 0;
        }

        // Bill calculation
        double stage1 = 0.0, stage2 = 0.0, total = 0.0, base = 0.0;
        if (type == 'R' || type == 'r') {
            total = calculateRegularBill(minutes, stage1, stage2);
            base = 29.99;
        } else {
            total = calculateBusinessBill(minutes, stage1, stage2);
            base = 99.99;
        }

        // Display
        displayBill(phone, minutes, base, stage1, stage2, total);

        cout << "\nMore bills? [Y/N]: ";
        cin >> more;
    }

    cout << "\nExiting the program........." << endl;
    return 0;
}


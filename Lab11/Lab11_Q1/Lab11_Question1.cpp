#include <iostream>
#include <iomanip>
using namespace std;

class Tips {
private:
    double taxRate;

public:
    Tips(double rate = 0.085) : taxRate(rate) {}

    double computeTip(double totalBill, double tipRate) const {
        double mealCost = totalBill / (1.0 + taxRate);
        return mealCost * tipRate;
    }
};

int main() {
    Tips calculator;
    int invalidAttempts = 0;
    const int MAX_ATTEMPTS = 3;

    cout << fixed << setprecision(2);
    cout << "\t\tGratuity Calculator\n";
    cout << "\t\t-------------------\n";

    char again = 'y';

    while ((again == 'y' || again == 'Y') && invalidAttempts < MAX_ATTEMPTS) {
        double totalBill;
        double tipRate;

        // BILL INPUT LOOP
        while (true) {
            cout << "Enter the total bill amount (including tax): ";
            if (cin >> totalBill && totalBill >= 0) {
                break;
            } else {
                cout << "Invalid bill amount! Attempt " << invalidAttempts + 1 << " of 3.\n";
                cin.clear();
                cin.ignore(1000, '\n');
                invalidAttempts++;
                if (invalidAttempts >= MAX_ATTEMPTS) break;
            }
        }
        if (invalidAttempts >= MAX_ATTEMPTS) break;

        // TIP INPUT LOOP
        while (true) {
            cout << "Enter the tip rate (e.g., 0.15 for 15%): ";
            if (cin >> tipRate && tipRate >= 0) {
                break;
            } else {
                cout << "Invalid tip rate! Attempt " << invalidAttempts + 1 << " of 3.\n";
                cin.clear();
                cin.ignore(1000, '\n');
                invalidAttempts++;
                if (invalidAttempts >= MAX_ATTEMPTS) break;
            }
        }
        if (invalidAttempts >= MAX_ATTEMPTS) break;

        // CALCULATION
        double tip = calculator.computeTip(totalBill, tipRate);
        cout << "Calculated tip: $" << tip << "\n";

        // YES/NO LOOP
        while (true) {
            cout << "\nDo you want to enter another bill? (y/n): ";
            cin >> again;

            if (again == 'y' || again == 'Y' || again == 'n' || again == 'N') {
                break;
            } else {
                cout << "Invalid choice.\n";
                invalidAttempts++;
                if (invalidAttempts >= MAX_ATTEMPTS) break;
            }
        }

        cout << "\n";
    }

    if (invalidAttempts >= MAX_ATTEMPTS) {
        cout << "Too many invalid attempts!\n";
    }
    return 0;
}
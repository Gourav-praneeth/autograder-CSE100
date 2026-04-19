#include <iostream>
#include <iomanip>
#include <string>
#include <stdexcept>
using namespace std;

class Tips {
private:
    double taxRate;

public:
    Tips(double rate = 0.085) : taxRate(rate) {}

    double computeAmountWithoutTax(double totalBill) const {
        return totalBill / (1.0 + taxRate);
    }

    double computeTip(double totalBill, double tipRate) const {
        double amountWithoutTax = computeAmountWithoutTax(totalBill);
        return tipRate * amountWithoutTax;
    }

    double getTaxRate() const { return taxRate; }
};

int main() {
    cout << fixed << setprecision(2);
    cout << "===============================================\n";
    cout << "\t\tGratuity Calculator\n";
    cout << "===============================================\n";

    double taxRate = 0.0;
    int taxAttempts = 0;

    while (taxAttempts < 3) {
        cout << "Enter the tax rate as a positive real number: ";
        if (!(cin >> taxRate)) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Invalid input. Attempt " << taxAttempts + 1 << " of 3. Please enter a number.\n";
            taxAttempts++;
            continue;
        }
        break;
    }

    if (taxAttempts >= 3) {
        cout << "Too many invalid attempts!\n";
        return 0;
    }

    double effectiveTaxRate = (taxRate <= 0.0) ? 0.085 : taxRate;
    Tips calculator(effectiveTaxRate);

    while (true) {
        double totalBill = 0.0;
        int billAttempts = 0;

        while (billAttempts < 3) {
            cout << "Enter the total bill amount: ";
            string input;
            cin >> input;

            try {
                size_t idx;
                totalBill = stod(input, &idx);
                if (idx != input.size() || totalBill <= 0.0) {
                    throw invalid_argument("Invalid");
                }
                break;
            } catch (...) {
                cout << "Invalid input. Attempt " << billAttempts + 1 << " of 3. Value must be positive.\n";
                billAttempts++;
            }
        }

        if (billAttempts >= 3) {
            cout << "Too many invalid attempts!\n";
            return 0;
        }

        double tipRate = 0.0;
        int tipAttempts = 0;

        while (tipAttempts < 3) {
            cout << "Enter the tip rate: ";
            if (!(cin >> tipRate) || tipRate <= 0.0) {
                cin.clear();
                cin.ignore(1000, '\n');
                cout << "Invalid input. Attempt " << tipAttempts + 1 << " of 3. Value must be positive.\n";
                tipAttempts++;
                continue;
            }
            break;
        }

        if (tipAttempts >= 3) {
            cout << "Too many invalid attempts!\n";
            return 0;
        }

        double tipAmount = calculator.computeTip(totalBill, tipRate);

        cout << "\nTotal Bill Amount: $" << totalBill << "\n";
        cout << "Tax Rate: " << calculator.getTaxRate() * 100 << "%\n";
        cout << "Tip Rate: " << tipRate * 100 << "%\n";
        cout << "Tip Amount: $" << tipAmount << "\n";

        char cont = ' ';
        int contAttempts = 0;
        while (contAttempts < 3) {
            cout << "\nDo you want to continue (y/n)?";
            cin >> cont;
            if (cont == 'y' || cont == 'Y' || cont == 'n' || cont == 'N') {
                break;
            }
            cout << "Invalid choice. Attempt " << contAttempts + 1 << " of 3.\n";
            contAttempts++;
        }

        if (cont == 'n' || cont == 'N') {
            break;
        }
        cout << "\n";
    }

    return 0;
}

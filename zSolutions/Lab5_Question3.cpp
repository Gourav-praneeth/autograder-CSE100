#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    const int SIZE = 10;
    double sales[SIZE];

    for (int i = 0; i < SIZE; i++) {
        int invalidAttempts = 0;
        while (invalidAttempts < 3) {
            cout << "Enter the sales for store " << i << " : ";
            cin >> sales[i];
            if (sales[i] >= 0) {
                break;
            } else {
                invalidAttempts++;
                cout << "Invalid sale amount! Please enter a non-negative number. Attempt " << invalidAttempts 
                     << " of 3.\n";
            }
        }
        if (invalidAttempts == 3) {
            cout << "Too many invalid attempts. Sale for store " << i << " set to 0.\n";
            sales[i] = 0;
        }
    }

    double highest = sales[0], lowest = sales[0], sum = sales[0];
    int highStore = 0, lowStore = 0;

    for (int i = 1; i < SIZE; i++) {
        sum += sales[i];
        if (sales[i] > highest) {
            highest = sales[i];
            highStore = i;
        }
        if (sales[i] < lowest) {
            lowest = sales[i];
            lowStore = i;
        }
    }

    double average = sum / SIZE;

    cout << fixed << setprecision(2);
    cout << "\nHighest Sale: " << highest << " at Store " << highStore << endl;
    cout << "Lowest Sale: " << lowest << " at Store " << lowStore << endl;
    cout << "Average Sale: " << average << endl;

    return 0;
}

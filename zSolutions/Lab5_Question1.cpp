#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int choice;
    int person = 1;
    int coffee = 0, tea = 0, coke = 0, orangeJuice = 0;
    int totalSurveyed = 0;

    while (true) {
        int invalidAttempts = 0;
        bool validInput = false;

        while (invalidAttempts < 3) {
            cout << "Please input the favorite beverage of person #" << person
                 << ": Choose 1, 2, 3, or 4 from the above menu or -1 to exit the program"
                 << endl;
            cin >> choice;

            if (choice == -1) {
                // End program immediately
                cout << "\nThe total number of people surveyed is " << totalSurveyed << "." << endl;
                cout << "The results are as follows:\n";
                cout << left << setw(15) << "Beverage" << "Number of Votes" << endl;
                cout << "********************************\n";
                cout << left << setw(15) << "Coffee" << coffee << endl;
                cout << left << setw(15) << "Tea" << tea << endl;
                cout << left << setw(15) << "Coke" << coke << endl;
                cout << left << setw(15) << "Orange Juice" << orangeJuice << endl;
                return 0;
            }

            if (choice >= 1 && choice <= 4) {
                // Valid input
                switch (choice) {
                    case 1: coffee++; break;
                    case 2: tea++; break;
                    case 3: coke++; break;
                    case 4: orangeJuice++; break;
                }
                totalSurveyed++;
                validInput = true;
                break;
            } else {
                invalidAttempts++;
                cout << "Invalid choice! Attempt " << invalidAttempts << " of 3." << endl;
                if (invalidAttempts == 3) {
                    cout << "Too many invalid attempts. Moving to next person.\n";
                }
            }
        }

        person++;
    }

    return 0;
}


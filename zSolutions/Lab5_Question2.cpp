#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

int main() {
    int numCities, invalidCount = 0;
    int population[50];

    cout << "Enter the number of cities: ";
    cin >> numCities;

    if (numCities <= 0) {
        cout << "Invalid number of cities!" << endl;
        return 0;
    }

    for (int i = 0; i < numCities; i++) {
        while (true) {
            cout << "Enter the population for city " << i+1 << ": ";
            cin >> population[i];

            if (cin.fail() || population[i] < 0) {
                cin.clear();
                cin.ignore(10000, '\n');
                cout << "Invalid population!" << endl;
                invalidCount++;
            } else {
                break;
            }

            if (invalidCount >= 3) {
                cout << "Too many invalid inputs. Exiting program." << endl;
                return 0;
            }
        }

      }
      
    cout << "\nCity    Population Bar Graph\n";
    cout << "---------------------------------\n";

	for (int i = 0; i < numCities; i++) {  
		// Round up to nearest 1000
        	int rounded = ((population[i] + 999) / 1000) * 1000;
        	int stars = rounded / 1000;
        	cout << setw(2) << i+1 << "       ";
        	for (int j = 0; j < stars; j++) {
            		cout << "*";
       	 	}
        	cout << endl;
	}
    

    return 0;
}

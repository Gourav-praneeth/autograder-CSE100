
#include <iostream>
#include <cctype>   // for isupper, islower, isdigit

using namespace std;


// Function to compute distance fallen after t seconds
double distanceFallen(int t) {
    const double g = 9.8;
    return 0.5 * g * t * t;
}

int main() {
    int timeOfFall, height;
    int invalidAttempts = 0;

    // Input time with validation
    while (true) {
        cout << "Enter the time of fall (in seconds): ";
        cin >> timeOfFall;
        if (cin.fail() || timeOfFall < 0) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Invalid time!" << endl;
            if (++invalidAttempts >= 3) return 0;
        } else break;
    }

    // Input height with validation
    while (true) {
        cout << "Enter the height of the bridge (in meters): ";
        cin >> height;
        if (cin.fail() || height <= 0) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "Invalid height!" << endl;
            if (++invalidAttempts >= 3) return 0;
        } else break;
    }

    // Output header
    cout << "\nTime (s)" << "\t" << "Distance (m)" << endl;

    bool exceeded = false;
    for (int t = 0; t <= timeOfFall; t++) {
        double d = distanceFallen(t);
        cout << "    " << t << "\t\t" << d << endl;
        if (d > height) {
            exceeded = true;
            break;
        }
    }

    if (exceeded) {
        cout << "\nWarning - Bad Data: The distance fallen exceeds the height of the bridge." << endl;
    }

    return 0;
}

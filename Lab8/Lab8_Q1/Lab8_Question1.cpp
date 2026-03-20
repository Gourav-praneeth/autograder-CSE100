#include <iostream>
#include <string>
#include <limits>
using namespace std;

const int MAX_SIZE = 100;
const int MAX_INVALID_SIZE_ATTEMPTS = 3;
const int MAX_INVALID_NAME_ATTEMPTS = 3;

void selectionSort(string arr[], int size) {
    for (int start = 0; start < size - 1; start++) {
        int minIndex = start;
        string minValue = arr[start];
        for (int i = start + 1; i < size; i++) {
            if (arr[i] < minValue) {
                minValue = arr[i];
                minIndex = i;
            }
        }
        arr[minIndex] = arr[start];
        arr[start] = minValue;
    }
}

bool isValidName(const string &name) {
    // Valid if it contains at least one comma and at least one space.
    // This rejects examples like "JohnsonJill", "Johnson,Jill", "Johnson Jill".
    return !name.empty() &&
           name.find(',') != string::npos &&
           name.find(' ') != string::npos;
}

int main() {
    int n;
    int sizeAttempts = 0;

    // Prompt for number of names with up to 3 invalid attempts
    while (true) {
        cout << "Enter the number of names: ";
        if (!(cin >> n)) {
            return 0;
        }
        if (n > 0 && n <= MAX_SIZE) {
            break;
        }
        sizeAttempts++;
        cout << "Invalid number! Attempt " << sizeAttempts << " of 3." << endl;
        if (sizeAttempts >= MAX_INVALID_SIZE_ATTEMPTS) {
            cout << "Too many Invalid Attempts!" << endl;
            return 0;
        }
    }

    string names[MAX_SIZE];

    // Consume leftover newline before using getline
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    int totalInvalidNameAttempts = 0;

    for (int i = 0; i < n; i++) {
        while (true) {
            cout << "Enter name " << (i + 1) << " : ";
            string input;
            if (!getline(cin, input)) {
                return 0;
            }

            if (isValidName(input)) {
                names[i] = input;
                break;
            }

            totalInvalidNameAttempts++;
            cout << "Invalid name! Attempt " << totalInvalidNameAttempts << " of 3." << endl;
            if (totalInvalidNameAttempts >= MAX_INVALID_NAME_ATTEMPTS) {
                cout << "Too many Invalid Attempts!" << endl;
                return 0;
            }
        }
    }

    selectionSort(names, n);

    cout << "Sorted names:" << endl;
    for (int i = 0; i < n; i++) {
        cout << names[i] << endl;
    }

    return 0;
}

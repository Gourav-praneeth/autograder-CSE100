#include <iostream>
#include <limits>
#include <string>
using namespace std;

int main() {

    const int MAX_CAPACITY = 100;
    const int MAX_INVALID_SIZE_ATTEMPTS = 3;
    const int MAX_INVALID_NAME_ATTEMPTS = 3;
    const int MAX_INVALID_ID_ATTEMPTS = 3;

    struct Student {
        string name;
        int id;
        string academicLevel;
    };

    Student roster[MAX_CAPACITY];

    // --- Read total number of students
    int totalStudents = 0;
    int sizeAttempts = 0;
    while (true) {
        cout << "Enter the number of students: " << flush;
        if (!(cin >> totalStudents)) {
            return 0;
        }
        if (totalStudents > 0 && totalStudents <= MAX_CAPACITY) {
            break;
        }
        sizeAttempts++;
        cout << "Invalid input! " << totalStudents << " should be positive."
             << endl;
        if (sizeAttempts >= MAX_INVALID_SIZE_ATTEMPTS) {
            cout << "Too many Invalid Attempts!" << endl;
            return 0;
        }
    }

    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    int totalInvalidNameAttempts = 0;
    const int initialCount = totalStudents - 1;

    for (int i = 0; i < initialCount; i++) {
        while (true) {
            cout << "Enter name " << (i + 1)
                 << " (last name, first name) : " << flush;
            string input;
            if (!getline(cin, input)) {
                return 0;
            }

            bool validName = !input.empty() &&
                             input.find(", ") != string::npos &&
                             input.find(' ') != string::npos;

            if (validName) {
                roster[i].name = input;
                break;
            }

            totalInvalidNameAttempts++;
            cout << "Invalid name! Attempt " << totalInvalidNameAttempts << " of 3."
                 << endl;
            if (totalInvalidNameAttempts >= MAX_INVALID_NAME_ATTEMPTS) {
                cout << "Too many Invalid Attempts!" << endl;
                return 0;
            }
        }

        // Student ID: must be positive; up to 3 invalid attempts
        int idAttempts = 0;
        while (true) {
            cout << "Enter student ID: " << flush;
            if (!(cin >> roster[i].id)) {
                return 0;
            }
            if (roster[i].id > 0) {
                break;
            }
            idAttempts++;
            cout << "Invalid input! ID should be positive." << endl;
            if (idAttempts >= MAX_INVALID_ID_ATTEMPTS) {
                cout << "Too many Invalid Attempts!" << endl;
                return 0;
            }
        }
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        cout << "Enter academic level: " << flush;
        if (!getline(cin, roster[i].academicLevel)) {
            return 0;
        }
    }


    for (int start = 0; start < initialCount - 1; start++) {
        int minIndex = start;
        string minName = roster[start].name;
        for (int j = start + 1; j < initialCount; j++) {
            if (roster[j].name < minName) {
                minName = roster[j].name;
                minIndex = j;
            }
        }
        if (minIndex != start) {
            Student tmp = roster[start];
            roster[start] = roster[minIndex];
            roster[minIndex] = tmp;
        }
    }

    // Read the last student to insert (after sort)
    Student newStudent;
    while (true) {
        cout << "Enter name " << totalStudents << " (last name, first name) : "
             << flush;
        string input;
        if (!getline(cin, input)) {
            return 0;
        }

        bool validName = !input.empty() &&
                         input.find(", ") != string::npos &&
                         input.find(' ') != string::npos;

        if (validName) {
            newStudent.name = input;
            break;
        }

        totalInvalidNameAttempts++;
        cout << "Invalid name! Attempt " << totalInvalidNameAttempts << " of 3."
             << endl;
        if (totalInvalidNameAttempts >= MAX_INVALID_NAME_ATTEMPTS) {
            cout << "Too many Invalid Attempts!" << endl;
            return 0;
        }
    }

    int newIdAttempts = 0;
    while (true) {
        cout << "Enter student ID: " << flush;
        if (!(cin >> newStudent.id)) {
            return 0;
        }
        if (newStudent.id > 0) {
            break;
        }
        newIdAttempts++;
        cout << "Invalid input! ID should be positive." << endl;
        if (newIdAttempts >= MAX_INVALID_ID_ATTEMPTS) {
            cout << "Too many Invalid Attempts!" << endl;
            return 0;
        }
    }
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    cout << "Enter academic level: " << flush;
    if (!getline(cin, newStudent.academicLevel)) {
        return 0;
    }

    // --- Insert new student into the sorted array at the correct index
    int insertAt = 0;
    while (insertAt < initialCount &&
           roster[insertAt].name < newStudent.name) {
        insertAt++;
    }
    for (int j = initialCount; j > insertAt; j--) {
        roster[j] = roster[j - 1];
    }
    roster[insertAt] = newStudent;

    // Output
    for (int i = 0; i < totalStudents; i++) {
        cout << roster[i].name << '\t' << roster[i].id << '\t'
             << roster[i].academicLevel << endl;
    }

    return 0;
}

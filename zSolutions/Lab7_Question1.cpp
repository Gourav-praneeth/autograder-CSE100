#include <iostream>
#include <iomanip>
#include <limits>
using namespace std;

// Function prototypes
void readScore(const string &label, double &score);
void readTestandHwScore(double &t1, double &t2, double &hw);
double calcFinalScore(double t1, double t2, double hw);
void printFinalScore(double finalScore);

const int MAX_ATTEMPTS = 3;

int main() {
    double test1, test2, hw;
    readTestandHwScore(test1, test2, hw);

    double finalScore = calcFinalScore(test1, test2, hw);
    printFinalScore(finalScore);

    return 0;
}

void readScore(const string &label, double &score) {
        int attempts = 0;
        while (true) {
            cout << "Enter " << label << " score (0–100): ";
            if (cin >> score && score >= 0 && score <= 100) break;

            cout << "Invalid input! Score must be between 0 and 100.\n";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            if (++attempts >= MAX_ATTEMPTS) {
                cout << "Too many invalid attempts!\n";
                exit(0);
            }
        }
}

// Reads test and homework scores with validation and at most 3 attempts
void readTestandHwScore(double &test1, double &test2, double &hw) {
    
    readScore("Test 1", test1);
    readScore("Test 2", test2);
    readScore("Homework", hw);
}

// Calculates final weighted score
double calcFinalScore(double t1, double t2, double hw) {
    return (t1 * 0.40) + (t2 * 0.40) + (hw * 0.20);
}

// Prints final score and letter grade
void printFinalScore(double finalScore) {
    cout << fixed << setprecision(2);
    cout << "\nFinal Score: " << finalScore << endl;

    char grade;
    if (finalScore >= 90) grade = 'A';
    else if (finalScore >= 80) grade = 'B';
    else if (finalScore >= 70) grade = 'C';
    else if (finalScore >= 60) grade = 'D';
    else grade = 'F';

    cout << "Letter Grade: " << grade << endl;
}

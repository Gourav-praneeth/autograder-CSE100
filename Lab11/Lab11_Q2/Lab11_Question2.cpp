#include <cctype>
#include <iostream>
#include <string>
using namespace std;

class teamScore {
private:
    string teamName;
    int wins;
    int ties;
    int losses;

    int computePoints() const { return 3 * wins + ties; }

public:
    teamScore(const string& name) : teamName(name), wins(0), ties(0), losses(0) {}

    void updateWins() { wins++; }
    void updateTies() { ties++; }
    void updateLosses() { losses++; }

    void displayRecord() const {
        int totalPoints = computePoints();

        cout << "\n=====================================\n";
        cout << "           TEAM RECORD\n";
        cout << "=====================================\n";
        cout << "Team Name\t: " << teamName << "\n";
        cout << "-------------------------------------\n";
        cout << "Wins\t\t: " << wins << "\n";
        cout << "Ties\t\t: " << ties << "\n";
        cout << "Losses\t\t: " << losses << "\n";
        cout << "-------------------------------------\n";
        cout << "Total Points\t: " << totalPoints << "\n";
        cout << "=====================================\n\n";
    }
};

int main() {
    cout << "=====================================\n";
    cout << "        SOCCER POINTS SYSTEM\n";
    cout << "=====================================\n";

    string name;
    cout << "Enter team name: ";
    getline(cin, name);

    teamScore team(name);

    cout << "\n------------------------------------- Action menu ------------------------------------\n";
    cout << "W - Record a WIN | ";
    cout << "T - Record a TIE | ";
    cout << "L - Record a LOSS | ";
    cout << "D - Display Record | ";
    cout << "E - Exit\n";
    cout << "--------------------------------------------------------------------------------------\n";

    char action;
    int invalidAttempts = 0;

    while (invalidAttempts < 3) {
        cout << "Select an action: ";
        cin >> action;

        switch (toupper(static_cast<unsigned char>(action))) {
            case 'W':
                team.updateWins();
                //cout << "Win recorded!\n";
                break;

            case 'T':
                team.updateTies();
                //cout << "Tie recorded!\n";
                break;

            case 'L':
                team.updateLosses();
                //cout << "Loss recorded!\n";
                break;

            case 'D':
                team.displayRecord();
                break;

            case 'E':
                team.displayRecord();
                return 0;

            default:
                invalidAttempts++;
                cout << "Invalid choice! Attempt " << invalidAttempts << " of 3.\n";
                break;
        }

        if (invalidAttempts >= 3) {
            cout << "\nToo many Invalid Attempts!\n";
            break;
        }
    }

    team.displayRecord();

    return 0;
}

#include <iostream>
#include <limits>
#include <string>
using namespace std;

class TeamScore {
private:
    string teamName;
    int wins;
    int ties;
    int losses;

public:
    TeamScore(const string& name) : teamName(name), wins(0), ties(0), losses(0) {}

    void updateWins() { wins++; }
    void updateTies() { ties++; }
    void updateLosses() { losses++; }

    void displayRecord() const {
        int totalPoints = (wins * 3) + (ties * 1);

        cout << "\n=====================================\n";
        cout << "           TEAM RECORD\n";
        cout << "=====================================\n";
        cout << "Team Name   : " << teamName << "\n";
        cout << "-------------------------------------\n";
        cout << "Wins        : " << wins << "\n";
        cout << "Ties        : " << ties << "\n";
        cout << "Losses      : " << losses << "\n";
        cout << "-------------------------------------\n";
        cout << "Total Points: " << totalPoints << "\n";
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

    TeamScore team(name);

    char action;
    int invalidAttempts = 0;

    while (invalidAttempts < 3) {
        cout << "\nChoose an action:\n";
        cout << "W - Record a WIN | ";
        cout << "T - Record a TIE | ";
        cout << "L - Record a LOSS | ";
        cout << "D - Display Record | ";
        cout << "E - Exit\n";
        cout << "Enter choice: ";
        cin >> action;

        switch (toupper(action)) {
            case 'W':
                team.updateWins();
                cout << "Win recorded!\n";
                break;

            case 'T':
                team.updateTies();
                cout << "Tie recorded!\n";
                break;

            case 'L':
                team.updateLosses();
                cout << "Loss recorded!\n";
                break;

            case 'D':
                team.displayRecord();
                break;

            case 'E':
                exit(0);

            default:
                invalidAttempts++;
                cout << "Invalid choice! Attempt " << invalidAttempts << " of 3.\n";
                break;
        }

        if (invalidAttempts >= 3) {
            cout << "\nToo many invalid attempts!\n";
            break;
        }
    }

    cout << "\nFinal Team Summary:";
    team.displayRecord();

    return 0;
}
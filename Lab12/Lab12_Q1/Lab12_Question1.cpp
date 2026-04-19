#include <cctype>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static string trim(const string &s) {
    size_t start = 0;
    while (start < s.size() && isspace(static_cast<unsigned char>(s[start]))) {
        start++;
    }
    size_t end = s.size();
    while (end > start && isspace(static_cast<unsigned char>(s[end - 1]))) {
        end--;
    }
    return s.substr(start, end - start);
}

static bool openFileOrExit(const string &prompt, ifstream &in, string *openedPath = nullptr) {
    cout << prompt;
    string name;
    if (!getline(cin, name)) {
        return false;
    }
    name = trim(name);
    in.open(name);
    if (in.is_open()) {
        if (openedPath != nullptr) {
            *openedPath = name;
        }
        return true;
    }
    cout << name << " does not exist!\n";
    in.clear();
    return false;
}

static void readAllLines(ifstream &in, vector<string> &out) {
    string line;
    while (getline(in, line)) {
        out.push_back(line);
    }
}

static int countWins(const vector<string> &winners, const string &team) {
    int n = 0;
    for (const string &w : winners) {
        if (w == team) {
            n++;
        }
    }
    return n;
}

int main() {
    string teamsPath;
    ifstream teamsIn;
    if (!openFileOrExit("Enter the teams data file name: ", teamsIn, &teamsPath)) {
        return 1;
    }
    vector<string> teams;
    readAllLines(teamsIn, teams);
    teamsIn.close();

    ifstream winnersIn;
    if (!openFileOrExit("Enter the World Series winners file name: ", winnersIn)) {
        return 1;
    }
    vector<string> winners;
    readAllLines(winnersIn, winners);
    winnersIn.close();

    cout << "Contents of " << teamsPath << ":\n";
    for (const string &t : teams) {
        cout << t << "\n";
    }

    while (true) {
        const int kMaxTeamAttempts = 3;
        string team;
        bool gotValidTeam = false;
        for (int attempt = 1; attempt <= kMaxTeamAttempts; ++attempt) {
            cout << "Enter the team name: ";
            string teamLine;
            if (!getline(cin, teamLine)) {
                return 0;
            }
            team = trim(teamLine);
            if (countWins(winners, team) > 0) {
                gotValidTeam = true;
                break;
            }
            if (attempt < kMaxTeamAttempts) {
                cout << "Team name does not exist! Enter a different team.\n";
            }
        }
        if (!gotValidTeam) {
            cout << "Too many invalid attempts!\n";
            return 1;
        }

        int wins = countWins(winners, team);
        cout << team << " won " << wins << " times.\n";

        while (true) {
            cout << "Look up another team? (y/n): ";
            string choiceLine;
            if (!getline(cin, choiceLine)) {
                return 0;
            }
            string c = trim(choiceLine);
            if (c == "y" || c == "Y") {
                break;
            }
            if (c == "n" || c == "N") {
                return 0;
            }
            cout << "Invalid choice. Please enter y or n.\n";
        }
    }

    return 0;
}

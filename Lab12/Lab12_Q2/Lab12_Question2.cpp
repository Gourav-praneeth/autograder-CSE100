#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

string trim(const string &s) {
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

bool isValidName(const string &t) {
    size_t pos = t.find(", ");
    return !t.empty() && pos != string::npos &&
           pos > 0 && pos < t.size() - 2;
}

int main() {
    vector<string> names;
    int invalidAttempts = 0;

    cout << "Enter the names (Last, First) below. Enter 0 to finish.\n";

    while (true) {
        string line;
        if (!getline(cin, line)) return 0;

        string t = trim(line);
        if (t == "0") break;

        if (isValidName(t)) {
            names.push_back(t); // already trimmed and valid
        } else {
            invalidAttempts++;
            cout << "Invalid name! Attempt " << invalidAttempts << " of 3.\n";
            if (invalidAttempts >= 3) {
                cout << "Too many Invalid Attempts!\n";
                return 0;
            }
        }
    }

    sort(names.begin(), names.end());
    names.erase(unique(names.begin(), names.end()), names.end());

    cout << "Unique names:\n";
    for (const string &n : names) {
        cout << n << "\n";
    }

    return 0;
}
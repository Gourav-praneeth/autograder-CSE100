
#include <iostream>
#include <cctype>   // for isupper, islower, isdigit

using namespace std;

//Question 2
int main() {
    cout << "Enter the String (denote the end of the string with a #): ";

    char ch;
    int totalChars = 0;
    int uppercaseCount = 0;
    int lowercaseCount = 0;
    int digitCount = 0;

    // Read until '#' is encountered (works across multiple lines)
    while (cin.get(ch)) {
        if (ch == '#') {
            break; // stop reading input
        }

        totalChars++;

        if (isupper(ch)) {
            uppercaseCount++;
        } else if (islower(ch)) {
            lowercaseCount++;
        } else if (isdigit(ch)) {
            digitCount++;
        }
        // whitespace, punctuation, and other symbols count only toward totalChars
    }

    cout << "\n===== String Statistics =====" << endl;
    cout << "Total Characters   : " << totalChars << endl;
    cout << "Uppercase Letters  : " << uppercaseCount << endl;
    cout << "Lowercase Letters  : " << lowercaseCount << endl;
    cout << "Digits             : " << digitCount << endl;

    return 0;
}

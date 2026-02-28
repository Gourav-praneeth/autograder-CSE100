#include <iostream>
#include <cctype>
#include <iomanip>
using namespace std;
int main(){
    int favoritechoice, totalsurveyed = 0, attempts = 0, user = 1;
    int votes[4] = {0,0,0,0};

    bool input = true;
    while (input == true){
        input = false;
        attempts = 0;
        while (attempts < 3 && !input){
            cout << "Please input favorite beverage of person #" << user << ": Choose 1, 2, 3, or 4 from the above menu or -1 to exit the program.";
            cin >> favoritechoice;
            if (favoritechoice == -1){
                cout << "\nThe total number of people surveyed is " << totalsurveyed << ".\n";
                cout << "The results are as follows: \n";
                cout << left << setw(15) << "Beverage" << "Number of Votes\n";
                cout << "********************************\n";
                cout << left << setw(15) << "Coffee" << votes[0] <<endl;
                cout << left << setw(15) << "Tea" << votes[1] <<endl;
                cout << left << setw(15) << "Coke" << votes[2] <<endl;
                cout << left << setw(15) << "Orange Juice" << votes[3] <<endl;
                return 0;
            } else if (favoritechoice >=1 && favoritechoice <= 4){
                totalsurveyed++;
                user++;
                votes[favoritechoice-1]++;
                input = true;
                break;
            } else {
                attempts++;
                cout << "Invalid choice! Attempt " << attempts << " of 3.\n";
                if (attempts ==3){
                    cout << "Too many invalid attempts. Moving to next person.";
                    user++;
                    input = true;
                    break;
                }
            }
        }
    }
}

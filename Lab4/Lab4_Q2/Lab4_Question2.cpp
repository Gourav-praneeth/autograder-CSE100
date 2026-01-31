#include <iostream>
#include <cmath>
#include <cctype>
#include <algorithm>
#include <cstdlib> // Required for system()
using namespace std;

//Question 2

int main() {
    char n;
    string v;
	string text;
    cout << "Enter the pet type (cat or dog) : " << endl;
    cin >>  v;
    transform(v.begin(), v.end(), v.begin(), ::toupper);
    		if (v == "CAT") {
			cout << "Has the pet been spayed or neutered (y/n)? \n";
    		    cin >> n;
			if (n == 'Y' || n == 'y')
				cout << "Pet Tag fee is $4.00\n";
			else if (n == 'N' || n == 'n')
				cout << "Pet Tag fee is $8.00\n";
			else {
				cout << "Re-enter spayed or neutered (y/n):";
				cin >> n;
				if (n == 'Y' || n == 'y')
					cout << "Pet Tag fee is $4.00\n";
				else if (n == 'N' || n == 'n')
					cout << "Pet Tag fee is $8.00\n";
				else 
					cout << "Invalid choice for Spayed or neutered!\n"; } }
		else if (v == "DOG") {
			cout << "Has the pet been spayed or neutered (y/n)? \n";
    			cin >> n;
			if (n == 'Y' || n == 'y')
				cout << "Pet Tag fee is $6.00\n";
			else if (n == 'N' || n == 'n')
				cout << "Pet Tag fee is $12.00\n";
			else {
				cout << "Re-enter spayed or neutered (y/n):";
				cin >> n;
				if (n == 'Y' || n == 'y')
					cout << "Pet Tag fee is $6.00\n";
				else if (n == 'N' || n == 'n')
					cout << "Pet Tag fee is $12.00\n";
				else 
					cout << "Invalid choice for Spayed or neutered!\n"; } }
	else
		cout << "Only cats and dogs need pet tags!\n";
			

    return 0;
}

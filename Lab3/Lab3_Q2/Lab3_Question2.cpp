#include <iostream>
#include <string> 
using namespace std;

int main() {
    int panLength, panWidth;
    int brownieSize;

    int numberOfBrownies;
    string size;

    cout << "Enter the length of the baking pan (in inches): ";
    cin >> panLength;
    if (panLength < 1) {
	cout << "Invalid length of pan!\n";
	return 0;
    } 

    cout << "Enter the width of the baking pan (in inches): ";
    cin >> panWidth;
    if (panWidth < 1) {
	cout << "Invalid width of pan!\n";
	return 0;
    } 

    cout << "Enter the size of the brownie (in inches): ";
    cin >> brownieSize;

    if (brownieSize == 1)
	size = "small";
    else if(brownieSize == 2)
	size = "large"; 
    else {
	cout << "Invalid brownie size!";
	return 0;
    }

    numberOfBrownies = (panLength / brownieSize) * (panWidth / brownieSize);

    cout << endl;
    
    cout << "A " << panLength << " x " << panWidth << " pan can hold " << numberOfBrownies << " " << size << " brownies.\n";

    return 0;
}

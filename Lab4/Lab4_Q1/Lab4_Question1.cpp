#include <iostream>
#include <cmath>
#include <cctype>
#include <cstdlib> // Required for system()
using namespace std;


// Question 1

int main() {
    double n;
    int v;
    cout << "Enter choice of object based on the following menu:\n\t1 -- Square\n\t2 -- Circle\n\t3 -- Right Triangle\n";
    cin >>  v;
    if (v == 1) {
	cout << "Enter the side for a Square:\n";
	cin >> n;
	if (n < 0) 
		cout << "Incorrect Value!\n";
	else
		cout << "Area of the Square is " << n*n << endl;
    }
    else if (v == 2) {
	cout << "Enter the radius for a Circle:\n";
	cin >> n;
	if (n < 0) 
		cout << "Incorrect Value!\n";
	else
		cout << "Area of the Circle is " << M_PI*n*n << endl;
    }
    else if (v == 3) { 
	cout << "Enter the side for a Right Triangle:\n";
	cin >> n;
	if (n < 0) 
		cout << "Incorrect Value!\n";
	else
		cout << "Area of the Right Triangle is " << 0.5*n*n << endl;
    }
    else
        cout << "Invalid Choice of Object!\n";
	
    return 0;
}
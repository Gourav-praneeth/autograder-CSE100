#include <iostream>
#include <cstdlib> // Required for system()
using namespace std;

int main() {
    string v1, v2, v3, v4, v5, v6, v7;
    cout << "Name of the instructor : ";
    cin >>  v1;
    cout << "Name of the student : ";
    cin >>  v2;
    cout << "Choice of food : ";
    cin >> v3;
    cout << "A number between 100 and 110 : ";
    cin >>  v4;
    cout << "An adjective : ";
    cin >>  v5;
    cout << "A color : ";
    cin >> v6;
    cout << "An animal : ";
    cin >>  v7;
    cout << endl; 
    
    cout << "Dear Instructor "<< v1 << "," << endl << endl; 
    cout << "I am sorry that I am unable to turn in my homework at this time. First, I ate a rotten " << v3;
    cout << ", which made me turn " << v6 << " and extremely ill. I come down with a fever of " << v4;
    cout << ". Next, my " << v5 << " pet " << v7 << " must have smelled the remains of the " << v3;
    cout << " on my homework, because he ate it. I am currently rewriting my homework and hope you will accept it here." << endl << endl; 
    cout << "Sincerely,\n" << v2; 
	
    return 0;
}
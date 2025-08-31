#include <iostream>
using namespace std;

int main(){
    int length, width;
    // 1. Declare variables
    int surfaceArea, smallBrownies, largeBrownies;

    // 2. Get user input
    cout << "Enter the length of the baking pan (in inches): ";
    cin >> length;
    cout << "Enter the width off the baking pan (in inches): ";
    cin >> width;

    // 3. Compute surface area
    surfaceArea = length * width;

    // 4. Compute number of brownies
    smallBrownies = surfaceArea;  // 1x1 brownies
    largeBrownies = surfaceArea / 4;  // 2x2 brownies

    // 5. Display results
    cout << "A " << length << " X " << width << " inch pan can hold " << smallBrownies << " small brownies or " << largeBrownies << " large brownies." << endl;

    return 0;
}
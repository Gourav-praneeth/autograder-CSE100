
#include <iostream>
#include <iomanip>

using namespace std;

int main()
{
    int cityNumber, population, rounded; //Declare variables
    const int MAX_CITIES = 1000; //Maximum amount of cities (cityArray elements)
    int cityArray [MAX_CITIES]; //Define array 

    cout << "Enter the number of cities: ";
    cin >> cityNumber;  //Gain input for number of array elements

    if (cityNumber <= 0) 
    {
    cout << "Invalid number of cities!";
    return 0;
    }
    
    for (int i = 0; i < cityNumber; i++) // Loop for entering the rounded population total into each city
    {
        int attempts = 0;
        while (attempts < 3) //Input validation (exit program if three invalid entries are made)
        {
            cout << "Enter the population for city "<<i + 1<<": ";
            cin >> population;

            if (population < 0)
            {
                cout << "Invalid population!\n";
                attempts++;
            }

            else if (population >= 0)
            {
                break;
            }

            if (attempts == 3) //Exit program after three unsuccessful attempts 
            {
                cout << "Too many invalid inputs. Exiting program.";
                return 0;
            }
        
        }

        rounded = ((population + 999) / 1000) * 1000; // First half of equation truncates to integer, then the second half turns back to thousand

        cityArray [i] = rounded; //Store the rounded population total in each element 
    }

    cout << "\nCity    Population Bar Graph";
    cout << "\n---------------------------------";
    for (int j = 0; j < cityNumber; j++) // Display text bar graph showing totals 
    {
            cout <<"\n "<< j + 1<<"       ";

        for (int k = 0; k < cityArray [j] / 1000; k++)
        {
            cout << "*";
        }
    }

    return 0; 
}


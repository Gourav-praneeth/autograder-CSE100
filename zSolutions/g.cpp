// #include <iostream>
// #include <string>
// #include <iomanip>
// using namespace std;

// // Function declarations
// double calculateAverage(double arr[], int size);
// double findMax(double arr[], int size);
// double findMin(double arr[], int size);

// // This function returns the number of days in a month using if-else
// int getDaysInMonth(string month) {
//     if (month == "January" || month == "March" || month == "May" ||
//         month == "July" || month == "August" || month == "October" || month == "December") {
//         return 31;
//     } else if (month == "April" || month == "June" || month == "September" || month == "November") {
//         return 30;
//     } else if (month == "February") {
//         return 28; // Not handling leap years for simplicity
//     } else {
//         return -1; // Invalid month
//     }
// }

// int main() {
//     const int NUM_DAYS = 7;
//     int days[NUM_DAYS];
//     double distances[NUM_DAYS];
//     string month;

//     cout << "Enter month name: ";
//     getline(cin, month);

//     int maxDay = getDaysInMonth(month);
//     if (maxDay == -1) {
//         cout << "Invalid month entered. Program exiting." << endl;
//         return 1;
//     }

//     for (int i = 0; i < NUM_DAYS; i++) {
//         cout << "\nEntry " << i + 1 << ":" << endl;

//         int day;
//         cout << "Enter day of the month (1-" << maxDay << "): ";
//         cin >> day;

//         while (day < 1 || day > maxDay) {
//             cout << "Invalid day. Please try again: ";
//             cin >> day;
//         }

//         double distance;
//         cout << "Enter commute distance (miles): ";
//         cin >> distance;

//         while (distance < 0) {
//             cout << "Distance cannot be negative. Enter again: ";
//             cin >> distance;
//         }

//         days[i] = day;
//         distances[i] = distance;
//     }

//     // Print Report
//     cout << fixed << setprecision(1);
//     cout << "\n=== Commute Report for " << month << " ===" << endl;
//     cout << "Day    Distance (miles)" << endl;
//     cout << "------------------------" << endl;

//     for (int i = 0; i < NUM_DAYS; i++) {
//         cout << days[i] << "      " << distances[i] << endl;
//     }

//     cout << "\nLongest commute: " << findMax(distances, NUM_DAYS) << " miles" << endl;
//     cout << "Shortest commute: " << findMin(distances, NUM_DAYS) << " miles" << endl;
//     cout << "Average commute: " << calculateAverage(distances, NUM_DAYS) << " miles" << endl;

//     return 0;
// }

// // Function to calculate average
// double calculateAverage(double arr[], int size) {
//     double sum = 0;
//     for (int i = 0; i < size; i++) {
//         sum += arr[i];
//     }
//     return sum / size;
// }

// // Function to find maximum
// double findMax(double arr[], int size) {
//     double max = arr[0];
//     for (int i = 1; i < size; i++) {
//         if (arr[i] > max) {
//             max = arr[i];
//         }
//     }
//     return max;
// }

// // Function to find minimum
// double findMin(double arr[], int size) {
//     double min = arr[0];
//     for (int i = 1; i < size; i++) {
//         if (arr[i] < min) {
//             min = arr[i];
//         }
//     }
//     return min;
// }

#include<iostream>
#include<iomanip>
using namespace std;


// Program to develop a system that generates bills for a cellular phone company.

int main()
{
    // declar variables 
    char customerT;
    int minuteused;
    string customerP;
    double costbase;
    double stage1R;
    double stage2R;
    double totalMinutes;
    double stage1cost;
    double stage2cost;
    double totalcost;
    double monthbase;
    char moreBills;
    int invalidcustomerAttempts =0;
    int invalidminuteAttempts =0;
    const double regular_basepay = 29.99;
    const double regular_stage1r = 0.55;
    const double regular_stage2r = 0.88;
    const double business_basepay = 99.99;
    const double business_stage1r = 0.99;
    const double business_stage2r = 0.88;
    // Display program name
    cout << "=============================================" << endl;
    cout <<  "\tPhone Bill Generation Software\t"<< endl;
    cout << "=============================================" << endl;
   
    // get customer input for customer type
do {
    // Validate customer type input
    while(true) {
    cout << "Please Enter the Customer Type (R for regular, B for business):";
    cin >> customerT;

     if (customerT == 'R' || customerT == 'r' || customerT == 'B'|| customerT == 'b') {
        break;
     }
     else {
        cout << "Invalid customer type! Please enter R, r for regular and B, b for business customers"<<endl;
        invalidcustomerAttempts++;
        
        // limit excess
        if (invalidcustomerAttempts >=3) {
        cout << "Too many invalid attempts, existing the program"<<endl;
        return 1;
        }
    }
}
 // get customer phone number
    cout << "Please Enter the Customer Phone Number:";
    cin >> customerP;

while (true) {
    // get customer input for minuites used
    cout << "Enter the phone usage in minutes:";
    cin >> minuteused;
      // Validate customer minutes used
    if (minuteused >= 0) {
        break;
    }
    else {
        cout << "Minutes used should be grater than zero"<<endl;
        invalidminuteAttempts++;  
    // limit excess
       if (invalidcustomerAttempts >= 3) {
        cout << "Too many invalid attempts, existing the program"<<endl;
        return 1;
       }
}
}    
    // display customer's input
    cout << "\tPhone Bill for : "<<customerP<< endl;
    cout << "\t============================"<< endl;
    cout <<"Total Minutes Used:"<<minuteused<<endl;
    
    // Calculate bill for business customer
    if (customerT == 'R'|| customerT == 'r') {
        monthbase = regular_basepay;
        stage1R = regular_stage1r;
        stage2R = regular_stage2r;
    }
    else {
        monthbase = business_basepay;
        stage1R = business_stage1r;
        stage2R = business_stage2r;
    }
    // Calculate cost
    if (minuteused<=200) {
        stage1cost = 0.0;
        stage2cost =0.0;
    }   
    else if (minuteused <=450) {
        stage1cost =(minuteused-200)*stage1R;
        stage2cost = 0.0;
    }
    else {
        stage1cost =250*stage1R;
        stage2cost = (minuteused-450)*stage2R;
    }
    totalcost= monthbase+stage1cost+stage2cost;           
    //    Output the bill
    cout <<"Monthly Base Payment:"<<monthbase<<endl;
    cout<<"Stage 1 cost: $"<<stage1cost<<endl;
    cout<<"Stage 2 cost: $"<<stage2cost<<endl;
    cout<<"--------------------------"<<endl;
    cout<<"Total cost : $ "<<totalcost<<endl;

    // Ask for more bill
    cout<<"More Bills? [Y/N]: ";
    cin >> moreBills;
}  while (moreBills == 'Y' || moreBills== 'y');


return 0;
}


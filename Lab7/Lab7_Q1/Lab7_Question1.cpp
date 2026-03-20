#include <iostream>
#include <iomanip>
#include <limits>
#include <string>
#include <algorithm>
#include <vector>
using namespace std;

string ordinalSuffix(int d) {
	if (d % 100 >= 11 && d % 100 <= 13) return "th";
	switch (d % 10) {
		case 1: return "st";
		case 2: return "nd";
		case 3: return "rd";
		default: return "th";
	}
}

int isMonth(string &s) {
	string month_array[] = {"january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"};
	int j;
	for (j = 0; j < 12; j++) {
		if(s == month_array[j])
			return(j);
	}
	return(j);
}


int main() {
	const int N = 7;
	string month, s;
	int dates[N], index;
	double snowInches[N];
	int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	bool ok;

	int attempt = 0;
	while (attempt < 3) {
		cout << "Enter the month name: ";
		cin >> month;
		s = month;
		transform(s.begin(), s.end(), s.begin(), ::tolower);
		index = isMonth(s);
		if (index != 12) break; 
		else {
			attempt++;
			cout << "Invalid month!\n";
		}
	}

	if (attempt == 3) {
		cout << "Exceeded the number of Invalid Attempts!\n";
		return(0);
	}

	for (int i = 0; i < N; ++i) {
		int attempts = 0;
		while (attempts < 3) {
			cout << "Enter day of month and snowfall (inches) for entry " << (i + 1) << " (e.g., 12 8.750): ";
			int d; double s;
			if (cin >> d >> s) {
				ok = true;
				if (d < 1) { 
					cout << "Date must be non-negative!\n"; 
					ok = false;}
				if (i == 0 && d > days[index]-7) { 
					cout << "Range exceeds the days in the month!\n"; 
					ok = false;} 
				else if (d > days[index]) { 
					cout << "Date is larger than number of days in the month!\n"; 
					ok = false; }
				if (s < 0.0) { cout << "Invalid snowfall!\n"; ok = false; }
				if (i > 0 && d != dates[i - 1] + 1) {
					cout << "Dates must be strictly consecutive!\n";
					ok = false;
				}
			}
			if (ok) { dates[i] = d; snowInches[i] = s; break; }
			else {
				attempts++;
				continue;
			}
		}
		if (attempts == 3) {
			cout << "Exceeded the number of Invalid Attempts!\n";
			return 0;
		}
	}

	int maxIdx = 0, minIdx = 0;
	double sum = snowInches[0];
	for (int i = 1; i < N; ++i) {
		sum += snowInches[i];
		if (snowInches[i] > snowInches[maxIdx]) maxIdx = i;
		if (snowInches[i] < snowInches[minIdx]) minIdx = i;
	}
	double avg = sum / N;

	cout << fixed << setprecision(2);
	cout << "\nSnow report " << month << ' ' << dates[0] << " - " << dates[N - 1] << "\n";
	cout << "============\n";
	cout << "Date\tSnow Fall\n";
	for (int i = 0; i < N; ++i) {
		cout << "  " << dates[i] << "\t" << snowInches[i] << '\n';
	}
	cout << "============\n";
	cout << "Highest snow fall is " << snowInches[maxIdx] << " on "<< dates[maxIdx] << ordinalSuffix(dates[maxIdx]) << "\n";
	cout << "Lowest snow fall is " << snowInches[minIdx] << " on "<< dates[minIdx] << ordinalSuffix(dates[minIdx]) << "\n";
	cout << "The average snow fall is " << avg << "\n";

	return 0;
}

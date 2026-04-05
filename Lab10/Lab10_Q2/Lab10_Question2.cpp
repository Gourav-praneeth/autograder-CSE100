#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
using namespace std;

const int N_MONTHS = 4;
const int MAX_INVALID_PER_MONTH = 3;

struct MonthlyFinance {
    double housing;
    double food;
    double medical;
    double entertainment;
    double miscellaneous;

    MonthlyFinance()
        : housing(0.0), food(0.0), medical(0.0), entertainment(0.0),
          miscellaneous(0.0) {}

    MonthlyFinance(double h, double f, double med, double ent, double misc)
        : housing(h), food(f), medical(med), entertainment(ent), miscellaneous(misc) {}
};

void readInput(MonthlyFinance arr[], int size = 4);
MonthlyFinance compareToBudget(const MonthlyFinance months[],
                               const MonthlyFinance &budget, int size = 4);
void displayOutput(const MonthlyFinance &summary);

int main() {
    MonthlyFinance budget(1200.0, 300.0, 100.0, 150.0, 250.0);
    MonthlyFinance months[N_MONTHS];

    readInput(months, N_MONTHS);
    MonthlyFinance summary = compareToBudget(months, budget, N_MONTHS);
    displayOutput(summary);

    return 0;
}

void readInput(MonthlyFinance arr[], int size) {
    const char *labels[5] = {"Housing", "Food", "Medical", "Entertainment",
                             "Miscellaneous"};

    for (int m = 0; m < size; ++m) {
        cout << "--- Month " << (m + 1) << " ---\n";
        int invalidCount = 0;

        double *fields[5] = {&arr[m].housing, &arr[m].food, &arr[m].medical,
                             &arr[m].entertainment, &arr[m].miscellaneous};

        for (int i = 0; i < 5; ++i) {
            while (true) {
                cout << labels[i] << ": ";
                double v;
                if (cin >> v && v >= 0.0) {
                    *fields[i] = v;
                    break;
                }

                cout << "Invalid input! Expenses should be non-negative.\n";
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');

                if (++invalidCount >= MAX_INVALID_PER_MONTH) {
                    cout << "Too many Invalid Attempts!\n";
                    exit(0);
                }
            }
        }
        cout << "\n";
    }
}

MonthlyFinance compareToBudget(const MonthlyFinance months[],
                               const MonthlyFinance &budget, int size) {
    MonthlyFinance r;
    double sumH = 0, sumF = 0, sumM = 0, sumE = 0, sumX = 0;

    for (int m = 0; m < size; ++m) {
        sumH += months[m].housing;
        sumF += months[m].food;
        sumM += months[m].medical;
        sumE += months[m].entertainment;
        sumX += months[m].miscellaneous;
    }

    auto rd = [](double x) { return round(x * 100.0) / 100.0; };

    r.housing = rd(static_cast<double>(size) * budget.housing - sumH);
    r.food = rd(static_cast<double>(size) * budget.food - sumF);
    r.medical = rd(static_cast<double>(size) * budget.medical - sumM);
    r.entertainment =
        rd(static_cast<double>(size) * budget.entertainment - sumE);
    r.miscellaneous =
        rd(static_cast<double>(size) * budget.miscellaneous - sumX);

    return r;
}

void displayOutput(const MonthlyFinance &summary) {
    cout << fixed << setprecision(2);
    cout << "=== Four-month budget comparison ===\n\n";

    const char *names[5] = {"Housing", "Food", "Medical", "Entertainment",
                            "Miscellaneous"};
    const double diffs[5] = {summary.housing, summary.food, summary.medical,
                             summary.entertainment, summary.miscellaneous};
    const double eps = 1e-6;

    for (int i = 0; i < 5; ++i) {
        cout << names[i] << ": ";
        double d = diffs[i];
        if (d > eps) {
            cout << "Saved: $" << d << "\n";
        } else if (d < -eps) {
            cout << "Over expenditure: $" << (-d) << "\n";
        } else {
            cout << "On budget\n";
        }
    }
}
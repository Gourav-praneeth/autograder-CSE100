#include <iostream>
#include <iomanip>
#include <limits>
using namespace std;

static const int MAX_ATTEMPTS = 3;

bool readNonNegative(const string& prompt, double& value) {
    int attempts = 0;
    while (true) {
        cout << prompt;
        if (cin >> value && value >= 0.0) return true;

        cout << "Invalid input! Value should be non-negative.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (++attempts >= MAX_ATTEMPTS) {
            cout << "Too many invalid attempts!\n";
            return false;
        }
    }
}

bool readWithdrawalBounded(int month, double balanceAfterDeposit, double& withdrawal) {
    int attempts = 0;
    while (true) {
        cout << "Enter total withdrawals for month " << month << ": ";
        if (cin >> withdrawal && withdrawal >= 0.0 && withdrawal <= balanceAfterDeposit)
            return true;

        cout << "Withdrawal cannot be negative or exceed current balance!\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (++attempts >= MAX_ATTEMPTS) {
            cout << "Too many invalid attempts!\n";
            return false;
        }
    }
}

bool readDeposit(int month, double& deposit) {
    int attempts = 0;
    while (true) {
        cout << "Enter total deposits for month " << month << ": ";
        if (cin >> deposit && deposit >= 0.0) return true;

        cout << "Invalid input! Value should be non-negative.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        if (++attempts >= MAX_ATTEMPTS) {
            cout << "Too many invalid attempts!\n";
            return false;
        }
    }
}

double calculateMonthlyInterest(double annualRate, double startingBalance, double endingBalance) {
    double monthlyRate = annualRate / 12.0;
    double averageBalance = (startingBalance + endingBalance) / 2.0;
    return averageBalance * monthlyRate;
}

int main() {
    double startingBalance, annualRate;

    // Starting balance (≤3 invalid attempts)
    if (!readNonNegative("Enter starting balance: ", startingBalance)) return 0;

    // Annual interest rate (≤3 invalid attempts)
    // Expect decimal form, e.g., 0.05 for 5%
    if (!readNonNegative("Enter annual interest rate (as decimal, e.g., 0.05 for 5%): ", annualRate)) return 0;

    double balance = startingBalance;
    double totalDeposits = 0.0;
    double totalWithdrawals = 0.0;
    double totalInterest = 0.0;


    for (int month = 1; month <= 3; ++month) {
        double monthStart = balance;

        // Deposit (≤3 invalid attempts)
        double deposit = 0.0;
        if (!readDeposit(month, deposit)) return 0;
        balance += deposit;
        totalDeposits += deposit;

        // Withdrawal (≤3 invalid attempts, bounded by current balance)
        double withdrawal = 0.0;
        if (!readWithdrawalBounded(month, balance, withdrawal)) return 0;
        balance -= withdrawal;
        totalWithdrawals += withdrawal;

        // Interest
        double interest = calculateMonthlyInterest(annualRate, monthStart, balance);
        balance += interest;
        totalInterest += interest;
    }

    // Report
    cout << fixed << setprecision(2);
    cout << "\nSavings Account Report\n";
    cout << "----------------------\n";
    cout << "Starting Balance: $" << startingBalance << "\n";
    cout << "Total Deposits:   $" << totalDeposits << "\n";
    cout << "Total Withdrawals:$" << totalWithdrawals << "\n";
    cout << "Total Interest:   $" << totalInterest << "\n";
    cout << "Final Balance:    $" << balance << "\n";

    return 0;
}


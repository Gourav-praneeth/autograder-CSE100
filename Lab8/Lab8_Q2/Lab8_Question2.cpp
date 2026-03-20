#include <iostream>
using namespace std;

const int MAX = 101;
int grid[MAX][MAX];

bool isDescendingOrder(int m, int n) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n - 1; j++) {
            if (grid[i][j] < grid[i][j + 1]) return false;
        }
    }
    for (int j = 0; j < n; j++) {
        for (int i = 0; i < m - 1; i++) {
            if (grid[i][j] < grid[i + 1][j]) return false;
        }
    }
    return true;
}

void readMatrix(int m, int n) {
    for (int i = 0; i < m; i++) {
        cout << "Enter row " << (i + 1) << " of " << n << " integers: ";
        for (int j = 0; j < n; j++) {
            cin >> grid[i][j];
        }
    }
}

int main() {
    int m, n;
    int sizeAttempts = 0;

    while (true) {
        cout << "Enter number of rows (m) and columns (n): ";
        if (!(cin >> m >> n)) {
            return 0;
        }
        bool validRows = (m > 0 && m <= MAX);
        bool validCols = (n > 0 && n <= MAX);
        if (validRows && validCols) {
            break;
        }
        if (!validRows) cout << "Invalid number of rows" << endl;
        if (!validCols) cout << "Invalid number of columns" << endl;
        sizeAttempts++;
        if (sizeAttempts >= 3) {
            cout << "Too many Invalid Attempts!" << endl;
            return 0;
        }
    }

    readMatrix(m, n);
    if (!isDescendingOrder(m, n)) {
        cout << "Elements should be in descending order!" << endl;
        readMatrix(m, n);
        if (!isDescendingOrder(m, n)) {
            return 0;
        }
    }

    int count = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] < 0) count++;
        }
    }
    cout << "Number of negative numbers in the grid: " << count << endl;
    return 0;
}

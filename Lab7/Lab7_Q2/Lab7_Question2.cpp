#include <iostream>
using namespace std;

const int MAX_SIZE = 101;

int main() {
    int n;
    int attempts = 0;
    const int maxAttempts = 3;

    // Prompt for size with validation (up to 3 attempts)
    cout << "Enter the size n: ";
    while (cin >> n) {
        if (n > 0)
            break;
        attempts++;
        cout << "Size must be positive!" << endl;
        if (attempts >= maxAttempts) {
            return 0;
        }
        cout << "Enter the size n: ";
    }

    // Matrix of size (n+1) x (n+1); last row and column for sums
    int matrix[MAX_SIZE][MAX_SIZE] = {{0}};

    // Read n x n elements (store in rows 0..n-1, cols 0..n-1)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << "Enter the " << (i + 1) << " x " << (j + 1) << " element: ";
            cin >> matrix[i][j];
        }
    }

    // Row sums -> last column
    for (int i = 0; i < n; i++) {
        matrix[i][n] = 0;
        for (int j = 0; j < n; j++)
            matrix[i][n] += matrix[i][j];
    }

    // Column sums -> last row
    for (int j = 0; j < n; j++) {
        matrix[n][j] = 0;
        for (int i = 0; i < n; i++)
            matrix[n][j] += matrix[i][j];
    }

    // Total -> last row, last column
    matrix[n][n] = 0;
    for (int i = 0; i < n; i++)
        matrix[n][n] += matrix[i][n];

    // Validate: sum of last column = sum of last row = total
    int sumLastCol = 0, sumLastRow = 0;
    for (int i = 0; i < n; i++)
        sumLastCol += matrix[i][n];
    for (int j = 0; j < n; j++)
        sumLastRow += matrix[n][j];
    if (sumLastCol == sumLastRow && sumLastRow == matrix[n][n]) {
        cout << "Matrix computations Validated!" << endl;
    }

    // Display the (n+1) x (n+1) matrix
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= n; j++) {
            if (j > 0) cout << " ";
            cout << matrix[i][j];
        }
        cout << endl;
    }

    return 0;
}

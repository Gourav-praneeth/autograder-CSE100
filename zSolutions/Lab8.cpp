#include <iostream>
#include <string>

#include <algorithm>
#include <cctype>
#include <limits>
#include <cstdlib>
#include <ctime>

// -------- Prototypes --------
void runGame();
void printWelcomeAndMapping();
int  getPositiveInt(const std::string& prompt);
int  getPlayerChoiceOrQuit();                    // returns 0=Rock,1=Paper,2=Scissors; -1=quit sentinel
int  getComputerChoice();                        // uses rand() and a static array mapping
int  determineWinner(int player, int computer);  // returns 1=player win, 0=draw, -1=computer win
void playOneRound(int roundNumber, int& wins, int& losses, int& draws, std::vector<int>& perRoundOutcome);  // dynamic array storage: 1 win, 0 draw, -1 loss
void showRoundResult(int roundNumber, int player, int computer, int outcome);
void showFinalSummary(const std::vector<int>& outcomes, int wins, int losses, int draws);

// -------- Helpers (local) --------
static inline std::string toLower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c){ return static_cast<char>(std::tolower(c)); });
    return s;
}

static inline void clearCinLine() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

// -------- Main (ONLY declarations + call) --------
int main() {
    runGame();
    return 0;
}

// -------- Definitions --------
void runGame() {
    // Seed RNG here (kept out of main’s logic responsibilities)
    std::srand(static_cast<unsigned>(std::time(nullptr)));

    printWelcomeAndMapping();

    int initialRounds = getPositiveInt("How many rounds would you like to play initially? ");
    int targetRounds  = initialRounds;
    int currentRound  = 0;

    int wins = 0, losses = 0, draws = 0;          // tallies (updated by reference)
    std::vector<int> outcomes;                    // per-round results: 1=win, 0=draw, -1=loss

    bool keepPlaying = true;
    while (keepPlaying) {
        // If we've reached the target, offer extension before starting another round
        if (currentRound >= targetRounds) {
            std::cout << "\nYou set " << targetRounds << " round(s). Do you want to play more? (y/n): ";
            std::string ans; std::getline(std::cin, ans);
            ans = toLower(ans);
            if (!ans.empty() && ans[0] == 'y') {
                int more = getPositiveInt("How many additional rounds would you like to add? ");
                targetRounds += more;
            } else {
                break; // end game if no extension
            }
        }

        // Play one round; user may quit early via sentinel in the choice prompt
        playOneRound(currentRound + 1, wins, losses, draws, outcomes);
        // If player chose to quit, playOneRound pushes nothing and returns immediately
        if (outcomes.size() != static_cast<size_t>(currentRound + 1)) {
            // user quit early
            break;
        }

        currentRound++;

        // After each round, ask if they want to continue (even if rounds remain)
        std::cout << "Play again? (y to continue, n to stop): ";
        std::string again; std::getline(std::cin, again);
        again = toLower(again);
        if (again.empty() || again[0] != 'y') {
            keepPlaying = false;
        }
    }

    showFinalSummary(outcomes, wins, losses, draws);
}

void printWelcomeAndMapping() {
    std::cout << "================ Rock, Paper, Scissors ================\n"
              << "Rules:\n"
              << "  - Rock beats Scissors\n"
              << "  - Scissors beats Paper\n"
              << "  - Paper beats Rock\n"
              << "  - Same choice = Draw\n\n"
              << "INPUT MAPPING (case-insensitive):\n"
              << "  r / rock      -> Rock\n"
              << "  p / paper     -> Paper\n"
              << "  s / scissors  -> Scissors\n"
              << "  1             -> Rock\n"
              << "  2             -> Paper\n"
              << "  3             -> Scissors\n"
              << "  q             -> Quit immediately (sentinel)\n"
              << "=======================================================\n\n";
}

int getPositiveInt(const std::string& prompt) {
    while (true) {
        std::cout << prompt;
        std::string line;
        if (!std::getline(std::cin, line)) {
            // Hard input error
            std::cerr << "\nInput stream error. Terminating.\n";
            std::exit(1);
        }
        // trim spaces
        line.erase(line.begin(), std::find_if(line.begin(), line.end(), [](unsigned char c){return !std::isspace(c);} ));
        line.erase(std::find_if(line.rbegin(), line.rend(), [](unsigned char c){return !std::isspace(c);} ).base(), line.end());
        if (line.empty()) {
            std::cout << "Please enter a positive integer.\n";
            continue;
        }
        // numeric?
        bool numeric = std::all_of(line.begin(), line.end(), [](unsigned char c){ return std::isdigit(c); });
        if (!numeric) {
            std::cout << "Invalid input type. Please enter digits only (e.g., 3).\n";
            continue;
        }
        try {
            int value = std::stoi(line);
            if (value > 0) return value;
            std::cout << "Value must be a positive integer greater than 0.\n";
        } catch (...) {
            std::cout << "Number too large or invalid. Try again.\n";
        }
    }
}

// Returns 0=Rock, 1=Paper, 2=Scissors, or -1 if user entered sentinel to quit
int getPlayerChoiceOrQuit() {
    while (true) {
        std::cout << "Enter your choice (r/rock, p/paper, s/scissors, 1/2/3, or q to quit): ";
        std::string in;
        if (!std::getline(std::cin, in)) {
            std::cerr << "\nInput stream error. Terminating.\n";
            std::exit(1);
        }
        // normalize
        std::string s = toLower(in);
        // trim spaces
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char c){return !std::isspace(c);} ));
        s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char c){return !std::isspace(c);} ).base(), s.end());

        if (s.empty()) {
            std::cout << "No input detected. Please enter a valid choice.\n";
            continue;
        }
        if (s == "q" || s == "quit" || s == "exit") {
            return -1; // sentinel
        }
        if (s == "r" || s == "rock" || s == "1") return 0;
        if (s == "p" || s == "paper" || s == "2") return 1;
        if (s == "s" || s == "scissors" || s == "3") return 2;

        // Consider the case where user typed something like "rockk" or an integer word etc.
        std::cout << "Invalid input. Please enter r/p/s (or 1/2/3), or 'q' to quit.\n";
    }
}

// Uses rand() and a static array for mapping
int getComputerChoice() {
    static const char* CHOICES[3] = { "Rock", "Paper", "Scissors" }; // mapping array as required
    int idx = std::rand() % 3; // 0..2
    // CHOICES[idx] would be used for display; we return idx as the choice.
    (void)CHOICES; // suppress unused warning in case optimization removes usage elsewhere
    return idx;
}

// 1 = player win, 0 = draw, -1 = computer win
int determineWinner(int player, int computer) {
    if (player == computer) return 0;
    // Rock(0) beats Scissors(2); Paper(1) beats Rock(0); Scissors(2) beats Paper(1)
    if ((player == 0 && computer == 2) ||
        (player == 1 && computer == 0) ||
        (player == 2 && computer == 1)) {
        return 1;
    }
    return -1;
}

void playOneRound(int roundNumber,
                  int& wins, int& losses, int& draws,
                  std::vector<int>& perRoundOutcome) {
    static const char* CHOICES[3] = { "Rock", "Paper", "Scissors" };

    std::cout << "\n--- Round " << roundNumber << " ---\n";
    int player = getPlayerChoiceOrQuit();
    if (player == -1) {
        std::cout << "You chose to quit. Ending the game early.\n";
        return; // do not record an outcome for this round; caller will detect via size check
    }
    int computer = getComputerChoice();
    int outcome  = determineWinner(player, computer);

    // Update tallies via reference
    if (outcome == 1)      ++wins;
    else if (outcome == 0) ++draws;
    else                   ++losses;

    perRoundOutcome.push_back(outcome);

    showRoundResult(roundNumber, player, computer, outcome);

    (void)CHOICES; // CHOICES is used in showRoundResult; this keeps intent explicit
}

void showRoundResult(int roundNumber, int player, int computer, int outcome) {
    static const char* CHOICES[3] = { "Rock", "Paper", "Scissors" };

    std::cout << "Player chose   : " << CHOICES[player]   << "\n"
              << "Computer chose : " << CHOICES[computer] << "\n";

    if (outcome == 1)      std::cout << "Result: You win this round!\n";
    else if (outcome == 0) std::cout << "Result: It's a draw.\n";
    else                   std::cout << "Result: Computer wins this round.\n";
}

void showFinalSummary(const std::vector<int>& outcomes, int wins, int losses, int draws) {
    std::cout << "\n========== Final Score ==========\n"
              << " Wins : " << wins  << "\n"
              << " Losses: " << losses << "\n"
              << " Draws : " << draws << "\n"
              << "=================================\n";

    // Optional: show per-round outcome timeline from dynamic array
    if (!outcomes.empty()) {
        std::cout << "Per-round results (1=win, 0=draw, -1=loss):\n  ";
        for (size_t i = 0; i < outcomes.size(); ++i) {
            std::cout << outcomes[i];
            if (i + 1 < outcomes.size()) std::cout << ", ";
        }
        std::cout << "\n";
    }
    std::cout << "Thanks for playing!\n";
}

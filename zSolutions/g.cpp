/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cctype>
#include <string>
#include <vector>
using namespace std;

int rounds;                           // global variables
string weapon[] = {"Rock", "Paper", "Scissors"};// static weapon array
vector<int> roundtracker;                       // dynamic round tracker array
bool con = true;                                // exit status

void startGame(int&);                           // beginning message, get rounds
bool run();                                     // main game
void finalScore();                              // calc//print final score
void exit();                                    // exit message

int main(){
    startGame(rounds);
    while(run())                                //loop until quit status
        continue;
    exit();
    return 0;
}

void startGame(int& rounds){
    int tryc = 0;                               // input try count
    string in;
    
    
    while(tryc<3){
        if(tryc == 2)
            cout<<"One attempt left!"<<endl;
        cout<<"Enter the number of rounds you would like to play: ";
        cin>>in;
        cout<<endl;
        if(in[0]=='q'){
            con = false;
            break;
        }
        else if(in.size()<10){
            bool kill = false;
            for(int i = 0; i<in.size();i++){
                if(!isdigit(in[i])){
                kill = true;
                break;
                }
            }
            if(!kill){
                rounds = stoi(in);
                if(rounds<=0){
                    cout<<"Number must be larger than 0."<<endl;
                    tryc++;
                }
                else break;
            }
            else{
                tryc++;
                cout<<"Please enter a whole, non-negative number that is less than 1,000,000."<<endl;
            }
        }
        else{
            tryc++;
            cout<<"Entry too big. Please enter a whole, non-negative number that is less than 1,000,000."<<endl;
        }
    }
    if (tryc>=3)                                // quit status after 3 failed trys
        con = false;
}

bool run(){
    int tryc = 0;
    srand(time(0));
    string wi;                                  // weapon input buffer
    int uw;                                     // user weapon index
    int cw = rand() % 3;                        // computer weapon index
    char yes;

    if(con){                                    // check for start input failure
        while(tryc<3){
            if(tryc == 2)
                cout<<"One attempt left!"<<endl;
            cout<<"\nEnter your weapon (Rock, Paper, or Scissors): ";
            cin>>wi;
            cout<<endl;
            if(wi[0]=='q'){
                con = false;
                break;
            }
            for(int i = 0; i < wi.size(); i++){ // case standardize
                if(isalpha(wi[i]))
                    wi[i] = tolower(wi[i]);
            }
            if(wi!="rock" && wi!="paper" && wi!="scissors" && wi!="r" && wi!="p" && wi!="s" && wi!="1" && wi!="2" && wi!="3"){ // input filtering
                tryc++;
                cout<<"Please enter Rock, Paper, or Scissors"<<endl;
                continue;
            }
            if (wi == "rock" || wi =="r" || wi=="1")                   // user weapon index assignment
                uw = 0;
            if (wi == "paper" || wi =="p" || wi=="2")
                uw = 1;
            if (wi == "scissors" || wi =="s" || wi=="3")
                uw = 2;
            cout<<"Human picks: "<<weapon[uw]<<endl;
            cout<<"Computer picks: "<<weapon[cw]<<endl;
            if (uw == cw){                      // Draw handling. Tracker update
                cout<<"its a draw!"<<endl;
                roundtracker.push_back(0);
            }
            else{
                switch (uw){                    // Win/Loss handling. Tracker update
                    case 0:
                    if(cw == 1){
                        cout<<"Paper wraps Rock, The Computer Wins!"<<endl;
                        roundtracker.push_back(-1);
                    }
                    else{
                        cout<<"Rock breaks Scissors, The Human Wins!"<<endl;
                        roundtracker.push_back(1);
                    }
                    break;

                    case 1:
                    if(cw == 2){
                        cout<<"Scissors cut Paper, The Computer Wins!"<<endl;
                        roundtracker.push_back(-1);
                    }
                    else{
                        cout<<"Paper wraps Rock, The Human Wins!"<<endl;
                        roundtracker.push_back(1);
                    }
                    break;
                    
                    case 2:
                    if(cw == 0){
                        cout<<"Rock breaks Scissors, The Computer Wins!"<<endl;
                        roundtracker.push_back(-1);
                    }
                    else{
                        cout<<"Scissors cut Paper, The Human Wins!"<<endl;
                        roundtracker.push_back(1);
                    }
                    break;
                }
            }

            if(roundtracker.size()==rounds){    // round check
                cout<<"Keep going? (Y for yes, else quit): ";// continue check
                cin>>yes;
                cout<<endl;
                if(yes != 'y' && yes != 'Y'){
                    finalScore();
                    con = false;
                    break;
                }
                cout<<"\nAdd more rounds? (Y for yes, else quit): ";// add more rounds?
                cin>>yes;
                cout<<endl;
                if(yes=='y' ||yes=='Y'){
                    int trycc = 0;
                    string in;
                    int addrounds;
                    while(trycc<3){
                        if(trycc == 2)
                            cout<<"One attempt left!"<<endl;
                        cout<<"Enter the number of extra rounds you would like to play: ";
                        cin>>in;
                        cout<<endl;
                        if(in[0]=='q'){
                            con = false;
                            break;
                        }
                        else if(in.size()<10){
                            bool kill = false;
                            for(int i = 0; i<in.size();i++){
                                if(!isdigit(in[i])){
                                kill = true;
                                break;
                                }
                            }
                            if(!kill){
                                addrounds = stoi(in);
                                if(addrounds<=0){
                                    cout<<"Number must be larger than 0."<<endl;
                                    trycc++;
                                }
                                else {
                                    rounds +=addrounds;
                                    break;
                                }
                            }
                            else{
                                trycc++;
                                cout<<"Please enter a whole, non-negative number that is less than 1,000,000."<<endl;
                            }
                        }
                        else{
                            trycc++;
                            cout<<"Entry too big. Please enter a whole, non-negative number that is less than 1,000,000."<<endl;
                        }

                    }
                    if (trycc>=3)
                        con = false;
                }
                else {
                    con = false;
                    finalScore();
                }
            }
            else{
                cout<<"Keep going? (Y for yes, else quit): ";// continue check
                cin>>yes;
                cout<<endl;
                if(yes != 'y' && yes != 'Y'){
                    finalScore();
                    con = false;
                }
            }
            break;
        }
        if (tryc>=3)
            con = false;
    }
    return con;
}

void finalScore(){
    int wins = 0;
    int lose = 0;
    int draw = 0;
    int total = 0;
    for(int i = 0; i < roundtracker.size(); i++){
        total += roundtracker[i];               // for quick overall results calculation
        if(roundtracker[i]>0)
            wins++;
        else if(roundtracker[i]<0)
            lose++;
        else
            draw++;
    }
    cout<<"\n----Final Results----"<<endl;
    cout<<"Human Wins:     "<<wins<<endl;
    cout<<"Computer Wins:  "<<lose<<endl;
    cout<<"Draws:          "<<draw<<endl;
    cout<<"\nOverall Winner: ";
    if(total>0)
        cout<<"Human!"<<endl;
    else if(total<0)
        cout<<"Computer!"<<endl;
    else
        cout<<"Its a Draw!"<<endl;
}

void exit(){
    cout<<"\nSimulation has ended.\nThank you for playing!!!"<<endl;
}

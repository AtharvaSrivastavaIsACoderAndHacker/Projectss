#include<stdio.h>
#include<conio.h>
#include<stdlib.h>
#include<time.h>

static int score = 0;

void incrementOrDecrement(int x){
    switch (x){
    case 0:
        --score;
        break;
    case 1:
        ++score;
        break;
    }
}
int winLose(int x){
    switch (x){
    case 0:
        incrementOrDecrement(0);
        printf("Lose\n");
        break;
    case 1:
        incrementOrDecrement(1);
        printf("Win\n");
        break;
    }
    return 0;
}

int main(int argc, char const *argv[]){
    
    printf("Welcome To StonePaperSccissors In C !\n");
    printf("0 = Stone | 1 = Paper | 2 = Scissors | 10 = Exit The Game !\n");

    int startMsg;
    printf("ENTER 100 To Start !!!!! ");
    scanf("%d",&startMsg);
    if (startMsg!=100){
        return 0;
    }

    system("cls");

    srand(time(NULL));

    int playersTurn;
    int computersTurn;

    while(1){
        printf("Your Turn : ");
        scanf("%d",&playersTurn);

        switch (playersTurn){
        case 0:
            break;
        case 1:
            break;
        case 2:
            break;
        case 10:
            break;
        
        default:
            continue;
        }

        computersTurn = rand()%3;
        printf("Computer Chose : %d\n",computersTurn);

        if(playersTurn==computersTurn){
            printf("Draw\n");
        }
        else if((playersTurn==0 & computersTurn==1)||(playersTurn==1 & computersTurn==2)||(playersTurn==2 & computersTurn==0)){
            winLose(0);
        }
        else if((playersTurn==1 & computersTurn==0)||(playersTurn==2 & computersTurn==1)||(playersTurn==0 & computersTurn==2)){
            winLose(1);
        }
        else if(playersTurn==10){
            system("cls");            
            printf("Your Score Against Computer Is : %d\n",score);
            return 0;
        }

    }

    return 0;
}
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <cstdlib>
#include <unistd.h>

// Vending Machine starting variables
int total_price = 0;
int total_products = 0;
int received_money_amount = 0;
int change = 0;

int drink_stock[] = {10, 10, 5, 5};   // Coke, Fanta, Americano, Latte
int drink_price[] = {10, 13, 30, 35}; //prices of drinks
int snack_stock[] = {15, 10, 10}; //sunflower seed, bean, sour pork
int snack_price[] = {13, 20, 15}; //prices of snacks

// bills and coins variables in the machine and user input
int bill_types[] = {1000, 500, 100, 50, 20};
int bill_counts[5] = {1, 1, 3, 8, 15};
int coin_types[] = {10, 5, 1};
int coin_counts[3] = {200, 500, 1000};

int user_bill_input[5] = {0};
int user_coin_input[3] = {0}; 

int admin_bill_input[5] = {0};
int admin_coin_input[3] = {0};

char chosen_products[100][30]; // Array to store product names: 100 lists, 29 characters
int chosen_count = 0; // Number of products chosen

// function
int menu();
void finalizeTransaction();
void receivedMoney();
void admin();
void adminMenu();

int menu() {

    int choice_menu;
    printf("----------------Welcome!------------------\n");
    printf("1. Drinks\n2. Snacks\n3. Admin \n4. Exit\n");
    printf("Please choose the menu you want: ");
    scanf("%d", &choice_menu);

    return choice_menu;

} // end menu function

// Function to handle product selection
int choosingMenu() {

    int selectedMenu = menu();
    int drinkProduct, snackProduct;
    int coke_choice, fanta_choice, americano_choice, latte_choice;
    int sunflower_choice, bean_choice, sour_pork_choice;

    //drinks menu
    if (selectedMenu == 1) {

        //get money from user
        receivedMoney();

        while (1) {

            printf("----------------Drinks menu!------------------\n");
            printf("1. Coke 10 baht\n2. Fanta 13 baht\n3. Americano 30 baht\n4. Latte 35 baht\n5. Payment\n6. return to main menu\n");
            printf("Please choose a drink: ");
            scanf("%d", &drinkProduct);

            switch (drinkProduct) {

                case 1:

                    printf("----------------------------------\n");
                    printf("You selected Coke.\n");

                    if (drink_stock[0] > 0) {

                        printf("Coke is available.\n");
                        printf("Price: %d baht\n", drink_price[0]);
                        printf("Do you want to buy it? (1 for Yes, 0 for No): ");
                        scanf("%d", &coke_choice);

                        if (coke_choice == 1) {

                            total_price += drink_price[0];
                            drink_stock[0]--;
                            strcpy(chosen_products[chosen_count++], "Coke");
                            printf("You bought Coke. Total money: %d baht\n", total_price);
                            printf("Remaining Coke stock: %d\n", drink_stock[0]);
                            printf("Money left: %d baht\n", received_money_amount - total_price);
                            continue;

                        } //end if

                    } else {

                        printf("Coke is out of stock.\n");
                        continue;

                    } // end if
                    break;
                
                case 2:

                    printf("----------------------------------\n");
                    printf("You selected Fanta.\n");

                    if (drink_stock[1] > 0) {

                        printf("Fanta is available.\n");
                        printf("Price: %d baht\n", drink_price[1]);
                        printf("Do you want to buy it? (1 for Yes, 0 for No): ");
                        scanf("%d", &fanta_choice);

                        if (fanta_choice == 1) {
                            total_price += drink_price[1];
                            drink_stock[1]--;
                            strcpy(chosen_products[chosen_count++], "Fanta");
                            printf("You bought Fanta. Total money: %d baht\n", total_price);
                            printf("Remaining Fanta stock: %d\n", drink_stock[1]);
                            printf("Money left: %d baht\n", received_money_amount - total_price);
                            continue;
                        } // end if

                    } else {

                        printf("Fanta is out of stock.\n");
                        continue;

                    } // end if
                    break;

                case 3:

                    printf("----------------------------------\n");
                    printf("You selected Americano.\n");

                    if (drink_stock[2] > 0) {

                        printf("Americano is available.\n");
                        printf("Price: %d baht\n", drink_price[2]);
                        printf("Do you want to buy it? (1 for Yes, 0 for No): ");
                        scanf("%d", &americano_choice);

                        if (americano_choice == 1) {

                            total_price += drink_price[2];
                            drink_stock[2]--;
                            strcpy(chosen_products[chosen_count++], "Americano");
                            printf("You bought Americano. Total money: %d baht\n", total_price);
                            printf("Remaining Americano stock: %d\n", drink_stock[2]);
                            printf("Money left: %d baht\n", received_money_amount - total_price);
                            continue;

                        } // end if

                    } else {

                        printf("Americano is out of stock.\n");
                        continue;

                    }// end if
                    break;

                case 4:

                    printf("----------------------------------\n");
                    printf("You selected Latte.\n");

                    if (drink_stock[3] > 0) {

                        printf("Latte is available.\n");
                        printf("Price: %d baht\n", drink_price[3]);
                        printf("Do you want to buy it? (1 for Yes, 0 for No): ");
                        scanf("%d", &latte_choice);

                        if (latte_choice == 1) {

                            total_price += drink_price[3];
                            drink_stock[3]--;
                            strcpy(chosen_products[chosen_count++], "Latte");
                            printf("You bought Latte. Total money: %d baht\n", total_price);
                            printf("Remaining Latte stock: %d\n", drink_stock[3]);
                            printf("Money left: %d baht\n", received_money_amount - total_price);
                            continue;

                        } // end if

                    } else {

                        printf("Latte is out of stock.\n");
                        continue;

                    } // end if
                    break;
                case 5:

                    finalizeTransaction();
                    return 4; // Exit the program

                case 6:

                    printf("Returning to main menu.\n");
                    return 0; // Return to main menu

                default:

                    printf("Invalid drink selection.\n");
                    continue;

            } //end switch
            break;
        } // end while
    } //end if

    // Snacks menu
    if (selectedMenu == 2) {

        //get money from user
        receivedMoney();

        while (1) {

            printf("----------------Snacks menu!------------------\n");
            printf("1. Sunflower seed 13 baht\n2. Bean 20 baht\n3. Sour pork 15 baht\n4. Payment\n5. return to main menu\n");
            printf("Please choose a snack: ");
            scanf("%d", &snackProduct);

            switch (snackProduct) {
                case 1:

                    printf("----------------------------------\n");
                    printf("You selected Sunflower seed.\n");

                    if (snack_stock[0] > 0) {

                        printf("Sunflower seed is available.\n");
                        printf("Price: %d baht\n", snack_price[0]);
                        printf("Do you want to buy it? (1 for Yes, 0 for No): ");
                        scanf("%d", &sunflower_choice);
                        if (sunflower_choice == 1) {
                            total_price += snack_price[0];
                            snack_stock[0]--;
                            strcpy(chosen_products[chosen_count++], "Sunflower seed");
                            printf("You bought Sunflower seed. Total money: %d baht\n", total_price);
                            printf("Remaining Sunflower seed stock: %d\n", snack_stock[0]);
                            printf("Money left: %d baht\n", received_money_amount - total_price);
                            continue;
                        } //end if

                    } else {
                        printf("Sunflower seed is out of stock.\n");
                        continue;
                    } //end if
                    break;

                case 2:

                    printf("----------------------------------\n");
                    printf("You selected Bean.\n");

                    if (snack_stock[1] > 0) {

                        printf("Bean is available.\n");
                        printf("Price: %d baht\n", snack_price[1]);
                        printf("Do you want to buy it? (1 for Yes, 0 for No): ");
                        scanf("%d", &bean_choice);

                        if (bean_choice == 1) {
                            total_price += snack_price[1];
                            snack_stock[1]--;
                            strcpy(chosen_products[chosen_count++], "Bean");
                            printf("You bought Bean. Total money: %d baht\n", total_price);
                            printf("Remaining Bean stock: %d\n", snack_stock[1]);
                            printf("Money left: %d baht\n", received_money_amount - total_price);
                            continue;
                        }//end if

                    } else {

                        printf("Bean is out of stock.\n");
                        continue;

                    }//end if
                    break;
                
                case 3:
                    
                    printf("----------------------------------\n");
                    printf("You selected Sour pork.\n");

                    if (snack_stock[2] > 0) {

                        printf("Sour pork is available.\n");
                        printf("Price: %d baht\n", snack_price[2]);
                        printf("Do you want to buy it? (1 for Yes, 0 for No): ");
                        scanf("%d", &sour_pork_choice);

                        if (sour_pork_choice == 1) {

                            total_price += snack_price[2];
                            snack_stock[2]--;
                            strcpy(chosen_products[chosen_count++], "Sour pork");
                            printf("You bought Sour pork. Total money: %d baht\n", total_price);
                            printf("Remaining Sour pork stock: %d\n", snack_stock[2]);
                            printf("Money left: %d baht\n", received_money_amount - total_price);
                            continue;

                        }//end if

                    } else {

                        printf("Sour pork is out of stock.\n");
                        continue;

                    }//end if
                    break;

                case 4:
                    printf("Returning to main menu.\n");
                    break;

                case 5:
                    finalizeTransaction();
                    return 4; // Exit the program

                default:
                    printf("Invalid snack selection.\n");
                    continue;

            } // end switch
        }// end while
    } // end if

    if (selectedMenu == 3) {
        admin();
        return 3;
    } //end if

    if (selectedMenu == 4) {
        printf("Exiting the vending machine. Thank you!\n");
        return 4;
    } // end if

    return selectedMenu;
}// end choosingMenu

void admin() {
    char username[10];
    char password[20];
    int attemptLogin;

    printf("Enter your user name: ");
    scanf("%s", username);
    printf("Enter your password: ");
    scanf("%s", password);

    if (strcmp(username, "admin01") == 0 && strcmp(password, "asdfghjkl") == 0) {
        printf("\n-------------welcome, %s !-------------\n", username);

        adminMenu();

    } else if (strcmp(username, "admin02") == 0 && strcmp(password, "asdfghjkl") == 0) {
        printf("\n-------------welcome, %s !-------------\n", username);

        adminMenu();

    } else {
        printf("Invalid username and password! Please enter your information again.\n");
        printf("--------------------------------------------------------------------------------\n");
    } // end if

    if (attemptLogin == 5) {
        printf("Too many attempt. The program will terminate.");

    }
} // end admin

void adminMenu() {
    int choice_admin;
    int choice_money;
    int choice_product;
    int money_refill;
    int count;

    printf("\n\t--- Admin's menu ---\n");
    printf("1. Money stock\n2. Product stock\n3. Main menu\n");
    scanf("%d", choice_admin);

    if(choice_admin == 1) {
        // Show remaining money in machine
        printf("\nMoney left in machine:\n\n");

        for (int i = 0; i < 5; i++) {
            printf("%d baht bills: %d\n", bill_types[i], bill_counts[i]);
        } // end for

        for (int i = 0; i < 3; i++) {
            printf("%d baht coins: %d\n", coin_types[i], coin_counts[i]);
        }// end for

        printf("---------------------------------------------");

        printf("Do you want to refill the stock? (1 for Yes | 0 for No): ", choice_money);
        scanf("%d", choice_money);

        for (int i = 0; i < 5; i++) admin_bill_input[i] = 0;
        for (int i = 0; i < 3; i++) admin_coin_input[i] = 0;

        if( choice_money == 1) {
            printf("What type of money are you restocking?");
            printf("1. Bills\n2. Coins\n 3. Both");
            scanf("%d", money_refill);

            if (money_refill == 1 || money_refill == 3) {
                printf("Enter the number of bills you want to insert:\n");
                for (int i = 0; i < 5; i++) {
                    printf("%d baht: ", bill_types[i]);
                    scanf("%d", &count);
                    admin_bill_input[i] += count;
                    received_money_amount += count * bill_types[i];
                } // end for
            } // end if

            if (money_refill == 2 || money_refill == 3) {
                printf("Enter the number of coins you want to insert:\n");
                for (int i = 0; i < 3; i++) {
                    printf("%d baht: ", coin_types[i]);
                    scanf("%d", &count);
                    admin_coin_input[i] += count;
                    received_money_amount += count * coin_types[i];
                } // end for
            } // end if

            for (int i = 0; i < 5; i++) bill_counts[i] += admin_bill_input[i];
            for (int i = 0; i < 3; i++) coin_counts[i] += admin_bill_input[i];

            printf("---------------------------------------------------\n");
            
            for (int i = 0; i < 5; i++) {
                printf("%d baht bills: %d\n", bill_types[i], bill_counts[i]);
            } // end for

            for (int i = 0; i < 3; i++) {
                printf("%d baht coins: %d\n", coin_types[i], coin_counts[i]);
            }// end for
            
        } else {
            printf("Returning to Main menu for Admin.");
        }
    } else if (choice_admin == 2) {
        printf("\n---------Product stocks!--------\n");
        printf("----Drinks----\n");
        printf("Coke stocks: %d\n", drink_stock[0]);
        printf("Fanta stocks: %d\n", drink_stock[1]);
        printf("Americano stocks: %d\n", drink_stock[2]);
        printf("Latte stocks: %d\n", drink_stock[3]);

        printf("----Snacks----\n");
        printf("Sunflower seed stocks: %d\n", snack_stock[0]);
        printf("Bean stocks: %d\n", snack_stock[1]);
        printf("Sour pork stocks: %d\n", snack_stock[2]);

        printf("----------------------------------------------------\n");

        printf("Do you want to refill the stock? (1 for Yes | 0 for No): ", choice_product);

        if (choice_product == 1) {
            printf("Which items do you want to refill? \n");
            printf("1. Drinks\n2. Snacks\n3. Both\n");
            printf("Please choose: ");
            scanf("%d", &choice_product);

            if (choice_product == 1 || choice_product == 3) {
                printf("Enter the number of drinks you want to refill: \n");
                for (int i = 0; i < 4; i++) {
                    printf("%s stocks: ", (i == 0 ? "Coke" : (i == 1 ? "Fanta" : (i == 2 ? "Americano" : "Latte"))));
                    scanf("%d", &drink_stock[i]);
                } // end for
            } // end if

            if (choice_product == 2 || choice_product == 3) {
                printf("Enter the number of snacks you want to refill:\n");
                for (int i = 0; i < 3; i++) {
                    printf("%s stocks: ", (i == 0 ? "Sunflower seed" : (i == 1 ? "Bean" : "Sour pork")));
                    scanf("%d", &snack_stock[i]);
                } // end for
            } // end if

            printf("\nStocks have been refilled successfully!\n");
            printf("----------------------------------------------------\n");

            printf("\n---------Product stocks!--------\n");
            printf("----Drinks----\n");
            printf("Coke stocks: %d\n", drink_stock[0]);
            printf("Fanta stocks: %d\n", drink_stock[1]);
            printf("Americano stocks: %d\n", drink_stock[2]);
            printf("Latte stocks: %d\n", drink_stock[3]);

            printf("----Snacks----\n");
            printf("Sunflower seed stocks: %d\n", snack_stock[0]);
            printf("Bean stocks: %d\n", snack_stock[1]);
            printf("Sour pork stocks: %d\n", snack_stock[2]);
        } else {
            printf("\n\nReturn to main menu!");
        }

    } else {
        menu();
    }
}

//function for calculate change
void receivedMoney() {
    int count, choice;
    received_money_amount = 0; // Reset before every use

    for (int i = 0; i < 5; i++) user_bill_input[i] = 0;
    for (int i = 0; i < 3; i++) user_coin_input[i] = 0;

    printf("What type of money do you want to insert?\n");
    printf("1. Bills\n2. Coins\n3. Both\n");
    printf("Please choose: ");
    scanf("%d", &choice);

    if (choice == 1 || choice == 3) {
        printf("Enter the number of bills you want to insert:\n");
        for (int i = 0; i < 5; i++) {
            printf("%d baht: ", bill_types[i]);
            scanf("%d", &count);
            user_bill_input[i] += count;
            received_money_amount += count * bill_types[i];
        } // end for
    } // end if

    if (choice == 2 || choice == 3) {
        printf("Enter the number of coins you want to insert:\n");
        for (int i = 0; i < 3; i++) {
            printf("%d baht: ", coin_types[i]);
            scanf("%d", &count);
            user_coin_input[i] += count;
            received_money_amount += count * coin_types[i];
        } // end for
    } // end if

    printf("\nTotal money received: %d baht\n", received_money_amount);

    printf("Bills inserted:\n");
    for (int i = 0; i < 5; i++) {
        if (user_bill_input[i] > 0)
            printf("%d baht: %d\n", bill_types[i], user_bill_input[i]); // end if
    }// end for

    printf("Coins inserted:\n");
    for (int i = 0; i < 3; i++) {
        if (user_coin_input[i] > 0)
            printf("%d baht: %d\n", coin_types[i], user_coin_input[i]); // end if
    }// end for
}

void finalizeTransaction() {
    int change = received_money_amount - total_price;
    int remaining_change = change;
    int bills_given[5] = {0};
    int coins_given[3] = {0};

    // --- Print Product List ---
    printf("\n\t--- Product List ---\n");
    printf("Total price: %d baht\n", total_price);

    printf("-----------Chosen products------------\n");

    for (int i = 0; i < chosen_count; i++) {
        printf("%d. %s\n", i + 1, chosen_products[i]);
    } // end for

    if (chosen_count == 0) {
        printf("No products chosen yet.\n");
    } // end if

    printf("--------------------------------------\n");
    printf("Total products chosen: %d\n", chosen_count);
    printf("Total money received: %d baht\n", received_money_amount);
    printf("Change: %d baht\n", change);
    printf("--------------------------------------\n");

    //Change calculation section
    if (change < 0) {
        printf("Error: Not enough money received. Please insert more money.\n");
        // Reset
        total_price = 0;
        received_money_amount = 0;
        chosen_count = 0;
        return;
    } // end if

    printf("\n\t---- Dispensing change ----\n");

    // Dispense bills
    for (int i = 0; i < 5; i++) {
        while (remaining_change >= bill_types[i] && bill_counts[i] > 0) {
            remaining_change -= bill_types[i];
            bills_given[i]++;
            bill_counts[i]--;
        } // end while
    } // end for

    // Dispense coins
    for (int i = 0; i < 3; i++) {
        while (remaining_change >= coin_types[i] && coin_counts[i] > 0) {
            remaining_change -= coin_types[i];
            coins_given[i]++;
            coin_counts[i]--;
        } // end while
    } // end for

    if (remaining_change > 0) {
        printf("Error: Unable to give exact change for %d baht.\n", remaining_change);

        // Restore original stock
        for (int i = 0; i < 5; i++) bill_counts[i] += bills_given[i];
        for (int i = 0; i < 3; i++) coin_counts[i] += coins_given[i];

        // Reset
        total_price = 0;
        received_money_amount = 0;
        chosen_count = 0;
        return;
    }// end if

    // Show the change given
    printf("Change given to user:\n");
    for (int i = 0; i < 5; i++) {
        if (bills_given[i] > 0)
            printf("- %d x %d baht bill\n", bills_given[i], bill_types[i]); // end if
    }//end for

    for (int i = 0; i < 3; i++) {
        if (coins_given[i] > 0)
            printf("- %d x %d baht coin\n", coins_given[i], coin_types[i]); // end if
    } // end for

    // Add user’s inserted money to machine stock
    for (int i = 0; i < 5; i++) bill_counts[i] += user_bill_input[i];
    for (int i = 0; i < 3; i++) coin_counts[i] += user_coin_input[i];

    printf("Transaction complete. Thank you for using the vending machine!\n");
    printf("--------------------------------------\n");

    // Final Reset
    total_price = 0;
    received_money_amount = 0;
    chosen_count = 0;
} // end finalizeTransaction

// Main function
int main() {
    int selectedMenu;
    do {
        selectedMenu = choosingMenu();
    } while (selectedMenu != 4);
        printf("Exiting the program. Thank you!\n");
    //end do-while

    return 0;
}// end main

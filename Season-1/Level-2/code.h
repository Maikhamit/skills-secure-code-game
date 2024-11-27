// Welcome to Secure Code Game Season-1/Level-2!

// Follow the instructions below to get started:

// 1. Perform code review. Can you spot the bug? 
// 2. Run tests.c to test the functionality
// 3. Run hack.c and if passing then CONGRATS!
// 4. Compare your solution with solution.c

#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h> // For handling strtol errors

#define MAX_USERNAME_LEN 39
#define SETTINGS_COUNT 10
#define MAX_USERS 100
#define INVALID_USER_ID -1

// Internal counter of user accounts
unsigned long userid_next = 0;

// Structure representing a user account
typedef struct {
    bool isAdmin;
    unsigned long userid;
    char username[MAX_USERNAME_LEN + 1];
    long setting[SETTINGS_COUNT];
} user_account;

// Array to store active user accounts
user_account *accounts[MAX_USERS];

// Creates a new user account and returns its unique identifier
int create_user_account(bool isAdmin, const char *username) {
    if (userid_next >= MAX_USERS) {
        fprintf(stderr, "The maximum number of users has been exceeded\n");
        return INVALID_USER_ID;
    }

    if (username == NULL) {
        fprintf(stderr, "Username cannot be null\n");
        return INVALID_USER_ID;
    }

    if (strlen(username) > MAX_USERNAME_LEN) {
        fprintf(stderr, "The username is too long\n");
        return INVALID_USER_ID;
    }

    user_account *ua = malloc(sizeof(user_account));
    if (ua == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return INVALID_USER_ID;
    }

    ua->isAdmin = isAdmin;
    ua->userid = userid_next; // Assign current ID
    strncpy(ua->username, username, MAX_USERNAME_LEN);
    ua->username[MAX_USERNAME_LEN] = '\0'; // Ensure null termination
    memset(ua->setting, 0, sizeof(ua->setting));

    accounts[userid_next] = ua; // Store the new user in the correct slot
    return userid_next++;
}

// Frees memory allocated for a user account
void delete_user_account(int user_id) {
    if (user_id < 0 || user_id >= MAX_USERS || accounts[user_id] == NULL) {
        fprintf(stderr, "Invalid user ID\n");
        return;
    }

    free(accounts[user_id]);
    accounts[user_id] = NULL;
}

// Updates a setting for a specified user
bool update_setting(int user_id, const char *index, const char *value) {
    if (user_id < 0 || user_id >= MAX_USERS || accounts[user_id] == NULL) {
        fprintf(stderr, "Invalid user ID\n");
        return false;
    }

    char *endptr;
    errno = 0; // Reset errno before strtol
    long i = strtol(index, &endptr, 10);
    if (*endptr || errno == ERANGE || i < 0 || i >= SETTINGS_COUNT) {
        fprintf(stderr, "Invalid setting index\n");
        return false;
    }

    errno = 0; // Reset errno before strtol
    long v = strtol(value, &endptr, 10);
    if (*endptr || errno == ERANGE) {
        fprintf(stderr, "Invalid setting value\n");
        return false;
    }

    accounts[user_id]->setting[i] = v;
    return true;
}

// Returns whether the specified user is an admin
bool is_admin(int user_id) {
    if (user_id < 0 || user_id >= MAX_USERS || accounts[user_id] == NULL) {
        fprintf(stderr, "Invalid user ID\n");
        return false;
    }
    return accounts[user_id]->isAdmin;
}

// Returns the username of the specified user
const char *username(int user_id) {
    if (user_id < 0 || user_id >= MAX_USERS || accounts[user_id] == NULL) {
        fprintf(stderr, "Invalid user ID\n");
        return NULL;
    }
    return accounts[user_id]->username;
}

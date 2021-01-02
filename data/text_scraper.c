
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum ReadInfo {
    LINE_BUF_SIZE = 1024,
    NUM_LINES_PER_RECORD = 16,
    URL_RECORD_POS = 1,
    URL_POS_START = 20
};

int main(){

    FILE* f;
    errno_t err = fopen_s(&f, "beep.txt", "r");

    if(err != 0){
        return EXIT_FAILURE;
    }
    
    char* result = NULL;
    int ctr = 0;

    char buf[LINE_BUF_SIZE] = {'\0'};

    while ((result = fgets(buf, LINE_BUF_SIZE, f)) != NULL) {
        if(ctr % NUM_LINES_PER_RECORD == URL_RECORD_POS){
            *(buf+strlen(buf)-1) = '\0';
            printf("%s\n", buf+URL_POS_START);
        }
        ++ctr;
    }

    return EXIT_SUCCESS;
}
#include <stdio.h>
#include <stdlib.h> // Replace <malloc.h> with this line for atoi
#include <math.h>

int main(int argc, char *argv[]) {
    int i, j, k;
    int n;
    FILE *fp;
    float *q_list, **q_matrix;

    // Parse the first argument as the size of the matrix.
    n = atoi(argv[1]);

    // Allocate memory for q_list (upper triangle elements) and q_matrix.
    q_list = (float *)malloc(n * (n + 1) / 2 * sizeof(float));
    q_matrix = (float **)malloc(n * sizeof(float *));
    for(i = 0; i < n; i++){
        q_matrix[i] = (float *)malloc(n * sizeof(float));
    }

    // Read the upper triangle elements from the file specified in argv[2].
    fp = fopen(argv[2], "r");
    if(fp == NULL){
        printf("Failed to open input file.\n");
        return 1;
    }

    float value;
    int count = 0;
    while(fscanf(fp, "%f", &value) == 1 && count < n * (n + 1) / 2){
        q_list[count++] = value;
    }
    if(count != n * (n + 1) / 2){
        fclose(fp);
        printf("Input file is empty or doesn't contain enough data.\n");
        return 1;
    } else {
        fclose(fp);

        // Populate the upper and lower triangles of the symmetric matrix.
        
        int k = 0;
        for(int i = 0; i < n; i++){
            for(int j = i; j < n; j++, k++){
                q_matrix[i][j] = q_list[k];
            }    
          // Add this block to set diagonal elements to 0.0 
        }
        // Symmetrically copy the upper triangle to the lower triangle.
        for(i = 0; i < n; i++){
            q_matrix[i][i] = 0.0;
        }
        
        for(i = 0; i < n; i++){
            for(j = 0; j < i; j++){
                q_matrix[i][j] = q_matrix[j][i];
            }
	}

        // Write the symmetric matrix into "all_out.txt".
        FILE *out_file = fopen("all_contact.txt", "w");
        if(out_file == NULL){
            printf("Failed to open output file 'all_contact.txt'.\n");
            return 1;
        }

        for(i = 0; i < n; i++) {
            for(j = 0; j < n; j++) {
                fprintf(out_file, "%.2f ", q_matrix[i][j]);
            }
            fprintf(out_file, "\n"); // New line after each row
        }

        fclose(out_file); // Close the output file.

        // Free allocated memory.
        for(i = 0; i < n; i++) {
            free(q_matrix[i]);
        }
        free(q_matrix);
        free(q_list);
    }
    
    return 0;
}

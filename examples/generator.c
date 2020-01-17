/* Graph generator for the CLIQUE problem by
       Marcus Peinado
       Department of Computer Science
       Boston University
*/

/* Parameters of the graph */

#define prob 0.5  /* edge probability for the random part of the graph */
#define alpha 0.5 /* determines bits l of largest clique (l = n^alpha) */

#include <math.h>
#include <stdio.h>

#define TRUE 1
#define FALSE 0
#define AND &&
#define OR ||
#define NOT !
#define MOD %
#define BOOL char
#define randomNat(n) (random() MOD(n))

#define MAXLONG 0x7fffffff
extern long random();

#define MAX_NR_VERTICES 5000
#define MAX_NR_VERTICESdiv8 625

BOOL bitmap[MAX_NR_VERTICES][MAX_NR_VERTICESdiv8];
int nr_vert, nr_edges, cl_size, Clique[MAX_NR_VERTICES];
double p2;

char masks[8] = {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80};

double randomFloat() { return ((double)random() / (double)MAXLONG); }

BOOL get_edge(register int i, register int j) {
    register int byte, bit, mask;

    bit = 7 - (j & 0x00000007);
    byte = j >> 3;

    mask = masks[bit];
    return ((bitmap[i][byte] & mask) == mask);
}

void set_edge(register int i, register int j, BOOL x) {
    register int byte, bit, mask;

    bit = 7 - (j & 0x00000007);
    byte = j >> 3;

    mask = masks[bit];
    if (x == 1)
        bitmap[i][byte] |= mask;
    else
        bitmap[i][byte] &= ~mask;
}

int round_(int r, int q) {
    if ((r MOD q) == 0)
        return (r / q);
    else
        return (1 + r / q);
}

void write_graph_DIMACS(char *file) {
    char c;
    int i, j, line_length;
    BOOL tmp;
    FILE *fp;

    if ((fp = fopen(file, "w")) == NULL) {
        printf("ERROR: cannot open file\n");
        exit(10);
    }

    fprintf(fp, "c This graph contains a clique of bits %d\n", cl_size);
    fprintf(fp, "p edge %d %d\n", nr_vert, nr_edges);
    for (i = 1; i < nr_vert; i++) {
        for (j = 0; j < i; j++)
            if (get_edge(i, j))
                fprintf(fp, "e %d %d\n", i, j);
    }
    fclose(fp);
}

void make_random_set(int G[], int size) {
    int i, j;

    for (i = 0; i < nr_vert; i++)
        G[i] = 0;

    for (i = 1; i <= size; i++) {
        do {
            j = randomNat(nr_vert);
        } while (G[j] == 1);
        G[j] = 1;
    }
}

void empty_graph() {
    int i, j;

    for (i = 0; i < nr_vert; i++)
        for (j = 0; j < nr_vert; j++)
            set_edge(i, j, FALSE);
}

void complete_graph(int G[]) {
    int i, j;

    for (i = 1; i < nr_vert; i++)
        for (j = 0; j < i; j++)
            if ((G[i] == 1) && (G[j] == 1)) {
                set_edge(i, j, TRUE);
                set_edge(j, i, TRUE);
            }
    nr_edges = cl_size * (cl_size - 1) / 2;
}

void rand_graph() {
    int i, j, no;

    for (i = 0; i < nr_vert; i++)
        for (j = 0; j < i; j++)
            if ((Clique[i] == 0) AND(Clique[j] == 0))
                if (randomFloat() < prob) {
                    nr_edges++;
                    set_edge(i, j, TRUE);
                    set_edge(j, i, TRUE);
                } else {
                    set_edge(i, j, FALSE);
                    set_edge(j, i, FALSE);
                }
            else if (((Clique[i] == 1) AND(Clique[j] == 0)) OR((Clique[i] == 0) AND(Clique[j] == 1)))
                if (randomFloat() < p2) {
                    nr_edges++;
                    set_edge(i, j, TRUE);
                    set_edge(j, i, TRUE);
                } else {
                    set_edge(i, j, FALSE);
                    set_edge(j, i, FALSE);
                }
}

main(int argc, char *argv[]) {
    int i, j;

    srandom(time((char *)0));

    if (argc != 3) {
        printf("usage: %s file no_of_vertices\n", argv[0]);
        exit(10);
    }

    sscanf(argv[2], "%d", &nr_vert);

    cl_size = (int)pow((double)nr_vert, alpha);
    p2 = ((double)nr_vert * prob - (double)cl_size) / (double)(nr_vert - cl_size);

    make_random_set(Clique, cl_size);
    empty_graph();
    complete_graph(Clique);
    rand_graph();

    write_graph_DIMACS(argv[1]);
}

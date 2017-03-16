/*
 ============================================================================
 Name        : OpenMP_Fib.c
 Author      : Shayan Mukhtar
 Version     :
 Copyright   : Nothing to see
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

int main(int argc, char *argv[])
{
	int num_threads = 0;// = omp_get_num_threads();
	#pragma omp parallel
	{
		int thread_id = omp_get_thread_num();

		if (thread_id == 0)
		{
			num_threads = omp_get_num_threads();
		}
		#pragma omp barrier
		printf("Hello World from thread %d of %d\n",thread_id, num_threads);

	}     //omp parallel
	return(0);
}

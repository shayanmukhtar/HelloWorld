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

#define NUM_THREADS_TO_USE		4
#define DEFAULT_FIB_LENGTH		3

int Fibonacci(int sequenceLength);
int __kmp_omp_num_threads = NUM_THREADS_TO_USE;
int __kmp_debugging = 1;

int main(int argc, char *argv[])
{
	int fibLength = DEFAULT_FIB_LENGTH;
	if (argc > 1)
	{
		fibLength = atoi(argv[1]);
	}
	//test parallel threads are building with openMP
	int num_threads = 0;// = omp_get_num_threads();
	int fibonacciSequence;
	omp_set_num_threads(NUM_THREADS_TO_USE);
	#pragma omp parallel
	{
		#pragma omp single
		{
			fprintf( stderr, "Total Number of Shayan's Threads: %d ",omp_get_num_threads());
			fibonacciSequence = Fibonacci(fibLength);
		}
	}
	printf("Fibonacci returns %d\n", fibonacciSequence);
	return(0);
}

int Fibonacci(int sequenceLength)
{
	int returnValue, x, y;
	if (sequenceLength < 2)
	{
		returnValue = sequenceLength;
	}
	else
	{
#pragma omp task shared(x) firstprivate(sequenceLength)
		x = Fibonacci(sequenceLength - 1);
#pragma omp task shared(y) firstprivate(sequenceLength)
		y = Fibonacci(sequenceLength - 2);
#pragma omp taskwait
		returnValue = x + y;
	}
	return returnValue;
}

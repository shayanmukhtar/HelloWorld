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

int Fibonacci(int sequenceLength);

int main(int argc, char *argv[])
{
	//test parallel threads are building with openMP
	int num_threads = 0;// = omp_get_num_threads();
	int fibonacciSequence;
	#pragma omp parallel
	{
		int thread_id = omp_get_thread_num();

		if (thread_id == 0)
		{
			num_threads = omp_get_num_threads();
		}
		#pragma omp barrier
		printf("Hello World from thread %d of %d\n",thread_id, num_threads);



	fibonacciSequence = Fibonacci(10);
	}     //omp parallel
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
#pragma omp task shared(x)
		x = (sequenceLength - 1);
#pragma omp task shared(y)
		y = (sequenceLength - 2);
#pragma omp taskwait
		returnValue = x + y;
	}
	return returnValue;
}

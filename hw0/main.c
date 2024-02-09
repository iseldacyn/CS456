#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

char *decrypt( char *, int );

int main( int argv, char **argc )
{
	assert( argc[1] != NULL );
	FILE *input = fopen( argc[1], "r" );

	char curr;
	int len = 0;
	char *c = NULL;
	
	while ( (curr = fgetc(input)) != EOF )
	{
		len++;
		c = (char *)realloc( c, sizeof(char) * len );
		c[len-1] = curr;
	}

	char *m = decrypt( c, len );
	printf( "%s", m );

	return 0;
}

char *decrypt( char *cipher, int length )
{
	char *message = (char *)malloc( sizeof(char) * length );
	int n = 0;

	for ( int i = 0; i < length; i++ )
	{
		if ( (cipher[i] < 'A') || (cipher[i] > 'Z') )
		{
			message[i] = cipher[i];
			continue;
		}

		//				ABCDEFGHIJKLMNOPQRSTUVWXYZ
		char *alpha1 = "AlibnhsHIodLwgtaekSurpcmYf";
		char *alpha2 = "elumxgciIhftMNOpdsarnVWoYy";
		char *alpha3 = "glisbFoyInKLfeOcatkpUdmhYr";

		if ( n%3 == 0 )
			message[i] = alpha1[cipher[i]-'A'];
		else if ( n%3 == 1 )
			message[i] = alpha2[cipher[i]-'A'];
		else
			message[i] = alpha3[cipher[i]-'A'];

		if ( message[i] < 'a' )
			fprintf( stderr, "%d, %c\n", n%3, message[i] );

		n++;
	}

	return message;
}

#include <stdio.h>

namespace utils {
  COO load_double_embedding(const std::string& filename){
    FILE * pFile;
    long lSize;
    char * buffer;
    size_t result;

    pFile = fopen (filename , "rb" );
    if (pFile==NULL) {fputs ("File error",stderr); exit (1);}

    // obtain file size:
    fseek (pFile , 0 , SEEK_END);
    lSize = ftell (pFile);
    rewind (pFile);

    // allocate memory to contain the whole file:
    buffer = (char*) malloc (sizeof(char)*lSize);
    if (buffer == NULL) {fputs ("Memory error",stderr); exit (2);}

    // copy the file into the buffer:
    result = fread (buffer,1,lSize,pFile);
    if (result != lSize) {fputs ("Reading error",stderr); exit (3);}

    /* the whole file is now loaded in the memory buffer. */
    COO((COO_elem*)buffer,lSize);

    // terminate
    fclose (pFile);
    return 0;
  }
}

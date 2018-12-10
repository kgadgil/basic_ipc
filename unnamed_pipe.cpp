#include <unistd.h>
#include <random>
#include <iostream>
#include <string>
/* The index of the "read" end of the pipe */
#define READ 0

/* The index of the "write" end of the pipe */
#define WRITE 1

void gen_rand(){
  std::random_device rd;
  std::mt19937 mt(rd());
  std::uniform_real_distribution<double> dist(1.0, 10.0);
  for (int i=0; i<16; ++i)
    std::cout << dist(mt) << "\n";
}

int main () {

  int arr [3] = {1,2,3};
  int fd[2], bytesRead;
  int message;
  pipe ( fd ); //Create an unnamed pipe//
  
  if ( fork ( ) == 0 ) {
    //Child Writer
    close (fd[READ]); // Close unused end
    for(int i=0; i<3;i++){
      write (fd[WRITE], &arr[i], 1); // include NULL  
      std::cout << "wrote " << arr[i] << std::endl;
    }
    close (fd[WRITE]);  //Close used end
  } else {
    // Parent Reader
    close (fd[WRITE]); // Close unused end
    bytesRead = read ( fd[READ], &message, 100);
    printf ( "Parent: Read %d bytes from pipe: %d \n", bytesRead, message);
    close ( fd[READ]); // Close used end
  }
}

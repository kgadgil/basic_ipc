#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>

#include <sys/wait.h>
#include <unistd.h>

using namespace std;

int main()
{
    //const char * target= "./top_block.py";
    const char * target= "./pipe_filter_test1.py";

    enum PIPE_FILE_DESCRIPTERS {
        READ_FD = 0, WRITE_FD = 1
    };

    /* Make pipes */
    int parentToChild[2]; /* Parent to child pipe */
    if (pipe(parentToChild) < 0)
    {
        perror("Can't make pipe");
        exit(1);
    }
    int childToParent[2]; /* Child to parent pipe */
    if (pipe(childToParent) < 0)
    {
        perror("Can't make pipe");
        exit(1);
    }

    /* Create a child to run command. */
    pid_t pid = fork();
    switch (pid)
    {
        case -1:
            perror("Can't fork");
            exit(1);

        case 0: /* Child */
            close(parentToChild[WRITE_FD]);
            close(childToParent[READ_FD]);
            dup2(parentToChild[READ_FD], STDIN_FILENO);
            dup2(childToParent[WRITE_FD], STDOUT_FILENO);
            close(parentToChild[READ_FD]);
            close(childToParent[WRITE_FD]);
            execlp(target, target, (char *) NULL);
            perror("Can't execute target");
            exit(1);

        default: /* Parent */
            close(parentToChild[READ_FD]);
            close(childToParent[WRITE_FD]);
            cout << "Child " << pid << " process running..." << endl;
    }

    /* Read data from child */
    string dataReadFromChild;
    char ch;
    int rc;
    while ((rc = read(childToParent[READ_FD], &ch, 1)) != 0)
    {
        if (rc == -1) {
            if ((errno == EINTR) || (errno == EAGAIN)) {
                continue;
            }
            perror("read() failed");
            exit(-1);
        }
        dataReadFromChild += ch;
    }
    close(childToParent[READ_FD]);
    cout << "End of file reached..." << endl;
    cout << "Data received was (" << dataReadFromChild.size() << "):" << endl;
    cout << dataReadFromChild << endl;

    /* Write data to child */
    cout << "starting writing" << endl;
    const char bufferW[] = "{\"AElement\":\"Something\"}\0";
    while (true) {
        int rc = write(parentToChild[WRITE_FD], bufferW, sizeof(bufferW));
        if (rc == -1) {
            if ((errno == EINTR) || (errno == EAGAIN)) {
                continue;
            }
            perror("write() failed");
            exit(-1);
        }
        break;
    }
    close(parentToChild[WRITE_FD]);

    /* Wait for child to exit */
    int status;
    int retWait = waitpid(pid, &status, 0);
    cout << endl << "Child exit status is:  " << WEXITSTATUS(status) << endl << endl;
}

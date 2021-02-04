import sys
import os
import re
from datetime import date


def listTodos():
    '''
    Lists all todos in descending order of time of creation
    '''

    directory = os.path.join(os.getcwd(), 'todo.txt')
    try:
        with open(directory) as text_file:
            lines = text_file.readlines()
            for index in range(len(lines), 0, -1):
                # Iterate from end to start (latest first)
                print(f'[{index}]', lines[index-1], end='')
    except FileNotFoundError:
        # In case, file does not exist
        # No pending todos exist
        print('There are no pending todos!')
    except Exception as exc:
        print(f'Error: {str(exc)}')


def findline(string: str):
    '''
    Return the 1-based index of the line where the string is found
    in the todo.txt file. In case not found, returns 0. Else -1.
    '''

    directory = os.path.join(os.getcwd(), 'todo.txt')
    string = string+'\n'
    index: int = -1
    try:
        with open(directory, 'r') as text_file:
            # 
            lines = text_file.readlines()
            for current_line in lines:
                index += 1
                if current_line == string:
                    # Return 1-based index
                    return index+1
            # If not found
            return 0
    except FileNotFoundError:
        return -1
    except Exception as exc:
        print(f'Error: {str(exc)}')
        exit()


def addTodo(arg: str):
    '''
    Appends the Todo to todo.txt in the user's current working directory
    if not already added
    '''

    directory = os.path.join(os.getcwd(), 'todo.txt')
    try:
        # Search if already present
        # If not present, add todo
        if findline(arg) <= 0:
            with open(directory, 'a') as text_file:
                text_file.writelines(f'{arg}\n')
                print(f'Added todo: "{arg}"')
        else:
            print('Error: Todo Already Exists')
    except Exception as exc:
        print(f'Error: {str(exc)}')


def deleteTodo(arg: int):
    '''
    Deletes the {arg}th todo
    '''

    if arg <= 0:
        print(f'Error: todo #{arg} does not exist. Nothing deleted.')

    directory = os.path.join(os.getcwd(), 'todo.txt')
    try:
        # Read all lines
        initial_lines = open(directory, 'r').readlines()
        # Open todo.txt in write mode
        current_file = open(directory, 'w')

        if len(initial_lines) < arg:
            print(f'Error: todo #{arg} does not exist. Nothing deleted.')
        # Write all lines except the {arg}th line
        for index in range(1, len(initial_lines)+1):
            if index != arg:
                current_file.write(initial_lines[index-1])
        print(f'Deleted todo #{arg}')

    except FileNotFoundError:
        print('No Todo Found')
    except Exception as exc:
        print(f'Error: {str(exc)}')


def completeTodo(arg: int):
    '''
    Removes the todo from todo.txt and appends into
    the done.txt
    '''

    if arg <= 0:
        print(f'Error: todo #{arg} does not exist.')

    directory = os.path.join(os.getcwd(), 'todo.txt')
    done_dir = os.path.join(os.getcwd(), 'done.txt')

    try:
        # Delete the {arg}th line from todo.txt
        # And append into the done.txt

        initial_lines = open(directory, 'r').readlines()
        current_file = open(directory, 'w')
        done_file = open(done_dir, 'a')

        if len(initial_lines) < arg:
            print(f'Error: todo #{arg} does not exist.')

        for index in range(1, len(initial_lines)+1):
            if index != arg:
                current_file.write(initial_lines[index-1])
            else:
                done_file.write(f"x {date.today()} {initial_lines[index-1]}")
        print(f'Marked todo #{arg} as done.')

    except FileNotFoundError:
        print(f'Error: todo #{arg} does not exist.')
    except Exception as exc:
        print(f'Error: {str(exc)}')


def report():
    '''
    Prints the number of completed and pending todos
    '''

    directory = os.path.join(os.getcwd(), 'todo.txt')
    done_dir = os.path.join(os.getcwd(), 'done.txt')

    pending: int = 0
    completed: int = 0

    try:
        todos: list = open(directory, 'r').readlines()
        for line in todos:
            if line.strip() != '':
                # Ignore blank lines
                pending += 1
    except FileNotFoundError:
        pass  # Ignore if the file does not exists
    except Exception as exc:
        print(f"Error: {str(exc)}")

    try:
        done: list = open(done_dir, 'r').readlines()
        for line in done:
            # Format for completed todos
            # x yyyy-mm-dd todo
            if re.search('^x [0-2][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] *', line):
                completed += 1
    except FileNotFoundError:
        pass  # Ignore if the file does not exists
    except Exception as exc:
        print(f'Error: {str(exc)}')

    # Used two different error handling
    # to ignore the respective part
    # if the corresponding file does not exist
    print(f'{date.today()} Pending : {pending} Completed : {completed}')


usage = lambda : print('''Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics''')


mono_argument_functions = {
    'help': usage,
    'ls': listTodos,
    'report': report,
}

if __name__ == "__main__":

    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print(usage())

    elif sys.argv[1] in mono_argument_functions.keys():
        # help, ls, report
        mono_argument_functions[sys.argv[1]]()

    elif sys.argv[1] == 'add':
        if len(sys.argv) < 3:
            print('Error: Missing todo string. Nothing added!')
        else:
            addTodo(sys.argv[2])

    elif sys.argv[1] == 'done':
        if len(sys.argv) < 3:
            print('Error: Missing NUMBER for marking todo as done.')
        else:
            try:
                completeTodo(int(sys.argv[2]))
            except ValueError:
                print('Error: Invalid NUMBER for marking todo as done.')

    elif sys.argv[1] == 'del':
        if len(sys.argv) < 3:
            print('Error: Missing NUMBER for deleting todo.')
        else:
            try:
                deleteTodo(int(sys.argv[2]))
            except ValueError:
                print('Error: Invalid NUMBER for deleting todo.')

    else:
        print('Invalid Argument')
        usage()

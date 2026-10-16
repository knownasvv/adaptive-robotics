from test_cases import (
    test_step, 
    test_choose_action, 
    test_get_neighbors, 
    test_find_path,
    test_action_between,
    test_execute_path
)

if __name__ == '__main__':

    #               x
    #         0 1 2 3
    #       ┌─────────
    # y = 0 │ . . . .
    # y = 1 │ . R # .
    # y = 2 │ . . . .
    
    test_step()
    test_choose_action()
    test_get_neighbors()
    test_find_path()
    test_action_between()
    test_execute_path()
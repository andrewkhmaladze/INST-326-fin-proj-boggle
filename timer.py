from inputimeout import inputimeout, TimeoutOccurred
import time

def input_timer(prompt, timeout=60):
    print(prompt)
    start_time = time.time()
    responses = []

    while time.time() - start_time <= timeout:
        try:
            # get user input with a timeout
            user_input = inputimeout(prompt='', timeout=timeout - (time.time() - start_time))
            responses.append(user_input)
        except TimeoutOccurred:
            # break the loop when TimeoutOccurred exception is raised 
            print("\nout of time")
            break

    return responses


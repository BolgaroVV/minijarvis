from services import container
import time
from ai import call_function_by_ai

def main():
    # container.client.init()
    container.stt.start() 
    container.stt.listen(call_function_by_ai)



if __name__ == '__main__':
    main()
    while True:
        time.sleep(1)
    
    

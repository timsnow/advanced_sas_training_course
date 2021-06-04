import matplotlib.pyplot as plt
import numpy as np

def quick_function(something_to_print):
    print(something_to_print)

test_variable = 3
test_string = 'hello'
test_array = np.linspace(0, 100, 1000)

quick_function('thing')

plt.plot(test_array)

plt.show()
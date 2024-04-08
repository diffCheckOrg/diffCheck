import numpy as np
import matplotlib.pyplot as plt

def main():
    # open csv file
    time_data = np.genfromtxt('times.csv', delimiter=',', skip_header=1)
    error_data = np.genfromtxt('errors.csv', delimiter=',', skip_header=1)
    x = np.linspace(1, len(time_data), len(time_data))
    plt.plot(x, time_data)
    plt.xlabel('Iteration')
    plt.ylabel('Time [s]')
    plt.title('Time vs Iteration: additive 00')
    plt.legend(["FGR Feature Matching","FGR Correspondance","Ransac Correspondance","Ransac Feature Matching"])
    plt.show()


    plt.plot(x, error_data)
    plt.xlabel('Iteration')
    plt.ylabel('Mean error [mm]')
    plt.title('Error vs Iteration: additive 00')
    plt.legend(["FGR Feature Matching","FGR Correspondance","Ransac Correspondance","Ransac Feature Matching"])
    plt.show()


if __name__ == '__main__':
    main()
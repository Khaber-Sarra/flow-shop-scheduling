from multiprocessing.dummy import Pool as ThreadPool

def squareNumber(n,m):
    return n ** m

# function to be mapped over
def calculateParallel(numbers, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(squareNumber, [numbers,2])
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    squaredNumbers = calculateParallel(numbers, 4)
    print (squaredNumbers)
    
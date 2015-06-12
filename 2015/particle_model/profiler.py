'''
A file for easy profiling of main()
'''
import cProfile
import pstats
import main as mp
import sys

def main():
    name  = "main_profile_hrf"
    try:
        name = sys.argv[1]
    except:
        pass
    print("name is now", name)
    cProfile.run("mp.main()","profiling_data/main_profile_bin")
    stream = open(name,'w')
    stats = pstats.Stats("profiling_data/main_profile_bin",stream = stream)
    stats.sort_stats("cumulative")
    stats.print_stats()
    stream.close()

if __name__ == '__main__':
    main()
import services, sys,os

def main():
    args = sys.argv

    if args==[__file__.split(os.path.sep)[-1]]:
        services.generate_yesterday()
        return
    
    services.generate_day(args[1])
if __name__=="__main__":
    main()
    
    
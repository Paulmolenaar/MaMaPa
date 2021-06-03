from  code.classes.models import House, water 

if __name__ == "__main__":

    a = water.load_water('docs/wijk_2.csv')
    print(a[2].top_right)


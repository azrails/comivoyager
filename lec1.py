import click
from itertools import permutations
import matplotlib.pyplot as plt

def min(routs):
    m = 0
    for i in range(len(routs)):
        if routs[i] < routs[m]:
            m = i
    return m

def l2_distance(point_1, point_2):
    l = ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5
    return l

def print_route(m, points, n_p,  route_list, start, plot):
    print(f'{start} -> ',end='')
    for i in range(len(n_p[m])):
        print(f'{points[n_p[m][i]]}[{route_list[m][i]}]',end='')
        if i != len(n_p[m]) - 1:
            print(' -> ', end='')
    print(f' = {route_list[m][len(route_list[m]) - 1]}')
    if plot != None:
        p = []
        p.append(list(points.values())[0])
        for i in range(len(n_p[m])):
            p.append(points[n_p[m][i]])
        x,y = zip(*p)
        plt.plot(x,y)
        for i in range(len(n_p[m])):
            plt.annotate(n_p[m][i], points[n_p[m][i]])
        plt.xlabel('Ось X')
        plt.ylabel('Ось Y')
        plt.grid()
        plt.show()
    
def standart_route(points, plot):
    start = list(points.keys())[0]
    start = points[start]
    n_p = list(permutations(list(points.keys())[1:]))
    for i in range(len(n_p)):
        n_p[i] = list(n_p[i])
        n_p[i].append(list(points.keys())[0])
    route_list = []
    for i in range(len(n_p)):
        route_list.append([])
        for j in range(len(n_p[i])):
            if j == 0:
                route_list[i].append(l2_distance(start, points[n_p[i][j]]))
            else:
                route_list[i].append(l2_distance(points[n_p[i][j - 1]], points[n_p[i][j]]))
    routs = []
    for i in range(len(route_list)):
        sum = 0;
        for j in range(len(route_list[i])):
            sum += route_list[i][j]
            route_list[i][j] = sum
        routs.append(sum)
    m = min(routs)
    print_route(m, points, n_p, route_list, start, plot)

def check_file(file):
    try:
        with open(file) as f:
            points = {}
            for line in f.readlines():
                token = line.split(':')
                if token[1].find("\n") != -1:
                    token[1] = token[1][:token[1].find("\n")]
                token[1] = token[1][1:token[1].find(')')]
                token[1] = token[1].split(',')
                for i in range(2):
                    token[1][i] = int(token[1][i])
                points.update({token[0]:tuple(token[1])})
    except FileNotFoundError:
        print(f'No file with path: {file}')   
        exit()
    return points

@click.command()
@click.option('--algo', '-a', help='chose algo for solving problem')
@click.option('--file', '-f', help='path to file with points')
@click.option('--plot', '-p', help='draw plot')
def main(algo, file, plot):
    """
    Program for founding the shortest route between n specified points. 

    Chose algorithm for solve [--algo|-a]:                                                                                
        1) standart - brute force                                                            
        2) optimize - maybe in future
    
    Use data from file [--file|-f]                                              
    tip: "name":(x,y)\n
    """
    if file == None:
        points = {"Почтовое отделение": (0,2), "Ул. Грибоедова, 104/25": (2,5),\
                "Ул. Бейкер стрит, 221б": (5,2), "Ул. Большая Садовая, 302-бис": (6,6),\
                "Вечнозелёная Аллея, 742": (8,3)}
    else:
        points = check_file(file)
    if algo == "standart" or algo == None:
        standart_route(points, plot)
    else:
        print("Coming soon")
    
if __name__ == '__main__':
    main()
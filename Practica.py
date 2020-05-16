data = [(x, y) for x in [1, 2, 3] for y in [3, 1, 4] if x != y]

print(data)


for i in range(75, 150):
    print('ADD COLUMN campo_' + str(i) + ' TEXT', end=',')

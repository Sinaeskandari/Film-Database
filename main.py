def add_film(film_id, name, director, production_year, genre):
    is_id_unique(film_id, 'Film')
    film_file = open('Film.txt', 'r+')
    line_number = len(film_file.readlines()) + 1
    record = f'{line_number}-{film_id}/{name}/{director}/{production_year}/{genre}\n'
    check_if_record_exists('Film', record)
    film_file.write(record)
    film_file.close()


def add_artist(artist_id, name, age, artist_movies):
    is_artist_id_unique(artist_id)
    if is_films_existed(artist_movies.split(',')):
        artist_file = open('Artist.txt', 'r+')
        line_number = len(artist_file.readlines()) + 1
        record = f'{line_number}-{artist_id}/{name}/{age}/{artist_movies}\n'
        check_if_record_exists('Artist', record)
        artist_file.write(record)
        artist_file.close()
        add_index(artist_id, line_number)
    else:
        print('Films don\'t exist in the database.')


def check_if_record_exists(artist_or_film, record):
    file = open(f'{artist_or_film}.txt', 'r')
    for line in file.readlines():
        if line[line.index('-'):] == record[line.index('-'):]:
            file.close()
            raise RuntimeError('Record exists')


def is_id_unique(ID, artist_or_film):
    file = open(f'{artist_or_film}.txt', 'r')
    for line in file.readlines():
        line = line[line.index('-') + 1:].split('/')
        if line[0] == str(ID):
            raise RuntimeError('ID is not unique')


def is_artist_id_unique(ID):
    file = open('ArtistIDIndex.txt', 'r')
    lines = file.readlines()
    lines = [line.split() for line in lines]
    keys = [int(l[0]) for l in lines]
    index = binary_search(keys, 0, len(keys) - 1, ID)
    if index != -1:
        raise RuntimeError('ID is not unique')


def find_film_by_id(film_id):
    file = open('Film.txt', 'r')
    for line in file.readlines():
        line = line[line.index('-') + 1:].split('/')
        if line[0] == str(film_id):
            file.close()
            return '/'.join(line)
    file.close()
    return 'There is no film with this id.'


def find_film_by_name(name):
    file = open('Film.txt', 'r')
    for line in file.readlines():
        line = line.split('/')
        if name in line[1]:
            file.close()
            return '/'.join(line)
    file.close()
    return 'There is no film with this name.'


def remove_film(film_id):
    try:
        remove_film_from_artist(get_film_name(str(film_id)))
    except:
        pass
    finally:
        file = open('Film.txt', 'r')
        lines = file.readlines()
        file.close()
        file = open('Film.txt', 'w')
        i = 1
        for line in lines:
            change_num_line = line.split('-')
            line = line[line.index('-') + 1:].split('/')
            if line[0] != str(film_id):
                change_num_line[0] = str(i)
                file.write('-'.join(change_num_line))
                i += 1
        file.close()


def remove_artist(artist_id):
    index = get_record_by_index(artist_id)[1]
    file = open('Artist.txt', 'r')
    lines = file.readlines()
    file.close()
    lines.pop(index)
    index_file = open('ArtistIDIndex.txt', 'r')
    index_dict = {}
    for line in index_file.readlines():
        line = line.split()
        index_dict[line[0]] = line[1]
    index_dict[str(artist_id)] = -1
    index_file.close()
    line_num = 1
    lines_to_write = []
    for line in lines:
        line = line.split('-')
        line[0] = str(line_num)
        change_index_line = line[1].split('/')
        index_dict[change_index_line[0]] = str(line_num)
        line_num += 1
        line = '-'.join(line)
        lines_to_write.append(line)
    file = open('Artist.txt', 'w')
    for line in lines_to_write:
        file.write(line)
    file.close()
    index_file = open('ArtistIDIndex.txt', 'w')
    for ID in list(index_dict.items()):
        if ID[1] != -1:
            index_file.write(f'{ID[0]} {ID[1]}' + '\n')
    index_file.close()


def change_id(artist_or_movie, current_id, new_id):
    is_id_unique(new_id, f'{artist_or_movie}')
    file = open(f'{artist_or_movie}.txt', 'r')
    lines = file.readlines()
    file.close()
    file = open(f'{artist_or_movie}.txt', 'w')
    for line in lines:
        line = line.split('-')
        line[1] = line[1].split('/')
        if line[1][0] == str(current_id):
            line[1][0] = str(new_id)
        line[1] = '/'.join(line[1])
        a = '-'.join(line)
        file.write(a)


def change_artist_id(current_id, new_id):
    is_artist_id_unique(new_id)
    index = get_record_by_index(current_id)[1]
    file = open('Artist.txt', 'r')
    lines = file.readlines()
    file.close()
    line = lines[index]
    line = line.split('-')
    line[1] = line[1].split('/')
    line[1][0] = str(new_id)
    line[1] = '/'.join(line[1])
    lines[index] = '-'.join(line)
    file.close()
    file = open('Artist.txt', 'w')
    for l in lines:
        file.write(l)
    file.close()
    index_file = open('ArtistIDIndex.txt', 'r')
    lines = index_file.readlines()
    index_dict = {}
    for line in lines:
        line = line.split()
        index_dict[line[0]] = line[1]
    # index_dict[str(current_id)] = -1
    index_file.close()
    index_file = open('ArtistIDIndex.txt', 'w')
    line_num = 0
    for ID in list(index_dict.items()):
        if ID[0] != str(current_id):
            index_file.write(f'{ID[0]} {ID[1]}' + '\n')
        else:
            line_num = ID[1]
    index_file.close()
    add_index(new_id, line_num)


def change_artist_age(artist_id, new_age):
    file = open('Artist.txt', 'r')
    lines = file.readlines()
    file.close()
    file = open('Artist.txt', 'w')
    for line in lines:
        line = line.split('-')
        line[1] = line[1].split('/')
        if line[1][0] == str(artist_id):
            line[1][2] = str(new_age)
        line[1] = '/'.join(line[1])
        a = '-'.join(line)
        file.write(a)


def is_films_existed(name_list):
    file = open('Film.txt', 'r')
    lines = file.readlines()
    bool_set = set()
    for name in name_list:
        for line in lines:
            line = line.split('-')
            line[1] = line[1].split('/')
            if line[1][1] == name:
                bool_set.add(name)
    if len(bool_set) == len(name_list):
        return True
    return False


def remove_film_from_artist(name):
    file = open('Artist.txt', 'r')
    lines = file.readlines()
    file.close()
    file = open('Artist.txt', 'w')
    for line in lines:
        line = line.split('-')
        line[1] = line[1].split('/')
        movie_list = line[1][3].replace('\n', '').split(',')
        if name in movie_list:
            movie_list.remove(name)
        line[1][3] = ','.join(movie_list)
        line[1] = '/'.join(line[1])
        line = '-'.join(line)
        file.write(line + '\n')
    file.close()


def get_film_name(film_id):
    file = open('Film.txt', 'r')
    lines = file.readlines()
    for line in lines:
        line = line.split('-')
        line[1] = line[1].split('/')
        if line[1][0] == str(film_id):
            return line[1][1]


def change_film_name(current_name, name):
    change_film_name_artist_file(current_name, name)
    file = open('Film.txt', 'r')
    lines = file.readlines()
    file = open('Film.txt', 'w')
    for line in lines:
        line = line.split('-')
        line[1] = line[1].split('/')
        if line[1][1] == current_name:
            line[1][1] = name
        line[1] = '/'.join(line[1])
        line = '-'.join(line)
        file.write(line)


def change_film_name_artist_file(current_name, new_name):
    file = open('Artist.txt', 'r')
    lines = file.readlines()
    file.close()
    file = open('Artist.txt', 'w')
    for line in lines:
        line = line.split('-')
        line[1] = line[1].split('/')
        movie_list = line[1][3].replace('\n', '').split(',')
        if current_name in movie_list:
            movie_list[movie_list.index(current_name)] = new_name
        line[1][3] = ','.join(movie_list)
        line[1] = '/'.join(line[1])
        line = '-'.join(line)
        file.write(line + '\n')
    file.close()


def binary_search(arr, l, r, x):
    l = int(l)
    r = int(r)
    x = int(x)
    if r >= l:
        mid = l + (r - l) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binary_search(arr, l, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, r, x)
    else:
        return -1


def add_index(artist_id, line_num):
    file = open('ArtistIDIndex.txt', 'r')
    lines = file.readlines()
    lines = [line.split() for line in lines]
    lines.append([str(artist_id), str(line_num)])
    lines.sort()
    file.close()
    file = open('ArtistIDIndex.txt', 'w')
    for line in lines:
        file.write(' '.join(line) + '\n')
    file.close()


def get_record_by_index(artist_id):
    file = open('ArtistIDIndex.txt', 'r')
    lines = file.readlines()
    lines = [line.split() for line in lines]
    keys = [int(l[0]) for l in lines]
    index = binary_search(keys, 0, len(keys) - 1, artist_id)
    file.close()
    file = open('Artist.txt', 'r')
    rec = file.readlines()[int(lines[index][1]) - 1]
    return rec, int(lines[index][1]) - 1


def ui_add_film(req):
    # req = input()  # Add FilmID: 1123 , FilmName: The Salesman , DirectorName: Asghar Farhadi , ProductionYear: 2016 , Genre: Drama
    for i in ['Add ', 'FilmID: ', ' FilmName: ', ' DirectorName: ', ' ProductionYear: ', ' Genre: ']:
        req = req.replace(i, '')
    req_list = req.split(' ,')
    add_film(req_list[0], req_list[1], req_list[2], req_list[3], req_list[4])


def ui_add_artist(req):
    # req = input()  # Add ArtistID: 2243 , ArtistName: Shahab Hosseini , Age: 46 , ArtistFilms: The Salesman
    for i in ['Add ', 'ArtistID: ', ' ArtistName: ', ' Age: ', ' ArtistFilms: ']:
        req = req.replace(i, '')
    req_list = req.split(' ,')
    add_artist(req_list[0], req_list[1], req_list[2], req_list[3])


def ui_find_film_by_id(req):  # Find Film 1123 By FilmID
    req = req.replace('Find Film ', '')
    req = req.replace(' By FilmID', '')
    print(find_film_by_id(req))


def ui_find_film_by_name(req):  # Find Film Salesman By FilmName
    req = req.replace('Find Film ', '')
    req = req.replace(' By FilmName', '')
    print(find_film_by_name(req))


def ui_remove_artist(req):
    # Remove ArtistID ---
    req = req.replace('Remove ArtistID ', '')
    remove_artist(req)


def ui_remove_film(req):
    # Remove FilmID ---
    req = req.replace('Remove FilmID ', '')
    remove_film(int(req))


def ui_change_artist_id(req):
    req = req.replace('Update Artist ', '')
    req = req.replace(' Set ID to', '')
    req = req.split()
    change_artist_id(int(req[0]), int(req[1]))


def ui_change_artist_age(req):
    # Update Artist 2243 Set Age to 47
    req = req.replace('Update Artist ', '')
    req = req.replace(' Set Age to', '')
    req = req.split()
    change_artist_age(int(req[0]), int(req[1]))


def ui_change_film_id(req):
    # Update Film 2243 Set ID to 4721
    req = req.replace('Update Film ', '')
    req = req.replace(' Set ID to', '')
    req = req.split()
    change_id('Film', int(req[0]), int(req[1]))


def ui_change_film_name(req):
    # Update Film The Salesman Set Name to Forooshande
    req = req.replace('Update Film ', '')
    req = req.replace(' Set Name to ', '-')
    req = req.split('-')
    change_film_name(req[0], req[1])


def main():
    while True:
        req = input()
        if req.startswith('Add FilmID'):
            ui_add_film(req)
        if req.startswith('Add ArtistID'):
            ui_add_artist(req)
        if req.startswith('Find Film') and req.endswith('FilmID'):
            ui_find_film_by_id(req)
        if req.startswith('Find Film') and req.endswith('FilmName'):
            ui_find_film_by_name(req)
        if req.startswith('Remove FilmID'):
            ui_remove_film(req)
        if req.startswith('Remove ArtistID'):
            ui_remove_artist(req)
        if req.startswith('Update Artist') and 'Set ID' in req:
            ui_change_artist_id(req)
        if req.startswith('Update Artist') and 'Set Age' in req:
            ui_change_artist_age(req)
        if req.startswith('Update Film') and 'Set ID' in req:
            ui_change_film_id(req)
        if req.startswith('Update Film') and 'Set Name' in req:
            ui_change_film_name(req)
        if req == 'end':
            break


if __name__ == '__main__':
    main()

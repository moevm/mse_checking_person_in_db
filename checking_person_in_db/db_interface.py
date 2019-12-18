import _pickle
import os
import face_recognition
import re
from app.model import Persons


def init_database(path_to_train_dir='../resources/train/'):  # change path
    train_dir = os.listdir(path_to_train_dir)
    count_persons = len(train_dir)
    person_counter = 0
    train_dir = os.listdir(path_to_train_dir)
    print(f'\r0/{count_persons} of people have been processed (0.0%).', end='')

    for path_to_person_dir in train_dir:
        insert_person(path_to_person_dir, path_to_train_dir + path_to_person_dir)
        person_counter += 1
        print(f'{person_counter}/{count_persons} '
              f'of people have been processed ({person_counter / count_persons * 100: .0f}%).', end='')


def insert_person(name, path_to_person_dir):
    try:
        paths_to_person_imgs = os.listdir(path_to_person_dir)
    except FileNotFoundError:
        print(f'No such file or directory: {path_to_person_dir}')
        exit(0)

    persons = Persons.objects(name=name)
    encodings = _pickle.loads(persons[0].face_encodings) if persons else []

    for path_to_person_img in paths_to_person_imgs:
        face = face_recognition.load_image_file(
            path_to_person_dir + '/' + path_to_person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            encodings.append(face_enc)

    person = Persons(name=name, face_encodings=_pickle.dumps(encodings, protocol=2))
    person.save()
    print(f'{name} successfully added')


def delete_person(name='.*'):
    regex = re.compile(name)
    person = Persons.objects(name=regex)
    if person:
        person.delete()
        print(f'All {name}\'s data was deleted')
    else:
        print('No such person in bd')


def show_persons():
    names = [person.name for person in Persons.objects]
    if names:
        for name in sorted(names):
            print(name)
    else:
        print("No persons in db")
    return names


if __name__ == '__main__':
    # delete_person()
    show_persons()
    # insert_person('Morgan_Freeman', '../resources/train/Morgan_Freeman')
    # show_persons()
    # delete_person("Morgan_Freeman")
    # show_persons()
    # init_database('../resources/train/')
    # show_persons()
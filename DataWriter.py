import pickle

def load_from_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

def write_to_txt(filename, data):
    with open(filename, 'w') as file:
        for key in data:
            file.write(key + " :\n")
            for i, value in data[key].items():
                file.write("Level " + str(i) + " - " + str(value) + "\n")
            file.write("\n")

pickle_filename = "winning_data.pickle"
txt_filename = "data.txt"

data = load_from_pickle(pickle_filename)

write_to_txt(txt_filename, data)

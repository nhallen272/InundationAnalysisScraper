import shelve

def main():
    data = shelve.open("Inundation_python")
    # blank list to hold all the dictionaries
    data_list = []
    for key in data.keys():
        # this is where the data can somehow be plugged in to arcgis or another program
        # to access specific values, specify which ones i.e.
        print(data[key]['elevation_above_datum'])

        # or save the dict back into a list of them
        data_list.append(data[key])

main()

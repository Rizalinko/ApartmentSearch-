# Print 10 top options
def printOptions(apartments):

    count = 0
    for iaprt in range(len(apartments)):
        if count > 50:
            break
        if not apartments['option'][iaprt]:
            continue
        else:
            print('*' * 100)
            count += 1
        for key in apartments.keys():
            print(key, ':', apartments[key][iaprt])

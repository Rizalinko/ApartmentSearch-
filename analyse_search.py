# Print 10 top options
def PrintOptions(df, **kwargs):
    nopt = 100
    if kwargs['noptions'] != 'all':
        nopt = int(kwargs['noptions'])
    count = 0

    # apartments = df[(df.option.eq(True)) & (df.T_ks < 31)].sort_index(ascending=False)
    apartments = df[(df.option.eq(True)) & (df.T_ks < 40)].sort_index(ascending=True)

    # TodO: remove repetitions
    f = open('options', 'w+')
    count=0
    for iaprt in range(len(apartments))[::2]:
        if count > nopt:
            break

        print('*' * 100)
        f.write('\n')
        f.write('*' * 100)
        count += 1
        for key in apartments.keys():
            if key.count('total') == 0 and key.count('dectris') == 0 and key.count('option') ==0:
                value = apartments[key].values[iaprt]
                if isinstance(value, float):
                    value = '{} min'.format(int(round(value)))
                print(key, ':', value)
                f.write('\n {} : {}'.format(key, value))
    print('Total number of options', count)
    f.write('\n Total number of options {}'.format(count))
    f.close()
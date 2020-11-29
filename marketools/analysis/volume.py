

def mean_volume_on_date(volume_data, day, over_last=90):
    volume = volume_data[:day].tail(over_last)['Volume']
    output = volume.mean()
    return output

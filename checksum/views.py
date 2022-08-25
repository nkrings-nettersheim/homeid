from django.shortcuts import render
from .forms import HomeidForm

def homeid(request):
    if request.method == "POST":
        form = HomeidForm()
        request.session['homeid_start'] = str(request.POST['homeid'])
        #lowercase to uppercase
        homeid = change_to_uppercase(str(request.POST['homeid']))

        #replace O to 0
        homeid = homeid.replace("O", "0")

        request.session['homeid_changed'] = homeid

        # check length is 7
        length_status = check_length(homeid)
        if length_status:
            ...
        else:
            request.session['check_num_status'] = "Falsche Länge"
            return render(request, 'checksum/input.html', {'form': form, 'result': request.session})

        # check is alphanumeric
        alphanumeric_status = check_alphanumeric(homeid)
        if alphanumeric_status:
            ...
        else:
            request.session['check_num_status'] = "Ungültige Zeichen"
            return render(request, 'checksum/input.html', {'form': form, 'result': request.session})

        # check 'alter Standard'
        alter_standard_status = check_alter_standard(homeid)
        if alter_standard_status:
            request.session['check_num_status'] = "Home-ID 'Alter Standard'"
            return render(request, 'checksum/input.html', {'form': form, 'result': request.session})

        # check checksum of new Home ID
        homeid = homeid.replace("V", "A")
        homeid = homeid.replace("W", "E")
        homeid = homeid.replace("X", "I")
        homeid = homeid.replace("Y", "O")
        homeid = homeid.replace("Z", "U")
        request.session['check_num_status'] = check_check_number(homeid)

        return render(request, 'checksum/input.html', {'form': form, 'result': request.session})

    form = HomeidForm()
    return render(request, 'checksum/input.html', {'form': form})



def change_to_uppercase(homeid):
    homeid = homeid.upper()
    return homeid


def check_length(homeid):
    length = len(homeid)
    if length == 7:
        length_status = True
    else:
        length_status = False
    return length_status


def check_alphanumeric(homeid):
    alphanumeric_status = homeid.isalnum()
    return alphanumeric_status


def check_alter_standard(homeid):
    if homeid[0].isalpha():
        if homeid[1:7].isnumeric():
            alter_standard_status = True
        else:
            alter_standard_status = False
    else:
        alter_standard_status = False

    return alter_standard_status


def check_check_number(homeid):
    alpha_to_num = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "A": 10, "B": 11,
                    "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, "J": 19, "K": 20, "L": 21, "M": 22,
                    "N": 23, "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30, "V": 10, "W": 14, "X": 18,
                    "Y": 24, "Z": 30}

    if homeid[0].isnumeric():
        digit0 = int(homeid[0]) * 1
    else:
        digit0 = int(alpha_to_num[homeid[0]]) * 1

    if homeid[1].isnumeric():
        digit1 = int(homeid[1]) * 3
    else:
        digit1 = int(alpha_to_num[homeid[1]]) * 3

    if homeid[2].isnumeric():
        digit2 = int(homeid[2]) * 1
    else:
        digit2 = int(alpha_to_num[homeid[2]]) * 1

    if homeid[3].isnumeric():
        digit3 = int(homeid[3]) * 3
    else:
        digit3 = int(alpha_to_num[homeid[3]]) * 3

    if homeid[4].isnumeric():
        digit4 = int(homeid[4]) * 1
    else:
        digit4 = int(alpha_to_num[homeid[4]]) * 1

    if homeid[5].isnumeric():
        digit5 = int(homeid[5]) * 3
    else:
        digit5 = int(alpha_to_num[homeid[5]]) * 3

    digit_sum = digit0 + digit1 + digit2 + digit3 + digit4 + digit5

    while digit_sum > 30:
        digit_sum = digit_sum - 31

    check_num = ''
    for x in alpha_to_num:
        if alpha_to_num[x] == digit_sum:
            check_num = x

    if homeid[6] == check_num:
        check_num_status = "Gültige Home-ID"
    else:
        check_num_status = "!!! keine gültige Home-ID !!!"

    return check_num_status

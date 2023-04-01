from googletrans import Translator
import pyttsx3
import serial
import keyboard
import time
import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier
import math
import openpyxl

arduino = serial.Serial('com5', 9600)  # port com5 and baud rate 9600
packet = arduino.readline()  # read line of arduino variable
translator = Translator()  # initialize translator variable by assigning it the Translator() class
pd.options.mode.chained_assignment = None  # removes warning when working with slices of a dataframe


def calibrate(cthumb, cindex, cmiddle, cring, cpinky, maxvals, minvals):
    # arduino values range from 0 to 4095. This function converts it from 0 to 90
    # THUMB
    OldMax = maxvals[0]  # initialize old maximum with the maximum value of thumb
    OldMin = minvals[0]  # initialize old minimum with the minimum value of thumb
    NewMax = 90  # new maximum of range is 90
    NewMin = 0  # new minimum of range is 0
    OldValue = cthumb  # the real-time value of thumb resistance
    OldRange = (OldMax - OldMin)  # calculating the old range before calibration
    NewRange = (NewMax - NewMin)  # calculating the new range after calibration
    # formula for converting real-time thumb value to the range (0 to 90)
    nthumb = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    # if less than 0, output 0. If greater than 90, output 90.
    if nthumb < 0:
        nthumb = 0
    elif nthumb > 90:
        nthumb = 90

    # INDEX
    OldMax = maxvals[1]  # initialize old maximum with the maximum value of index
    OldMin = minvals[1]  # initialize old minimum with the minimum value of index
    NewMax = 90  # new maximum of range is 90
    NewMin = 0  # new minimum of range is 0
    OldValue = cindex    # the real-time value of index resistance
    OldRange = (OldMax - OldMin)  # calculating the old range before calibration
    NewRange = (NewMax - NewMin)  # calculating the new range after calibration
    # formula for converting real-time thumb value to the range (0 to 90)
    nindex = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    # if less than 0, output 0. If greater than 90, output 90.
    if nindex < 0:
        nindex = 0
    elif nindex > 90:
        nindex = 90

    # MIDDLE
    OldMax = maxvals[2]  # initialize old maximum with the maximum value of middle
    OldMin = minvals[2]  # initialize old minimum with the minimum value of middle
    NewMax = 90  # new maximum of range is 90
    NewMin = 0  # new minimum of range is 0
    OldValue = cmiddle  # the real-time value of middle resistance
    OldRange = (OldMax - OldMin)  # calculating the old range before calibration
    NewRange = (NewMax - NewMin)  # calculating the new range after calibration
    # formula for converting real-time thumb value to the range (0 to 90)
    nmiddle = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    # if less than 0, output 0. If greater than 90, output 90.
    if nmiddle < 0:
        nmiddle = 0
    elif nmiddle > 90:
        nmiddle = 90

    # RING
    OldMax = maxvals[3]  # initialize old maximum with the maximum value of ring
    OldMin = minvals[3]  # initialize old minimum with the minimum value of ring
    NewMax = 90  # new maximum of range is 90
    NewMin = 0  # new minimum of range is 0
    OldValue = cring  # the real-time value of ring resistance
    OldRange = (OldMax - OldMin)  # calculating the old range before calibration
    NewRange = (NewMax - NewMin)  # calculating the new range after calibration
    # formula for converting real-time ring value to the range (0 to 90)
    nring = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    # if less than 0, output 0. If greater than 90, output 90.
    if nring < 0:
        nring = 0
    elif nring > 90:
        nring = 90

    # PINKY
    OldMax = maxvals[4]  # initialize old maximum with the maximum value of pinky
    OldMin = minvals[4]  # initialize old minimum with the minimum value of pinky
    NewMax = 90  # new maximum of range is 90
    NewMin = 0  # new minimum of range is 0
    OldValue = cpinky  # the real-time value of pinky resistance
    OldRange = (OldMax - OldMin)  # calculating the old range before calibration
    NewRange = (NewMax - NewMin)  # calculating the new range after calibration
    # formula for converting real-time ring value to the range (0 to 90)
    npinky = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    # if less than 0, output 0. If greater than 90, output 90.
    if npinky < 0:
        npinky = 0
    elif npinky > 90:
        npinky = 90

    # return the calibrated values list after rounding the individual elements of the list
    return [round(nthumb), round(nindex), round(nmiddle), round(nring), round(npinky)];


def databasecheck(thumb_d, index_d, middle_d, ring_d, pinky_d, classifier_d):
    # create a dataframe out of the real-time values being passed to this function.
    check = pd.DataFrame(
        {'Thumb': [thumb_d], 'Index': [index_d], 'Middle': [middle_d], 'Ring': [ring_d], 'Pinky': [pinky_d]})
    word = classifier_d.predict(check)  # use the passed classifier parameter to check the dataframe for matches
    if word != 'Null':  # if returning value is not Null string
        t_end = time.time() + 0.1  # add 0.1 seconds delay
        while time.time() < t_end:  # loop until 0.1 seconds end
            packet = arduino.readline()  # read arduino during the 0.1 seconds delay

        #this part of the code will check to see if the sign is held for 0.5 seconds. Then it will output that word.
        t_end = time.time() + 0.5
        while time.time() < t_end:  # loop until sign is being performed for 0.5 seconds
            packet = arduino.readline()  # read the arduino line from serial port
            decoded_values = packet.decode('utf')  # decode using utf
            flex_sensors = decoded_values.split(',')  # split into a list using commas
            # flex_sensors list values range from 0 to 4095. We will calibrate it to 0 to 90
            # calibrate real-time vals of sensors to (0 to 90). int() converting elements of flex_sensors list to int
            # assign returning 5 element list to new variable after calibration has been done.
            new = calibrate(int(flex_sensors[0]), int(flex_sensors[1]), int(flex_sensors[2]), int(flex_sensors[3]),
                            int(flex_sensors[4]), closedhand_values, openhand_values)
            thumb_temp = new[0]  # initialize calibrated (0 to 90) thumb value to thumb var
            index_temp = new[1]  # initialize calibrated (0 to 90) index value to index var
            middle_temp = new[2]  # initialize calibrated (0 to 90) middle value to middle var
            ring_temp = new[3]  # initialize calibrated (0 to 90) ring value to ring var
            pinky_temp = new[4]  # initialize calibrated (0 to 90) pinky value to pinky var
            # create a dataframe out of the real-time values being passed to this function.
            check = pd.DataFrame(
                {'Thumb': [thumb_temp], 'Index': [index_temp], 'Middle': [middle_temp], 'Ring': [ring_temp],
                 'Pinky': [pinky_temp]})
            temp = classifier_d.predict(check)  # use the passed classifier parameter to check the dataframe for matches
            if temp != word:  # if the temp variable contains something other than word
                # if the user does another sign within the 0.5 seconds loop, output false.
                return False
        return word[0]  # return the word for speaking through speaker if it has been performed for 0.5seconds
    else:
        # if output is Null string from database, return false. As in- no signs are performed.
        return False


def translate_and_speak(text_t):  # pass text_t parameter to function
    # translate the text by specifying source english language and destination as entered by user. Convert to string
    translated_text_raw = str(translator.translate(text_t, src='en', dest=destination_lang))
    translated_text_by_comma = translated_text_raw.split(',')  # split translated string by commas
    translated_text = translated_text_by_comma[2].split('=')  # split translated string by =
    print(translated_text[1])  # print the translated text
    engine = pyttsx3.init()  # initialize the TTS engine
    engine.say(translated_text[1])  # say the translated text
    engine.runAndWait()  # wait after running the TTS engine
    t_end = time.time() + 0.7  # 0.7 seconds delay after speaking the text
    while time.time() < t_end:  # loop until 0.7 seconds ends
        packet = arduino.readline()  # read arduino lines during delay


def calibrate_open():
    # starting values for comparison
    thumb_open = 45
    index_open = 45
    middle_open = 45
    ring_open = 45
    pinky_open = 45
    ending_time = time.time() + 1  # loop for 1 seconds
    arduino.readline()
    while time.time() < ending_time:  # loop until 1 second is over
        packet = arduino.readline()  # read the arduino line from serial port
        decoded_values_closed = packet.decode('utf')  # decode using utf
        flex_sensors_closed = decoded_values_closed.split(',')   # split data from commas since serial data had commas
        temp_list = []  # initialize an empty list
        # append vals of flex_sensors_closed to temp_list after converting to int
        temp_list.append(int(flex_sensors_closed[0]))
        temp_list.append(int(flex_sensors_closed[1]))
        temp_list.append(int(flex_sensors_closed[2]))
        temp_list.append(int(flex_sensors_closed[3]))
        temp_list.append(int(flex_sensors_closed[4]))
        # assign integer temp list to flex_sensors_closed list
        flex_sensors_closed = temp_list
        if flex_sensors_closed[0] < thumb_open:  # if real-time thumb value is less than initialized thumb_open
            thumb_open = flex_sensors_closed[0]  # assign real-time val to thumb_open if real-time value is lower

        if flex_sensors_closed[1] < index_open:  # if real-time index value is less than initialized index_open
            index_open = flex_sensors_closed[1]  # assign real-time val to index_open if real-time value is lower

        if flex_sensors_closed[2] < middle_open:  # if real-time middle value is less than initialized middle_open
            middle_open = flex_sensors_closed[2]  # assign real-time val to middle_open if real-time value is lower

        if flex_sensors_closed[3] < ring_open:  # if real-time ring value is less than initialized ring_open
            ring_open = flex_sensors_closed[3]  # assign real-time val to ring_open if real-time value is lower

        if flex_sensors_closed[4] < pinky_open:  # if real-time pinky value is less than initialized pinky_open
            pinky_open = flex_sensors_closed[4]  # assign real-time val to pinky_open if real-time value is lower

        # print the real-time values of flex sensors
        print('Thumb:', flex_sensors_closed[0], ' ', 'Index:', flex_sensors_closed[1], ' ', 'Middle:',
              flex_sensors_closed[2], ' ', 'Ring:', flex_sensors_closed[3], ' ', 'Pinky:', flex_sensors_closed[4])
    # assign the lowest values of thumb,index,middle,ring and pinky finger to min_open list
    min_open = [thumb_open, index_open, middle_open, ring_open, pinky_open]
    # return the min_open list which contains the minimum resistance values of an open hand
    return min_open


def calibrate_closed():
    # starting values for comparison
    thumb_closed = 45
    index_closed = 45
    middle_closed = 45
    ring_closed = 45
    pinky_closed = 45
    ending_time = time.time() + 1  # loop for 1 seconds
    arduino.readline()
    while time.time() < ending_time:  # loop until 1 second is over
        packet1 = arduino.readline()  # read the arduino line from serial port
        decoded_values_closed = packet1.decode('utf')  # decode using utf
        flex_sensors_closed = decoded_values_closed.split(',')  # split data from commas since serial data had commas
        temp_list = []  # initialize an empty list
        # append vals of flex_sensors_closed to temp_list after converting to int
        temp_list.append(int(flex_sensors_closed[0]))
        temp_list.append(int(flex_sensors_closed[1]))
        temp_list.append(int(flex_sensors_closed[2]))
        temp_list.append(int(flex_sensors_closed[3]))
        temp_list.append(int(flex_sensors_closed[4]))
        # assign integer temp list to flex_sensors_closed list
        flex_sensors_closed = temp_list
        if flex_sensors_closed[0] > thumb_closed:  # if real-time thumb value is greater than initialized thumb_closed
            thumb_closed = flex_sensors_closed[0]  # assign real-time val to thumb_closed if real-time value is greater

        if flex_sensors_closed[1] > index_closed:  # if real-time index value is greater than initialized index_closed
            index_closed = flex_sensors_closed[1]  # assign real-time val to index_closed if real-time value is greater

        if flex_sensors_closed[2] > middle_closed:  # if real-time middle val is greater than initialized middle_closed
            middle_closed = flex_sensors_closed[2]  # assign real-time val to middle_closed if real-time val is greater

        if flex_sensors_closed[3] > ring_closed:  # if real-time ring val is greater than initialized ring_closed
            ring_closed = flex_sensors_closed[3]  # assign real-time val to ring_closed if real-time value is greater

        if flex_sensors_closed[4] > pinky_closed:  # if real-time pinky val is greater than initialized pinky_closed
            pinky_closed = flex_sensors_closed[4]  # assign real-time val to pinky_closed if real-time value is greater

        # print the real-time values of flex sensors
        print('Thumb:', flex_sensors_closed[0], ' ', 'Index:', flex_sensors_closed[1], ' ', 'Middle:',
              flex_sensors_closed[2], ' ', 'Ring:', flex_sensors_closed[3], ' ', 'Pinky:', flex_sensors_closed[4])
    # assign the greater values of thumb,index,middle,ring and pinky finger to max_closed list
    max_closed = [thumb_closed, index_closed, middle_closed, ring_closed, pinky_closed]
    # return the max_closed list which contains the minimum resistance values of a closed hand
    return max_closed


def record():
    print('reading database...')
    # read excelsheet of signs database. Assign columns to df var
    df = pd.read_excel('data.xlsx')
    # if no signs have previously been added to database
    if df.empty:
        # initialize n to 1.0 string so that it shows up in datasheet as the first sign
        n = '1.0'
        # make an empty dataframe with headers and add the value of n in the header
        # example Thumb1.0, Index1.0, Middle1.0, Ring1.0, Pinky1.0
        data = pd.DataFrame(
            {'Thumb' + n: [], 'Index' + n: [], 'Middle' + n: [], 'Ring' + n: [], 'Pinky' + n: [], 'Meaning' + n: []})
    else:
        shape = df.shape  # check the characteristics of the dataframe
        columns = shape[1]  # no.of columns is the 2nd element in the list of characteristics
        # +6 because there are 5 finger columns and 1 Meaning column per sign. n represents no.of signs in database
        # +1 to increment value of n so that new sign can be added. n represents no.of signs in database
        n = (columns / 6) + 1
        n = str(n)  # convert n to string
        # make a new dataframe with headers and add the value of n in the header signifying the number of latest sign
        # assuming 10 signs are in database. The new headers will be Thumb11.0, Index11.0 and so on for this new sign
        data = pd.DataFrame(
            {'Thumb' + n: [], 'Index' + n: [], 'Middle' + n: [], 'Ring' + n: [], 'Pinky' + n: [], 'Meaning' + n: []})
    gesturemeaning = input("Enter your gesture meaning: ")
    print('Do your gesture for 10 seconds. Press the r key to continue')
    print(' ')
    loop = True
    while loop:  # infinite loop until r key is pressed
        if keyboard.is_pressed('r'):
            loop = False
    print(' ')
    print('recording....')
    print(' ')
    t_end = time.time() + 2  # 2 second delay
    while time.time() < t_end:  # loop until 2 seconds are over
        packet = arduino.readline()  # read arduino during the 2-second delay
    t_end = time.time() + 10  # read flex sensor vals for 10s to fill the database with rows of data
    while time.time() < t_end:  # loop until 10 seconds are over
        packet_record = arduino.readline()  # read packets coming into arduino variable from serial port
        decoded_values_closed = packet_record.decode('utf')  # decode using utf
        flex_sensors = decoded_values_closed.split(',')  # split data from commas since serial data had commas
        # flex_sensors list values range from 0 to 4095. We will calibrate it to 0 to 90
        # calibrate real-time vals of sensors to (0 to 90). int() converting elements of flex_sensors list to int
        # assign returning 5 element list to new variable after calibration has been done.
        new_record_vals = calibrate(int(flex_sensors[0]), int(flex_sensors[1]), int(flex_sensors[2]),
                                    int(flex_sensors[3]),
                                    int(flex_sensors[4]), closedhand_values, openhand_values)
        thumb_record = new_record_vals[0]  # initialize calibrated (0 to 90) thumb value to thumb var
        index_record = new_record_vals[1]  # initialize calibrated (0 to 90) index value to index var
        middle_record = new_record_vals[2]  # initialize calibrated (0 to 90) middle value to middle var
        ring_record = new_record_vals[3]  # initialize calibrated (0 to 90) ring value to ring var
        pinky_record = new_record_vals[4]  # initialize calibrated (0 to 90) pinky value to pinky var
        print('Thumb:', thumb_record, ' ', 'Index:', index_record, ' ', 'Middle:', middle_record, ' ',
              'Ring:', ring_record, ' ', 'Pinky:', pinky_record)  # pint real-time values of the flex sensors.
        # make a new dataframe with the real-time values
        flex_dataframe = pd.DataFrame({'Thumb' + n: [thumb_record], 'Index' + n: [index_record],
                                       'Middle' + n: [middle_record], 'Ring' + n: [ring_record],
                                       'Pinky' + n: [pinky_record], 'Meaning' + n: [gesturemeaning]})
        # concatenate the real-time values
        data = pd.concat([data, flex_dataframe], ignore_index=True)
        # all real-time values for 10 seconds will be concatenated into a single dataframe
    print('reading database...')
    excelsheet = pd.read_excel('data.xlsx')  # read the signs database
    excelsheet = excelsheet.dropna()  # drop any NaN values
    print('database reading finished')
    print('')
    print('writing recorded sign to database...')
    entire_database = pd.concat([excelsheet, data], axis=1)  # concatenate recorded sign column to the signs database
    # send the entire dataset of signs with the new sign added to it, to the excel sheet of signs
    entire_database.to_excel('data.xlsx', index=False, header=True)
    print('writing to database finished.')
    print('preparing to train model....')
    # so far we have written to the .xlsx version of the database which is for user-readability
    # now we are going to write to the .csv file which is for python to use for machine learning (KNN algo)
    entire_database = entire_database.dropna()  # drop any NaN values
    shape = entire_database.shape  # get the characteristics of the signs database
    # n represents the number of signs in database
    if n != '1.0':  # if previous signs exist in the database
        columns = shape[1]  # no.of columns is the 2nd element in the list of characteristics
        # +6 because there are 5 finger columns and 1 Meaning column per sign. n represents no.of signs in database
        # +1 to increment value of n so that new sign can be added. n represents no.of signs in database
        n = (columns / 6) + 1
        n = str(n)  # convert n to string
    # create a new empty dataframe with headers Thumb,Index,Middle,Ring,Pinky and Meaning
    new_csv_columns = pd.DataFrame({'Thumb': [], 'Index': [], 'Middle': [], 'Ring': [], 'Pinky': [], 'Meaning': []})
    # n can not possibly be 0 because if no signs previously existed, then we have just recorded a new one
    # therefore the minimum possible value of n is 1.
    if n == '1.0':  # if 1 sign exists in database
        number = '1.0'  # initialize number var to 1.0 string
        # extract the Thumb1.0, Index1.0, Middle1.0, Ring1.0 and Pinky1.0 columns
        extractedcolumns = entire_database[['Thumb' + number, 'Index' + number, 'Middle' + number, 'Ring' + number,
                                            'Pinky' + number, 'Meaning' + number]]
        # create a dictionary that represents Thumb1.0 key with Thumb value
        # create a dictionary that represents Index1.0 key with Index value
        # create a dictionary that represents Middle1.0 key with Middle value
        # create a dictionary that represents Ring1.0 key with Ring value
        # create a dictionary that represents Pinky1.0 key with Pinky value
        # create a dictionary that represents Meaning1.0 key with Meaning value
        dict = {'Thumb' + number: 'Thumb', 'Index' + number: 'Index', 'Middle' + number: 'Middle',
                'Ring' + number: 'Ring',
                'Pinky' + number: 'Pinky', 'Meaning' + number: 'Meaning'}
        # rename the extractedcolumns variable
        # example rename Thumb1.0 to Thumb, Index1.0 to Index, Middle1.0 to Middle and so on
        extractedcolumns.rename(columns=dict, inplace=True)
        # concatenate the empty dataframe new_csv_columns with the renamed extractedcolumn
        new_csv_columns = pd.concat([new_csv_columns, extractedcolumns], ignore_index=True, axis=0)
        new_csv_columns = new_csv_columns.dropna()  # drop any NaN values
        new_csv_columns.to_csv('data.csv', index=False, header=True)  # send to .csv file
    else:
        x = n.split(".")  # split the n variable based on '.' since the value of n is 2.0 for example
        x_2 = 1  # initialize x_2 with a value of 1
        # start loop with 1 and loop till the integer value of n which is x[0]
        while x_2 < (int(x[0])):
            number = str(x_2)  # convert x_2 to string and store it in number
            number = number + ".0"  # add .0 next to the number variable
            # extract the Thumb2.0, Index2.0, Middle2.0, Ring2.0, Pinky2.0 and Meaning2.0 columns
            extractedcolumns = entire_database[['Thumb' + number, 'Index' + number, 'Middle' + number, 'Ring' + number,
                                                'Pinky' + number, 'Meaning' + number]]
            # create a dictionary that represents Thumb2.0 key with Thumb value
            # create a dictionary that represents Index2.0 key with Index value
            # create a dictionary that represents Middle2.0 key with Middle value
            # create a dictionary that represents Ring2.0 key with Ring value
            # create a dictionary that represents Pinky2.0 key with Pinky value
            # create a dictionary that represents Meaning2.0 key with Meaning value
            dict = {'Thumb' + number: 'Thumb', 'Index' + number: 'Index', 'Middle' + number: 'Middle',
                    'Ring' + number: 'Ring',
                    'Pinky' + number: 'Pinky', 'Meaning' + number: 'Meaning'}
            # rename the extractedcolumns variable
            # example rename Thumb2.0 to Thumb, Index2.0 to Index, Middle2.0 to Middle and so on
            extractedcolumns.rename(columns=dict, inplace=True)
            # concatenate the dataframe new_csv_columns with the renamed extractedcolumn
            new_csv_columns = pd.concat([new_csv_columns, extractedcolumns], ignore_index=True, axis=0)
            x_2 = x_2 + 1  # increment the value of x_2
        new_csv_columns = new_csv_columns.dropna()  # drop any NaN values
        new_csv_columns.to_csv('data.csv', index=False, header=True)  # send to .csv file
    print('reading database....')
    signsdatabase = pd.read_csv('data.csv')  # read the csv file of signs database for KNN algorithm
    # assign the column of 5 fingers to the x_data variable by dropping the Meaning variable
    x_data = signsdatabase.drop(['Meaning'], axis=1)
    x_data = x_data.dropna()  # drop any NaN values
    y_data = signsdatabase['Meaning']  # assign the Meaning column to y_data
    y_data = y_data.dropna()  # drop the NaN values
    knn_clf = KNeighborsClassifier()  # initialize the KNN classifier
    print('training model....')
    # train the model with the new recorded sign added to the database
    knn_clf.fit(x_data, y_data)
    # return the updated classifier
    return knn_clf


destination_lang = input("Enter destination language:")
print('Press the S key after closing your hand')
while True:  # infinite loop until s key is pressed on the keyboard
    if keyboard.is_pressed('s'):  # check if s key is pressed on keyboard
        temp_list = []  # initialize an empty list
        # call calibrate_closed() func & assign returning val to closedhand_values
        closedhand_values = calibrate_closed()
        for item in closedhand_values:  # convert all items of list to int and store in temp_list
            temp_list.append(int(item))  # append items to temp_list
        closedhand_values = temp_list  # assign integer list to closedhand_values
        break  # break the while loop
print(' ')
print('Press the S key after opening your hand')
while True:  # infinite loop until s key is pressed on the keyboard
    if keyboard.is_pressed('s'):  # check if s key is pressed
        temp_list = []  # initialize an empty list
        openhand_values = calibrate_open()  # call calibrate_open() func & assign returning val to openhand_values
        for item in openhand_values:  # convert all items of list to int and store in temp_list
            temp_list.append(int(item))  # append items to temp_list
        openhand_values = temp_list  # assign integer list to closedhand_values
        break  # break the while loop
print(' ')
t_end = time.time() + 1.5  # add 1.5seconds delay
while time.time() < t_end:  # until 1.5 seconds is reached
    pass  # break the loop after delay is made

print('reading database...')
df = pd.read_csv('data.csv')  # read excelsheet of signs database. Assign columns to df var
classifier = KNeighborsClassifier()  # initialize the classifier var with KNN
x_data = df.drop(['Meaning'],axis=1)  # axis=1 column. Drop meaning col and leave remaining 5 finger resistance columns
x_data = x_data.dropna()  # drop NaN values

y_data = df['Meaning']  # initialize the y_data with the column 'Meaning' from signs database
y_data = y_data.dropna()  # drop NaN values
print('training model....')
classifier.fit(x_data, y_data)  # train the model with x_data on x-axis and y_data on y-axis

loop = True  # initialize True to loop variable
while True:  # start infinite loop
    if not loop:  # if loop variable is False
        t_end = time.time() + 0.1  # 0.1seconds delay after sign perform
        while time.time() < t_end:  # until 0.1 seconds is not reached.
            arduino.readline()  # read arduino during delay
        loop = True  # assign true to loop var
    while loop:  # while loop is True
        if arduino.in_waiting:  # if values are coming into arduino variable
            # clear_console()
            packet = arduino.readline()  # read packets coming into arduino variable from serial port
            decoded_values = packet.decode('utf')  # decode using utf scheme
            flex_sensors = decoded_values.split(',')  # split data from commas since serial data had commas
            # flex_sensors list values range from 0 to 4095. We will calibrate it to 0 to 90
            # calibrate real-time vals of sensors to (0 to 90). int() converting elements of flex_sensors list to int
            # assign returning 5 element list to new variable after calibration has been done.
            new = calibrate(int(flex_sensors[0]), int(flex_sensors[1]), int(flex_sensors[2]), int(flex_sensors[3]),
                            int(flex_sensors[4]), closedhand_values, openhand_values)
            thumb = new[0]  # initialize calibrated (0 to 90) thumb value to thumb var
            index = new[1]  # initialize calibrated (0 to 90) index value to index var
            middle = new[2]  # initialize calibrated (0 to 90) middle value to middle var
            ring = new[3]  # initialize calibrated (0 to 90) ring value to ring var
            pinky = new[4]  # initialize calibrated (0 to 90) pinky value to pinky var
            print('Thumb:', thumb, ' ', 'Index:', index, ' ', 'Middle:', middle, ' ', 'Ring:', ring, ' ', 'Pinky:',
                  pinky)  # pint real-time values of the flex sensors.
            if keyboard.is_pressed('r'):  # check to see if "r" key is pressed on keyboard
                print(' ')
                classifier = record()  # update classifier variable with new recorded sign
            # check to see if the real-time values match the existing database
            text = databasecheck(thumb, index, middle, ring, pinky, classifier)
            if text:  # if returning value is not false ( not returning the Null class from machine-learning )
                translate_and_speak(text) # translate and speak the text through the speaker
                loop = False  # assign False to loop variable to break the loop


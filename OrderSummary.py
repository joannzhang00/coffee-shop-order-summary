import orderlog
ORDER = orderlog.orderlst

openingTime = 6 * 60
closingTime = 24 * 60

def labelString(intervalNumber, openingTime, intervalLength):
    '''
    The function will be passed the interval number, opening time, and the length of \
    the time interval as input parameters and must return a string defining the start \
    and end time of the interval. For example, to generate the second value \
    ('7:00 - 7:59'), the function should be called as labelString(1, 6*60, 60 ).
    '''

    #convert hours into minutes
    beginmin = openingTime + (intervalNumber - 1) * intervalLength
    endmin = openingTime + (intervalNumber * intervalLength - 1)
    
    #calculate the hour and minute
    beginLabelHour = str(beginmin // 60)
    beginLabelMin = str(beginmin % 60).zfill(2)
    
    endLabelHour = str(endmin // 60)
    endLabelMin = str(endmin % 60).zfill(2)
    
    #combine the begin time and end time of each time label
    if endmin > 24 * 60:
        labelStr = format(beginLabelHour, ">2s") + ':' + beginLabelMin + ' - ' + '23:59'
    else:
        labelStr = format(beginLabelHour, ">2s") + ':' + beginLabelMin + ' - ' + \
        format(endLabelHour, ">2s") + ':' + endLabelMin
    
    return labelStr


def composeOrderMatrix(daynum = 31, intervalLength = 60):
    '''
    This function includes two parameters: the number of days, with a default value of 31, \
    and the length of the interval in minutes, defaulting to 60. The method should create \
    and return a two-dimensional list, representing the order summary matrix. \
    In the matrix, each column c will represent one day’s data for day number (c+1). \
    Values in row r will represent the number of orders in the time interval number r+1 \
    from the beginning of the day.
    '''
    #determine the interval number, which is also the row number of the matrix
    if (closingTime - openingTime) % intervalLength == 0:
        rownum =(closingTime - openingTime)// intervalLength
    else:
        rownum =(closingTime - openingTime)// intervalLength + 1
        
    colnum = daynum
    
    #create the two-dimensional list populated with as many rows of 0s, \
    #as the number of time intervals that would fit in the work day
    outer = []
    for j in range(rownum):
        inner = []
        for i in range(colnum):
            inner.append(0)
        outer.append(inner)
    
    #organize the order list and extract date and time of each order
    #make a copy of the order in case mutable property changing the list
    orderlst = ORDER.copy()
    #rule out the first element from the order list
    orderlst.pop(0)
    
    #extract date and time from order list
    ordercount = []
    for i in range(len(orderlst)):
        dateTime = orderlst[i][0].split()
        ordercount.append(dateTime)
    
    #convert the hour and minute into minute in order to determine which interval each order belongs
    dateTimeMatrix = []
    for j in range(len(ordercount)):
    
        datestr = int(ordercount[j][0][8:10])
        timestrh = int(ordercount[j][1][:2])
        timestrm = int(ordercount[j][1][3:5])
        ordermin = timestrh * 60 + timestrm
        dateTimeMatrix.append([datestr, ordermin])
    
    #determine the time-interval belonging of each order and substitute the matrix with order number
    for day in range(daynum):
        for row in range(rownum):
            counter = 0
            for lst in dateTimeMatrix:
                if lst[0] == day + 1 and (openingTime + row * intervalLength) <= lst[1] \
                < (openingTime + ((row + 1) * intervalLength)):
                    counter += 1
            outer[row][day] = counter
                
    return outer


def printOrderSummaryMatrix(twoDlst, intervalLength):
    '''
    This function has two parameters: a two-dimensional list of integers and \
    the length of the time interval. It's output is a matrix with day number of \
    columns and time-interval numbers of rows, demonstrating the number of orders \
    of corresponding position.
    '''
    
    #print matrix title and name of first column
    print('                     ORDER SUMMARY')
    print()
    print('  TIME \ DAY ', ' |', end = ' ')
    
    #print day number in the first row
    days = len(twoDlst[0])
    for day in range(days):
        print('', format((day + 1), "2d"), end = ' ')
    print()
    print('-----------------' + '----' * days)
    
    #determine the row number of the matrix
    if (closingTime - openingTime) % intervalLength == 0:
        rownum =(closingTime - openingTime)// intervalLength
    else:
        rownum =(closingTime - openingTime)// intervalLength + 1
    
    #print the time label and order number of each position
    for row in range(rownum):
        labelStr = labelString((row + 1), openingTime, intervalLength)
        print()
        print(labelStr, ' | ', end = ' ')
        for col in range(days):
            print(format(twoDlst[row][col], "2d"), end = '  ')
    print()
    #return ''    


def printHistogram(twoDlst, daynum, intervalLength):
    '''
    This function accepts three parameters: a two-dimensional list storing matrix \
    values, the day number (1-based) and the length of the time interval. The function\ 
    will display a histogram, which visualizes the numbers from the appropriate column \
    of the matrix using * symbols.
    '''
    #print matrix title
    print()
    print('          NUMBER OF ORDERS PER', intervalLength, 'min FOR DAY', daynum)
    print()
    
    #determine the row number
    if (closingTime - openingTime) % intervalLength == 0:
        rownum =(closingTime - openingTime)// intervalLength
    else:
        rownum =(closingTime - openingTime)// intervalLength + 1
    
    #print each line for the corresponding time interval of one required day
    for row in range(rownum):
        labelStr = labelString((row + 1), openingTime, intervalLength)
        ordernum = twoDlst[row][daynum - 1]
        print(labelStr, ' | ', '*' * ordernum)
    
    #return '' 


def main():
    '''
    Create and display the order summary matrix, summarizing how many orders were placed \
    during each interval starting from opening and closing time, for each day starting from \
    the first of the month until the day number, provided by the user.\
    Ask the user to specify the date, for which a histogram will be displayed. The histogram \
    displays each order as one * symbol. If the user enters a number that falls beyond the range \
    from 1 to the number of days in the summary matrix, the program should just repeat this step 
    until -1 is entered.
    '''
    
    #ask the user to get the input as argument for the functions
    days = eval(input('How many days would you like to include? '))
    timeInterval = eval(input('Please specify the length of the time interval in minutes: '))
    print()
    
    #generate the summary matrix using the composeOrderMatrix function and printOrderSummaryMatrix function
    summaryLst = composeOrderMatrix(days, timeInterval)
    printOrderSummaryMatrix(summaryLst, timeInterval)
    
    #ask the user to get the day number in order to create the histogram
    print()
    
    #('Enter day number from 1 to %s to see a histogram, or -1 to exit: ')%(days)
    
    repeat = -2
    while repeat != -1:
        daynum = eval(input(('Enter day number from 1 to %s to see a histogram, or -1 to exit: ')%(days)))
        if daynum in range(1, days + 1):
            printHistogram(summaryLst, daynum, timeInterval)
        elif daynum == -1:
            print('bye!')
            repeat = -1
                
            
    
          
main()


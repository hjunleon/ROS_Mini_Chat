#!/usr/bin/env python
import rospy, os, random
from std_msgs.msg import Header, String
from assignment1.msg import Chat
from datetime import datetime
from colorama import Fore, Back, Style

valid_hex = '0123456789ABCDEF'.__contains__
def cleanhex(data):
    return ''.join(filter(valid_hex, data.upper()))

def fore_fromhex(text, hexcode):
    """print in a hex defined color"""
    hexint = int(cleanhex(hexcode), 16)
    print("\x1B[38;2;{};{};{}m{}\x1B[0m".format(hexint>>16, hexint>>8&0xFF, hexint&0xFF, text))


"""
Return random color in hex string
"""
def getRandColor():
    r = random.randrange(40,206)
    g = random.randrange(40,206)
    b = random.randrange(40,206)
    return "#" + hex(r)[2:] + hex(g)[2:] + hex(b)[2:]

def getStandardTime():
    return datetime.today().strftime('%Y-%m-%d-%H_%M_%S')

defaultPersonalColor = "#00FF00"
msgQueue = []
user2Color = {}
colorSet = set([defaultPersonalColor])
username = ""
def receiveMsg(data):
    global username
    os.system('clear')
    #print(colorSet)
    #print(data)
    msgQueue.append(data)
    if len(msgQueue) > 10:
        msgQueue.pop(0)
    for msg in msgQueue:
        textColor = "#FFFFFF"
        curAuthor = msg.author.data
        curMsg = msg.message.data
        curTime = msg.Header.stamp
        curTime = datetime.utcfromtimestamp(curTime.to_sec()).strftime('%Y-%m-%d-%H_%M_%S')
        if(curAuthor == username):
            textColor = defaultPersonalColor
        else:
            if curAuthor not in user2Color:
                ranColor = getRandColor()
                while(ranColor in colorSet):
                    ranColor = getRandColor()
                colorSet.add(ranColor)
                user2Color[curAuthor] = ranColor
            
            textColor = user2Color[curAuthor]

        
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s from %s", msg.message, msg.author)
        fore_fromhex(curTime+ " ::: " + curAuthor + ">>>"+curMsg, textColor)
        Style.RESET_ALL
def talker():
    global username
    print("Welcome to Jun Leong's ROS Chat!")
    username = raw_input("Tell me your name: ")
    if len(username) == 0:
        username = "Guest_"+getStandardTime()
    pub = rospy.Publisher('chatter', Chat, queue_size=10)
    rospy.Subscriber("chatter", Chat, receiveMsg)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #
        hello_str = raw_input()

        header = Header()
        header.stamp = rospy.Time.now()
        source_id = String(username)#(rospy.get_name())
        message = String(hello_str)
        c = Chat(header, source_id, message)
        #print(c)
        pub.publish(c)

        
        
        
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
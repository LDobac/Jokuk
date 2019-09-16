import sys
import array

## OPERATIONS ##
OPER_READ_PLUS = "+"
OPER_READ_MINUS = "-"
OPER_READ_NUM = "#"
OPER_PUSH_BUF_TO_PTR = "%"
OPER_LOAD_BUF = ","
OPER_PUSH_BUF = "."
OPER_PRINT = "?"
OPER_PLUS = "("
OPER_MINUS = ")"
OPER_LABLE = "^"
OPER_JMP = "<"

fileName = sys.argv[1]
file = open(fileName, "r")

code = file.read()
## STATUS VARIABLES ##
buffer = array.array("l", [0] * 30000)

codeCursor = 0
ptrCursor = 0

readStride = 1

onRegNum1Load = False
onRegNum2Load = False
regNum1 = 0
regNum2 = 0
result = 0

onPushBuffer = False
onReadNumber = False

## RUN
while codeCursor < len(code):
    if onReadNumber:
        readingNumStr = ""
        readCounter = 0
        while (len(readingNumStr) < readStride) and (readCounter + codeCursor) < len(code):
            numberStr = code[(codeCursor + readCounter):(codeCursor + readCounter) + 1]
            if numberStr.isdecimal():
                readingNumStr += numberStr
            readCounter += 1
        if onPushBuffer:
            buffer[ptrCursor] = int(readingNumStr)
        else:
            ptrCursor = int(readingNumStr)
        codeCursor += readCounter
        onReadNumber = False
        onPushBuffer = False
    else:
        operation = code[codeCursor:codeCursor+1]
        if operation == OPER_READ_PLUS:
            readStride+=1
        elif operation == OPER_READ_MINUS:
            if (readStride > 1):
                readStride-=1
        elif operation == OPER_READ_NUM:
            onReadNumber = True
        elif operation == OPER_PUSH_BUF_TO_PTR:
            ptrCursor = buffer[ptrCursor]
        elif operation == OPER_LOAD_BUF:
            if not onRegNum1Load:
                regNum1 = buffer[ptrCursor]
                onRegNum1Load = True
            elif not onRegNum2Load:
                regNum2 = buffer[ptrCursor]
                onRegNum2Load = True
        elif operation == OPER_PUSH_BUF:
            onPushBuffer = True
        elif operation == OPER_PRINT:
            print(chr(buffer[ptrCursor]),end="")
        elif operation == OPER_PLUS:
            if (onRegNum1Load and onRegNum2Load):
                result = regNum1 + regNum2
                buffer[ptrCursor] = result
                onRegNum1Load = False
                onRegNum2Load = False
        elif operation == OPER_MINUS:
            if (onRegNum1Load and onRegNum2Load):
                result = regNum1 - regNum2
                buffer[ptrCursor] = result
                onRegNum1Load = False
                onRegNum2Load = False
        elif operation == OPER_LABLE:
            pass
        elif operation == OPER_JMP:
            if not (buffer[ptrCursor] == 0):
                for i in range(codeCursor, -1, -1):
                    if code[i] == OPER_LABLE:
                        codeCursor = i
                        break;
        else:
            pass

        codeCursor = codeCursor + 1

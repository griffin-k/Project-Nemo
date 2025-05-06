from gpiozero import Motor, DigitalInputDevice
import time

# Define GPIO pins (BCM numbering) for motors
RmotorFWD = 5   # Right motor forward
RmotorBCK = 6   # Right motor backward
LmotorFWD = 13  # Left motor forward
LmotorBCK = 19  # Left motor backward

# Define encoder pins
RencoderPin = 21  # Right encoder
LencoderPin = 20  # Left encoder

# Initialize encoder counters
RencoderCount = 0
LencoderCount = 0

# Initialize motors
rightMotor = Motor(forward=RmotorFWD, backward=RmotorBCK, pwm=True)
leftMotor = Motor(forward=LmotorFWD, backward=LmotorBCK, pwm=True)

# Initialize encoder pins
rightEncoder = DigitalInputDevice(RencoderPin, pull_up=True)
leftEncoder = DigitalInputDevice(LencoderPin, pull_up=True)

# Encoder event handlers
def right_encoder_callback():
    global RencoderCount
    RencoderCount += 1

def left_encoder_callback():
    global LencoderCount
    LencoderCount += 1

# Attach interrupt handlers
rightEncoder.when_activated = right_encoder_callback
leftEncoder.when_activated = left_encoder_callback

# Time-based functions
def forward(speed):
    print("Moving forward")
    rightMotor.forward(speed)
    leftMotor.forward(speed)

def backward(speed):
    print("Moving backward")
    rightMotor.backward(speed)
    leftMotor.backward(speed)

def left(speed):
    print("Turning left")
    rightMotor.forward(speed)
    leftMotor.backward(speed)

def right(speed):
    print("Turning right")
    rightMotor.backward(speed)
    leftMotor.forward(speed)

# Encoder-based functions
def encoderforward(speed, ticks):
    global RencoderCount, LencoderCount
    print("Moving forward (encoder)")
    RencoderCount = 0
    LencoderCount = 0
    rightMotor.forward(speed)
    leftMotor.forward(speed)
    while (RencoderCount < ticks) or (LencoderCount < ticks):
        time.sleep(0.1)
    rightMotor.stop()
    leftMotor.stop()

def encoderbackward(speed, ticks):
    global RencoderCount, LencoderCount
    print("Moving backward (encoder)")
    RencoderCount = 0
    LencoderCount = 0
    rightMotor.backward(speed)
    leftMotor.backward(speed)
    while (RencoderCount < ticks) or (LencoderCount < ticks):
        time.sleep(0.1)
    rightMotor.stop()
    leftMotor.stop()

def encoderleft(speed, ticks):
    global RencoderCount, LencoderCount
    print("Turning left (encoder)")
    RencoderCount = 0
    LencoderCount = 0
    rightMotor.forward(speed)
    leftMotor.backward(speed)
    while RencoderCount < ticks:
        time.sleep(0.1)
    rightMotor.stop()
    leftMotor.stop()

def encoderright(speed, ticks):
    global RencoderCount, LencoderCount
    print("Turning right (encoder)")
    RencoderCount = 0
    LencoderCount = 0
    rightMotor.backward(speed)
    leftMotor.forward(speed)
    while LencoderCount < ticks:
        time.sleep(0.1)
    rightMotor.stop()
    leftMotor.stop()

# Stop function
def stop():
    print("Stopped")
    rightMotor.stop()
    leftMotor.stop()

try:
    speed = 0.6
    ticks = 200
    # Time-based sequence (2 seconds each)
    forward(speed)
    time.sleep(2)
    stop()

    backward(speed)
    time.sleep(2)
    stop()

    left(speed)
    time.sleep(2)
    stop()

    right(speed)
    time.sleep(2)
    stop()

    # Encoder-based sequence (100 ticks each)
    encoderforward(speed, ticks)
    encoderbackward(speed, ticks)
    encoderleft(speed, ticks)
    encoderright(speed, ticks)
    
    stop()

except KeyboardInterrupt:
    stop()
    print("Stopped by user")
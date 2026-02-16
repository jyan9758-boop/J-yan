# Makefile for STM32 Firmware
# This is a template - adjust according to your specific STM32 board and toolchain

# Toolchain
CC = arm-none-eabi-gcc
AS = arm-none-eabi-as
LD = arm-none-eabi-ld
OBJCOPY = arm-none-eabi-objcopy
SIZE = arm-none-eabi-size

# Target
TARGET = fire_inspection_robot

# Directories
BUILD_DIR = build
SRC_DIR = src
INC_DIR = include

# Source files
C_SOURCES = \
	$(SRC_DIR)/main.c \
	$(SRC_DIR)/motor_control.c \
	$(SRC_DIR)/sensor_interface.c \
	$(SRC_DIR)/patrol_control.c \
	$(SRC_DIR)/communication.c

# Include directories
INCLUDES = \
	-I$(INC_DIR)

# MCU specific flags (example for STM32F407)
MCU = -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard

# C flags
CFLAGS = $(MCU) $(INCLUDES) -Wall -Wextra -O2 -g

# Linker flags
LDFLAGS = $(MCU) -specs=nosys.specs

# Build
all: $(BUILD_DIR)/$(TARGET).elf $(BUILD_DIR)/$(TARGET).hex $(BUILD_DIR)/$(TARGET).bin

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/$(TARGET).elf: $(C_SOURCES:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)
	$(CC) $(LDFLAGS) $^ -o $@
	$(SIZE) $@

$(BUILD_DIR)/$(TARGET).hex: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

$(BUILD_DIR)/$(TARGET).bin: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O binary $< $@

# Flash to board (using st-flash)
flash: $(BUILD_DIR)/$(TARGET).bin
	st-flash write $(BUILD_DIR)/$(TARGET).bin 0x8000000

# Clean
clean:
	rm -rf $(BUILD_DIR)

.PHONY: all flash clean

#!/usr/bin/python

import time
import smbus
from rpi_i2c_new  import rpi_i2c

# ===========================================================================
# INA219 Class
# ===========================================================================

class BQ25910:
	i2c = None

# ===========================================================================
#   I2C DEVICE ADDRESS
# ==========================================================================
	__BQ25910_DEV_ID                          = 0x4B
# ===========================================================================

# ===========================================================================
#    BATTERY VOLTAGE LIMIT REGISTER (R/W) Range 3.5V to 4.775V
# ===========================================================================
	__BQ25910_BATTERY_VOLTAGE_LIMIT           = 0x00 # ADDRESS
# ===========================================================================
	__BQ25910_BATTERY_VOLTAGE_LIMIT_LSB       = 0.005
	__BQ25910_BATTERY_VOLTAGE_LIMIT_OFFSET    = 3.5

# ===========================================================================
#    CHARGE CURRENT LIMIT REGISTER (R/W) Range 0A to 6A, 0x78 and larger is 6A
# ===========================================================================
	__BQ25910_CHARGE_CURRENT_LIMIT            = 0x01 # ADDRESS
# ===========================================================================
	__BQ25910_CHARGE_CURRENT_LIMIT_LSB        = 0.05
	__BQ25910_CHARGE_CURRENT_LIMIT_MAX        = 6.0

# ===========================================================================
#    INPUT VOLTAGE LIMIT REGISTER (R/W) Range 3.9V to 14V, 0x65 and larger is 14V
# ===========================================================================
	__BQ25910_INPUT_VOLTAGE_LIMIT             = 0x02 # ADDRESS
# ===========================================================================
	__BQ25910_INPUT_VOLTAGE_LIMIT_OFFSET      = 3.9
	__BQ25910_INPUT_VOLTAGE_LIMIT_LSB         = 0.1
	__BQ25910_INPUT_VOLTAGE_LIMIT_MAX         = 14.0

# ===========================================================================
#    INPUT CURRENT LIMIT REGISTER (R/W) Range 0.5 to 3.6A, 0x1F and larger is 3.6A
# ===========================================================================
	__BQ25910_INPUT_CURRENT_LIMIT             = 0x03 # ADDRESS
# ===========================================================================
	__BQ25910_INPUT_CURRENT_LIMIT_OFFSET      = 0.5
	__BQ25910_INPUT_CURRENT_LIMIT_LSB         = 0.1
	__BQ25910_INPUT_CURRENT_LIMIT_MAX         = 3.6

# ===========================================================================
#    CHARGER CONTROL 1 REGISTER (R/W)
# ===========================================================================
	__BQ25910_CHARGER_CONTROL_1               = 0x05 # ADDRESS
# ===========================================================================
	__BQ25910_CHARGER_CONTROL_1_TMR2X_EN      = 0x01
	__BQ25910_CHARGER_CONTROL_1_CHG_TIMER_5H  = 0x00
	__BQ25910_CHARGER_CONTROL_1_CHG_TIMER_8H  = 0x02
	__BQ25910_CHARGER_CONTROL_1_CHG_TIMER_12H = 0x04
	__BQ25910_CHARGER_CONTROL_1_CHG_TIMER_20H = 0x06
	__BQ25910_CHARGER_CONTROL_1_EN_TIMER      = 0x08
	__BQ25910_CHARGER_CONTROL_1_WD_DISABLE    = 0x00
	__BQ25910_CHARGER_CONTROL_1_WD_40S        = 0x10
	__BQ25910_CHARGER_CONTROL_1_WD_80S        = 0x20
	__BQ25910_CHARGER_CONTROL_1_WD_160S       = 0x30
	__BQ25910_CHARGER_CONTROL_1_WD_BIT_MASK   = 0x30
	__BQ25910_CHARGER_CONTROL_1_WD_RST        = 0x40
	__BQ25910_CHARGER_CONTROL_1_EN_TERM       = 0x80

# ===========================================================================
#    CHARGER CONTROL 2 REGISTER (R/W)
# ===========================================================================
	__BQ25910_CHARGER_CONTROL_2               = 0x06 # ADDRESS
# ===========================================================================
	__BQ25910_CHARGER_CONTROL_2_VBATLOW_2P6V  = 0x00
	__BQ25910_CHARGER_CONTROL_2_VBATLOW_2P9V  = 0x01
	__BQ25910_CHARGER_CONTROL_2_VBATLOW_3P2V  = 0x02
	__BQ25910_CHARGER_CONTROL_2_VBATLOW_3P5V  = 0x03
	__BQ25910_CHARGER_CONTROL_2_EN_CHG        = 0x08
	__BQ25910_CHARGER_CONTROL_2_TREG_60C      = 0x00
	__BQ25910_CHARGER_CONTROL_2_TREG_80C      = 0x10
	__BQ25910_CHARGER_CONTROL_2_TREG_100C     = 0x20
	__BQ25910_CHARGER_CONTROL_2_TREG_120C     = 0x30

# ===========================================================================
#    INT STATUS REGISTER (RO)
# ===========================================================================
	__BQ25910_INT_STATUS                      = 0x07 # ADDRESS
# ===========================================================================
	__BQ25910_INT_STATUS_CHRG_STAT_OFF        = 0x00
	__BQ25910_INT_STATUS_CHRG_STAT_CC_MODE    = 0x03
	__BQ25910_INT_STATUS_CHRG_STAT_CV_MODE    = 0x04
	__BQ25910_INT_STATUS_WD                   = 0x08
	__BQ25910_INT_STATUS_TREG                 = 0x10
	__BQ25910_INT_STATUS_VINDPM               = 0x20
	__BQ25910_INT_STATUS_INDPM                = 0x40
	__BQ25910_INT_STATUS_PG                   = 0x80

# ===========================================================================
#    FAULT STATUS REGISTER (RO)
# ===========================================================================
	__BQ25910_FAULT_STATUS                    = 0x08 # ADDRESS
# ===========================================================================
	__BQ25910_FAULT_STATUS_POORSRC            = 0x02
	__BQ25910_FAULT_STATUS_CAP_COND           = 0x04
	__BQ25910_FAULT_STATUS_CFLY               = 0x10
	__BQ25910_FAULT_STATUS_BATOVP             = 0x20
	__BQ25910_FAULT_STATUS_TSHUT              = 0x40
	__BQ25910_FAULT_STATUS_VBUS_OVP           = 0x80

# ===========================================================================
#    INT FLAG REGISTER (RO)
# ===========================================================================
	__BQ25910_INT_FLAG                        = 0x09 # ADDRESS
# ===========================================================================
	__BQ25910_INT_FLAG_CHRG                   = 0x01
	__BQ25910_INT_FLAG_CHRG_TERM              = 0x04
	__BQ25910_INT_FLAG_WD                     = 0x08
	__BQ25910_INT_FLAG_TREG                   = 0x10
	__BQ25910_INT_FLAG_VINDPM                 = 0x20
	__BQ25910_INT_FLAG_INDPM                  = 0x40
	__BQ25910_INT_FLAG_PG                     = 0x80

# ===========================================================================
#    FAULT FLAG REGISTER (RO)
# ===========================================================================
	__BQ25910_FAULT_FLAG                      = 0x0A # ADDRESS
# ===========================================================================
	__BQ25910_FAULT_FLAG_POORSRC              = 0x02
	__BQ25910_FAULT_FLAG_CAP_COND             = 0x04
	__BQ25910_FAULT_FLAG_CFLY                 = 0x10
	__BQ25910_FAULT_FLAG_BATOVP               = 0x20
	__BQ25910_FAULT_FLAG_TSHUT                = 0x40
	__BQ25910_FAULT_FLAG_VBUS_OVP             = 0x80

# ===========================================================================
#    INT MASK REGISTER (R/W)
# ===========================================================================
	__BQ25910_INT_MASK                        = 0x0B # ADDRESS
# ===========================================================================
	__BQ25910_INT_MASK_CHRG                   = 0x01
	__BQ25910_INT_MASK_CHRG_TERM              = 0x04
	__BQ25910_INT_MASK_WD                     = 0x08
	__BQ25910_INT_MASK_TREG                   = 0x10
	__BQ25910_INT_MASK_VINDPM                 = 0x20
	__BQ25910_INT_MASK_INDPM                  = 0x40
	__BQ25910_INT_MASK_PG                     = 0x80

# ===========================================================================
#    FAULT MASK REGISTER (R/W)
# ===========================================================================
	__BQ25910_FAULT_MASK                      = 0x0C # ADDRESS
# ===========================================================================
	__BQ25910_FAULT_MASK_POORSRC              = 0x02
	__BQ25910_FAULT_MASK_CAP_COND             = 0x04
	__BQ25910_FAULT_MASK_CFLY                 = 0x10
	__BQ25910_FAULT_MASK_BATOVP               = 0x20
	__BQ25910_FAULT_MASK_TSHUT                = 0x40
	__BQ25910_FAULT_MASK_VBUS_OVP             = 0x80

# ===========================================================================
#    PART INFORMATION REGISTER (Bit 7 is R/W, all others are RO)
# ===========================================================================
	__BQ25910_PART_INFO                       = 0x0D # ADDRESS
# ===========================================================================
	__BQ25910_PART_INFO_DEV_REV               = 0x01
	__BQ25910_PART_INFO_PN                    = 0x08
	__BQ25910_PART_INFO_REG_RST               = 0x80


	# Constructor
	def __init__(self, address=__BQ25910_DEV_ID, debug=False):
		self.i2c = rpi_i2c(address, debug=debug, name="bq25910")
		self.address = address
		self.debug = debug
		
	def read_modify_write(self,address,value):
		present_reg_val = self.i2c.readU8(address)
		modified_reg_val = (present_reg_val | value) & 0xFF
		self.i2c.write8(address,modified_reg_val)
		
	def read_clear_write(self,address,value):
		present_reg_val = self.i2c.readU8(address)
		modified_reg_val = (present_reg_val & (~value)) & 0xFF
		self.i2c.write8(address,modified_reg_val)
		
	def write_bit_field(self, address, bit_mask, value): # value must be within the bit_mask
		present_reg_val = self.i2c.readU8(address)
		modified_reg_val = ((present_reg_val & (~bit_mask & 0xFF)) + (value & bit_mask & 0xFF)) & 0xFF
		self.i2c.write8(address,modified_reg_val)
		if (self.debug == True):
			print "CALLED: write_bit_field, Address 0x%02x, Read value 0x%02x, Modified it to be 0x%02x, and wrote it" % (address,present_reg_val,modified_reg_val)

	def set_battery_voltage_limit(self,battery_voltage_limit):
		if (battery_voltage_limit < 3.5 or battery_voltage_limit > 4.775):
			print "ERROR invalid battery voltage limit given, must be between 3.5 and 4.775V"
			return -1
		else:
			raw_data = int((battery_voltage_limit - self.__BQ25910_BATTERY_VOLTAGE_LIMIT_OFFSET) / self.__BQ25910_BATTERY_VOLTAGE_LIMIT_LSB ) & 0xFF
			self.i2c.write8(self.__BQ25910_BATTERY_VOLTAGE_LIMIT, raw_data)
			if (self.debug == True):
				print "CALLED: set_battery_voltage_limit, given limit %f, address 0x%02x, raw register data written 0x%02x" % (battery_voltage_limit,self.__BQ25910_BATTERY_VOLTAGE_LIMIT,raw_data)
			return 1
	
	def set_charge_current_limit(self,charge_current_limit):
		if (charge_current_limit > self.__BQ25910_CHARGE_CURRENT_LIMIT_MAX):
			print "ERROR invalid charge current limit, must be equal to or below %f" % self.__BQ25910_CHARGE_CURRENT_LIMIT_MAX
			return -1
		else:
			raw_data = int(charge_current_limit / self.__BQ25910_CHARGE_CURRENT_LIMIT_LSB) & 0xFF
			self.i2c.write8(self.__BQ25910_CHARGE_CURRENT_LIMIT, raw_data)
			if (self.debug == True):
				print "CALLED: set_charge_current_limit, given limit %f, address 0x%02x, raw register data written 0x%02x" % (charge_current_limit,self.__BQ25910_CHARGE_CURRENT_LIMIT,raw_data)
			return 1

	def set_input_voltage_limit(self,input_voltage_limit):
		if (input_voltage_limit < 3.9 or input_voltage_limit > 14.0):
			print "ERROR invalid input voltage limit given, must be between 3.9 and 14V"
			return -1
		else:
			raw_data = int((input_voltage_limit - self.__BQ25910_INPUT_VOLTAGE_LIMIT_OFFSET) / self.__BQ25910_INPUT_VOLTAGE_LIMIT_LSB ) & 0xFF
			self.i2c.write8(self.__BQ25910_INPUT_VOLTAGE_LIMIT, raw_data)
			if (self.debug == True):
				print "CALLED: set_input_voltage_limit, given limit %f, address 0x%02x, raw register data written 0x%02x" % (input_voltage_limit,self.__BQ25910_INPUT_VOLTAGE_LIMIT,raw_data)
			return 1

	def set_input_current_limit(self,input_current_limit):
		if (input_current_limit > self.__BQ25910_INPUT_CURRENT_LIMIT_MAX):
			print "ERROR invalid input current limit, must be greater than %f or below %f" % (self.__BQ25910_INPUT_CURRENT_LIMIT_OFFSET,self.__BQ25910_INPUT_CURRENT_LIMIT_MAX)
			return -1
		else:
			raw_data = int(input_current_limit / self.__BQ25910_INPUT_CURRENT_LIMIT_LSB) & 0xFF
			self.i2c.write8(self.__BQ25910_INPUT_CURRENT_LIMIT, raw_data)
			if (self.debug == True):
				print "CALLED: set_input_current_limit, given limit %f, address 0x%02x, raw register data written 0x%02x" % (input_current_limit,self.__BQ25910_INPUT_CURRENT_LIMIT,raw_data)
			return 1
		
	def enable_charging(self):
		self.read_modify_write(self.__BQ25910_CHARGER_CONTROL_2,self.__BQ25910_CHARGER_CONTROL_2_EN_CHG)
		present_reg_val = self.i2c.readU8(self.__BQ25910_CHARGER_CONTROL_2)
		if (present_reg_val & self.__BQ25910_CHARGER_CONTROL_2_EN_CHG == self.__BQ25910_CHARGER_CONTROL_2_EN_CHG):
			print "BQ25910 CHARGING ENABLED"
		else:
			print "*** ERROR: tried to enable charging but not successful"
		
	def disable_charging(self):
		self.read_clear_write(self.__BQ25910_CHARGER_CONTROL_2,self.__BQ25910_CHARGER_CONTROL_2_EN_CHG)
		print "BQ25910 CHARGING DISABLED"
		
	def read_charge_status(self):
		present_reg_val = self.i2c.readU8(self.__BQ25910_INT_STATUS)
		if (present_reg_val & self.__BQ25910_INT_STATUS_CHRG_STAT_CC_MODE == self.__BQ25910_INT_STATUS_CHRG_STAT_CC_MODE):
			print "BQ25910 charge status is CC MODE"
		elif (present_reg_val & self.__BQ25910_INT_STATUS_CHRG_STAT_CV_MODE == self.__BQ25910_INT_STATUS_CHRG_STAT_CV_MODE):
			print "BQ25910 charge status is CV MODE"
		else:
			print "BQ25910 charge status is OFF"
		if (self.debug == True):
			print "CALLED: read_charge_status, address 0x%02x, register data is 0x%02x" % (self.__BQ25910_INT_STATUS,present_reg_val)

	def reset_all_registers(self):
		self.read_modify_write(self.__BQ25910_PART_INFO, self.__BQ25910_PART_INFO_REG_RST)
		if (self.debug == True):
			print "BQ25910 RESET ALL REGISTERS"
	
	def read_all_int_status(self):
		present_reg_val = self.i2c.readU8(self.__BQ25910_INT_STATUS)
		if (self.debug == True):
			print "CALLED: read_all_int_status, address 0x%02x, read data 0x%02x" % (self.__BQ25910_INT_STATUS,present_reg_val)
		if (present_reg_val & self.__BQ25910_INT_STATUS_WD == self.__BQ25910_INT_STATUS_WD):
			print "INT STATUS: WatchDog Expired"
		if (present_reg_val & self.__BQ25910_INT_STATUS_TREG == self.__BQ25910_INT_STATUS_TREG):
			print "INT STATUS: Thermal Regulation ACTIVE"
		if (present_reg_val & self.__BQ25910_INT_STATUS_VINDPM == self.__BQ25910_INT_STATUS_VINDPM):
			print "INT STATUS: Voltage Regulation ACTIVE"
		if (present_reg_val & self.__BQ25910_INT_STATUS_INDPM == self.__BQ25910_INT_STATUS_INDPM):
			print "INT STATUS: Current Regulation ACTIVE"
		if (present_reg_val & self.__BQ25910_INT_STATUS_PG == self.__BQ25910_INT_STATUS_PG):
			print "INT STATUS: POWER GOOD"
	
	def read_all_fault_status(self):
		present_reg_val = self.i2c.readU8(self.__BQ25910_FAULT_STATUS)
		if (self.debug == True):
			print "CALLED: read_all_fault_status, address 0x%02x, read data 0x%02x" % (self.__BQ25910_FAULT_STATUS,present_reg_val)
		if (present_reg_val & self.__BQ25910_FAULT_STATUS_POORSRC == self.__BQ25910_FAULT_STATUS_POORSRC):
			print "FAULT STATUS: Poor Source"
		if (present_reg_val & self.__BQ25910_FAULT_STATUS_CAP_COND == self.__BQ25910_FAULT_STATUS_CAP_COND):
			print "FAULT STATUS: Cap Condition"
		if (present_reg_val & self.__BQ25910_FAULT_STATUS_CFLY == self.__BQ25910_FAULT_STATUS_CFLY):
			print "FAULT STATUS: Fly Cap"
		if (present_reg_val & self.__BQ25910_FAULT_STATUS_BATOVP == self.__BQ25910_FAULT_STATUS_BATOVP):
			print "FAULT STATUS: Battery Over Voltage Protection"
		if (present_reg_val & self.__BQ25910_FAULT_STATUS_TSHUT == self.__BQ25910_FAULT_STATUS_TSHUT):
			print "FAULT STATUS: Thermal Shutdown"
		if (present_reg_val & self.__BQ25910_FAULT_STATUS_VBUS_OVP == self.__BQ25910_FAULT_STATUS_VBUS_OVP):
			print "FAULT STATUS: VBUS Over Voltage Protection"
	
	def read_all_int_flags(self):
		present_reg_val = self.i2c.readU8(self.__BQ25910_INT_FLAG)
		if (self.debug == True):
			print "CALLED: read_all_int_flags, address 0x%02x, read data 0x%02x" % (self.__BQ25910_INT_FLAG,present_reg_val)
		if (present_reg_val & self.__BQ25910_INT_FLAG_CHRG == self.__BQ25910_INT_FLAG_CHRG):
			print "INT FLAG: Charger Status Changed"
		if (present_reg_val & self.__BQ25910_INT_FLAG_CHRG_TERM == self.__BQ25910_INT_FLAG_CHRG_TERM):
			print "INT FLAG: Charge Termination"
		if (present_reg_val & self.__BQ25910_INT_FLAG_WD == self.__BQ25910_INT_FLAG_WD):
			print "INT FLAG: WatchDog Expired"
		if (present_reg_val & self.__BQ25910_INT_FLAG_TREG == self.__BQ25910_INT_FLAG_TREG):
			print "INT FLAG: Thermal Regulation ACTIVE"
		if (present_reg_val & self.__BQ25910_INT_FLAG_VINDPM == self.__BQ25910_INT_FLAG_VINDPM):
			print "INT FLAG: Voltage Regulation ACTIVE"
		if (present_reg_val & self.__BQ25910_INT_FLAG_INDPM == self.__BQ25910_INT_FLAG_INDPM):
			print "INT FLAG: Current Regulation ACTIVE"
		if (present_reg_val & self.__BQ25910_INT_FLAG_PG== self.__BQ25910_INT_FLAG_PG):
			print "INT FLAG: POWER GOOD"
		
	def read_all_fault_flags(self):
		present_reg_val = self.i2c.readU8(self.__BQ25910_FAULT_FLAG)
		if (self.debug == True):
			print "CALLED: read_all_fault_flags, address 0x%02x, read data 0x%02x" % (self.__BQ25910_FAULT_FLAG,present_reg_val)
		if (present_reg_val & self.__BQ25910_FAULT_FLAG_POORSRC == self.__BQ25910_FAULT_FLAG_POORSRC):
			print "FAULT FLAG: Poor Source"
		if (present_reg_val & self.__BQ25910_FAULT_FLAG_CAP_COND == self.__BQ25910_FAULT_FLAG_CAP_COND):
			print "FAULT FLAG: Cap Condition"
		if (present_reg_val & self.__BQ25910_FAULT_FLAG_CFLY == self.__BQ25910_FAULT_FLAG_CFLY):
			print "FAULT FLAG: Fly Cap"
		if (present_reg_val & self.__BQ25910_FAULT_FLAG_BATOVP == self.__BQ25910_FAULT_FLAG_BATOVP):
			print "FAULT FLAG: Battery Over Voltage Protection"
		if (present_reg_val & self.__BQ25910_FAULT_FLAG_TSHUT == self.__BQ25910_FAULT_FLAG_TSHUT):
			print "FAULT FLAG: Thermal Shutdown"
		if (present_reg_val & self.__BQ25910_FAULT_FLAG_VBUS_OVP == self.__BQ25910_FAULT_FLAG_VBUS_OVP):
			print "FAULT FLAG: VBUS Over Voltage Protection"
	
	def disable_watchdog(self):
		self.write_bit_field(self.__BQ25910_CHARGER_CONTROL_1, self.__BQ25910_CHARGER_CONTROL_1_WD_BIT_MASK, self.__BQ25910_CHARGER_CONTROL_1_WD_DISABLE)
		print "BQ25910 WATCHDOG DISABLED"

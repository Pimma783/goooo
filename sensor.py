"""
===============================================================
  ตรวจจับวัตถุด้วย MH-Sensor Flying-Fish (3 ขา)
  Raspberry Pi Pico - MicroPython (Best Practice Version)
===============================================================
  การต่อวงจร (ยึดตามเลข GP เป็นหลัก):
  Flying-Fish      Raspberry Pi Pico
  VCC       ->     3.3V  (Pin 36)
  GND       ->     GND   (Pin 38)
  OUT       ->     GP14  (Physical Pin 19)

  LED แจ้งเตือน ->   GP15  (Physical Pin 20)
===============================================================
"""

from machine import Pin
import utime

# ============================================================
# 1. ตั้งค่า Pin (ใช้เลข GP เสมอ!)
# ============================================================
SENSOR_PIN = 14  # ใช้เลข 14 สำหรับ GP14
LED_PIN = 15  # ใช้เลข 15 สำหรับ GP15

sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)
ext_led = Pin(LED_PIN, Pin.OUT)

# รองรับทั้ง Pico ธรรมดา (Pin 25) และ Pico W (Pin "LED")
try:
    onboard_led = Pin("LED", Pin.OUT)
except TypeError:
    onboard_led = Pin(25, Pin.OUT)


# ============================================================
# 2. ฟังก์ชันหลัก
# ============================================================
def is_detected() -> bool:
    """
    อ่านค่าจากเซ็นเซอร์
    เซ็นเซอร์เป็นแบบ Active LOW:
    - อ่านได้ 0 = มีวัตถุบัง (Return True)
    - อ่านได้ 1 = ไม่มีวัตถุ (Return False)
    """
    return sensor.value() == 0


def set_led(state: bool):
    """สั่งเปิด-ปิด LED ทั้งบนบอร์ดและต่อแยก"""
    val = 1 if state else 0  # ถ้า state เป็น True ให้ส่ง 1 (ไฟติด)
    ext_led.value(val)
    onboard_led.value(val)


# ============================================================
# 3. Main Program
# ============================================================
def main():
    print("=" * 40)
    print("  System Ready: Object Detection")
    print("  Sensor: GP14 | LED: GP15")
    print("=" * 40)

    # ปิดไฟ LED ก่อนเริ่มทำงาน
    set_led(False)

    # ตัวแปรเก็บสถานะ "ก่อนหน้า" เพื่อเช็คว่ามีการเปลี่ยนแปลงหรือไม่
    # (ป้องกันการ Print รัวๆ ค้างหน้าจอ)
    last_state = None

    while True:
        # อ่านค่า "ปัจจุบัน" ในลูปทุกครั้ง
        current_state = is_detected()

        # ทำงานก็ต่อเมื่อสถานะ "เปลี่ยนไปจากเดิม" เท่านั้น (Edge Detection)
        if current_state != last_state:
            if current_state == True:
                print("[ Alert ] พบวัตถุ!")
                set_led(True)  # เปิดไฟ
            else:
                print("[ Info ] วัตถุหายไปแล้ว")
                set_led(False)  # ปิดไฟ

            # อัปเดตสถานะก่อนหน้า ให้เท่ากับสถานะปัจจุบัน
            last_state = current_state

        # หน่วงเวลา 50 มิลลิวินาที (เพื่อให้บอร์ดไม่ทำงานหนักเกินไป และอ่านค่าได้เสถียร)
        utime.sleep_ms(50)


# สั่งรันฟังก์ชัน main
if __name__ == "__main__":
    main()

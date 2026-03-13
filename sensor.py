from machine import Pin
import utime

# ============================================================
# 1. ตั้งค่า Pin
# ============================================================
SENSOR_PIN = 14
LED_PIN = 15

sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_UP)
ext_led = Pin(LED_PIN, Pin.OUT)

# ตรวจสอบประเภทบอร์ดเพื่อเปิด Onboard LED
try:
    onboard_led = Pin("LED", Pin.OUT)
except (TypeError, ValueError):
    onboard_led = Pin(25, Pin.OUT)

# ============================================================
# 2. ฟังก์ชันเสริม
# ============================================================
def get_stable_state() -> bool:
    """
    อ่านค่าแบบ Debounce: เช็คซ้ำ 3 ครั้งเพื่อให้แน่ใจว่าไม่ใช่สัญญาณรบกวน
    Returns: True ถ้าพบวัตถุ (Active LOW), False ถ้าไม่พบ
    """
    first_read = sensor.value()
    utime.sleep_ms(5) # รอแป๊บเดียวเพื่อเช็คซ้ำ
    second_read = sensor.value()
    
    # ถ้าอ่านได้ 0 ทั้งสองรอบ แสดงว่าเจอวัตถุจริงๆ (ไม่ใช่ Noise)
    if first_read == 0 and second_read == 0:
        return True
    return False

def set_led(state: bool):
    """สั่งเปิด-ปิด LED ทั้งหมด"""
    val = 1 if state else 0
    ext_led.value(val)
    onboard_led.value(val)

# ============================================================
# 3. Main Program
# ============================================================
def main():
    print("=" * 40)
    print("  System Ready: Object Detection (Stable Version)")
    print("  Sensor: GP14 | LED: GP15")
    print("=" * 40)

    set_led(False)

    last_state = get_stable_state()
    
    if last_state:
        print("ตรวจพบวัตถุ")
        set_led(True)
    else:
        print("ระบบว่าง")

    while True:
        current_state = get_stable_state()

        if current_state != last_state:
            if current_state:
                print("[ Alert ] พบวัตถุ! (Detected)")
                set_led(True)
            else:
                print("[ Info ] วัตถุออกไปแล้ว (Cleared)")
                set_led(False)

            # อัปเดตสถานะ
            last_state = current_state

        # หน่วงเวลาลูปหลักเล็กน้อย
        utime.sleep_ms(20)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # ปิดไฟก่อนออกจากโปรแกรมเมื่อกด Stop (Ctrl+C)
        set_led(False)
        print("\nSystem Stopped.")
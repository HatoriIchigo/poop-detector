#!/usr/bin/env python3
"""匂い検出の閾値確認用。3秒ごとにBME688のガス抵抗値を永遠にprintする。

起動直後の数回の中央値をベースラインにして、ratio(現在値/ベースライン)を出す。
VOCが増えるとガス抵抗値は下がるので、ratioが小さいほど臭い。Ctrl+Cで終了。
"""
import statistics
import time

import bme680

INTERVAL = 3  # 秒
BASELINE_COUNT = 5  # ベースラインに使う回数

sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)  # 0x76。だめなら I2C_ADDR_SECONDARY (0x77)
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

samples = []
baseline = None

for i in range(1000000):
    if sensor.get_sensor_data() and sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        if baseline is None:
            samples.append(gas)
            print(f"ベースライン取得中 [{len(samples)}/{BASELINE_COUNT}] gas={gas:.0f} Ω")
            if len(samples) == BASELINE_COUNT:
                baseline = statistics.median(samples)
                print(f"ベースライン={baseline:.0f} Ω")
        else:
            print(f"{time.strftime('%H:%M:%S')}  gas={gas:.0f} Ω  ratio={gas / baseline:.3f}")
    else:
        print("ヒーター安定待ち...")
    time.sleep(INTERVAL)

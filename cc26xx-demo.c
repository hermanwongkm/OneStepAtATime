
#include "contiki.h"
#include "sys/etimer.h"
#include "sys/ctimer.h"
#include "dev/leds.h"
#include "dev/watchdog.h"
#include "random.h"
#include "button-sensor.h"
#include "batmon-sensor.h"
#include "board-peripherals.h"
#include "rf-core/rf-ble.h"

#include "ti-lib.h"

#include <stdio.h>
#include <stdint.h>

PROCESS(cc26xx_demo_process, "cc26xx demo process");
AUTOSTART_PROCESSES(&cc26xx_demo_process);
/*---------------------------------------------------------------------------*/
#if BOARD_SENSORTAG
static struct ctimer mpu_timer;
/*---------------------------------------------------------------------------*/
static void init_mpu_reading(void *not_used);
/*---------------------------------------------------------------------------*/
static void
get_mpu_reading()
{
  //clock_time() returns number of elapsed ticks. CLOCK_SECOND returns number of ticks per second.
  printf("%03u.%03u ", clock_time()/CLOCK_SECOND, (clock_time()%CLOCK_SECOND*8) / 10);
  int value;
  value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_X);
	if(value < 0 ){	
		value = value * -1;	
	}
 printf("%d.%02d ", value / 100, value % 100);

  value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Y);
if(value < 0 ){	
		value = value * -1;	
	}
  printf("%d.%02d ", value / 100, value % 100);
  value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Z);
if(value < 0 ){	
		value = value * -1;	
	}
  printf("%d.%02d \n", value / 100, value % 100);
  ctimer_reset(&mpu_timer);
}

/*---------------------------------------------------------------------------*/
static void
init_mpu_reading(void *not_used)
{
  mpu_9250_sensor.configure(SENSORS_ACTIVE, MPU_9250_SENSOR_TYPE_ALL);
}
#endif
/*---------------------------------------------------------------------------*/
static void
init_sensor_readings(void)
{
#if BOARD_SENSORTAG
  init_mpu_reading(NULL);
#endif
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(cc26xx_demo_process, ev, data)
{

  PROCESS_BEGIN();
  init_sensor_readings();
  ctimer_set(&mpu_timer, CLOCK_SECOND/20.00, get_mpu_reading, NULL);
  while(1) {
    PROCESS_YIELD();
  }

  PROCESS_END();
}
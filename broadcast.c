#include "contiki.h"
#include "dev/leds.h"
#include <stdio.h>
#include "core/net/rime/rime.h"
#include "dev/serial-line.h"
#include "dev/uart1.h"
#include "node-id.h"
#include "defs_and_types.h"
#include "math.h"

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

#include <stdint.h>
#include <string.h>
#include <stdlib.h>

/*---------------------------------------------------------------------------*/
#if BOARD_SENSORTAG

/*
 * Update sensor readings in a staggered fashion every SENSOR_READING_PERIOD
 * ticks + a random interval between 0 and SENSOR_READING_RANDOM ticks
 */
#define SENSOR_READING_PERIOD (CLOCK_SECOND * 0.02)
#define SENSOR_READING_RANDOM (CLOCK_SECOND << 4)

static struct ctimer opt_timer;

static void init_mpu_reading(void *not_used);
static void init_opt_reading(void *not_used);

int lightValue = 1;
/*---------------------------------------------------------------------------*/
static void
get_light_reading()
{
  int tempValue = opt_3001_sensor.value(0);
  if (tempValue != CC26XX_SENSOR_READING_ERROR) {
    printf("Reading error \n");
    lightValue = tempValue;
    printf(tempValue);
    printf("\n");
  }
}
/*---------------------------------------------------------------------------*/
static void
get_mpu_reading(int * arrayOfAxis)
{
  int value;
  value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_X);
	if(value < 0 ){	
		value = -value;	
	}
    arrayOfAxis[0] = value / 100;
    arrayOfAxis[1] = value % 100;
  
  value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Y);
if(value < 0 ){	
		value = -value;	
	}
    arrayOfAxis[2] = value / 100;
    arrayOfAxis[3] = value % 100;
  
  value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Z);
if(value < 0 ){	
		value = -value;	
	}
    arrayOfAxis[4] = value / 100;
    arrayOfAxis[5] = value % 100;
}

/*---------------------------------------------------------------------------*/
static void
init_opt_reading(void *not_used)
{
  SENSORS_ACTIVATE(opt_3001_sensor);
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
  init_opt_reading(NULL);
  init_mpu_reading(NULL);
#endif
}
/*---------------------------------------------------------------------------*/
// sender timer
static struct rtimer rt;
static struct pt pt;
/*---------------------------------------------------------------------------*/
static data_packet_struct received_packet;
static data_packet_struct data_packet;
unsigned long curr_timestamp;
/*---------------------------------------------------------------------------*/
PROCESS(cc2650_comm_process, "cc2650 communication process");
AUTOSTART_PROCESSES(&cc2650_comm_process);
/*---------------------------------------------------------------------------*/
static void
broadcast_recv(struct broadcast_conn *c, const linkaddr_t *from)
{
  memcpy(&received_packet, packetbuf_dataptr(), sizeof(data_packet_struct));

  if(received_packet.dst_id == node_id && node_id == SINK_NODE_ID){
    leds_on(LEDS_RED);
    printf("%d.%02d %d.%02d %d.%02d, %d.%02d \n",received_packet.xaxis1, received_packet.xaxis2, received_packet.yaxis1, received_packet.yaxis2, received_packet.zaxis1, received_packet.zaxis2, received_packet.light1, received_packet.light2);
     // printf("TimeStamp: %3lu.%03lu, x: %d.%02d y: %d.%02d z: %d.%02d,  OPT: Light=%d.%02d lux\n",received_packet.timestamp[0] / 1000, received_packet.timestamp[0] % 1000,received_packet.xaxis1,received_packet.xaxis2,received_packet.yaxis1,received_packet.yaxis2,received_packet.zaxis1,received_packet.zaxis2,received_packet.light1, received_packet.light2 );
    // printf("TimeStamp: %3lu.%03lu, x: %d.%02d y: %d.%02d z: %d.%02d,  OPT: Light=%d.%02d lux\n",data_packet.timestamp[0] / 1000, data_packet.timestamp[0] % 1000,data_packet.xaxis1,data_packet.xaxis2,data_packet.yaxis1,data_packet.yaxis2,data_packet.zaxis1,data_packet.zaxis2, data_packet.light1, data_packet.light2);
    leds_off(LEDS_RED);
  }
}
static const struct broadcast_callbacks broadcast_call = {broadcast_recv};
static struct broadcast_conn broadcast;
/*---------------------------------------------------------------------------*/
float getMagnitude(float x, float y, float z) {
  return sqrt(x*x + y*y + z*z);
}
/*---------------------------------------------------------------------------*/
char sender_scheduler(struct rtimer *t, void *ptr) {
  static uint8_t i = 0;
  int arrayOfData[6];
  static uint8_t j = 0; 
  PT_BEGIN(&pt);
  while(1){
    // leds_on(LEDS_RED);
    data_packet.seq++;
    curr_timestamp = (clock_time()*1e3) / CLOCK_SECOND;
    for(i = 0; i < TIMESTAMP_NUMBERS; i++){
      data_packet.timestamp[i] = curr_timestamp;
      
    }

    if(j % 25 == 0){
      SENSORS_ACTIVATE(opt_3001_sensor);
    }

    get_mpu_reading(arrayOfData);
    data_packet.xaxis1 = arrayOfData[0];
    data_packet.xaxis2 = arrayOfData[1];

    data_packet.yaxis1 = arrayOfData[2];
    data_packet.yaxis2 = arrayOfData[3];

    data_packet.zaxis1 = arrayOfData[4];
    data_packet.zaxis2 = arrayOfData[5];

    j++;

    if(j % 25 == 0){
      printf("before \n");
      get_light_reading();
      printf("after \n");
      data_packet.light1 = lightValue / 100;
      data_packet.light2 = lightValue % 100;
    }

    printf("%d.%02d %d.%02d %d.%02d, %d.%02d \n",data_packet.xaxis1, data_packet.xaxis2, data_packet.yaxis1, data_packet.yaxis2, data_packet.zaxis1, data_packet.zaxis2, data_packet.light1, data_packet.light2);

    packetbuf_copyfrom(&data_packet, (int)sizeof(data_packet_struct));
    broadcast_send(&broadcast);
    leds_off(LEDS_RED);

    rtimer_set(t, RTIMER_TIME(t) + SENDING_RATE, 1, (rtimer_callback_t)sender_scheduler, ptr);
    PT_YIELD(&pt);
  }
  PT_END(&pt);
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(cc2650_comm_process, ev, data)
{
  PROCESS_EXITHANDLER(broadcast_close(&broadcast);)

  PROCESS_BEGIN();
  init_sensor_readings();

  broadcast_open(&broadcast, 129, &broadcast_call);

  // for serial port
  #if !WITH_UIP && !WITH_UIP6
  uart1_set_input(serial_line_input_byte);
  serial_line_init();
  #endif

  printf("node ID: %d", node_id);
  
  if(node_id == SOURCE_NODE_ID) { // source
    printf("CC2650 communication - I'm source\n");
    printf("Will be sending packet of size %d Bytes\n", (int)sizeof(data_packet_struct));
    // initialize data packet
    data_packet.dst_id = SINK_NODE_ID;
    data_packet.seq = 0;

    // Start sender in one millisecond.
    rtimer_set(&rt, RTIMER_NOW() + (RTIMER_SECOND / 1000), 1, (rtimer_callback_t)sender_scheduler, NULL);

  } else if(node_id == SINK_NODE_ID){ // sink
    printf("CC2650 communication - I'm sink\n");
    leds_on(LEDS_GREEN);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
/*	Author: ebramkw
	Typedef and definitions	*/

/*---------------------------------------------------------------------------*/
#define SINK_NODE_ID 27398 // MQTT
// #define SINK_NODE_ID 39430 //Ebram's node 
#define SOURCE_NODE_ID 37379
/*---------------------------------------------------------------------------*/
// #define SENDING_RATE RTIMER_SECOND          // 1 HZ
//#define SENDING_RATE RTIMER_SECOND / 10  // 10 HZ
 #define SENDING_RATE RTIMER_SECOND / 50 // 100 HZ
/*---------------------------------------------------------------------------*/
// #define PACKET_SIZE 12  // size in Bytes
//#define PACKET_SIZE 32  // size in Bytes
 #define PACKET_SIZE 64  // size in Bytes
/*---------------------------------------------------------------------------*/
#define TIMESTAMP_NUMBERS (PACKET_SIZE / 4) - 2
typedef struct {
  unsigned long dst_id;
  unsigned long timestamp[TIMESTAMP_NUMBERS];
  unsigned long seq;
  unsigned int xaxis1;
  unsigned int xaxis2;
  unsigned int yaxis1;
  unsigned int yaxis2;
  unsigned int zaxis1;
  unsigned int zaxis2;
  unsigned int light1;
  unsigned int light2;
} data_packet_struct;
/*---------------------------------------------------------------------------*/

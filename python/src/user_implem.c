/*
 * Implementation of Map, Reduce function for terrasort benchmark.
 * user_implem.c
 *
 *  Created on: 15.07.2012
 *      Author: yaroslav
 */

#include <unistd.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <stddef.h> //size_t
#include <stdio.h> //printf
#include <assert.h>

#include "user_implem.h"
#include "mapreduce/map_reduce_lib.h"
#include "defines.h"
#include "mapreduce/elastic_mr_item.h"
#include "mapreduce/buffered_io.h"
#include "mapreduce/buffer.h"

#include "Python.h"
#include "ztestmodule.h"

extern PyObject* PyComparatorHashFunc;
extern PyObject* PyReduceFunc;
extern PyObject* PyMapFunc;
static int 
ComparatorHash(const void *h1, const void *h2){
  PyObject* args = Py_BuildValue("(s#, s#)", h1, HASH_SIZE, h2, HASH_SIZE);
  PyObject* val = PyObject_CallObject(PyComparatorHashFunc, args);
  Py_DECREF(args);

  int ret = PyInt_AsLong(val);
  Py_DECREF(val);
  return ret;

//  return memcmp(h1,h2, sizeof(HASH_TYPE));
}

static int 
ComparatorElasticBufItemByHashQSort(const void *p1, const void *p2){
    return ComparatorHash( &((ElasticBufItemData*)p1)->key_hash,
			   &((ElasticBufItemData*)p2)->key_hash );
}

/*use ascii key as is for output*/
static char* 
PrintableHash( char* str, const uint8_t* hash, int size){
    memcpy(str, hash, sizeof(HASH_TYPE));
    return str;
}

static inline int 
CanReadRecord( const char* databegin, const char* dataend, int index ){
    if( &databegin[index] + TERRASORT_RECORD_SIZE <= dataend )
	return 1;
    else 
	return 0;
}



/*@return record size if OK or 0 if can't not read a whole record*/
static inline int 
DirectReadRecord( const char* databegin, const char* dataend, 
		  struct ElasticBufItemData* record, int *index ){
    const char* c = &databegin[*index];

    /*set key data: pointer + key data length. using pointer to existing data*/
    record->key_data.addr = (uintptr_t)c;
    record->key_data.size = HASH_SIZE;
    record->own_key = EDataNotOwned;
    /*save as hash record key without changes to variable length struct member*/
    memcpy( &record->key_hash, c, HASH_SIZE );
    /*interpret elasticdata->value.addr as 4bytes pointer and save data as binary*/
    record->value.size = TERRASORT_RECORD_SIZE - HASH_SIZE;
    record->value.addr = (uintptr_t)c + HASH_SIZE;
    record->own_value = EDataNotOwned;
    /*update current pos*/
    (*index) += TERRASORT_RECORD_SIZE;
    return TERRASORT_RECORD_SIZE;
}

/*******************************************************************************
 * User map for MAP REDUCE
 * Readed data will organized as MrItem with a 
 * 10bytes key, 90bytes data and 10bytes hash exactly equal to the key
 * @param size size of data must be multiple on 100, 
 * set MAP_CHUNK_SIZE env variable properly*/
int Map(const char *data, 
	size_t size, 
	int last_chunk, 
	Buffer *map_buffer ){

  assert(PyMapFunc);
  fprintf(stderr, "before buffer count = %d, size = %d \n", map_buffer->header.count,
          map_buffer->header.buf_size);

  // create arguments for Reduce function call
  // MapReduceBuffer to fill
  PyObject* MapReduceBuffer = MapReduceBuffer_FromBuffer(map_buffer);
  // buffer and memoryview to scan for raw data
  Py_buffer* buffer = (Py_buffer*) malloc(sizeof(Py_buffer));
  PyBuffer_FillInfo(buffer, NULL, data, size, 0, PyBUF_CONTIG);
  PyObject* mv = PyMemoryView_FromBuffer(buffer);
  // size and last_chunk vars
  PyObject* args = Py_BuildValue("(OniO)",
                                 mv,
                                 size,
                                 last_chunk,
                                 MapReduceBuffer);
  // call python reduce routine
  PyObject* val = PyObject_CallObject(PyMapFunc, args);
//  TODO: uncomment and fix that!
  //  Py_DECREF(args);

  if (!val) {
    // error happened
    return -1;
  }

  fprintf(stderr, "after buffer count = %d, size = %d \n", map_buffer->header.count,
          map_buffer->header.buf_size);

  int ret = PyInt_AsLong(val);
  Py_DECREF(val);
  return ret;

//  ElasticBufItemData* elasticdata;
//  int current_pos = 0;
//  while( CanReadRecord( data, data+size, current_pos) == 1 ){
//    /*it's guarantied that item space will reserved in buffer, and no excessive
//    copy doing, elasticdata points directly to buffer item*/
//    elasticdata = (ElasticBufItemData*)
//                  BufferItemPointer(map_buffer,
//                                    AddBufferItemVirtually(map_buffer) );
//    /*read directly into cell of array*/
//    DirectReadRecord( data, data+size, elasticdata, & );
//  }
//  /*return real handled data pos*/
//  return current_pos;
}

int Reduce( const Buffer *reduced_buffer ){
  assert(PyReduceFunc);

  // create arguments for Reduce function call
  PyObject* MapReduceBuffer = MapReduceBuffer_FromBuffer((Buffer*)reduced_buffer);
  PyObject* args = Py_BuildValue("(O)", MapReduceBuffer);
  // call python reduce routine
  PyObject* val = PyObject_CallObject(PyReduceFunc, args);
  Py_DECREF(args);

  if (!val) {
    // error happened
    return -1;
  }

  int ret = PyInt_AsLong(val);
  Py_DECREF(val);

  // do cleanup after pyreduce
  for ( int i=0; i < reduced_buffer->header.count; i++ ){
    ElasticBufItemData* elasticdata = (ElasticBufItemData*)BufferItemPointer( reduced_buffer, i );
    TRY_FREE_MRITEM_DATA(elasticdata);
  }
  return ret;



  //    BufferedIOWrite* bio = AllocBufferedIOWrite( malloc(IO_BUF_SIZE), IO_BUF_SIZE);

//    /*declare buf item to use it as current loop item*/
//    ElasticBufItemData* elasticdata;
//    HASH_TYPE prev_key;
//    for ( int i=0; i < reduced_buffer->header.count; i++ ){
//	elasticdata = (ElasticBufItemData*)BufferItemPointer( reduced_buffer, i );

//	bio->write(bio, STDOUT, (void*)elasticdata->key_data.addr, elasticdata->key_data.size);
//	bio->write(bio, STDOUT, (void*)elasticdata->value.addr, elasticdata->value.size);

//	/*test data sorted by hash*/
//	HASH_TYPE* keyhash = (HASH_TYPE*)&elasticdata->key_hash;
//	if ( i>0 && ComparatorHash(&prev_key, keyhash) >0 ){
//	    bio->flush_write(bio, STDOUT);
//	    printf("test failed prev_key=%s, key=%s\n",
//		   PrintableHash(alloca(HASH_STR_LEN), (const uint8_t *)&prev_key, HASH_SIZE),
//		   PrintableHash(alloca(HASH_STR_LEN), (const uint8_t *)keyhash, HASH_SIZE) );
//	    fflush(0);
//	    exit(-1);
//	}

//	memcpy( &prev_key, &elasticdata->key_hash, HASH_SIZE );
//	TRY_FREE_MRITEM_DATA(elasticdata);
//    }
//    bio->flush_write(bio, STDOUT);

//    free(bio->data.buf);     /*free buffer in this way because not saved pointer*/
//    WRITE_LOG("OK");
//    free(bio);
//    return 0;
}


void InitInterface( struct MapReduceUserIf* mr_if ){
    memset( mr_if, '\0', sizeof(struct MapReduceUserIf) );
    PREPARE_MAPREDUCE(mr_if, 
		      Map, 
		      NULL, 
		      Reduce, 
		      ComparatorElasticBufItemByHashQSort,
		      ComparatorHash,
		      PrintableHash,
          0,
		      ALIGNED_RECORD_SIZE,
          HASH_SIZE );
}



/*
 * defines.h
 *
 *  Created on: 14.07.2012
 *      Author: yaroslav
 */

#ifndef DEFINES_H_
#define DEFINES_H_

#define DEBUG

#define ENV_MAP_NODE_NAME "MAP_NAME"
#define ENV_REDUCE_NODE_NAME "REDUCE_NAME"

#define STDIN  0
#define STDOUT 1 //fd

struct TerrasortHashKey{
    char hash[10];
};

#define HASH_TYPE         struct TerrasortHashKey
#define HASH_SIZE         sizeof(HASH_TYPE)
#define HASH_STR_LEN      HASH_SIZE*2+1
#define IO_BUF_SIZE       0x100000

#define TERRASORT_RECORD_SIZE 100
#define ALIGNED_RECORD_SIZE sizeof(		\
    struct{					\
	BinaryData     key_data;		\
	BinaryData     value;			\
	uint8_t        own_key;			\
	uint8_t        own_value;		\
	HASH_TYPE      key_hash;		\
    })


/*Default data value for new Map items*/
#define DEFAULT_INT_VALUE 1
#define DEFAULT_STR_VALUE "1"

#ifdef DEBUG
/*use OUTPUT_HASH_KEYS option only for debugging purposes, output file contains 
 *values and hashes and their size even bigger than input data size */
/* #  define OUTPUT_HASH_KEYS */
#endif //DEBUG

#ifdef DEBUG
#  ifndef WRITE_FMT_LOG
#    define WRITE_FMT_LOG(fmt, args...) fprintf(stderr, fmt, args)
#    define WRITE_LOG(str) fprintf(stderr, "%s\n", str)
#  endif
#else
#  ifndef WRITE_FMT_LOG
#    define WRITE_FMT_LOG(fmt, args...)
#    define WRITE_LOG(str)
#  endif
#endif


#endif /* DEFINES_H_ */

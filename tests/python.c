#include <Python.h>
#include <zmapreducemodule.h>

#define BUFFER_SIZE 1*1024*1024

int main(int argc, char** argv) {
  PyObject* module;
  PyObject* dictionary;
  PyObject* mv;

  char* data;


  Py_Initialize();
  data = (char*) malloc(BUFFER_SIZE);
  int i;
  // read from terasort/wordcount data
  for (i=0;i<BUFFER_SIZE;++i)
    data[i] = i + 48;

  // borrowed, no decref
  module = PyImport_AddModule("__main__");
  assert(module);

  // borrowed, no decref
  dictionary = PyModule_GetDict(module);
  assert(dictionary);


  // inject raw data into module
  Py_buffer* buffer = (Py_buffer*) malloc(sizeof(Py_buffer));
  PyBuffer_FillInfo(buffer, NULL, data, BUFFER_SIZE, 0, PyBUF_CONTIG);
  mv = PyMemoryView_FromBuffer(buffer);
  assert (!PyDict_SetItemString(dictionary, "data", mv));

  // inject buffer object into module
  Buffer mr_buffer;
  AllocBuffer(&mr_buffer, 28 /* ??? */, 1024);
  PyObject* MapReduceBuffer = MapReduceBuffer_FromBuffer(&mr_buffer);
  printf("rc=%d\n", MapReduceBuffer->ob_refcnt);
  assert (!PyDict_SetItemString(dictionary, "buffer", MapReduceBuffer));
  printf("rc=%d\n", MapReduceBuffer->ob_refcnt);
  Py_DECREF(MapReduceBuffer);
  printf("rc=%d\n", MapReduceBuffer->ob_refcnt);

  // ok, now we read to run py interpreter: command, string, file
  int py_argc = 2;
  char* py_argv[] = {"python", "/dev/test.py"};
  assert(!Py_Main(py_argc, py_argv));
  printf("rc=%d\n", MapReduceBuffer->ob_refcnt);

  printf("rc=%d\n", MapReduceBuffer->ob_refcnt);
  PyBuffer_Release(buffer);
  printf("rc=%d\n", MapReduceBuffer->ob_refcnt);
  Py_DECREF(mv);
  printf("rc=%d\n", MapReduceBuffer->ob_refcnt);
  free(buffer);

  fprintf(stdout, "refcount=%d\n", MapReduceBuffer->ob_refcnt);
  Py_Finalize();
  return 0;
}

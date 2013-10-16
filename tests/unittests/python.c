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

  Buffer mr_obuffer; // output buffer
  AllocBuffer(&mr_obuffer, 28 /* ??? */, 1024);
  PyObject* MapReduceOBuffer = MapReduceBuffer_FromBuffer(&mr_obuffer);

  assert (!PyDict_SetItemString(dictionary, "buffer", MapReduceBuffer));
  assert (!PyDict_SetItemString(dictionary, "obuffer", MapReduceOBuffer));
  Py_DECREF(MapReduceBuffer);
  Py_DECREF(MapReduceOBuffer);

  // ok, now we read to run py interpreter: command, string, file
  int py_argc = 2;
  char* py_argv[] = {"python", "/dev/test.py"};
  assert(!Py_Main(py_argc, py_argv));
  PyBuffer_Release(buffer);
  Py_DECREF(mv);
  free(buffer);

  Py_Finalize();
  return 0;
}

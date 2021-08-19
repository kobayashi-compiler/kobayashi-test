#ifndef __SYLIB_H_
#define __SYLIB_H_

#include <stdio.h>
#include <stdarg.h>
#include <sys/time.h>
/* Input & output functions */

#ifdef __cplusplus
extern "C" {
#endif

int getint(), getch(), getarray(int a[]);
void putint(int a), putch(int a), putarray(int n, int a[]);
#define putf(fmt, ...) printf(fmt, __VA_ARGS__) // TODO?
/* Timing function implementation */
#define starttime() _sysy_starttime(__LINE__)
#define stoptime() _sysy_stoptime(__LINE__)
#define _SYSY_N 1024
#define true True
__attribute((constructor)) void before_main();
__attribute((destructor)) void after_main();
void _sysy_starttime(int lineno);
void _sysy_stoptime(int lineno);

#ifdef __cplusplus
}
#endif

#endif

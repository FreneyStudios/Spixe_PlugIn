#!/usr/bin/env python3
#/*--
#
# Copyright (c) 2025  Frêney Studios
#
# Module Name:
#
#	 spixe.py
#
# Abstract:
#
#	 Spixe Python decorators (Open-source)
#
# Author:
#
#	 Marco Panseri (Marx) 12-05-2025
#
# Revision History:
#
#--*/

# IMPORTS
import os
import sys
import functools
import time

# BASIC INFO
__version__ = "v.0.0.1"
__doc__     = f""" 

Copyright (c) 2025 Frêney Studios Holdings
Spixe {__version__}, Python Decorators lib

"""

# BASE class
class BASE:
    def MARKER(func):
        def wrapper(*args, **kwargs):
            """ BASE.MARKER(func) : marks a function execution"""
            print("Before function execution")
            result = func(*args, **kwargs)
            print("After function execution")
            return result 
        return wrapper

    def HANDLE(func):
        def wrapper(*args, **kwargs):
            """ BASE.HANDLE(func) : handles RAI exceptions during a function execution"""
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                print("Error: " + str(e))
            return result 
        return wrapper
    
    def SKIP_IF_TRUE(func, boolean : bool):
        def wrapper(*args, **kwargs):
            """ BASE.SKIP_IF_TRUE(func, boolean) : skip function execution if boolean is True (1)"""
            if not boolean:
                result = func(*args, **kwargs)
                
            return result 
        return wrapper

    def SKIP_IF_FALSE(func, boolean : bool):
        def wrapper(*args, **kwargs):
            """ BASE.SKIP_IF_FALSE(func, boolean) : skip function execution if boolean is False (0)"""
            if  boolean:
                result = func(*args, **kwargs)
                
            return result 
        return wrapper
    
    def ARGS_CHECK(func, boolean : bool):
        def wrapper(*args, **kwargs):
            """ BASE.ARGS_CHECK(func, boolean) : skip function execution if boolean is False (0)
                This decorator is specific for *args **kwargs checking 
            """
            if  boolean:
                result = func(*args, **kwargs)
                
            return result 
        return wrapper
    

def HOOK_TRACE(*exec_funcs): # The decorator itself now takes arguments (the functions to execute)
    """
    Decorator factory that executes a list of specified functions
    before and/or after the decorated function.

    Args:
        *exec_funcs: A variable number of callable objects (functions)
                     that should be executed when the decorated function runs.
                     These functions will receive the same *args and **kwargs
                     as the decorated function.
    """
    def decorator(func): # This is the actual decorator returned by HOOK_TRACE
        """
        The decorator that wraps 'func'.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that executes the specified hook functions
            and then the decorated function.
            """
            func_name = func.__name__
            
            # --- Step 1: Execute the hook functions BEFORE the decorated function ---
            # print(f"--- HOOK_TRACE for '{func_name}' ---")
            # print(f"  Executing {len(exec_funcs)} pre-hook functions:")
            
            hook_results = []
            for i, hook_func in enumerate(exec_funcs):
                if callable(hook_func):
                    hook_func_name = getattr(hook_func, '__name__', str(hook_func))
                    # print(f"    Calling hook[{i}]: '{hook_func_name}' with args={args}, kwargs={kwargs}")
                    try:
                        hook_start_time = time.perf_counter()
                        hook_res = hook_func(*args, **kwargs) # Pass the decorated function's args/kwargs to the hook functions
                        hook_end_time = time.perf_counter()
                        hook_exec_time_ms = (hook_end_time - hook_start_time) * 1000
                        # print(f"      -> '{hook_func_name}' finished (took {hook_exec_time_ms:.2f}ms). Result: {repr(hook_res)}")
                        hook_results.append((hook_func_name, hook_res))
                    except Exception as e:
                        # print(f"      -> Error in hook '{hook_func_name}': {type(e).__name__}: {e}")
                        hook_results.append((hook_func_name, f"ERROR: {e}"))
                else:
                    # print(f"    Warning: Item at index {i} ({repr(hook_func)}) is not callable. Skipping.")
                    pass

            # --- Step 2: Execute the decorated function itself ---
            # print(f"  Executing decorated function: '{func_name}' with args={args}, kwargs={kwargs}")
            main_func_start_time = time.perf_counter()
            try:
                main_func_result = func(*args, **kwargs)
            except Exception as e:
                main_func_end_time = time.perf_counter()
                main_func_exec_time_ms = (main_func_end_time - main_func_start_time) * 1000
                # print(f"  Error in '{func_name}' after {main_func_exec_time_ms:.2f}ms: {e}")
                raise # Re-raise the exception

            main_func_end_time = time.perf_counter()
            main_func_exec_time_ms = (main_func_end_time - main_func_start_time) * 1000
            # print(f"  '{func_name}' finished (took {main_func_exec_time_ms:.2f}ms). Result: {repr(main_func_result)}")
            # print(f"--- HOOK_TRACE for '{func_name}' Finished ---")

            return main_func_result # Return the result of the decorated function

        return wrapper
    return decorator
    


# DUMMY-ENTRY
if __name__ == "__main__":
    print(__doc__)


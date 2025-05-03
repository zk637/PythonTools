# trace_context.py
import uuid
import time
import inspect
import importlib
from datetime import datetime
from functools import wraps
import contextvars
from ResourceExplorer import ResourceMonitor
import model
# 注册模块对象
from model import tips_m, log_info_m, result_m

# 使用 contextvars，适配线程/异步
trace_id_ctx = contextvars.ContextVar("trace_id", default=None)
parent_span_id_ctx = contextvars.ContextVar("parent_span_id", default=None)


def new_trace():
    """生成新的 trace_id 并重置父级 span_id"""
    trace_id = str(uuid.uuid4())
    trace_id_ctx.set(trace_id)
    parent_span_id_ctx.set(None)
    return trace_id


def start_span():
    trace_id = trace_id_ctx.get()
    if not trace_id:
        # 如果没有 trace_id，则自动初始化一个新的 trace
        trace_id = uuid.uuid4().hex  # 或者调用 new_trace()，不过要注意不要重复覆盖
        trace_id_ctx.set(trace_id)
    parent_span_id = parent_span_id_ctx.get()
    span_id = uuid.uuid4().hex
    # 这里简单设置：当前 span 作为父级传递给下一层（如果需要完整嵌套栈，可考虑维护一个栈）
    parent_span_id_ctx.set(span_id)
    return {
        "trace_id": trace_id,
        "span_id": span_id,
        "parent_span_id": parent_span_id
    }

def end_span():
    """结束 span（简化：不做栈结构）"""
    parent_span_id_ctx.set(None)

def trace_with_attrs(name=None):
    if callable(name):
        func = name
        name = None

        if getattr(func, "_is_traced", False):
            return func  # 🛑 已装饰，直接返回

        @wraps(func)
        def wrapper(*args, **kwargs):
            span = start_span()
            start_time = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                duration = int((time.time() - start_time) * 1000)
                ResourceMonitor.get_instance().record_trace_span({
                    "name": func.__name__,
                    "trace_id": span["trace_id"],
                    "span_id": span["span_id"],
                    "parent_span_id": span["parent_span_id"],
                    "duration_ms": duration
                })
                end_span()
        wrapper._is_traced = True  # ✅ 打标记
        return wrapper

    def decorator(func):
        if getattr(func, "_is_traced", False):
            return func  # 🛑 已装饰，直接返回

        @wraps(func)
        def wrapper(*args, **kwargs):
            span = start_span()
            start_time = time.time()
            start = datetime.now()
            print(f"[Trace] {func.__name__}  {start.isoformat()}")
            try:
                return func(*args, **kwargs)
            finally:
                duration = int((time.time() - start_time) * 1000)
                ResourceMonitor.get_instance().record_trace_span({
                    "name": name or func.__name__,
                    "trace_id": span["trace_id"],
                    "span_id": span["span_id"],
                    "parent_span_id": span["parent_span_id"],
                    "duration_ms": duration
                })
                end_span()
        wrapper._is_traced = True  # ✅ 打标记
        return wrapper
    return decorator


def register_tracing_for_function(function):
    module = inspect.getmodule(function)
    if module:
        module_name = module.__name__
        log_info_m.print_message(f"Registering tracing for all functions in module: {module_name}")

        try:
            module_obj = importlib.import_module(module_name)
            for name, func in inspect.getmembers(module_obj, inspect.isfunction):
                # ✅ 跳过 trace 自己
                if func.__name__ in {"wrapper", "wraps", "trace_with_attrs", "register_tracing_for_function" ,"profile_all_functions"}:
                    continue
                if getattr(func, "_is_traced", False):
                    continue  # 已装饰，跳过
                decorated_func = trace_with_attrs()(func)
                setattr(module_obj, name, decorated_func)
                log_info_m.print_message(f"Function {name} in module {module_name} has been traced.")
        except Exception as e:
            log_info_m.print_message(f"Error while loading or processing module {module_name}: {e}")
    else:
        log_info_m.print_message(f"Could not find the module for the function {function.__name__}")



def register_tracing_for_user_input(methods,user_input_index):
    """
    根据用户输入的索引，从 methods 字典获取函数，并为该函数所在模块的所有函数注册装饰器。
    """
    try:
        # 从 methods 字典中获取函数
        selected_function = methods.get(user_input_index)

        if selected_function:
            # 注册该函数所在模块的所有函数
            register_tracing_for_function(selected_function)
        else:
            print(f"Invalid function index {user_input_index}.")

    except Exception as e:
        print(f"Error while processing user input: {e}")
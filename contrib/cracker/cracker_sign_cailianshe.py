from core.base.utils import u_javascript

filepath = r'E:\Projects\auto_datahandler\resource\cailianshe_sign.js'
executor = u_javascript.Executor_Javascript.execute_jsfile(filepath=filepath)
print(u_javascript.Executor_Javascript.execute_jsfunc(executor, 'getsign'))
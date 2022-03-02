"""
    采用方式：
        1. 注解的方式
            发现注解会先调用注解的内容，而我们希望在上传成功之后再打印结果，因此不适合用注解
        2. 调用的方式打印日志
            在上传成功后打印

"""
def logger_comment(func):
    def decorate(lis_totle, lis_success, lis_failed):
        print("上传日志：")
        print('上传评论总数据数目：', len(lis_totle), ' 成功上传数目：', len(lis_success), ' 失败上传数目：', len(lis_failed))
        print(' - 成功上传的记录：')
        for li in lis_success:
            print('   ', li)
        return func(lis_totle, lis_success, lis_failed)
    return decorate






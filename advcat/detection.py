
from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_util import models as util_models
import json
import uuid



def detection(ak,sk,text) -> None:
    service_parameters = {
            'content': text,
            'dataId': str(uuid.uuid1())
    }
    if service_parameters.get("content") is None or len(service_parameters.get("content").strip()) == 0:
        print("text moderation content is empty")
        return
    text_moderation_request = models.TextModerationRequest(
            # 文本检测service：内容安全控制台文本增强版规则配置的serviceCode，示例：chat_detection
            service = 'ad_compliance_detection',
            service_parameters = json.dumps(service_parameters)
        )
    config = Config(
            # 阿里云账号AccessKey拥有所有API的访问权限，建议您使用RAM用户进行API访问或日常运维。
            # 强烈建议不要把AccessKey ID和AccessKey Secret保存到工程代码里，否则可能导致AccessKey泄露，威胁您账号下所有资源的安全。
            # 常见获取环境变量方式：
            # 获取RAM用户AccessKey ID：os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
            # 获取RAM用户AccessKey Secret：os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
            access_key_id=ak,
            access_key_secret=sk,
            # 连接时超时时间，单位毫秒（ms）。
            connect_timeout=3000,
            # 读取时超时时间，单位毫秒（ms）。
            read_timeout=6000,
            # 接入区域和地址请根据实际情况修改。
            region_id='cn-shanghai',
            endpoint='green-cip.cn-shanghai.aliyuncs.com'
    )
    # 注意，此处实例化的client请尽可能重复使用，避免重复建立连接，提升检测性能。
    client = Client(config)

    # 创建RuntimeObject实例并设置运行参数。
    runtime = util_models.RuntimeOptions()
    runtime.read_timeout = 10000
    runtime.connect_timeout = 10000
    try:
        response = client.text_moderation_with_options(text_moderation_request, runtime)
        # 自动路由
        if UtilClient.equal_number(500, response.status_code) or not response or not response.body or 200 != response.body.code:
            # 服务端错误，区域切换到cn-beijing
            config.region_id = 'cn-beijing'
            config.endpoint = 'green-cip.cn-beijing.aliyuncs.com'
            client = Client(config)
            response = client.text_moderation_with_options(text_moderation_request, runtime)

        if response.status_code == 200:
            # 调用成功。
            # 获取审核结果。
            result = response.body
            print('response success. result:{}'.format(result))
            if result.code == 200:
                resultData = result.data
                print('labels:{}, reason:{}'.format(resultData.labels, resultData.reason))
        else:
            print('response not success. status:{} ,result:{}'.format(response.status_code, response))
    except Exception as err:
        print(err)
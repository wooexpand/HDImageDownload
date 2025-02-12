# 设置WebDriver路径
import requests
import re
import math
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import argparse

def extract_group_id(url):
    # 使用正则表达式匹配 /Online/ 后面的一串数字
    match = re.search(r'/Online/(\d+)/', url)
    if match:
        return match.group(1)
    else:
        return None
    
def main(url):
    print("Hello World")
    # 打开拍品详情页
    # url = 'https://bruun-rasmussen.dk/m/lots/A7EA1EB4A145?category_id=462'
    #url = 'file:///C:/00_Development/BruunRasmussenPictureDownload/sample.html'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 使用显式等待确保元素加载完成
    try:
        # 使用选择器匹配特定的 div 和 a 标签
        links = soup.select('li[id^="image_"] a')

        # 提取 href 属性并保存到列表
        images_url = []
        for link in links:
            href = link.get('href')
            print(href)
            if href:
                images_url.append("https://bruun-rasmussen.dk/"+  href)
        # 打印结果
        for image_url in images_url:
            subresponse = requests.get(image_url)
            subsoup = BeautifulSoup(subresponse.text, 'html.parser')
            # 查找具有特定 id 的 div 元素
            div_element = subsoup.find('div', id='zoom-viewer')

            # 提取 data-image-url 属性
            if div_element:
                data_image_url = div_element.get('data-image-url')
                print(data_image_url)
                # 确保 URL 是完整的
                if data_image_url.startswith("//"):
                    data_image_url = "https:" + data_image_url

                # 下载 JSON 文件
                response = requests.get(data_image_url)
                json_data = response.json()

                # 提取 width 和 height
                width = json_data.get('width')
                height = json_data.get('height')

                # 提取 group_id 和 image_id
                # 假设 URL 格式为 .../Online/{group_id}/br_{image_id}.tif/info.json
                url_parts = data_image_url.split('/')
                type_id = url_parts[4]
                group_id = url_parts[-3]
                #image_id = url_parts[-2].split('_')[1].split('.')[0]
                image_id = url_parts[-2].split('.')[0]

                if width > 2400:
                    # width整除2400计算需要几次下载
                    x=math.ceil(width/2400)
                else:
                    x=1
                if height > 2400:
                    y=math.ceil(height/2400)
                else:
                    y=1
                # 下载图片的计数器
                counter=0
                if x>1 or y>1:
                    combined_image = Image.new('RGB', (width, height))

                    for i in range(x):
                        x_start_position=i*2400
                        if i<x-1:
                            size_x=2400
                        else:
                            size_x=width  - i*2400
                        for j in range(y):
                            y_start_position=j*2400
                            if j<y-1:
                                size_y=2400
                            else:
                                size_y=height  - j*2400
                            
                            counter+=1
                            print(x_start_position,size_x,y_start_position,size_y)
             
                            # 构建文件名
                            file_name = f"br_{group_id}_{image_id}_{counter}.jpg"
                            file_download_url=f"https://img.bruun-rasmussen.dk/iiif/{type_id}/{group_id}/{image_id}.tif/{x_start_position},{y_start_position},{size_x},{size_y}/{size_x},{size_y}/0/default.jpg"
                            print(file_name)
                            print(file_download_url)
                            # 下载图片
                            response = requests.get(file_download_url)
                            image = Image.open(BytesIO(response.content))

                            combined_image.paste(image, (x_start_position,y_start_position))
                            #with open("./images/"+file_name, 'wb') as file:
                            #    file.write(response.content)
                    combined_image.save("./images/"+f"br_{group_id}_{image_id}_{width}_{height}.jpg")
                else:
                    # 构建文件名
                    file_name = f"br_{group_id}_{image_id}_{width}_{height}.jpg"
                    file_download_url=f"https://img.bruun-rasmussen.dk/iiif/Online/{group_id}/{image_id}.tif/full/{width},{height}/0/default.jpg"
                    print(file_name)
                    print(file_download_url)
                    # 下载图片
                    response = requests.get(file_download_url)
                    with open("./images/"+file_name, 'wb') as file:
                        file.write(response.content)
            else:
                print("未找到指定的 div 元素")

    except Exception as e:
        print("Error: ", e)
        exit()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a URL.')
    parser.add_argument('url', type=str, help='The URL to process')
    args = parser.parse_args()
    
    main(args.url)


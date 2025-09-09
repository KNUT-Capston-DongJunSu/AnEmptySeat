# your_app/views.py

from django.shortcuts import render
from src.utils.json_handler import load_json_data

def display_crawled_images(request):
    # 사용자로부터 받은 JSON 데이터 (실제로는 DB에서 가져오거나 다른 방식으로 받게 됩니다)
    # crawled_data = {
    #     "creator": "Junhee",
    #     "datetime": "2025-09-07T22:02:00.140670",
    #     "source": "https://map.naver.com/",
    #     "place_number": "1094965330",
    #     "image_links": [
    #         "https://pup-review-phinf.pstatic.net/MjAyNTA0MDNfMjMw/MDAxNzQzNjU3OTcyNzc0.OV4PqXf-kwOK73oI7g3UhYteZynaD_9oVGS12Ta5OOEg.NfzBdRF5KOC1v7QLd0aZM-Mie26yW9zVg6hPr4cdPqcg.JPEG/C2FAF67C-5F49-48E0-95F5-711FA028BCE9.jpeg?type=w560_sharpen",
    #         "https://pup-review-phinf.pstatic.net/MjAyNDExMjhfMjMg/MDAxNzMyNzYyOTg0NDg4.534Gotxg-MEOVr-P4we1FpttLuf7oFfhcZ-VbkUkw4Eg.utTzpHWO3Y001k8awbsSyQGi-X1nwdRyoHaJV5pTfoYg.JPEG/DEE394B3-B96D-430C-A15D-4FC1F93C8713.jpeg?type=w560_sharpen",
    #         "https://pup-review-phinf.pstatic.net/MjAyNDA2MDZfMjYx/MDAxNzE3NjU0MDU5NTI5.cMlm79GgEHw21zrvMZDYt2e3ip-0NXcqwJUz9-BHpyAg.A6tW1qrjv4G98HT-7UTnfijr53Y-vJbmhiNwetSblyYg.JPEG/2025AEAF-5464-4498-9DBA-93590168F98F.jpeg?type=w560_sharpen",
    #         "https://pup-review-phinf.pstatic.net/MjAyNDA2MDZfMzUg/MDAxNzE3NjU0MDU5NzQ2.0IshOPYuE3VAc6RMU-iLhCkMDEpll90c-1JLrUtszycg.KhWLbyoWLLiB9ikXOAb-cBLx61jQ3OszF68a0dKVVbcg.JPEG/E13643BE-4F9D-4DD6-9A5A-96D34F8D6061.jpeg?type=w560_sharpen",
    #         "https://pup-review-phinf.pstatic.net/MjAyNDA2MDZfOTkg/MDAxNzE3NjU0MDU5ODAy.i4kPdRYLiDprK0ip7or_8Z5IiW4DqeGRxogxynbUeSAg.sJhrR-h2IaIxj2P1fhEJrz8WHh3uuxuywOXXY9_5y8kg.JPEG/25E57068-D3F0-46D0-B042-BE5463D4B230.jpeg?type=w560_sharpen"
    #     ]
    # }

    crawled_data = load_json_data(json_path="1094965330.json")

    # 이미지 링크 리스트를 추출합니다.
    image_links = crawled_data.get("image_links", [])

    # context 딕셔너리에 담아서 템플릿으로 전달합니다.
    context = {
        'images': image_links
    }

    # render 함수를 사용해 HTML 파일을 렌더링합니다.
    return render(request, 'your_app/image_gallery.html', context)
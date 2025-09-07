import os
import re
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse, HttpResponseNotFound
from django.conf import settings

range_re = re.compile(r'bytes\s*=\s*(\d+)-(\d*)', re.I)

class RangeFileWrapper:
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If length not given, just read in blocks
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data

def stream_video(request, file_name):
    # 비디오 파일의 경로를 설정합니다.
    # 실제 프로덕션 환경에서는 이 부분을 모델과 연결하거나 더 안전한 방법을 사용해야 합니다.
    video_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(video_path):
        return HttpResponseNotFound("File not found")

    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(video_path)
    content_type = 'video/mp4' # 파일에 맞는 content_type으로 변경하세요.

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(video_path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = f'bytes {first_byte}-{last_byte}/{size}'
    else:
        # Range 헤더가 없을 경우, 전체 파일을 스트리밍합니다.
        resp = StreamingHttpResponse(FileWrapper(open(video_path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)

    resp['Accept-Ranges'] = 'bytes'
    return resp

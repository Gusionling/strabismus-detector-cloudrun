from google.cloud import storage
import os
import tempfile
from datetime import datetime

class CloudStorageClient:
    def __init__(self, bucket_name=None):
        """
        Google Cloud Storage 클라이언트 초기화

        Args:
            bucket_name: 사용할 GCS 버킷 이름. 환경 변수에서 가져오거나 인자로 전달
        """
        self.bucket_name = bucket_name or os.environ.get('GCS_BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("버킷 이름이 지정되지 않았습니다. 환경 변수 GCS_BUCKET_NAME을 설정하거나 초기화 시 전달하세요.")

        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_from_memory(self, data, destination_blob_name, content_type="image/jpeg"):
        """
        메모리에서 직접 데이터를 GCS에 업로드

        Args:
            data: 업로드할 바이너리 데이터
            destination_blob_name: GCS에 저장될 경로 및 파일명
            content_type: 업로드할 파일의 MIME 타입

        Returns:
            업로드된 객체의 공개 URL
        """
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_string(data, content_type=content_type)
        return blob.public_url

    def upload_file(self, source_file_path, destination_blob_name, content_type="image/jpeg"):
        """
        로컬 파일을 GCS에 업로드

        Args:
            source_file_path: 업로드할 로컬 파일 경로
            destination_blob_name: GCS에 저장될 경로 및 파일명
            content_type: 업로드할 파일의 MIME 타입

        Returns:
            업로드된 객체의 공개 URL
        """
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path, content_type=content_type)
        return blob.public_url

    def upload_cv2_image(self, cv2_img, destination_blob_name, content_type="image/jpeg"):
        """
        OpenCV 이미지를 GCS에 업로드

        Args:
            cv2_img: OpenCV로 처리된 이미지 객체
            destination_blob_name: GCS에 저장될 경로 및 파일명
            content_type: 업로드할 파일의 MIME 타입

        Returns:
            업로드된 객체의 공개 URL
        """
        import cv2
        import numpy as np

        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_path = temp_file.name

        # 이미지 저장
        cv2.imwrite(temp_path, cv2_img)

        try:
            # GCS에 업로드
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(temp_path, content_type=content_type)
            return blob.public_url
        finally:
            # 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def generate_filename(self, prefix='image', extension='jpg'):
        """
        타임스탬프를 이용한 고유한 파일명 생성

        Args:
            prefix: 파일명 접두사
            extension: 파일 확장자

        Returns:
            생성된 파일명
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        return f"{prefix}_{timestamp}.{extension}"
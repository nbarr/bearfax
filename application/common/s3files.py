# -*- coding: utf-8 -*-

import base64
from boto3.session import Session
from io import StringIO, BytesIO
from application.common.formatters import safe_join


def decode_metadata(metadata):
    decoded = {}

    if metadata:
        for key, value in metadata.items():
            if isinstance(value, str) and value.startswith('base64_'):
                value = base64.b64decode(value[7:]).decode('utf-8')

            decoded[key] = value

    return decoded


def encode_metadata(metadata):
    encoded = {}

    if metadata:
        for key, value in metadata.items():
            if type(value) != str:
                value = str(value)

            if not value.startswith('base64_'):
                value = 'base64_' + base64.b64encode(str(value).encode('utf8')).decode('utf-8')

            encoded[key] = value

    return encoded


def s3_get_file(key, secret, bucket, filename, prefix=''):
    try:
        s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
        s3 = s3_session.resource('s3')
        obj_path = safe_join([prefix, filename], '/')
        obj = s3.Object(bucket, obj_path)
        url = s3.meta.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': obj.key},
            ExpiresIn=0
        )
        url = url.split('?')[0]

        return obj, url, decode_metadata(obj.metadata)
    except Exception as ex:
        raise Exception('S3 error on metadata update:', ex)

    return None, None, None


def s3_list_files(key, secret, bucket, prefix=''):
    s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
    s3 = s3_session.resource('s3')
    s3_bucket = s3.Bucket(bucket)

    for obj in s3_bucket.objects.filter(Prefix=prefix):
        url = s3.meta.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': obj.key},
            ExpiresIn=0
        )
        url = url.split('?')[0]
        obj = obj.Object()
        yield obj, url, decode_metadata(obj.metadata)


def s3_list_bucket_files(key, secret, bucket):
    s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
    s3 = s3_session.resource('s3')
    s3_bucket = s3.Bucket(bucket)

    for obj in s3_bucket.objects.all():
        yield obj


def s3_update_metadata(key, secret, bucket, filename, prefix='', **kwargs):
    try:
        s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
        s3 = s3_session.resource('s3')

        obj_path = safe_join([prefix, filename], '/')
        obj = s3.Object(bucket, obj_path)
        metadata = obj.metadata or {}
        metadata.update(kwargs)

        keys_to_remove = [key for key, value in metadata.items() if value is None]
        for key in keys_to_remove:
            del metadata[key]

        s3.meta.client.copy_object(
            Bucket=bucket,
            Key=obj.key,
            CopySource={'Bucket': bucket, 'Key': obj.key},
            Metadata=encode_metadata(metadata),
            MetadataDirective='REPLACE'
        )
    except Exception as ex:
        raise Exception('S3 error on metadata update:', ex)


def s3_upload_file(key, secret, bucket, content, filename, prefix='', metadata=None):
    try:
        s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
        s3 = s3_session.resource('s3')
        s3_bucket = s3.Bucket(bucket)

        obj_path = obj_path = safe_join([prefix, filename], '/')

        metadata = encode_metadata(metadata)

        if is_s3_file_exists(key, secret, bucket, filename, prefix):
            s3_delete_file(key, secret, bucket, filename, prefix)

        if content:
            if isinstance(content, str):
                buffer = StringIO(content)
            elif isinstance(content, StringIO) or isinstance(content, BytesIO):
                buffer = content
            else:
                buffer = BytesIO(content)
            return s3_bucket.put_object(Bucket=bucket, Key=obj_path, Body=buffer.read(), Metadata=metadata)
        else:
            return s3_bucket.put_object(Bucket=bucket, Key=obj_path, Metadata=metadata)
    except Exception as ex:
        raise Exception('S3 error on upload:', ex)

    return None


def s3_delete_file(key, secret, bucket, filename, prefix=''):
    try:
        s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
        s3 = s3_session.resource('s3')
        s3_bucket = s3.Bucket(bucket)

        obj_path = safe_join((prefix, filename), '/')

        if filename.endswith('/'):
            objects_to_delete = [{'Key': obj.key} for obj in s3_bucket.objects.filter(Prefix=obj_path)]
            objects_to_delete.append({'Key': obj_path})

            s3_bucket.delete_objects(Delete={
                'Objects': objects_to_delete
            })
        else:
            s3_bucket.delete_objects(Delete={
                'Objects': [{'Key': obj_path}],
                'Quiet': True
            })

    except Exception as ex:
        raise Exception('S3 error on delete:', ex)
        return False

    return True


def s3_rename_file(key, secret, bucket, src_filename, src_prefix, dst_filename, dst_prefix):
    try:
        s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
        s3 = s3_session.resource('s3')
        s3_bucket = s3.Bucket(bucket)

        src_filepath = safe_join('/', (src_prefix, src_filename))
        dst_filepath = safe_join((dst_prefix, dst_filename), '/')
        s3_bucket.copy({'Bucket': bucket, 'Key': src_filepath}, dst_filepath)
        s3_bucket.delete_objects(Delete={'Objects': [{'Key': src_filepath}], 'Quiet': True})
    except Exception as ex:
        raise Exception('S3 error on rename:', ex)
        return False

    return True


def is_s3_file_exists(key, secret, bucket, filename, prefix=''):
    try:
        s3_session = Session(aws_access_key_id=key, aws_secret_access_key=secret)
        s3 = s3_session.resource('s3')
        obj_path = safe_join('/', (prefix, filename))
        s3.meta.client.head_object(Bucket=bucket, Key=obj_path)
    except Exception as ex:
        return False

    return True

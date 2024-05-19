from rest_framework import serializers


def validate_lesson_url(value: str):
    domain = value.split('/')[2]
    if domain not in ['www.youtube.com', 'youtube.com']:
        raise serializers.ValidationError("The video must only be from youtube.com!")

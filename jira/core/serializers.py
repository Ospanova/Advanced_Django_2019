from rest_framework import serializers
from core.models import *
import logging
from users.serializers import *
logger = logging.getLogger(__name__)



class ProjectSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ('id', 'name', 'descr', 'creator_name', 'creator')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class ProjectFullSerializer(ProjectSerializer):
    creator = UserSerializer(read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('descr',)


class BlockSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    name = serializers.CharField()
    status = serializers.IntegerField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Block
        fields = '__all__'

    def get_project_name(self, obj):
        if obj.project is not None:
            return obj.project.name
        return ''


class ProjectMemberSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    user_id = serializers.IntegerField()

    class Meta:
        model = ProjectMember
        fields = ('id', 'project_name', 'user_id')

    def get_project_name(self, obj):
        if obj.project is not None:
            return obj.project.name
        return ''


class ProjectMemberFullSerializer(ProjectMemberSerializer):
    user = UserSerializer()
    project = ProjectSerializer()

    class Meta(ProjectMemberSerializer.Meta):
        model = ProjectMember
        fields = ProjectMemberSerializer.Meta.fields + ('project', 'user')


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    executor = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TaskShortSerializer(serializers.ModelSerializer):
    block_id = serializers.IntegerField(write_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ('id', 'name', 'order', 'executor', 'creator', 'block_id')

    def validate_name(self, value):
        if len(value) < 3:
            logger.error('value of name must have at least 3 characters')
            raise serializers.ValidationError('name length less than 3')
        return value


class TaskFullSerializer(TaskShortSerializer):
    creator = UserSerializer(read_only=True)
    executor = UserSerializer()

    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('descr',)


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ('creator', 'stars')

    def validate_stars(self, value):
        if value > 10 or value < 0:
            raise serializers.ValidationError('name length less than 3')
        return value


class TaskCommentFullSerializer(TaskCommentSerializer):
    creator = UserSerializer(read_only=True)

    class Meta(TaskCommentSerializer.Meta):
        fields = TaskCommentSerializer.Meta.fields


class TaskDocumentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = TaskDocument
        fields = '__all__'
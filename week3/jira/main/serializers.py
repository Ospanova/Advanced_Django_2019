from main.models import Project, Block, Task, MemberProject, TaskDocument, TaskComment
from rest_framework import serializers
from users.serializers import UserSerializer
from main import constants


class ProjectSerializerGet(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'creator_id', 'creator_name', 'created_at')


    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class ProjectSerializerCreateUpdate(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class BlockSerializerGet(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()

    class Meta:
        model = Block
        fields = ('id', 'name', 'type', 'type_name', 'project_id', 'project_name', 'created_at')

    def get_project_name(self, obj):
        if obj.project is not None:
            return obj.project.name
        return ''

    def get_type_name(self, obj):
        d = dict(constants.BLOCK_TYPES)
        return d[int(obj.type)]


class BlockSerializerCreateUpdate(serializers.ModelSerializer):
    project = ProjectSerializerCreateUpdate(read_only=True)

    class Meta:
        model = Block
        fields = '__all__'


class TaskSerializerGet(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    executor_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description',
                  'creator_id', 'creator_name',
                  'executor_id', 'executor_name',
                  'order', 'block_id',
                  'created_at')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def get_executor_name(self, obj):
        if obj.executor is not None:
            return obj.executor.username
        return ''


class TaskSerializerCreateUpdate(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    executor = UserSerializer(read_only=True)
    block = BlockSerializerCreateUpdate(read_only=True)
    executor_id = serializers.IntegerField(write_only=True)
    block_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class MemberProjectSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)
    project_id = serializers.IntegerField(write_only=True)
    member = UserSerializer(read_only=True)
    project = ProjectSerializerGet(read_only=True)

    class Meta:
        model = MemberProject
        fields = '__all__'


class TaskDocumentSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)
    task = TaskSerializerGet(read_only=True)

    class Meta:
        model = TaskDocument
        fields = '__all__'


class TaskCommentSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)
    task = TaskSerializerGet(read_only=True)

    class Meta:
        model = TaskComment
        fields = '__all__'

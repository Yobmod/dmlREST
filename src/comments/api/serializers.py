from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
#from django.core.exceptions import ValidationError﻿
from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer

User = get_user_model()

def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
	class CommentCreateSerializer(ModelSerializer):
		class Meta:
			model=Comment
			fields = [			#'parent',
								'id',
								'content',
								'timestamp',
											]
		def __init__(self, *args, **kwargs):
			self.model_type = model_type
			self.slug = slug
			self.parent_obj = None
			if parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exists() and parent_qs.count==1:
					self.parent_obj = parent_qs.first()
			return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

		def validate(self, data):
			model_type = self.model_type
			model_qs = ContentType.objects.filter(model=model_type)
			if not model_qs.exists() or model_qs.count() != 1:
				raise ValidationError("This is not a valid content type")
			someModel = model_qs.first().model_class()
			obj_qs = someModel.objects.filter(slug=self.slug)
			if not obj_qs.exists() or obj_qs.count() != 1:
				raise ValidationError("This is not a slug for this content type")
			return data

		def create(self, validated_data):
			content = validated_data.get("content")
			if user:
				main_user = user
			else:
				main_user = User.objects.all().first()
			model_type = self.model_type
			slug = self.slug
			parent_obj = self.parent_obj
			commment = Comment.objects.create_by_model_type(model_type,
															slug,
															content,
															user,
															parent_obj=parent_obj,
														 							)
			return comment

	return CommentCreateSerializer

comment_detail_url = HyperlinkedIdentityField(view_name='comments-api:thread', lookup_field = 'id',)

class CommentListSerializer(ModelSerializer):
	url = comment_detail_url
	user = UserDetailSerializer(read_only=True)
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
					#'content_type',
					#'object_id',
					'url',
					# 'parent',
					'id',
					'content',
					'user',
					'reply_count',
								]
	def get_user(self, obj):
		return str(obj.user.username)

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

class CommentChildSerializer(ModelSerializer):
	#url = comment_detail_url
	user = UserDetailSerializer(read_only=True)
	class Meta:
		model = Comment
		fields = [
					'id',
					#'url',
					'content',
					'user',
					'timestamp',
								]

class CommentDetailSerializer(ModelSerializer):
	#url = comment_detail_url
	user = UserDetailSerializer(read_only=True)
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()
	content_object_url = SerializerMethodField() #getting the post/comment comment is on
	class Meta:
		model = Comment
		fields = [
					#'url',
					'id',
					#'object_id',
					'content',
					#'content_type',
					'user',
					'replies',
					'reply_count',
					'content_object_url',
					]

		read_only_fields = [	'replies',
								'reply_count',
							]


	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

	def get_content_object_url(self, obj):
		try:
			return obj.content_object.get_api_url()
		except:
			return None


class CommentEditSerializer(ModelSerializer):
	#url = comment_detail_url
	UserDetailSerializer(read_only=True)
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
					'id',
					'object_id',
					'content',
					'replies',
					'reply_count',
					'user',
					'timestamp',
								]
	def get_user(self, obj):
		return str(obj.user.username)

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0
